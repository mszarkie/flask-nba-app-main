from nba_app.auth import blp
from nba_app.models import user_schema, User, UserSchema, user_password_update_schema
from nba_app.utils import validate_content_type, token_required
from app import db

from webargs.flaskparser import use_args
from flask import jsonify, abort


@blp.route('/register', methods=['POST'])
@validate_content_type
@use_args(user_schema, error_status_code=400)
def register(args: dict):
    if User.query.filter(User.username == args['username']).first():
        abort(409, description=f'User with username <{args["username"]}> already exists.')
    if User.query.filter(User.email == args['email']).first():
        abort(409, description=f'User with email <{args["email"]}> already exists.')

    args['password'] = User.generate_hashed_password(args['password'])
    user = User(**args)

    db.session.add(user)
    db.session.commit()

    token = user.generate_jwt(user)

    return jsonify(({
        'success': True,
        'token': token
    }))


@blp.route('/login', methods=['POST'])
@validate_content_type
@use_args(UserSchema(only=['username', 'password']), error_status_code=400)
def login(args: dict):
    user = User.query.filter(User.username == args['username']).first()
    if not user:
        abort(401, description=f'Invalid credentials')

    if not user.is_password_valid(args['password']):
        abort(401, description=f'Invalid credentials')

    token = user.generate_jwt(user)

    return jsonify(({
        'success': True,
        'token': token
    }))


@blp.route('/userinfo', methods=['GET'])
@token_required
def get_current_user(user_id: int):
    user = User.query.get_or_404(user_id, description=f'User with id {user_id} nor found.')

    return jsonify({
        'success': True,
        'data': user_schema.dump(user)
    })


@blp.route('/update/password', methods=['PUT'])
@token_required
@validate_content_type
@use_args(user_password_update_schema, error_status_code=400)
def update_password(user_id: int, args: dict):
    user = User.query.get_or_404(user_id, description=f'User with id {user_id} nor found.')

    if not user.is_password_valid(args['current_password']):
        abort(401, description='Invalid password')

    user.password = user.generate_hashed_password(args['new_password'])
    db.session.commit()

    return jsonify({
        'success': True,
        'data': user_schema.dump(user),
        'message': "Password has been changed."
    })


@blp.route('/update/data', methods=['PUT'])
@token_required
@validate_content_type
@use_args(UserSchema(only=['username', 'email']), error_status_code=400)
def update_user_data(user_id: int, args: dict):
    if User.query.filter(User.username == args['username']).first():
        abort(409, description=f'User with username <{args["username"]}> already exists.')
    if User.query.filter(User.email == args['email']).first():
        abort(409, description=f'User with email <{args["email"]}> already exists.')

    user = User.query.get_or_404(user_id, description=f'User with id {user_id} nor found.')

    user.username = args['username']
    user.email = args['email']
    db.session.commit()

    return jsonify({
        'success': True,
        'data': user_schema.dump(user),
        'message': "Data has been changed."
    })
