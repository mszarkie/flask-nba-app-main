from app import db
from marshmallow import Schema, fields, validate
from flask_sqlalchemy import BaseQuery
from flask import request, url_for
from typing import Tuple
from config import Config


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(30), unique=True, nullable=False)
    coach = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    total_championships = db.Column(db.Integer, nullable=False)
    player = db.relationship('Player', back_populates='team', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {self.team_name}'

    @staticmethod
    #function below allow to view particular choosen data
    def get_schema_args(fields: str) -> dict:
        schema_args = {'many': True}
        if fields:
            schema_args['only'] = [field for field in fields.split(',') if field in Team.__table__.columns]
        return schema_args

    @staticmethod
    def apply_order(query: BaseQuery, sort_keys: str) -> BaseQuery:
        if sort_keys:
            for key in sort_keys.split(','):
                desc = False
                if key.startswith('-'):
                    key = key[1:]
                    desc = True
                column_attr = getattr(Team, key, None)
                if column_attr is not None:
                    query = query.order_by(column_attr.desc()) if desc else query.order_by(column_attr)

        return query

    @staticmethod
    def apply_filter(query: BaseQuery) -> BaseQuery:
        for param, value in request.args.items():
            if param not in {'fields', 'sort', 'page', 'limit'}:
                column_attr = getattr(Team, param, None)
                if column_attr is not None:
                    query = query.filter(column_attr == value)
        return query

    @staticmethod
    def get_pagination(query: BaseQuery) -> Tuple[list, dict]:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', Config.PER_PAGE, type=int)
        params = {key: value for key, value in request.args.items() if key != 'page'}
        paginate_obj = query.paginate(page=page, per_page=limit, error_out=False)
        pagination = {
            'total_pages': paginate_obj.pages,
            'total_records': paginate_obj.total,
            'current_page': url_for('teams.get_teams', page=page, **params)
        }

        if paginate_obj.has_next:
            pagination['next_page'] = url_for('teams.get_teams', page=page+1, **params)

        if paginate_obj.has_prev:
            pagination['previous_page'] = url_for('teams.get_teams', page=page-1, **params)

        return paginate_obj.items, pagination


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), unique=True, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    position = db.Column(db.String(15), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    team = db.relationship('Team', back_populates='player')

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {self.first_name} {self.last_name}'


class TeamSchema(Schema):
    id = fields.Integer(dump_only=True)
    team_name = fields.String(required=True, validate=validate.Length(max=30))
    coach = fields.String(required=True, validate=validate.Length(max=30))
    city = fields.String(required=True, validate=validate.Length(max=30))
    total_championships = fields.Integer(required=True)


teams_schema = TeamSchema()
