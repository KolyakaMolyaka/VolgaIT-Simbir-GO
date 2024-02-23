from app.extensions.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from .transport import Transport


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(128), nullable=False, unique=True)
	password = db.Column(db.Text(), nullable=False)
	is_admin = db.Column(db.Boolean, default=False)
	balance = db.Column(db.Float, default=0)

	transports = db.relationship(Transport, backref='owner')

	def __repr__(self):
		return f'<User: username={self.username}>'

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def is_correct_password(self, password):
		""" Проверка, совпадает ли переданный пароль с настоящим """
		return check_password_hash(self.password, password)

	def save(self):
		""" Запись изменений пользователя в БД """
		db.session.add(self)
		db.session.commit()

	@classmethod
	def get_user_by_username(cls, username: str):
		""" Получение пользователя по username или None """
		return cls.query.filter_by(username=username).one_or_none()

	@classmethod
	def is_user_exists(cls, username: str):
		"""Проверка, существует ли пользователь с именем username"""

		user = cls.get_user_by_username(username)
		return True if user else False
