from flask import Flask

import logging

logging.basicConfig(filename='logs',
					filemode='a',
					format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
					datefmt='%H:%M:%S',
					level=logging.DEBUG)


def create_app(testing=False):
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

	@click.command('fill-db')
	@with_appcontext
	def fill_db_command():
		from app.core.accounts.utils.utils import generate_n_users
		generate_n_users(100)
		from app.core.accounts.utils.utils import generate_n_admins
		generate_n_admins(5)
		from app.core.transports.utils import generate_n_transports
		generate_n_transports(500, max_users=100)  # пользователи + админы
		click.echo('Database data created!')

	app.cli.add_command(init_db_command)
	app.cli.add_command(fill_db_command)

	return app
