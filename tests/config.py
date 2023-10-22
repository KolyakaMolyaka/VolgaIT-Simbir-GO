from app.extensions.database import db
from app.app import create_app
from app.extensions.database.models import User


class DropDbMixin:
	def tearDown(self) -> None:
		with self.app.app_context():
			db.drop_all()


class SetUpMixin(DropDbMixin):
	def setUp(self) -> None:
		self.app = create_app(testing=True)
		with self.app.app_context():
			db.create_all()
			self.client = self.app.test_client()


class SetUpAdminMixin(SetUpMixin, DropDbMixin):
	def setUp(self) -> None:
		super(SetUpAdminMixin, self).setUp()

		# добавление администратора в бд
		with self.app.app_context():
			self.admin_username = 'admin'
			self.admin_password = 'secret'
			u = User(username=self.admin_username)
			u.set_password(self.admin_password)
			u.is_admin = True
			u.save()
			self.admin_id = u.id
