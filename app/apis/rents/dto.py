from datetime import datetime

from flask_restx import Model, fields
from flask_restx.reqparse import RequestParser

rent_model = Model('Rent', {
	'id': fields.Integer(requred=False, description='id аренды'),
	'transportId': fields.Integer(attribute='transport_id', required=True, description='id транспорта для аренды'),
	'userId': fields.Integer(attribute='user_id', required=True, description='id аккаунта арендатора'),
	'timeStart': fields.DateTime(attribute='time_start', required=True, format='iso8601',
								 description='дата и время начала аренды'),
	'timeEnd': fields.DateTime(attribute='time_end', required=False, format='iso8601',
							   description='дата и время окончания аренды'),
	'priceOfUnit': fields.Float(attribute='price_of_unit', required=True, description='цена единицы времени аренды'),
	'priceType': fields.String(attribute='price_type', required=True, enum=('Minutes', 'Days'),
							   description='единица времени аренды (тип оплаты)'),
	'finalPrice': fields.Float(attribute='final_price', required=False, description='общая стоимость аренды')
})

transport_cords_reqparser = RequestParser()
transport_cords_reqparser.add_argument(
	name='lat', type=float, required=True, location='args'
)
transport_cords_reqparser.add_argument(
	name='long', type=float, required=True, location='args'
)

free_for_rent_transport_reqparser = transport_cords_reqparser.copy()
free_for_rent_transport_reqparser.add_argument(
	name='radius', type=float, required=True, location='args'
)
free_for_rent_transport_reqparser.add_argument(
	name='type', type=str, required=False, location='args',
	choices=('Car', 'Bike', 'Scooter', 'All'),
	default='All'
)

rent_type_reqparser = RequestParser()
rent_type_reqparser.add_argument(
	name='rentType', type=str, required=True, location='args',
	choices=('Minutes', 'Days'),
)
