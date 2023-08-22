from app import db
from marshmallow import Schema, fields, validate


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(30), unique=True, nullable=False)
    coach = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    total_championships = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {self.team_name}'


class TeamSchema(Schema):
    id = fields.Integer(dump_only=True)
    team_name = fields.String(required=True, validate=validate.Length(max=30))
    coach = fields.String(required=True, validate=validate.Length(max=30))
    city = fields.String(required=True, validate=validate.Length(max=30))
    total_championships = fields.Integer(required=True)


teams_schema = TeamSchema()
