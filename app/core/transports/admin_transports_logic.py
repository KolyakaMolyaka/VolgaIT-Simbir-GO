from http import HTTPStatus
from flask import abort

from app.extensions.database import db
from app.extensions.database.models import Transport, User


def process_admin_get_transports_list(start: int, count: int, transport_type: str = 'All'):
	if transport_type == 'All':
		ts = Transport.query \
			.offset(start) \
			.limit(count) \
			.all()
	else:
		ts = Transport.query \
			.filter_by(transport_type=transport_type) \
			.offset(start) \
			.limit(count) \
			.all()

	return ts


def process_admin_create_transport(
		owner_id: int, can_be_rented: bool,
		transport_type: str, model: str, color: str,
		identifier: str, latitude: float, longitude: float,
		description=None, minute_price: float = None,
		day_price: float = None):
	owner = User.query.get(owner_id)
	if not owner:
		abort(HTTPStatus.NOT_FOUND, 'Владелец транспорта не существует.')

	t = Transport(
		can_be_rented=can_be_rented,
		transport_type=transport_type,
		model=model,
		color=color,
		identifier=identifier,
		description=description,
		latitude=latitude,
		longitude=longitude,
		minute_price=minute_price,
		day_price=day_price,
		owner_id=owner_id
	)

	t.save()


def process_admin_get_transport_info(transport_id):
	t = Transport.query.get(transport_id)
	if not t:
		abort(HTTPStatus.NOT_FOUND, f'Транспорт с id = {transport_id} не найден.')

	return t


def process_admin_edit_transport_info(
		transport_id: int,
		owner_id: int, can_be_rented: bool,
		transport_type: str, model: str, color: str,
		identifier: str, latitude: float, longitude: float,
		description=None, minute_price: float = None,
		day_price: float = None):
	t = Transport.query.get(transport_id)
	if not t:
		abort(HTTPStatus.NOT_FOUND, f'Транспорт с id = {transport_id} не найден.')

	owner = User.query.get(owner_id)
	if not owner:
		abort(HTTPStatus.NOT_FOUND, f'Владелец с id = {owner_id} не найден.')

	t.owner_id = owner_id
	t.can_be_rented = can_be_rented
	t.transport_type = transport_type
	t.model = model
	t.color = color
	t.identifier = identifier
	t.latitude = latitude
	t.longitude = longitude

	if description:
		t.description = description

	if minute_price:
		t.minute_price = minute_price

	if day_price:
		t.day_price = day_price

	t.save()

	return t


def process_admin_delete_transport(transport_id: int):
	t = Transport.query.get(transport_id)
	if not t:
		abort(HTTPStatus.NOT_FOUND, f'Транспорт с id = {transport_id} не найден.')

	db.session.delete(t)
	db.session.commit()

