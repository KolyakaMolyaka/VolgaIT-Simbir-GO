from http import HTTPStatus
from flask import jsonify
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required

from app.core.payments.replenish_balance_logic import process_replenish_user_balance
payments_ns = Namespace(
	name='Payment controller',
	description='Взаимодействие с балансом аккаунта',
	path='/payment/',
	validate=True
)


@payments_ns.route('/hesoyam/<int:user_id>')
class ReplenishBalance(Resource):
	method_decorators = [jwt_required()]

	@payments_ns.response(int(HTTPStatus.OK), 'Баланс пользователя пополнен.')
	@payments_ns.response(int(HTTPStatus.NOT_FOUND), 'Пользователь не найден.')
	@payments_ns.response(int(HTTPStatus.FORBIDDEN), 'Недостаточно прав для пополнения баланса.')
	@payments_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не аутентифицирован.')
	@payments_ns.doc(security='JWT')
	def post(self, user_id):
		"""Пополнение баланса пользователя на 250000 денежных единиц."""

		process_replenish_user_balance(user_id)
		response = jsonify({
			'message': f'Баланс пользователя с id = {user_id} пополнен на 250 тысяч единиц.'
		})
		response.status_code = HTTPStatus.OK
		return response

