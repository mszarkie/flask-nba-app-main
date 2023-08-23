from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


db = SQLAlchemy()
migrate = Migrate()

from nba_app.commands import blp as CommandBluePrint
from nba_app.errors import blp as ErrorsBluePrint
from nba_app.teams import blp as TeamsBluePrint


def create_app():

    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(CommandBluePrint)
    app.register_blueprint(ErrorsBluePrint)
    app.register_blueprint(TeamsBluePrint)

    return app
