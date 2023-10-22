from http import HTTPStatus
from flask import abort
from flask_jwt_extended import current_user

from app.extensions.database import db
from app.extensions.database.models import User


def process_admin_get_accounts_list(start: int, count: int):
	users = User.query.offset(start).limit(count).all()
	return users


def process_admin_create_user(username: str, password: str, is_admin: bool, balance: float):
	# проверка, существует ли такой пользователь
	if User.is_user_exists(username):
		abort(HTTPStatus.CONFLICT, f'Пользователь {username} уже существует.')

	user = User(username=username, is_admin=is_admin, balance=balance)
	user.set_password(password)
	user.save()


def process_admin_get_account_info(user_id: int):
	user = User.query.get(user_id)
	if not user:
		abort(HTTPStatus.NOT_FOUND, f'Пользователь с id = {user_id} не найден.')
	return user


def process_admin_update_user(user_id: int, username: str, password: str, is_admin: bool, balance: float):
	# проверка, существует ли такой пользователь

	user = User.get_user_by_username(username)
	if user and user.id != current_user.id:
		abort(HTTPStatus.CONFLICT, f'Пользователь {username} уже существует.')

	user = User.query.get(user_id)
	if not user:
		abort(HTTPStatus.NOT_FOUND, f'Пользователь с id = {user_id} не найден.')

	user.username = username
	user.is_admin = is_admin
	user.balance = balance
	user.set_password(password)

	user.save()

	return user


def process_admin_delete_user(user_id: int):
	user = User.query.get(user_id)
	if not user:
		abort(HTTPStatus.NOT_FOUND, f'Пользователь с id = {user_id} не найден.')

	db.session.delete(user)
	db.session.commit()

	pass
