from flask_restx import Model, fields
from flask_restx.reqparse import RequestParser

""" DTO """
user_model = Model('User', {
	'id': fields.Integer(required=False),
	'username': fields.String(required=True, example='markeeff'),
	'password': fields.String(required=True, example='super-secret'),
	'isAdmin': fields.Boolean(required=True, attribute='is_admin', example=False),
	'balance': fields.Float(required=True, example=0)
})

# auth parser
auth_reqparser = RequestParser(bundle_errors=True)
auth_reqparser.add_argument(
	name='username', type=str, location='json', required=True, nullable=False,
)
auth_reqparser.add_argument(
	name='password', type=str, location='json', required=True, nullable=False,
)
# pagination parser
pagination_parser = RequestParser(bundle_errors=True)
pagination_parser.add_argument(
	name='start', type=int, location='args', default=0
)
pagination_parser.add_argument(
	name='count', type=int, location='args', default=10
)
