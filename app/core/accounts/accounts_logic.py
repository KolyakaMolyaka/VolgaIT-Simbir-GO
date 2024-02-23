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


def process_registration_request(username: str, password: str) -> None:
	"""
	Обработка запроса регистрации пользователя
	:param username: имя пользователя
	:param password: пароль пользователя
	:return:
	"""

	# проверка, существует ли такой пользователь
	if User.is_user_exists(username):
		abort(HTTPStatus.CONFLICT, f'{username} уже зарегистрирован.')

	# создание и сохранение в БД пользователя
	new_user = User(username=username)
	new_user.set_password(password)
	new_user.save()


def _get_token_expire_time(how: ['min', 'sec', 'hours'] = 'min') -> float:
	"""Возвращает время истечения токена в минутах"""
	from datetime import timedelta
	dtime: timedelta = current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES')
	expires = dtime.total_seconds()
	if how == 'sec':
		return expires
	elif how == 'min':
		return expires / 60
	return expires / 3600



def process_login_request(username: str, password: str) -> list:
	"""
	Обработка запроса авторизации пользователя
	:param username: имя пользователя
	:param password: пароль пользователя
	:return: access и refresh JWT токены или ошибку
	"""

	# получение пользователя по имени
	user = User.get_user_by_username(username)

	# если пользователь не существует или отправленный пароль неправильный
	if not (user and user.is_correct_password(password)):
		abort(HTTPStatus.NOT_FOUND, f'Неправильное имя пользователя или пароль')

	# создание JWT токенов
	access_token = create_access_token(identity=user.id)
	refresh_token = create_refresh_token(identity=user.id)

	return access_token, refresh_token


def process_about_me_request():
	"""
	Обработка запроса получения последней информации о пользователе
	:return: текущий пользователь
	"""
	return current_user


def process_logout_request():
	"""
	Обработка запроса выхода из аккаунта
	:return:
	"""

	# получение JWT токена пользователя
	jwt = get_jwt()
	jti = jwt['jti']

	# добавление токена в блок-лист и создание в БД
	# повторная авторизация по токену невозможна
	new_blocked_token = TokenBlocklist(jti=jti)
	new_blocked_token.save()


def process_update_user_request(new_username: str, new_password: str):
	"""
	Обработка запроса обновления информации о пользователе
	:param new_username: новое имя пользователя
	:param new_password: новый пароль пользователя
	:return:
	"""
	# проверка, существует ли пользователь с таким именем
	if User.get_user_by_username(new_username):
		abort(HTTPStatus.CONFLICT, f'{new_username} уже существует.')

	# обновление данных
	current_user.username = new_username
	current_user.set_password(new_password)
	current_user.save()

	return current_user
