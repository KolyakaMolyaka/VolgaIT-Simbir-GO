from flask import Flask


def create_app(testing=True):
	app = Flask(__name__)

	if testing:
		from .configs import TestConfig
		app.config.from_object(TestConfig)
	else:
		app.config.from_prefixed_env()

	# Инициализация расширений
	# sqlalchemy (+marshmallow for serializing)
	from .extensions.database import db
	db.init_app(app)

	# jwt
	from .extensions.jwt import jwt
	jwt.init_app(app)

	# swagger
	from app.apis import api
	api.init_app(app)

	# команда создания БД
	import click
	from flask.cli import with_appcontext

	@click.command('init-db')
	@with_appcontext
	def init_db_command():
		db.drop_all()
		db.create_all()
		db.session.commit()
		click.echo('Database initialized.')

	app.cli.add_command(init_db_command)

	return app
