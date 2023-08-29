from flask import request, url_for, current_app
from werkzeug.exceptions import UnsupportedMediaType
from functools import wraps
from flask_sqlalchemy import DefaultMeta
from flask_sqlalchemy import BaseQuery
from config import Config
from typing import Tuple


def validate_content_type(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        if data is None:
            raise UnsupportedMediaType("Content must be application/json")
        return func(*args, **kwargs)
    return wrapper


#function below allow to view particular choosen data
def get_schema_args(model: DefaultMeta) -> dict:
    schema_args = {'many': True}
    fields = request.args.get('fields')
    if fields:
        schema_args['only'] = [field for field in fields.split(',') if field in model.__table__.columns]
    return schema_args


def apply_order(model: DefaultMeta, query: BaseQuery) -> BaseQuery:
    sort_keys = request.args.get('sort')
    if sort_keys:
        for key in sort_keys.split(','):
            desc = False
            if key.startswith('-'):
                key = key[1:]
                desc = True
            column_attr = getattr(model, key, None)
            if column_attr is not None:
                query = query.order_by(column_attr.desc()) if desc else query.order_by(column_attr)

    return query


def apply_filter(model: DefaultMeta, query: BaseQuery) -> BaseQuery:
    for param, value in request.args.items():
        if param not in {'fields', 'sort', 'page', 'limit'}:
            column_attr = getattr(model, param, None)
            if column_attr is not None:
                query = query.filter(column_attr == value)
    return query


def get_pagination(query: BaseQuery, func_name: str) -> Tuple[list, dict]:
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', current_app.config.get('PER_PAGE', 5), type=int)
    params = {key: value for key, value in request.args.items() if key != 'page'}
    paginate_obj = query.paginate(page=page, per_page=limit, error_out=False)
    pagination = {
        'total_pages': paginate_obj.pages,
        'total_records': paginate_obj.total,
        'current_page': url_for(func_name, page=page, **params)
    }

    if paginate_obj.has_next:
        pagination['next_page'] = url_for(func_name, page=page+1, **params)

    if paginate_obj.has_prev:
        pagination['previous_page'] = url_for(func_name, page=page-1, **params)

    return paginate_obj.items, pagination
