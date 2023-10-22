from flask import Flask


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

	return app
