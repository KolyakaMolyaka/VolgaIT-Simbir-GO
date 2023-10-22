from http import HTTPStatus
from flask import jsonify
from flask_restx import Namespace, Resource, marshal
from flask_jwt_extended import jwt_required
from .dto import user_transport_model, owner_transport_model, edit_transport_model

from app.core.transports.user_transports_logic import (
	process_user_create_new_transport,
	process_user_get_transport_info,
	process_user_update_transport_info,
	process_user_delete_transport
)

user_transport_ns = Namespace(
	name='Transport controller',
	description='Взаимодействие с транспортом пользователя',
	path='/transport/',
	validate=True
)


@user_transport_ns.route('/')
class CreateTransport(Resource):
	method_decorators = [jwt_required()]

	@user_transport_ns.response(int(HTTPStatus.CREATED), 'Транспорт создан.')
	@user_transport_ns.response(int(HTTPStatus.BAD_REQUEST), 'Некорректный запрос.')
	@user_transport_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@user_transport_ns.doc(security='JWT')
	@user_transport_ns.expect(user_transport_model)
	def post(self):
		"""Добавление нового транспорта."""

		request_data = user_transport_ns.payload
		can_be_rented = request_data.get('canBeRented')
		transport_type = request_data.get('transportType')
		model = request_data.get('model')
		color = request_data.get('color')
		identifier = request_data.get('identifier')
		latitude = request_data.get('latitude')
		longitude = request_data.get('longitude')
		description = request_data.get('description', user_transport_model.get('description').default)
		minute_price = request_data.get('minutePrice', user_transport_model.get('minutePrice').default)
		day_price = request_data.get('dayPrice', user_transport_model.get('dayPrice').default)

		transport = process_user_create_new_transport(can_be_rented, transport_type, model, color, identifier, latitude,
										  longitude, description, minute_price, day_price)

		response = jsonify(marshal(transport, user_transport_model))
		response.status_code = HTTPStatus.CREATED

		return request_data


def public_route(decorated_func):
	"""
	https://stackoverflow.com/questions/63188214/adding-auth-decorators-to-flask-restx
	This is a decorator to specify public endpoints in our flask routes
	:param decorated_func:
	:return:
	"""
	decorated_func.is_public = True
	return decorated_func


def _perform_auth(method):
	is_public_endpoint = getattr(method, 'is_public', False)
	decorator = jwt_required()
	if is_public_endpoint:
		return method
	return decorator(method)


@user_transport_ns.route('/<int:transport_id>')
class TransportAuthInfo(Resource):
	method_decorators = [_perform_auth]

	@user_transport_ns.response(int(HTTPStatus.OK), 'Информация обновлена.')
	@user_transport_ns.response(int(HTTPStatus.NOT_FOUND), 'Транспорт не найден.')
	@user_transport_ns.response(int(HTTPStatus.FORBIDDEN),
								'Пользователь не является владельцем обновляемого транспорта.')
	@user_transport_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@user_transport_ns.doc(security='JWT')
	@user_transport_ns.expect(edit_transport_model)
	def put(self, transport_id):
		"""Изменение транспорта по id. Только авторизованные пользователи."""

		request_data = user_transport_ns.payload
		can_be_rented = request_data.get('canBeRented')
		model = request_data.get('model')
		color = request_data.get('color')
		identifier = request_data.get('identifier')
		latitude = request_data.get('latitude')
		longitude = request_data.get('longitude')
		description = request_data.get('description', user_transport_model.get('description').default)
		minute_price = request_data.get('minutePrice', user_transport_model.get('minutePrice').default)
		day_price = request_data.get('dayPrice', user_transport_model.get('dayPrice').default)

		transport = process_user_update_transport_info(
			transport_id, can_be_rented, model, color, identifier, latitude, longitude,
			description, minute_price, day_price)

		response = jsonify(marshal(transport, user_transport_model))
		response.status_code = HTTPStatus.OK

		return response

	@user_transport_ns.response(int(HTTPStatus.OK), 'Транспорт удалён.')
	@user_transport_ns.response(int(HTTPStatus.NOT_FOUND), 'Транспорт не найден.')
	@user_transport_ns.response(int(HTTPStatus.FORBIDDEN), 'Пользователь не является владельцем транспорта.')
	@user_transport_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@user_transport_ns.doc(security='JWT')
	def delete(self, transport_id):
		"""Удаление транспорта по id. Только авторизованные пользователи."""

		process_user_delete_transport(transport_id)

		response = jsonify({
			'message': 'Транспорт удалён.'
		})
		response.status_code = HTTPStatus.OK

		return response

	@user_transport_ns.response(int(HTTPStatus.OK), 'Информация о транспорте.')
	@user_transport_ns.response(int(HTTPStatus.NOT_FOUND), 'Транспорт не найден.')
	@public_route
	def get(self, transport_id):
		"""Получение информации о транспорте по id."""

		transport = process_user_get_transport_info(transport_id)

		response = jsonify(marshal(transport, owner_transport_model))

		response.status_code = HTTPStatus.OK

		return response
