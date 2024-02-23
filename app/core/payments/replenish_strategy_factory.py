from .replenish_strategy import ReplenishStrategy, AdminReplenishStrategy, UserReplenishStrategy


class ReplenishStrategyFactory:
	"""
	Фабрика по созданию стратегий пополнения баланса
	"""

	@staticmethod
	def get_strategy(strategy_type: str) -> ReplenishStrategy:
		"""
		Получение стратегии для пополнения баланса
		:param type: тип стратегии: ['admin', 'user']
		:return: стратегия для пополнения баланса
		"""
		if strategy_type == 'admin':
			return AdminReplenishStrategy()
		elif strategy_type == 'user':
			return UserReplenishStrategy()

		raise Exception(f'strategy_type "{strategy_type}" неизвестен!')
