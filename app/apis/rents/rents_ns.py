import logging
from http import HTTPStatus
from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, marshal
from app.core.rents.rents_logic import (
	process_get_free_transport_for_rent_list,
	process_user_rents_transport,
	process_user_end_rents_transport,
	process_user_get_rents_history,
	process_user_get_rent_info,
	process_user_get_transports_history
)
from app.apis.transports.dto import owner_transport_model
from .dto import (
	free_for_rent_transport_reqparser,
	rent_type_reqparser,
	transport_cords_reqparser,
	rent_model
)

rents_ns = Namespace(
	name='Rent controller',
	description='Аренда транспорта',
	path='/rent'
)


@rents_ns.route('/transport')
class FreeForRentTransportList(Resource):
	@rents_ns.response(int(HTTPStatus.OK), 'Список доступного для аренды транспорта.')
	@rents_ns.expect(free_for_rent_transport_reqparser)
	def get(self):
		"""Получение транспорта, доступного для аренды."""


		logging.log(level=logging.DEBUG, msg='Пользователь хочет получить информацию о транспорте для аренды')
		request_args = free_for_rent_transport_reqparser.parse_args()

		latitude = request_args.get('lat')
		longitude = request_args.get('long')
		radius = request_args.get('radius')
		type = request_args.get('type')

		transports = process_get_free_transport_for_rent_list(latitude, longitude, radius, type)

		transports_info = [marshal(t, owner_transport_model) for t in transports]
		response = jsonify(transports_info)
		response.status_code = HTTPStatus.OK

		logging.log(level=logging.DEBUG, msg=f'Пользователь получил ответ на запрос об информацию ТС для аренды: {len(transports)} ТС')


		return response


@rents_ns.route('/<int:rent_id>')
class RentList(Resource):
	method_decorators = [jwt_required()]

	@rents_ns.response(int(HTTPStatus.OK), 'Информация об аренде.')
	@rents_ns.response(int(HTTPStatus.NOT_FOUND), 'Аренда не найдена.')
	@rents_ns.response(int(HTTPStatus.FORBIDDEN), 'Пользователь не является арендатором или владельцем транспорта.')
	@rents_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@rents_ns.doc(security='JWT')
	def get(self, rent_id):
		"""Получение информации об аренде по id."""

		rent = process_user_get_rent_info(rent_id)

		response = jsonify(
			marshal(rent, rent_model)
		)
		response.status_code = HTTPStatus.OK

		return response


@rents_ns.route('/myhistory')
class UserRentHistory(Resource):
	method_decorators = [jwt_required()]

	@rents_ns.response(int(HTTPStatus.OK), 'История аренд.')
	@rents_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@rents_ns.doc(security='JWT')
	def get(self):
		"""Получение истории аренд текущего аккаунта."""

		rs = process_user_get_rents_history()
		rents_info = [marshal(r, rent_model) for r in rs]

		response = jsonify(rents_info)
		response.status_code = HTTPStatus.OK

		return response


@rents_ns.route('/transporthistory/<int:transport_id>')
class TransportRentHistory(Resource):
	method_decorators = [jwt_required()]

	@rents_ns.response(int(HTTPStatus.OK), 'История аренд транспорта')
	@rents_ns.response(int(HTTPStatus.NOT_FOUND), 'Транспорт не найден.')
	@rents_ns.response(int(HTTPStatus.FORBIDDEN), 'Пользователь не является владельцем транспорта.')
	@rents_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@rents_ns.doc(security='JWT')
	def get(self, transport_id):
		"""Получение истории аренд транспорта."""

		rs = process_user_get_transports_history(transport_id)
		rs_info = [marshal(r, rent_model) for r in rs]

		response = jsonify(rs_info)
		response.status_code = HTTPStatus.OK

		return response


@rents_ns.route('/new/<int:transport_id>')
class CreateRent(Resource):
	method_decorators = [jwt_required()]

	@rents_ns.response(int(HTTPStatus.OK), 'Транспорт арендован.')
	@rents_ns.response(int(HTTPStatus.NOT_FOUND), 'Транспорт не найден.')
	@rents_ns.response(int(HTTPStatus.CONFLICT), 'Транспорт не может быть арендован.')
	@rents_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@rents_ns.doc(security='JWT')
	@rents_ns.expect(rent_type_reqparser)
	def post(self, transport_id):
		"""Аренда транспорта в личное пользование."""

		request_args = rent_type_reqparser.parse_args()
		rent_type = request_args.get('rentType')

		process_user_rents_transport(transport_id, rent_type)

		response = jsonify({
			'message': f'Вы арендовали транспорт с id = {transport_id}.'
		})
		response.status_code = HTTPStatus.OK

		return response


@rents_ns.route('/end/<int:rent_id>')
class FinishRent(Resource):
	method_decorators = [jwt_required()]

	@rents_ns.response(int(HTTPStatus.OK), 'Аренда завершена')
	@rents_ns.response(int(HTTPStatus.NOT_FOUND), 'Аренда отсутствует.')
	@rents_ns.response(int(HTTPStatus.CONFLICT), 'Невозможно завершить аренду.')
	@rents_ns.response(int(HTTPStatus.FORBIDDEN), 'Пользователь не является арендатором.')
	@rents_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@rents_ns.doc(security='JWT')
	@rents_ns.expect(transport_cords_reqparser)
	def post(self, rent_id):
		"""Завершение аренды транспорта по id аренды."""
		request_args = transport_cords_reqparser.parse_args()
		latitude = request_args.get('lat')
		longitude = request_args.get('long')

		process_user_end_rents_transport(latitude, longitude, rent_id)

		response = jsonify({
			'message': 'Аренда завершена.'
		})

		response.status_code = HTTPStatus.OK

		return response
