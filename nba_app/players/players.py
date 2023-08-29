from flask import jsonify
from webargs.flaskparser import use_args

from app import db
from nba_app.players import blp
from nba_app.utils import validate_content_type, get_schema_args, apply_order, apply_filter, get_pagination
from nba_app.models import Player, PlayerSchema, players_schema


@blp.route('/players', methods=['GET'])
def get_players():
    query = Player.query
    schema_args = get_schema_args(Player,)
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