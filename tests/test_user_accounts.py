import sys
sys.path.append('../')
from http import HTTPStatus
import unittest
from app.app import create_app
from app.extensions.database import db
from app.extensions.database.models import User, TokenBlocklist
from flask_jwt_extended import get_jti

from utils import *
from config import SetUpMixin


class TestAccountController(SetUpMixin, unittest.TestCase):
	"""Тест регистрации"""

	def test_register_new_user(self):
		"""Регистрация нового пользователя."""
		user_json = new_user_payload()
		response = register_new_user(self.client, user_json)

		self.assertEqual(response.status_code, int(HTTPStatus.CREATED), msg=response.json.get('message'))

		with self.app.app_context():
			# проврека, что был создан 1 ползователь
			created_users: int = User.query.count()
			self.assertEqual(created_users, 1)

			# проверка, что имя пользователя правильное
			created_user = User.query.first()
			self.assertEqual(user_json.get('username'), created_user.username)

	# можно проверить правильность пароля, но нужно ли это ...
	# ...

	def test_register_already_exist_user(self):
		"""Регистрация пользователя с именем, которое уже существует."""
		# регистрируем нового пользователя
		user_json = new_user_payload()
		register_new_user(self.client, user_json)
		# повторно регистрируем пользователя с такими же данными
		bad_register_response = register_new_user(self.client, user_json)

		self.assertEqual(bad_register_response.status_code, int(HTTPStatus.CONFLICT))

		with self.app.app_context():
			# проверка, что пользователь с таким же username не был создан
			created_users = User.query.count()
			self.assertEqual(created_users, 1)

	"""Тест авторизации"""

	def test_login_user(self):
		user_json = new_user_payload()
		login_response = register_and_login_user(self.client, user_json)
		self.assertEqual(login_response.status_code, int(HTTPStatus.OK), msg=login_response.json.get('message'))

		# проверка полей, согласно rfc2616
		login_json = login_response.json
		self.assertIn('access_token', login_json, 'отсутствует access_token в JSON при авторизации')
		self.assertIn('refresh_token', login_json, 'отсутствует refresh_token в JSON при авторизации')
		self.assertIn('expires_in', login_json)
		self.assertIn('token_type', login_json)

	def test_login_not_found_user(self):
		user_json = new_user_payload()
		bad_login_response = login_user(self.client, user_json)
		self.assertEqual(bad_login_response.status_code, int(HTTPStatus.NOT_FOUND))

	"""Тест получения информации о пользователе"""

	def test_anonymous_user_get_about_info(self):
		response = self.client.get('/api/account/me')
		self.assertEqual(response.status_code, int(HTTPStatus.UNAUTHORIZED))

	def test_logined_user_get_about_info(self):
		# авторизация пользователя
		user_json = new_user_payload()
		# получение access_token после авторизации
		access_token, AUTH_HEADER = get_access_token_and_auth_header(self.client, user_json)
		AUTH_HEADER = {'Authorization': f'Bearer {access_token}'}

		# получение информации о пользователе
		about_response = self.client.get('/api/account/me', headers=AUTH_HEADER)

		self.assertEqual(about_response.status_code, int(HTTPStatus.OK))
		self.assertIn('balance', about_response.json)
		self.assertIn('isAdmin', about_response.json)
		self.assertIn('password', about_response.json)
		self.assertIn('username', about_response.json)

	"""Тест выхода из аккаунта"""

	def test_user_logout(self):
		user_json = new_user_payload()

		access_token, AUTH_HEADER = get_access_token_and_auth_header(self.client, user_json)
		logout_response = self.client.post('/api/account/signout', headers=AUTH_HEADER)

		self.assertEqual(logout_response.status_code, int(HTTPStatus.OK))

		# проверка, что предыдущий токен заблокирован
		with self.app.app_context():
			blocked_tokens = TokenBlocklist.query.count()
			self.assertEqual(blocked_tokens, 1)

			access_token_jti = get_jti(encoded_token=access_token)
			blocked_token_jti = TokenBlocklist.query.first().jti
			self.assertEqual(access_token_jti, blocked_token_jti)

	def test_anonymous_user_logout(self):
		logout_response = self.client.post('/api/account/signout')
		self.assertEqual(logout_response.status_code, int(HTTPStatus.UNAUTHORIZED))

	"""Тест пользователь изменяет информацию об аккаунте"""

	def test_user_edit_his_account_info(self):
		# создание пользователя
		user_json = new_user_payload()
		access_token, AUTH_HEADER = get_access_token_and_auth_header(self.client, user_json)

		# обновление информации о пользователе
		new_user_json = {k: v + '_updated' for k, v in new_user_payload().items()}
		update_user_response = self.client.put('/api/account/update', json=new_user_json, headers=AUTH_HEADER)

		# инфомрация о пользователе обновлена
		self.assertEqual(update_user_response.status_code, int(HTTPStatus.OK))

		# проверка, что пользователь изменен в БД
		with self.app.app_context():
			user = User.query.first()
			self.assertEqual(user.username, new_user_json.get('username'))

	def test_user_edit_his_account_with_exists_username(self):
		user_json1 = new_user_payload()
		register_and_login_user(self.client, user_json1)

		user_json2 = {k: v + '_new' for k, v in new_user_payload().items()}
		access_token2, AUTH_HEADER2 = get_access_token_and_auth_header(self.client, user_json2)

		bad_update_response = self.client.put('/api/account/update', json=user_json1, headers=AUTH_HEADER2)

		self.assertEqual(bad_update_response.status_code, int(HTTPStatus.CONFLICT))

	def test_anonymous_edit_account_info(self):
		user_json = new_user_payload()
		bad_update_response = self.client.put('/api/account/update', json=user_json)

		self.assertEqual(bad_update_response.status_code, int(HTTPStatus.UNAUTHORIZED))


if __name__ == '__main__':
	unittest.main()
