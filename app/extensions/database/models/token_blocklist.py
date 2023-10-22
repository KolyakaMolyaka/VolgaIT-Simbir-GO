from datetime import datetime

from app.extensions.database import db


class TokenBlocklist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	jti = db.Column(db.String(), nullable=False)
	create_at = db.Column(db.DateTime(), default=datetime.utcnow)

	def __repr__(self):
		return f'<Token {self.jti}>'

	def save(self):
		""" Сохранение изменений в БД """
		db.session.add(self)
		db.session.commit()
