from app.extensions.database.models import User, TokenBlocklist
from flask_jwt_extended import JWTManager
from flask import jsonify

jwt = JWTManager()


@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(jwt_header, jwt_data):
	""" Проверка, находится ли JWT токен в блок-листе """
	jti = jwt_data['jti']
	blocked_token = TokenBlocklist.query.filter_by(jti=jti).all()
	return True if blocked_token else False


@jwt.user_lookup_loader
def user_lookup_callback(jwt_headers, jwt_data):
	""" Получение пользователя по JWT токену для использования current_user или get_current_user """
	identity = jwt_data['sub']
	user = User.query.get(identity)
	return user


@jwt.additional_claims_loader
def make_additional_claims(identity):
	""" Создание дополнительных JWT claims """
	user = User.query.get(identity)
	return {'is_admin': user.is_admin}


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
	""" Обработчик в случае недействительного (истёкшего) JWT Access/Refresh Token """
	return jsonify({'message': 'Token has expired', 'error': 'token_expired'}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
	""" Обработчик в случае неправильного JWT Access Token """
	return jsonify({'message': 'Signature verification failed', 'error': 'invalid_token'}), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
	""" Обработчик в случае отсутствия JWT Access Token """
	return jsonify({'message': 'Request doesnt contain a valid token', 'error': 'authorization_required'}), 401
