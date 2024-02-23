import logging

from flask import jsonify
from http import HTTPStatus

from flask_restx import Namespace, Resource, marshal
from flask_jwt_extended import jwt_required
from .dto import auth_reqparser, user_model

from app.core.accounts.accounts_logic import (
	process_registration_request,
	process_login_request,
	process_about_me_request,
	process_logout_request,
	process_update_user_request,
	_get_token_expire_time
)

user_accounts_ns = Namespace(
	name='Account controller',
	description='Взаимодействие с аккаунтом пользователя',
	path='/account/',
	validate=True
)


@user_accounts_ns.route('/signup', endpoint='auth_register')
class RegisterUser(Resource):
	@user_accounts_ns.response(int(HTTPStatus.CREATED), 'Новый пользователь успешно создан.')
	@user_accounts_ns.response(int(HTTPStatus.CONFLICT), 'Пользователь уже зарегистрирован.')
	@user_accounts_ns.expect(auth_reqparser)
	def post(self):
		"""Регистрация нового аккаунта."""

		request_data = auth_reqparser.parse_args()
		username = request_data.get('username')
		password = request_data.get('password')

		process_registration_request(username, password)

		response = jsonify({
			'message': 'sign up successfully'
		})
		response.status_code = HTTPStatus.CREATED
		return response


@user_accounts_ns.route('/signin', endpoint='auth_login')
class LoginUser(Resource):
	@user_accounts_ns.response(int(HTTPStatus.OK), 'Пользователь аутентифицирован.')
	@user_accounts_ns.response(int(HTTPStatus.NOT_FOUND), 'Пользователь не найден.')
	@user_accounts_ns.expect(auth_reqparser)
	def post(self):
		"""Получение нового JWT токена."""

		logging.log(level=logging.DEBUG, msg="Пользователь хочет авторизоваться")
		request_data = auth_reqparser.parse_args()
		username = request_data.get('username')
		password = request_data.get('password')

		access_token, refresh_token = process_login_request(username, password)
		response = jsonify({
			'access_token': access_token,
			'refresh_token': refresh_token,
			'token_type': 'bearer',
			'expires_in': _get_token_expire_time()
		})
		response.status_code = HTTPStatus.OK
		response.headers['Cache-Control'] = 'no-store'
		response.headers['Pragma'] = 'no-cache'
		logging.log(level=logging.DEBUG, msg="Пользователь получает ответ на запрос авторизации")

		return response


@user_accounts_ns.route('/me')
class AboutUser(Resource):
	method_decorators = [jwt_required()]

	@user_accounts_ns.response(int(HTTPStatus.OK), 'Получена информация о пользователе.')
	@user_accounts_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@user_accounts_ns.doc(security='JWT')
	def get(self):
		"""Получение данных о текущем аккаунте."""

		user = process_about_me_request()
		response = jsonify(
			marshal(user, user_model)
		)
		response.status_code = HTTPStatus.OK
		return response


@user_accounts_ns.route('/signout')
class LogoutUser(Resource):
	method_decorators = [jwt_required()]

	@user_accounts_ns.response(int(HTTPStatus.OK), 'Пользователь вышел из аккаунта.')
	@user_accounts_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@user_accounts_ns.doc(security='JWT')
	def post(self):
		"""Выход из аккаунта."""

		process_logout_request()
		response = jsonify({
			'message': 'Вы вышли из аккаунта.'
		})

		response.status_code = HTTPStatus.OK
		return response


@user_accounts_ns.route('/update')
class UpdateUser(Resource):
	method_decorators = [jwt_required()]

	@user_accounts_ns.response(int(HTTPStatus.OK), 'Информация о пользователе обновлена')
	@user_accounts_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@user_accounts_ns.response(int(HTTPStatus.CONFLICT), 'Пользователь уже существует.')
	@user_accounts_ns.doc(security='JWT')
	@user_accounts_ns.expect(auth_reqparser)
	def put(self):
		"""Обновление своего аккаунта."""

		request_data = auth_reqparser.parse_args()
		username = request_data.get('username')
		password = request_data.get('password')

		user = process_update_user_request(username, password)

		user_info = marshal(user, user_model)
		response = jsonify({
			'message': 'Информация обновлена',
			**user_info
		})
		response.status_code = HTTPStatus.OK
		return response
