from http import HTTPStatus
from flask import abort
from flask_jwt_extended import current_user
from app.extensions.database.models import User


def process_replenish_user_balance(user_id: int):
	# админ может добавить баланс всем
	if current_user.is_admin:
		user = User.query.get(user_id)
		if not user:
			abort(HTTPStatus.NOT_FOUND, f'Пользователем с id = {user_id} не найден.')

		user.balance += 250_000
		user.save()
		return

	# обычный пользователь может добавить баланс только себе
	if current_user.id != user_id:
		abort(HTTPStatus.FORBIDDEN,
			  'Пользователь, не обладающий правами администратора, может пополнить баланс только себе.')

	current_user.balance += 250_000
	current_user.save()
