from marshmallow import fields, Schema


class RentSchema(Schema):
	id = fields.Integer()
	time_start = fields.DateTime()
	time_end = fields.DateTime()
	price_of_unit = fields.Float()
	price_type = fields.String()
	final_price = fields.Float()
	transport_id = fields.Integer()
	user_id = fields.Integer()
