import functools

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request


def jwt_and_is_admin_required(view_function):
	"""
	Проверка на наличие JWT токена и администраторских прав.
	Если пользователь является администраторов, то он получает доступ к ресурсу,
	в противном случае пользователь получает сообщение Permission denied.
	"""

	@functools.wraps(view_function)
	def decorated(*args, **kwargs):
		_, jwt_data = verify_jwt_in_request()
		if not jwt_data.get('is_admin') is True:
			return {'message': 'Permission denied'}, 403
		return view_function(*args, **kwargs)

	return decorated
