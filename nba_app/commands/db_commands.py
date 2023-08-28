from app import db
import json
from pathlib import Path
from nba_app.models import Team, Player
from sqlalchemy.sql import text
from nba_app.commands import blp
from datetime import datetime


def load_json_data(filename: str) -> list:
    json_path = Path(__file__).parent.parent / 'data' / filename
    with open(json_path) as file:
        data_json = json.load(file)
    return data_json


@blp.cli.group()
def db_menage():
    """Database managment commands"""
    pass


@db_menage.command()
def add_data():
    """Add sample data to database"""
    try:
        data_json = load_json_data('teams.json')
        for item in data_json:
            team = Team(**item)
            db.session.add(team)

        data_json = load_json_data('players.json')
        for item in data_json:
            item['birth_date'] = datetime.strptime(item['birth_date'], '%d-%m-%Y').date()
            player = Player(**item)
            db.session.add(player)

        db.session.commit()
        print('Data has been successfully added to the database')
    except Exception as exc:
        print("Unexpected error: {}".format(exc))


@db_menage.command()
def remove_data():
    """Remove all data"""
    try:
        db.session.execute(text('DELETE FROM players'))
        db.session.execute(text('ALTER TABLE players AUTO_INCREMENT = 1'))
        db.session.execute(text('DELETE FROM teams'))
        db.session.execute(text('ALTER TABLE teams AUTO_INCREMENT = 1'))
        db.session.commit()
        print('Data has been successfully removed from the database')
    except Exception as exc:
        print("Unexpected error: {}".format(exc))
