from app import db
import json
from pathlib import Path
from nba_app.models.models import Team
from sqlalchemy.sql import text
from nba_app.commands import blp


@blp.cli.group()
def db_menage():
    """Database managment commands"""
    pass


@db_menage.command()
def add_data():
    """Add sample data to database"""
    try:
        teams_path = Path(__file__).parent.parent / 'data' / 'teams.json'
        with open(teams_path) as file:
            data_json = json.load(file)
        for item in data_json:
            team = Team(**item)
            db.session.add(team)
        db.session.commit()
        print('Data has been successfully added to the database')
    except Exception as exc:
        print("Unexpected error: {}".format(exc))


@db_menage.command()
def remove_data():
    """Remove all data"""
    try:
        db.session.execute(text('TRUNCATE TABLE teams'))
        db.session.commit()
        print('Data has been successfully removed from the database')
    except Exception as exc:
        print("Unexpected error: {}".format(exc))
