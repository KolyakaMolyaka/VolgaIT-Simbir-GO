from marshmallow import fields, Schema


class TransportSchema(Schema):
	id = fields.Integer()
	cat_be_rented = fields.Boolean()
	transport_type = fields.String()
	model = fields.String()
	color = fields.String()
	identifier = fields.String()
	description = fields.String()
	latitude = fields.Float()
	longitude = fields.Float()
	minute_price = fields.Float()
	day_price = fields.Float()

	owner_id = fields.Integer()
