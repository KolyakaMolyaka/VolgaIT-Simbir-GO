from marshmallow import fields, Schema


class UserSchema(Schema):
	id = fields.String()
	username = fields.String()
	is_admin = fields.Boolean()
	balance = fields.Integer()
