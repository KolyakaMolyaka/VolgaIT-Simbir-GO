from abc import ABC, abstractmethod

from http import HTTPStatus
from flask import abort
from flask_jwt_extended import current_user
from app.extensions.database.models import User


class ReplenishStrategy(ABC):
	"""
	Интерфейс стратегии пополнения баланса
	"""

	@abstractmethod
	def replenish_balance(self, user_id: int, money_amount: int):
		"""
		Добавление баланса пользователю в количестве денежных единиц
		:param user_id: id пользователя, которому нужно пополнить баланс
		:param money_amount: количество денежных единиц, на которые нужно пополнить баланс
		"""


class AdminReplenishStrategy(ReplenishStrategy):
	"""
	Стратегия пополнения баланса для администратора
	"""

	def replenish_balance(self, user_id: int, money_amount: int):
		user = User.query.get(user_id)
		if not user:
			abort(HTTPStatus.NOT_FOUND, f'Пользователем с id = {user_id} не найден.')

		user.balance += money_amount
		user.save()


class UserReplenishStrategy(ReplenishStrategy):
	"""
	Стратегия пополнения баланса для пользователя
	"""

	def replenish_balance(self, user_id: int, money_amount: int):
		if current_user.id != user_id:
			abort(HTTPStatus.FORBIDDEN,
				  'Пользователь, не обладающий правами администратора, может пополнить баланс только себе.')

		current_user.balance += money_amount
		current_user.save()
