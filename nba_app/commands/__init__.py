from flask import Blueprint

blp = Blueprint('db_commands', __name__, cli_group=None)

from nba_app.commands import db_commands