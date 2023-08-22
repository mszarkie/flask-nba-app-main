from flask import jsonify
from app import db
from nba_app.models.teamsM import Team, TeamSchema, teams_schema
from webargs.flaskparser import use_args
from nba_app.teams import blp
from nba_app.utils import validate_content_type

@blp.route('/teams', methods=['GET'])
def get_teams():
    teams = Team.query.all()
    teams_schema = TeamSchema(many=True)

    return jsonify({
        'success': True,
        'data': teams_schema.dump(teams),
        'number_of_records' : len(teams)
    })


@blp.route('/teams/<int:team_id>', methods=['GET'])
def get_team(team_id: int):
    team = Team.query.get_or_404(team_id, description=f'Team with id {team_id} not found')
    return jsonify({
        'success': True,
        'data': teams_schema.dump(team)
    })


@blp.route('/teams', methods=['POST'])
@use_args(teams_schema, error_status_code=400)
def create_team(args: dict):
    team = Team(**args)

    db.session.add(team)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': teams_schema.dump(team)
    }), 201


@blp.route('/teams/<int:team_id>', methods=['PUT'])
@validate_content_type
@use_args(teams_schema, error_status_code=400)
def update_team(args: dict, team_id: int):
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
def delete_team(team_id: int):
    team = Team.query.get_or_404(team_id, description=f'Team with id {team_id} not found')

    db.session.delete(team)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': f'Team with id {team_id} has been deleted'
    })
