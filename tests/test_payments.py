import sys

sys.path.append('../')

from http import HTTPStatus
import unittest
from app.app import create_app
from app.extensions.database import db
from app.extensions.database.models import User

from utils import *
from config import SetUpMixin


class TestPaymentController(SetUpMixin, unittest.TestCase):
	def test_anonymous_add_balance_to_account(self):
		user_id = 42
		response = self.client.post(f'/api/payment/hesoyam/{user_id}')
		self.assertEqual(response.status_code, int(HTTPStatus.UNAUTHORIZED), response.json.get('message'))

	def test_user_add_balance_to_another_account(self):
		# создание первого пользовтеля
		user_id1 = 1
		user_json1 = new_user_payload()
		register_new_user(self.client, user_json1)

		# создание второго пользователя user_id2 = 2
		user_json2 = {k: v + '2' for k, v in new_user_payload().items()}
		access_token2, AUTH_HEADER2 = get_access_token_and_auth_header(self.client, user_json2)

		# пополнение баланса первого пользователя от имени первого пользователя
		bad_response = self.client.post(f'/api/payment/hesoyam/{user_id1}', headers=AUTH_HEADER2)

		self.assertEqual(bad_response.status_code, int(HTTPStatus.FORBIDDEN))

	def test_user_add_balance_account(self):
		# создание пользователя
		user_id = 1
		user_json = new_user_payload()
		access_token, AUTH_HEADER = get_access_token_and_auth_header(self.client, user_json)

		# пополнение баланса первого пользователя от имени первого пользователя
		bad_response = self.client.post(f'/api/payment/hesoyam/{user_id}', headers=AUTH_HEADER)

		self.assertEqual(bad_response.status_code, int(HTTPStatus.OK))
		with self.app.app_context():
			user = User.query.first()

			self.assertEqual(user.balance, 250_000)


class TestAdminPaymentController(unittest.TestCase):
	def setUp(self) -> None:
		self.app = create_app(testing=True)
		with self.app.app_context():
			db.create_all()
			self.client = self.app.test_client()

			# добавление администратора в бд
			self.admin_username = 'admin'
			self.admin_password = 'secret'
			u = User(username=self.admin_username)
			u.set_password(self.admin_password)
			u.is_admin = True
			u.save()

	def tearDown(self) -> None:
		with self.app.app_context():
			db.drop_all()

	def test_admin_add_balance_to_user(self):
		# создание второго пользователя user_id = 2

		user_json = new_user_payload()
		user_id2 = 2
		register_resp = register_new_user(self.client, user_json)
		self.assertEqual(register_resp.status_code, int(HTTPStatus.CREATED))

		# получение токена для администратора
		admin_json = {
			'username': self.admin_username,
			'password': self.admin_password
		}
		login_response = login_user(self.client, admin_json)
		access_token = login_response.json.get('access_token')
		AUTH_HEADER = {'Authorization': f'Bearer {access_token}'}

		# пополнение баланса первого пользователя от имени первого пользователя
		bad_response = self.client.post(f'/api/payment/hesoyam/{user_id2}', headers=AUTH_HEADER)

		self.assertEqual(bad_response.status_code, int(HTTPStatus.OK))

		with self.app.app_context():
			u2 = User.query.get(user_id2)

			self.assertEqual(u2.balance, 250_000)


if __name__ == '__main__':
	unittest.main()
