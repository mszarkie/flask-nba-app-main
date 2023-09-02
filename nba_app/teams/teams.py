from flask import jsonify
from webargs.flaskparser import use_args

from app import db
from nba_app.teams import blp
from nba_app.utils import validate_content_type, get_schema_args, apply_order, apply_filter, get_pagination, \
token_required
from nba_app.models import Team, TeamSchema, teams_schema


@blp.route('/teams', methods=['GET'])
def get_teams():
    query = Team.query
    schema_args = get_schema_args(Team)
    query = apply_order(Team, query)
    query = apply_filter(Team, query)
    items, pagination = get_pagination(query, 'teams.get_teams')

    teams = TeamSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'data': teams,
        'number_of_records': len(teams),
        'pagination': pagination
    })


@blp.route('/teams/<int:team_id>', methods=['GET'])
def get_team(team_id: int):
    team = Team.query.get_or_404(team_id, description=f'Team with id {team_id} not found')
    return jsonify({
        'success': True,
        'data': teams_schema.dump(team)
    })


@blp.route('/teams', methods=['POST'])
@token_required
@validate_content_type
@use_args(teams_schema, error_status_code=400)
def create_team(user_id: str, args: dict):
    team = Team(**args)

    db.session.add(team)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': teams_schema.dump(team)
    }), 201


@blp.route('/teams/<int:team_id>', methods=['PUT'])
@token_required
@validate_content_type
@use_args(teams_schema, error_status_code=400)
def update_team(user_id: str, args: dict, team_id: int):
    team = Team.query.get_or_404(team_id, description=f'Team with id {team_id} not found')

    team.team_name = args['team_name']
    team.coach = args['coach']
    team.city = args['city']
    team.total_championships = args['total_championships']

    db.session.commit()

    return jsonify({
        'success': True,
        'data': teams_schema.dump(team)
    })


@blp.route('/teams/<int:team_id>', methods=['DELETE'])
@token_required
def delete_team(user_id: str, team_id: int):
    team = Team.query.get_or_404(team_id, description=f'Team with id {team_id} not found')

    db.session.delete(team)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': f'Team with id {team_id} has been deleted'
    })

