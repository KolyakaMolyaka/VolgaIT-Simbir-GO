from datetime import datetime

from app.extensions.database import db
from . import Transport


class Rent(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	time_start = db.Column(db.DateTime(), nullable=False)
	time_end = db.Column(db.DateTime(), nullable=True)
	price_of_unit = db.Column(db.Float, nullable=False)
	price_type = db.Column(db.String(7), nullable=False)  # len('Minutes')
	final_price = db.Column(db.Float, nullable=True)

	transport_id = db.Column(db.Integer, db.ForeignKey('transport.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def save(self):
		""" Сохранить изменения в БД """
		db.session.add(self)
		db.session.commit()

	def calculate_final_price(self, rent_time_end: datetime):
		"""
		Вычисление финальной цены аренды.
		Сохраняется дата окончания аренды и финальная стоимость,
		которая рассчитывается на основе price_type
		"""

		self.time_end = rent_time_end
		delta = datetime.replace(self.time_end, tzinfo=None) - datetime.replace(self.time_start, tzinfo=None)

		seconds = abs(delta.total_seconds())
		if self.price_type == 'Days':
			days = seconds // 86400  # 1 day = 86400 secondss
			self.final_price = days * self.price_of_unit
		elif self.price_type == 'Minutes':
			minutes = seconds // 60
			self.final_price = minutes * self.price_of_unit

	@classmethod
	def rented_transports(cls):
		now = datetime.utcnow()
		pre_finished_rents = Rent.query.filter(Rent.time_start < now, now < Rent.time_end).all()
		not_finished_rents = Rent.query.filter(Rent.time_end == None).all()
		print('not finished')
		for r in not_finished_rents:
			print(r)
		print('=')
		return [*pre_finished_rents, *not_finished_rents]

	def __repr__(self):
		return f'<Rent: time_start={self.time_start}, time_end={self.time_end}>'
