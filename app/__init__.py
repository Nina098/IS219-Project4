"""A simple flask web app"""
import os

import flask_login
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from app import cli
from app.cli import create_database
import app.db
from app.db import db
from app.db.models import User
from app import simple_pages
from app import auth


login_manager = flask_login.LoginManager()


def page_not_found(e):
    return render_template("404.html"), 404


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.secret_key = 'This is an INSECURE secret!! DO NOT use this in production!!'

    bootstrap = Bootstrap5(app)
    login_manager.init_app(app)
    app.register_blueprint(simple_pages.simple_pages)
    app.register_blueprint(auth.auth)
    app.register_error_handler(404, page_not_found)
    db_dir = "database/db.sqlite"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.abspath(db_dir)
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['WTF_CSRF_ENABLED'] = False
    db.init_app(app)

    # add command function to cli commands
    app.cli.add_command(create_database)

    return app


@login_manager.user_loader
def user_loader(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None