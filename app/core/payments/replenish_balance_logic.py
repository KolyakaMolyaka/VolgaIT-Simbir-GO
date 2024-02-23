from flask_jwt_extended import current_user
from .replenish_strategy_factory import ReplenishStrategyFactory
from .replenish_strategy import ReplenishStrategy


def process_replenish_user_balance(user_id: int, money_amount: int):
	"""
	Добавление баланса пользователю в количестве денежных единиц
	:param user_id: id пользователя, которому нужно пополнить баланс
	:param money_amount: количество денежных единиц, на которые нужно пополнить баланс
	:return:
	"""

	# получение стратегии пополнения баланса
	strategy_type = 'admin' if current_user.is_admin else 'user'
	strategy: ReplenishStrategy = ReplenishStrategyFactory.get_strategy(strategy_type)
	# пополнение баланса согласно стратегии
	strategy.replenish_balance(user_id, money_amount)
