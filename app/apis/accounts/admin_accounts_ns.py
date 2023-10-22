from http import HTTPStatus
from flask import jsonify
from flask_restx import Namespace, Resource, marshal
from app.core.accounts.admin_accounts_logic import (
	process_admin_get_accounts_list,
	process_admin_create_user,
	process_admin_get_account_info,
	process_admin_update_user,
	process_admin_delete_user
)
from app.core.accounts.utils import jwt_and_is_admin_required
from .dto import user_model, pagination_parser

admin_accounts_ns = Namespace(
	name='Admin Account controller',
	description='Взаимодействие с аккаунтов администратора',
	path='/admin/account/',
	validate=True
)


@admin_accounts_ns.route('/')
class AccountsList(Resource):
	method_decorators = [jwt_and_is_admin_required]

	@admin_accounts_ns.response(int(HTTPStatus.OK), 'Получен список пользователей.')
	@admin_accounts_ns.response(int(HTTPStatus.FORBIDDEN), 'Отсутствуют права администратора.')
	@admin_accounts_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@admin_accounts_ns.doc(security='JWT')
	@admin_accounts_ns.expect(pagination_parser)
	def get(self):
		"""Получение списка всех аккаунтов."""

		request_args = pagination_parser.parse_args()
		start = request_args.get('start')
		count = request_args.get('count')

		users = process_admin_get_accounts_list(start, count)
		users_info = [marshal(u, user_model) for u in users]

		response = jsonify(users_info)
		response.status_code = HTTPStatus.OK
		return response

	@admin_accounts_ns.response(int(HTTPStatus.CREATED), 'Пользователь создан.')
	@admin_accounts_ns.response(int(HTTPStatus.CONFLICT), 'Пользователь уже существует.')
	@admin_accounts_ns.response(int(HTTPStatus.FORBIDDEN), 'Отсутствуют права администратора')
	@admin_accounts_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@admin_accounts_ns.doc(security='JWT')
	@admin_accounts_ns.expect(user_model)
	def post(self):
		"""Создание администратором нового аккаунта."""
		request_data = admin_accounts_ns.payload

		username = request_data.get('username')
		password = request_data.get('password')
		is_admin = request_data.get('isAdmin')
		balance = request_data.get('balance')

		process_admin_create_user(username, password, is_admin, balance)

		response = jsonify({
			'message': f'Пользователь {username} создан.'
		})
		response.status_code = HTTPStatus.CREATED

		return response


@admin_accounts_ns.route('/<int:user_id>')
class AccountInfo(Resource):
	method_decorators = [jwt_and_is_admin_required]

	@admin_accounts_ns.response(int(HTTPStatus.OK), 'Информация о пользователе с id = {user_id}.')
	@admin_accounts_ns.response(int(HTTPStatus.NOT_FOUND), 'Пользователь не найден.')
	@admin_accounts_ns.response(int(HTTPStatus.FORBIDDEN), 'Отсутствуют права администратора.')
	@admin_accounts_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@admin_accounts_ns.doc(security='JWT')
	def get(self, user_id):
		"""Получение информации об аккаунте по user_id."""

		user = process_admin_get_account_info(user_id)
		response = jsonify(
			marshal(user, user_model)
		)
		response.status_code = HTTPStatus.OK
		return response

	@admin_accounts_ns.response(int(HTTPStatus.OK), 'Информация о пользователе обновлена.')
	@admin_accounts_ns.response(int(HTTPStatus.CONFLICT), 'Новое имя пользователя уже занято.')
	@admin_accounts_ns.response(int(HTTPStatus.NOT_FOUND), 'Пользователь не найден.')
	@admin_accounts_ns.response(int(HTTPStatus.FORBIDDEN), 'Отсутствуют права администратора.')
	@admin_accounts_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@admin_accounts_ns.expect(user_model)
	@admin_accounts_ns.doc(security='JWT')
	def put(self, user_id):
		"""Изменением администратором аккаунта по id."""

		request_data = admin_accounts_ns.payload

		username = request_data.get('username')
		password = request_data.get('password')
		is_admin = request_data.get('isAdmin')
		balance = request_data.get('balance')

		user = process_admin_update_user(user_id, username, password, is_admin, balance)

		response = jsonify(marshal(user, user_model))
		response.status_code = HTTPStatus.OK
		return response

	@admin_accounts_ns.response(int(HTTPStatus.OK), 'Пользователь удалён.')
	@admin_accounts_ns.response(int(HTTPStatus.NOT_FOUND), 'Пользователь не найден.')
	@admin_accounts_ns.response(int(HTTPStatus.FORBIDDEN), 'Отсутствуют права администратора.')
	@admin_accounts_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@admin_accounts_ns.doc(security='JWT')
	def delete(self, user_id):
		"""Удаление аккаунта по id."""

		process_admin_delete_user(user_id)
		response = jsonify({
			'message': f'Пользователь с id = {user_id} удалён.'
		})
		response.status_code = HTTPStatus.OK
		return response
