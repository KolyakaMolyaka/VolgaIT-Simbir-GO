from flask import abort
from flask_jwt_extended import current_user
from http import HTTPStatus

from app.extensions.database import db
from app.extensions.database.models import Transport


def process_user_create_new_transport(
		can_be_rented: bool,
		transport_type: str, model: str, color: str,
		identifier: str, latitude: float,
		longitude: float, description=None, minute_price: float = None,
		day_price: float = None):
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
		owner=current_user
	)
	t.save()

	return t


def process_user_get_transport_info(transport_id: int):
	transport = Transport.query.get(transport_id)
	if not transport:
		abort(HTTPStatus.NOT_FOUND, f'Транспорт с id = {transport_id} не найден.')
	return transport


def process_user_update_transport_info(
		transport_id: int, can_be_rented: bool, model: str, color: str, identifier: str,
		latitude: float, longitude: float, description: str = None,
		minute_price: float = None, day_price: float = None):
	t = Transport.query.get(transport_id)

	if not t:
		abort(HTTPStatus.NOT_FOUND, f'Транспорт с id = {transport_id} не найден.')

	if t.owner.id != current_user.id:
		abort(HTTPStatus.FORBIDDEN, 'Вы не являетесь владельцем этого транспорта.')

	t.can_be_rented = can_be_rented
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


def process_user_delete_transport(transport_id):
	t = Transport.query.get(transport_id)

	if not t:
		abort(HTTPStatus.NOT_FOUND, f'Транспорт с id = {transport_id} не найден.')

	if t.owner.id != current_user.id:
		abort(HTTPStatus.FORBIDDEN, 'Вы не являетесь владельцем этого транспорта.')

	db.session.delete(t)
	db.session.commit()