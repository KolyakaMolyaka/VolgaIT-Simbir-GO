from flask_restx import Model, fields

user_transport_model = Model('Transport', {
	'id': fields.Integer(required=False),
	'canBeRented': fields.Boolean(attribute='can_be_rented', required=True,
								  description='можно ли арендовать транспорт'),
	'transportType': fields.String(attribute='transport_type', required=True, enum=('Car', 'Bike', 'Scooter'),
								   description='тип транспорта'),
	'model': fields.String(required=True, description='модель транспорта', example='BMW'),
	'color': fields.String(required=True, description='цвет транспорта', example='Черный'),
	'identifier': fields.String(required=True, description='номерной знак', example='Н039КМ039'),
	'description': fields.String(required=False, description='описание транспорта', example='Лучше всех мерсов'),
	'latitude': fields.Float(required=True, description='географическая широта местонахождения транспорта'),
	'longitude': fields.Float(required=True, description='географическая долгота местонахождения транспорта'),
	'minutePrice': fields.Float(attribute='minute_price', required=False, description='цена аренды за минуту', example=1399.99),
	'dayPrice': fields.Float(attribute='day_price', required=False, description='цена аренды за сутки', example=7999.99)
})

owner_transport_model = user_transport_model.clone('AdminTransport', {
	'ownerId': fields.Integer(attribute='owner_id', required=True, description='id аккаунта владельца')
})

edit_transport_model = user_transport_model.clone('EditTransportModel')
edit_transport_model.pop('transportType')

from app.apis.accounts.dto import pagination_parser

pagination_with_transport_type_parser = pagination_parser.copy()
pagination_with_transport_type_parser.add_argument(
	name='transportType', choices=('Car', 'Bike', 'Scooter', 'All'), default='All', location='args', type=str
)