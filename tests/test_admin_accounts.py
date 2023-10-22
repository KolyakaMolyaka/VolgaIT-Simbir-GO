import sys
sys.path.append('../')

from http import HTTPStatus
import unittest
from app.app import create_app
from app.extensions.database import db
from app.extensions.database.models import User

from utils import *
from config import SetUpAdminMixin


class TestAdminAccountController(SetUpAdminMixin, unittest.TestCase):
	def admin_json(self):
		return {
			'username': self.admin_username,
			'password': self.admin_password
		}

	"""Получение списка всех аккаунтов"""

	def test_anonymous_get_list_account(self):
		"""Аноним получает список пользователей -> Не авторизован."""
		response = self.client.get('/api/admin/account/')
		self.assertEqual(int(HTTPStatus.UNAUTHORIZED), response.status_code)

	def test_user_get_list_account(self):
		"""Пользователь получает список пользователей -> Недостаточно прав."""
		user_json = new_user_payload()
		_, AUTH_HEADER = get_access_token_and_auth_header(self.client, user_json)

		response = self.client.get('/api/admin/account/', headers=AUTH_HEADER)

		self.assertEqual(int(HTTPStatus.FORBIDDEN), response.status_code)

	def test_admin_get_list_account(self):
		"""Админ получает список пользователей -> список пользователей."""
		_, AUTH_HEADER = login_by_json(self.client, self.admin_json())

		response = self.client.get('/api/admin/account/', headers=AUTH_HEADER)
		self.assertEqual(int(HTTPStatus.OK), response.status_code)

	def test_admin_get_list_account_with_count_param(self):
		"""Админ получает список пользователей с параметром ?count=x"""
		# добавляем 10 случайных аккаунтов
		add_users = 10
		register_users(self.client, add_users)

		count_users = 4
		query = {'count': count_users}

		# авторизация в качестве админа
		_, AUTH_HEADER = login_by_json(self.client, self.admin_json())
		response = self.client.get('/api/admin/account/', headers=AUTH_HEADER, query_string=query)

		resp_json = response.json

		self.assertEqual(count_users, len(resp_json))

	def test_admin_get_list_account_with_offset_param(self):
		"""Админ получает список аккаунтов с параметром ?start=x"""
		# добавление 10 случайных аккаунтов
		add_users = 10
		register_users(self.client, add_users)
		total_users = add_users + 1  # 1 is admin

		offset_users = 1
		query = {'start': offset_users}

		# авторизация в качестве админа
		_, AUTH_HEADER = login_by_json(self.client, self.admin_json())
		response = self.client.get('/api/admin/account/', headers=AUTH_HEADER, query_string=query)

		resp_json = response.json

		self.assertEqual(total_users - offset_users, len(resp_json))

	"""Создание администратором нового аккаунта """

	def test_anonymous_create_new_user(self):
		"""Аноним создаёт новый аккаунт от имени администратора -> Не авторизован."""
		new_user = new_user_payload_created_by_admin()
		response = self.client.post('/api/admin/account/', json=new_user)
		self.assertEqual(int(HTTPStatus.UNAUTHORIZED), response.status_code)

	def test_user_create_new_account(self):
		"""Пользоавтель создает новый аккаунт от имени администратора -> Доступ запрещен."""
		user_json = new_user_payload()
		_, AUTH_HEADER = get_access_token_and_auth_header(self.client, user_json)

		new_user_json = new_user_payload_created_by_admin()
		response = self.client.post('/api/admin/account/', json=new_user_json, headers=AUTH_HEADER)

		self.assertEqual(int(HTTPStatus.FORBIDDEN), response.status_code)

	def test_admin_create_new_account(self):
		"""Админ создаёт новый аккаунт -> ОК."""
		# авторизация в качестве админа
		_, AUTH_HEADER = login_by_json(self.client, self.admin_json())

		new_user = new_user_payload_created_by_admin()
		response = self.client.post('/api/admin/account/', json=new_user, headers=AUTH_HEADER)

		self.assertEqual(int(HTTPStatus.CREATED), response.status_code)

	def test_admin_create_new_account_with_exist_username(self):
		"""Админ создаёт новый аккаунт с существующим именем -> конфликт"""
		# авторизация в качестве админа
		_, AUTH_HEADER = login_by_json(self.client, self.admin_json())

		new_user = new_user_payload_created_by_admin()
		# создание 1-го аккаунта
		create_response = self.client.post('/api/admin/account/', json=new_user, headers=AUTH_HEADER)
		# создание 2-го аккаунта с таким же именем
		bad_create_response = self.client.post('/api/admin/account/', json=new_user, headers=AUTH_HEADER)

		self.assertEqual(int(HTTPStatus.CONFLICT), bad_create_response.status_code)

	"""Изменение администратором аккаунта по id"""

	def test_anonymous_edit_user(self):
		"""Аноним изменяет информацию об аккаунте -> Не авторизован."""
		new_user = new_user_payload_created_by_admin()
		response = self.client.put(f'/api/admin/account/{self.admin_id}', json=new_user)
		self.assertEqual(int(HTTPStatus.UNAUTHORIZED), response.status_code)

	def test_user_edit_account(self):
		"""Пользователь изменяет информацию об аккаунте от имени админа -> Доступ запрещён."""
		user_json = new_user_payload()
		_, AUTH_HEADER = get_access_token_and_auth_header(self.client, user_json)

		new_user_json = new_user_payload_created_by_admin()
		response = self.client.put(f'/api/admin/account/{self.admin_id}', json=new_user_json, headers=AUTH_HEADER)

		self.assertEqual(int(HTTPStatus.FORBIDDEN), response.status_code)

	def test_admin_edit_account(self):
		"""Админ редактирует аккаунт -> ОК."""
		new_user_id = 2
		user_json = new_user_payload()
		register_new_user(self.client, user_json)

		# авторизация в качестве админа
		_, AUTH_HEADER = login_by_json(self.client, self.admin_json())

		new_user = new_user_payload_created_by_admin(i=2)
		response = self.client.put(f'/api/admin/account/{new_user_id}', json=new_user, headers=AUTH_HEADER)

		self.assertEqual(int(HTTPStatus.OK), response.status_code)

	def test_admin_edit_not_found_account(self):
		"""Админ изменяет несуществующий аккаунт -> не найдено."""
		# авторизация в качестве админа
		not_found_user_id = 42
		_, AUTH_HEADER = login_by_json(self.client, self.admin_json())

		new_user = new_user_payload_created_by_admin(i=2)
		response = self.client.put(f'/api/admin/account/{not_found_user_id}', json=new_user, headers=AUTH_HEADER)

		self.assertEqual(int(HTTPStatus.NOT_FOUND), response.status_code)

	"""Удаление администратором аккаунта по id"""

	def test_anonymous_delete_account(self):
		"""Аноним удаляет аккаунт -> не авторизован."""
		response = self.client.delete(f'/api/admin/account/{self.admin_id}')
		self.assertEqual(int(HTTPStatus.UNAUTHORIZED), response.status_code)

	def test_user_delete_another_account(self):
		"""Пользователь удаляет аккаунт от имени админа -> запрещено."""
		user_json = new_user_payload()
		_, AUTH_HEADER = get_access_token_and_auth_header(self.client, user_json)

		response = self.client.delete(f'/api/admin/account/{self.admin_id}', headers=AUTH_HEADER)
		self.assertEqual(int(HTTPStatus.FORBIDDEN), response.status_code)

	def test_admin_delete_another_account(self):
		"""Админ удаляет аккаунт -> ОК."""
		new_user_id = 2
		user_json = new_user_payload()
		register_new_user(self.client, user_json)

		_, AUTH_HEADER = login_by_json(self.client, self.admin_json())
		response = self.client.delete(f'/api/admin/account/{new_user_id}', headers=AUTH_HEADER)

		self.assertEqual(int(HTTPStatus.OK), response.status_code)

	def test_admin_delete_not_found_account(self):
		"""Админ удаляет несуществующий аккаунт -> не найдено."""
		not_found_user = 42
		_, AUTH_HEADER = login_by_json(self.client, self.admin_json())
		response = self.client.delete(f'/api/admin/account/{not_found_user}', headers=AUTH_HEADER)

		self.assertEqual(int(HTTPStatus.NOT_FOUND), response.status_code)

	"""Получение информации об аккаунте по id"""

	def test_anonymous_get_account_info(self):
		"""Аноним получает информацию о пользователе -> не авторизован"""
		response = self.client.get(f'/api/admin/account/{self.admin_id}')
		self.assertEqual(int(HTTPStatus.UNAUTHORIZED), response.status_code)

	def test_user_get_other_account_info(self):
		"""Пользователь получает информацию от имени админа -> запрещено."""
		user_json = new_user_payload()
		_, AUTH_HEADER = get_access_token_and_auth_header(self.client, user_json)

		response = self.client.get(f'/api/admin/account/{self.admin_id}', headers=AUTH_HEADER)

		self.assertEqual(int(HTTPStatus.FORBIDDEN), response.status_code)

	def test_admin_get_other_account_info(self):
		"""Админ получает информацию о пользователе - ОК"""
		new_user_id = 2
		user_json = new_user_payload()
		register_new_user(self.client, user_json)

		_, AUTH_HEADER = login_by_json(self.client, self.admin_json())
		response = self.client.get(f'/api/admin/account/{new_user_id}', headers=AUTH_HEADER)

		self.assertEqual(int(HTTPStatus.OK), response.status_code)
		self.assertIn('username', response.json)
		self.assertIn('isAdmin', response.json)
		self.assertIn('balance', response.json)
		self.assertIn('password', response.json)

	def test_admin_get_not_found_account_info(self):
		"""Админ получает информацию о несуществующем аккаунте -> не найдено."""
		not_found_user_id = 42
		_, AUTH_HEADER = login_by_json(self.client, self.admin_json())
		response = self.client.get(f'/api/admin/account/{not_found_user_id}', headers=AUTH_HEADER)

		self.assertEqual(int(HTTPStatus.NOT_FOUND), response.status_code)


if __name__ == '__main__':
	unittest.main()
