from datetime import datetime
from http import HTTPStatus
from flask import jsonify
from flask_restx import Resource, Namespace, marshal
from .dto import rent_model, transport_cords_reqparser
from app.core.rents.admin_rents_logic import (
	process_admin_create_rent,
	process_admin_get_rent_info,
	process_admin_get_user_rent_history,
	process_admin_get_transport_rent_history,
	process_admin_end_user_rent,
	process_admin_delete_rent,
	process_admin_edit_rent
)
from app.core.accounts.utils.admin_utils import jwt_and_is_admin_required

admin_rents_ns = Namespace(
	name='Admin Rent controller',
	description='Взаимодействие с арендами от имени администратора',
	path='/admin/',
	validate=True
)


@admin_rents_ns.route('/rent')
class RentList(Resource):
	method_decorators = [jwt_and_is_admin_required]

	@admin_rents_ns.response(int(HTTPStatus.OK), 'Аренда создана.')
	@admin_rents_ns.response(int(HTTPStatus.CONFLICT), 'Невозможно создание аренды.')
	@admin_rents_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@admin_rents_ns.response(int(HTTPStatus.FORBIDDEN), 'Отсутствуют права администратора.')
	@admin_rents_ns.response(int(HTTPStatus.NOT_FOUND), 'Пользователь/транспорт не найден.')
	@admin_rents_ns.doc(security='JWT')
	@admin_rents_ns.expect(rent_model)
	def post(self):
		"""Создание новой аренды."""

		request_data = admin_rents_ns.payload
		transport_id = request_data.get('transportId')
		user_id = request_data.get('userId')
		time_start = datetime.fromisoformat(request_data.get('timeStart'))
		price_of_unit = request_data.get('priceOfUnit')
		price_type = request_data.get('priceType')
		time_end = request_data.get('timeEnd')
		if time_end:
			time_end = datetime.fromisoformat(time_end)
		final_price = request_data.get('finalPrice')

		process_admin_create_rent(
			transport_id, user_id, time_start, price_of_unit, price_type,
			time_end, final_price
		)

		response = jsonify({
			'message': 'Аренда успешно создана'
		})
		response.status_code = HTTPStatus.OK

		return response


@admin_rents_ns.route('/rent/<int:rent_id>')
class Rent(Resource):
	method_decorators = [jwt_and_is_admin_required]

	@admin_rents_ns.response(int(HTTPStatus.OK), 'Информация об аренде.')
	@admin_rents_ns.response(int(HTTPStatus.NOT_FOUND), 'Аренда не найдена.')
	@admin_rents_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@admin_rents_ns.response(int(HTTPStatus.FORBIDDEN), 'Отсутствуют права администратора.')
	@admin_rents_ns.doc(security='JWT')
	def get(self, rent_id):
		"""Получение информации об аренде по id."""

		rent = process_admin_get_rent_info(rent_id)

		response = jsonify(marshal(rent, rent_model))
		response.status_code = HTTPStatus.OK

		return response

	@admin_rents_ns.response(int(HTTPStatus.OK), 'Аренда удалена.')
	@admin_rents_ns.response(int(HTTPStatus.NOT_FOUND), 'Аренда не найдена.')
	@admin_rents_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@admin_rents_ns.response(int(HTTPStatus.FORBIDDEN), 'Отсутствуют права администратора.')
	@admin_rents_ns.doc(security='JWT')
	def delete(self, rent_id):
		"""Удаление информации об аренде по id."""

		process_admin_delete_rent(rent_id)
		response = jsonify({
			'message': 'Аренда удалена.'
		})

		response.status_code = HTTPStatus.OK
		return response

	@admin_rents_ns.response(int(HTTPStatus.OK), 'Аренда обновлена.')
	@admin_rents_ns.response(int(HTTPStatus.NOT_FOUND), 'Транспорт/Владелец/Аренда не найдены.')
	@admin_rents_ns.response(int(HTTPStatus.CONFLICT), 'Пользователь не может арендовать свой транспорт.')
	@admin_rents_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@admin_rents_ns.response(int(HTTPStatus.FORBIDDEN), 'Отсутствуют права администратора.')
	@admin_rents_ns.doc(security='JWT')
	@admin_rents_ns.expect(rent_model)
	def put(self, rent_id):
		"""Изменение записи об аренде по id."""

		request_data = admin_rents_ns.payload
		transport_id = request_data.get('transportId')
		user_id = request_data.get('userId')
		time_start = datetime.fromisoformat(request_data.get('timeStart'))
		price_of_unit = request_data.get('priceOfUnit')
		price_type = request_data.get('priceType')
		time_end = request_data.get('timeEnd')
		if time_end:
			time_end = datetime.fromisoformat(time_end)
		final_price = request_data.get('finalPrice')

		process_admin_edit_rent(rent_id, transport_id, user_id, time_start, price_of_unit, price_type, time_end, final_price)

		response = jsonify({
			'message': 'Аренда обновлена.'
		})
		response.status_code = HTTPStatus.OK

		return response



@admin_rents_ns.route('/userhistory/<int:user_id>')
class UserRentHistory(Resource):
	method_decorators = [jwt_and_is_admin_required]

	@admin_rents_ns.response(int(HTTPStatus.OK), 'Список аренд пользователя.')
	@admin_rents_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@admin_rents_ns.response(int(HTTPStatus.FORBIDDEN), 'Отсутствуют права администратора.')
	@admin_rents_ns.doc(security='JWT')
	def get(self, user_id):
		"""Получение истории аренд пользователя."""

		rents = process_admin_get_user_rent_history(user_id)
		rents_info = [marshal(r, rent_model) for r in rents]

		response = jsonify(rents_info)
		response.status_code = HTTPStatus.OK

		return response


@admin_rents_ns.route('/transporthistory/<int:transport_id>')
class TransportRentHistory(Resource):
	method_decorators = [jwt_and_is_admin_required]

	@admin_rents_ns.response(int(HTTPStatus.OK), 'Список аренд транспорта.')
	@admin_rents_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@admin_rents_ns.response(int(HTTPStatus.FORBIDDEN), 'Отсутствуют права администратора.')
	@admin_rents_ns.doc(security='JWT')
	def get(self, transport_id):
		"""Получение истории аренд транспорта по id."""

		rents = process_admin_get_transport_rent_history(transport_id)
		rents_info = [marshal(r, rent_model) for r in rents]

		response = jsonify(rents_info)
		response.status_code = HTTPStatus.OK

		return response


@admin_rents_ns.route('/rent/end/<int:rent_id>')
class EndRent(Resource):
	method_decorators = [jwt_and_is_admin_required]

	@admin_rents_ns.response(int(HTTPStatus.OK), 'Аренда завершена.')
	@admin_rents_ns.response(int(HTTPStatus.NOT_FOUND), 'Аренда не найдена.')
	@admin_rents_ns.response(int(HTTPStatus.CONFLICT), 'Окончание аренды была запланировано при создании.')
	@admin_rents_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@admin_rents_ns.response(int(HTTPStatus.FORBIDDEN), 'Отсутствуют права администратора.')
	@admin_rents_ns.doc(security='JWT')
	@admin_rents_ns.expect(transport_cords_reqparser)
	def post(self, rent_id):
		"""Завершение аренды транспорта по id аренды."""

		request_args = transport_cords_reqparser.parse_args()
		latitude = request_args.get('lat')
		longitude = request_args.get('long')

		process_admin_end_user_rent(rent_id, latitude, longitude)

		response = jsonify({
			'message': 'Аренда завершена.'
		})
		response.status_code = HTTPStatus.OK

		return response
