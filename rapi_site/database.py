import click

from flask import Flask
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dirs import ROOT_DIR


engine = create_engine(f"sqlite:///{ROOT_DIR / 'test.db'}")
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def shutdown_session(exception=None):
    db_session.remove()


def init_db():
    Base.metadata.create_all(bind=engine)


@click.command('init-db')       # a cli command to call init_db()
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app: Flask):
    app.teardown_appcontext(shutdown_session)
    app.cli.add_command(init_db_command)
