from flask import jsonify
from webargs.flaskparser import use_args

from app import db
from nba_app.players import blp
from nba_app.utils import validate_content_type, get_schema_args, apply_order, apply_filter, get_pagination, \
token_required
from nba_app.models import Player, PlayerSchema, players_schema, Team


@blp.route('/players', methods=['GET'])
def get_players():
    query = Player.query
    schema_args = get_schema_args(Player)
    query = apply_order(Player, query)
    query = apply_filter(Player, query)
    items, pagination = get_pagination(query, 'players.get_players')

    players = PlayerSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'data': players,
        'number_of_records': len(players),
        'pagination': pagination
    })


@blp.route('/player/<int:player_id>', methods=['GET'])
def get_player(player_id: int):
    player = Player.query.get_or_404(player_id, description=f'Player with id {player_id} not found')
    return jsonify({
        'success': True,
        'data': players_schema.dump(player)
    })


@blp.route('/player/<int:player_id>', methods=['PUT'])
@token_required
@validate_content_type
@use_args(players_schema, error_status_code=400)
def update_player(user_id: str, args: dict, player_id: int):
    player = Player.query.get_or_404(player_id, description=f'Player with id {player_id} not found')

    player.first_name = args['first_name']
    player.last_name = args['last_name']
    player.birth_date = args['birth_date']
    player.position = args['position']

    db.session.commit()

    return jsonify({
        'success': True,
        'data': players_schema.dump(player)
    })


@blp.route('/player/<int:player_id>', methods=['DELETE'])
@token_required
def delete_player(user_id: str, player_id: int):
    player = Player.query.get_or_404(player_id, description=f'Player with id {player_id} not found')

    db.session.delete(player)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': f'Player with id {player_id} has been deleted'
    })


@token_required
@blp.route('/teams/<int:team_id>/players', methods=['GET'])
def get_all_team_players(user_id: str, team_id: int):
    Team.query.get_or_404(team_id, description=f'Team with id {team_id} not found')
    players = Player.query.filter(Player.team_id == team_id).all()

    persons = PlayerSchema(many=True, exclude=['team']).dump(players)

    return jsonify(({
        'success': True,
        'data': persons,
        'number_of_records': len(persons)

    }))


@blp.route('/teams/<int:team_id>/players', methods=['POST'])
@token_required
@validate_content_type
@use_args(PlayerSchema(exclude=['team_id']), error_status_code=400)
def create_player(user_id: str, args: dict, team_id: int):
    Team.query.get_or_404(team_id, description=f'Team with id {team_id} not found')

    player = Player(team_id=team_id, **args)

    db.session.add(player)
    db.session.commit()

    return jsonify(({
        'success': True,
        'data': players_schema.dump(player)
    })), 201
