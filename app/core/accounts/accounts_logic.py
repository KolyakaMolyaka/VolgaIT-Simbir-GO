from http import HTTPStatus
from flask import abort
from app.extensions.database.models import User, TokenBlocklist
from flask import current_app

from flask_jwt_extended import (
	create_access_token,
	create_refresh_token,
	current_user,
	get_jwt
)


def process_registration_request(username, password):
	# проверка, существует ли такой пользователь
	if User.is_user_exists(username):
		abort(HTTPStatus.CONFLICT, f'{username} уже зарегистрирован.')

	# создание пользователя
	new_user = User(username=username)
	new_user.set_password(password)
	new_user.save()


def _get_token_expire_time(how: ['min', 'sec', 'hours'] = 'min'):
	"""Возвращает время истечения токена в минутах"""
	from datetime import timedelta
	dtime: timedelta = current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES')
	expires = dtime.total_seconds()
	if how == 'sec':
		return expires
	elif how == 'min':
		return expires / 60
	return expires / 3600



def process_login_request(username, password):
	user = User.get_user_by_username(username)

	# если пользователь не существует или отправленный пароль неправильный
	if not (user and user.check_password(password)):
		abort(HTTPStatus.NOT_FOUND, f'Неправильное имя пользователя или пароль')

	access_token = create_access_token(identity=user.id)
	refresh_token = create_refresh_token(identity=user.id)

	return access_token, refresh_token


def process_about_me_request():
	# serialized_user = UserSchema().dump(current_user)
	return current_user


def process_logout_request():
	jwt = get_jwt()
	jti = jwt['jti']

	new_blocked_token = TokenBlocklist(jti=jti)
	new_blocked_token.save()


def process_update_user_request(username, password):
	user = User.get_user_by_username(username)
	if user:
		abort(HTTPStatus.CONFLICT, f'{username} уже существует.')

	# обновление данных
	current_user.username = username
	current_user.set_password(password)
	current_user.save()

	return current_user
