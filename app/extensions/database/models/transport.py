import math
from app.extensions.database import db


class Transport(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	can_be_rented = db.Column(db.Boolean, nullable=False)
	transport_type = db.Column(db.String(7), nullable=False)
	model = db.Column(db.String(256), nullable=False)
	color = db.Column(db.String(32), nullable=False)
	identifier = db.Column(db.String(16), nullable=False)
	description = db.Column(db.String(256))
	latitude = db.Column(db.Float, nullable=False)
	longitude = db.Column(db.Float, nullable=False)
	minute_price = db.Column(db.Float)
	day_price = db.Column(db.Float)

	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def save(self):
		""" Сохранение изменений в БД """
		db.session.add(self)
		db.session.commit()

	@classmethod
	def get_transport_by_cords(cls, latitude: float, longitude: float, radius: float,
							   return_cursor=False):
		"""
		Получение транспорта в радиусе от указанных координат.
		return_cursor:bool Нужно вернуть курсор (например, для дальнейшей фильтрации),
						   или выборку объектов
		"""

		lon1 = longitude - radius / abs(math.cos(math.radians(latitude)) * 111.0)  # 1 градус широты = 111 км
		lon2 = longitude + radius / abs(math.cos(math.radians(latitude)) * 111.0)
		lat1 = latitude - (radius / 111.0)
		lat2 = latitude + (radius / 111.0)

		# фильтрация по местоположению транспорта
		ts = Transport.query.filter(
			lat1 <= Transport.latitude, Transport.latitude <= lat2,
			lon1 <= Transport.longitude, Transport.longitude <= lon2
		)
		if return_cursor:
			return ts
		return ts.all()

	def can_calculate_price(self):
		"""Можно ли вычислить цену транспорта.
		Да, когда есть цена за минуту или день.
		Нет, когда нет цены за минуту и день."""
		if (self.minute_price is None or self.minute_price == 0) and \
				(self.day_price is None or self.minute_price == 0):
			return False
		return True

	def __repr__(self):
		return f'<Transport: model={self.model}, owner={self.owner.username}'
