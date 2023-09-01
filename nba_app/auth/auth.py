from nba_app.auth import blp
from nba_app.models import user_schema, User
from nba_app.utils import validate_content_type
from app import db

from webargs.flaskparser import use_args
from flask import jsonify


@blp.route('/register', methods=['POST'])
@validate_content_type
@use_args(user_schema, error_status_code=400)
def register(args: dict):
    if User.query.filter(User.username == args['username']).first():
        return jsonify({
            "success": False,
            "message": f'User with username <{args["username"]}> already exists.'
        }), 409
    if User.query.filter(User.email == args['email']).first():
        return jsonify({
            "success": False,
            "message": f'User with email <{args["email"]}> already exists.'
        }), 409

    args['password'] = User.generate_hashed_password(args['password'])
    user = User(**args)

    db.session.add(user)
    db.session.commit()

    token = user.generate_jwt(user)

    return jsonify(({
        'success': True,
        'token': token
    }))
