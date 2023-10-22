from http import HTTPStatus
from flask import jsonify
from flask_restx import Namespace, Resource, marshal
from app.core.accounts.utils import jwt_and_is_admin_required
from app.core.transports.admin_transports_logic import (
	process_admin_get_transports_list,
	process_admin_create_transport,
	process_admin_get_transport_info,
	process_admin_edit_transport_info,
	process_admin_delete_transport
)
from .dto import pagination_with_transport_type_parser, owner_transport_model

admin_transport_ns = Namespace(
	name='Admin Transport controller',
	description='Взаимодействие с транспортом от имени администратора',
	path='/admin/transport',
	validate=True
)


@admin_transport_ns.route('/')
class TransportList(Resource):
	method_decorators = [jwt_and_is_admin_required]

	@admin_transport_ns.response(int(HTTPStatus.OK), 'Список транспортных средств.')
	@admin_transport_ns.response(int(HTTPStatus.FORBIDDEN), 'Отсутствуют права администратора.')
	@admin_transport_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@admin_transport_ns.expect(pagination_with_transport_type_parser)
	@admin_transport_ns.doc(security='JWT')
	def get(self):
		"""Получение списка всех транспортных средств."""

		request_args = pagination_with_transport_type_parser.parse_args()
		start = request_args.get('start')
		count = request_args.get('count')
		transport_type = request_args.get('transportType')

		transports = process_admin_get_transports_list(start, count, transport_type)
		transports_info = [marshal(t, owner_transport_model) for t in transports]

		response = jsonify(transports_info)
		response.status_code = HTTPStatus.OK

		return response

	@admin_transport_ns.response(int(HTTPStatus.OK), 'Транспорт создан.')
	@admin_transport_ns.response(int(HTTPStatus.NOT_FOUND), 'Владелец транспорта не найден.')
	@admin_transport_ns.response(int(HTTPStatus.FORBIDDEN), 'Отсутствуют права администратора.')
	@admin_transport_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@admin_transport_ns.doc(security='JWT')
	@admin_transport_ns.expect(owner_transport_model)
	def post(self):
		"""Создание нового транспорта."""

		request_data = admin_transport_ns.payload
		owner_id = request_data.get('ownerId')
		can_be_rented = request_data.get('canBeRented')
		transport_type = request_data.get('transportType')
		model = request_data.get('model')
		color = request_data.get('color')
		identifier = request_data.get('identifier')
		latitude = request_data.get('latitude')
		longitude = request_data.get('longitude')
		description = request_data.get('description', owner_transport_model.get('description').default)
		minute_price = request_data.get('minutePrice', owner_transport_model.get('minutePrice').default)
		day_price = request_data.get('dayPrice', owner_transport_model.get('dayPrice').default)

		process_admin_create_transport(owner_id, can_be_rented, transport_type, model, color, identifier, latitude,
									   longitude, description, minute_price, day_price)

		response = jsonify({
			'message': 'Транспорт создан.'
		})
		response.status_code = HTTPStatus.OK

		return response


@admin_transport_ns.route('/<int:transport_id>')
class Transport(Resource):
	method_decorators = [jwt_and_is_admin_required]

	@admin_transport_ns.response(int(HTTPStatus.OK), 'Информация о транспорте.')
	@admin_transport_ns.response(int(HTTPStatus.NOT_FOUND), 'Транспорт не найден.')
	@admin_transport_ns.response(int(HTTPStatus.FORBIDDEN), 'Отсутствуют права администратора.')
	@admin_transport_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@admin_transport_ns.doc(security='JWT')
	def get(self, transport_id):
		"""Получение информации о транспорте по id."""
		transport = process_admin_get_transport_info(transport_id)

		response = jsonify(marshal(transport, owner_transport_model))
		response.status_code = HTTPStatus.OK

		return response

	@admin_transport_ns.response(int(HTTPStatus.OK), 'Информация о транспорте обновлена.')
	@admin_transport_ns.response(int(HTTPStatus.NOT_FOUND), 'Транспорт/владелец_транспорта не найден.')
	@admin_transport_ns.response(int(HTTPStatus.FORBIDDEN), 'Отсутствуют права администратора.')
	@admin_transport_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@admin_transport_ns.doc(security='JWT')
	@admin_transport_ns.expect(owner_transport_model)
	def put(self, transport_id):
		"""Изменение транспорта по id."""

		request_data = admin_transport_ns.payload
		owner_id = request_data.get('ownerId')
		can_be_rented = request_data.get('canBeRented')
		transport_type = request_data.get('transportType')
		model = request_data.get('model')
		color = request_data.get('color')
		identifier = request_data.get('identifier')
		latitude = request_data.get('latitude')
		longitude = request_data.get('longitude')
		description = request_data.get('description', owner_transport_model.get('description').default)
		minute_price = request_data.get('minutePrice', owner_transport_model.get('minutePrice').default)
		day_price = request_data.get('dayPrice', owner_transport_model.get('dayPrice').default)

		transport = process_admin_edit_transport_info(transport_id, owner_id, can_be_rented, transport_type, model,
													  color, identifier, latitude,
													  longitude, description, minute_price, day_price)

		response = jsonify(marshal(transport, owner_transport_model))
		response.status_code = HTTPStatus.OK

		return response

	@admin_transport_ns.response(int(HTTPStatus.OK), 'Транспорт удалён.')
	@admin_transport_ns.response(int(HTTPStatus.NOT_FOUND), 'Транспорт не найден.')
	@admin_transport_ns.response(int(HTTPStatus.FORBIDDEN), 'Отсутствуют права администратора.')
	@admin_transport_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@admin_transport_ns.doc(security='JWT')
	def delete(self, transport_id):
		"""Удаление транспорта по id."""

		process_admin_delete_transport(transport_id)

		response = jsonify({
			'message': f'Траспорт с id = {transport_id} удалён.'
		})
		response.status_code = HTTPStatus.OK

		return response
