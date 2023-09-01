from app import db
from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import jwt
from flask import current_app


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(30), unique=True, nullable=False)
    coach = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    total_championships = db.Column(db.Integer, nullable=False)
    players = db.relationship('Player', back_populates='team', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {self.team_name}'


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), unique=True, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    position = db.Column(db.String(15), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    team = db.relationship('Team', back_populates='players')

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {self.first_name} {self.last_name}'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True, index=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def generate_hashed_password(password: str) -> str:
        return generate_password_hash(password)

    @staticmethod
    def generate_jwt(self):
        payload = {
            'user_id': self.id,
            'exp': datetime.utcnow() + timedelta(minutes=current_app.config.get('JWT_EXPIRED_MINUTES'))
        }
        return jwt.encode(payload, current_app.config.get('SECRET_KEY'))


class TeamSchema(Schema):
    id = fields.Integer(dump_only=True)
    team_name = fields.String(required=True, validate=validate.Length(max=30))
    coach = fields.String(required=True, validate=validate.Length(max=30))
    city = fields.String(required=True, validate=validate.Length(max=30))
    total_championships = fields.Integer(required=True)
    players = fields.List(fields.Nested(lambda: PlayerSchema(only=['id', 'first_name', 'last_name'])))


class PlayerSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True, validate=validate.Length(max=30))
    last_name = fields.String(required=True, validate=validate.Length(max=30))
    birth_date = fields.Date('%d-%m-%Y', required=True)
    position = fields.String(required=True)
    team_id = fields.Integer(load_only=True)
    team = fields.Nested(lambda: TeamSchema(only=['id', 'team_name']))

    @validates('birth_date')
    def validate_birth_date(self, value):
        if value > datetime.now().date():
            raise ValidationError(f'Birth date must be lower than {datetime.now().date()}')


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(max=255))
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6, max=255))
    creation_date = fields.Date(dump_only=True)


players_schema = PlayerSchema()
teams_schema = TeamSchema()
user_schema = UserSchema()
