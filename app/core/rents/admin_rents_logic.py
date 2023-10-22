from datetime import datetime
from http import HTTPStatus
from flask import abort

from app.extensions.database import db
from app.extensions.database.models import Rent, Transport, User


def process_admin_create_rent(
		transport_id: int, user_id: int,
		time_start: datetime, price_of_unit: float,
		price_type: str, time_end: datetime = None,
		final_price: float = None

):
	# проверка существования транспорта
	t = Transport.query.get(transport_id)
	if not t:
		abort(HTTPStatus.NOT_FOUND, f'Транспорт с id = {transport_id} не существует.')

	# проверка существования пользователя
	u = User.query.get(user_id)
	if not u:
		abort(HTTPStatus.NOT_FOUND, f'Пользователь с id = {user_id} не существует.')

	# проверка, что пользователь не является владельцем транспорта
	if user_id == t.owner_id:
		abort(HTTPStatus.CONFLICT, 'Пользователь не может арендовать свой транспорт.')

	# проверка, что у транспорта можно вычислить стоимость аренды
	if not t.can_calculate_price():
		abort(HTTPStatus.CONFLICT, f'У транспорта недостаточно данных для определения стоимости аренды.')

	# проверка, что транспорт еще не арендован
	busy_transport_ids = set((r.transport_id for r in Rent.rented_transports()))
	if transport_id in busy_transport_ids:
		abort(HTTPStatus.CONFLICT, f'Транспорт с id = {transport_id} уже арендован.')

	r = Rent(
		transport_id=transport_id,
		user_id=user_id,
		time_start=time_start,
		price_of_unit=price_of_unit,
		price_type=price_type,
	)

	# последовательность важна!
	# сначала проверяем вручную установленную общую стоимость,
	# затем время окончания аренды.
	# если финальная стоимость не задана, то
	# она считается на основе времени окончания аренды.
	if final_price:
		r.final_price = final_price

	if time_end:
		r.time_end = time_end

	# сохранить модель для последующей обработки расчёта финальной стоимости
	r.save()

	if not final_price and time_end:
		r.calculate_final_price(time_end)
		r.save()


def process_admin_edit_rent(
		rent_id: int,
		transport_id: int, user_id: int,
		time_start: datetime, price_of_unit: float,
		price_type: str, time_end: datetime = None,
		final_price: float = None
):
	# проверка существования транспорта
	t = Transport.query.get(transport_id)
	if not t:
		abort(HTTPStatus.NOT_FOUND, f'Транспорт с id = {transport_id} не существует.')

	# проверка существования пользователя
	u = User.query.get(user_id)
	if not u:
		abort(HTTPStatus.NOT_FOUND, f'Пользователь с id = {user_id} не существует.')

	# проверка, что пользователь не является владельцем транспорта
	if user_id == t.owner_id:
		abort(HTTPStatus.CONFLICT, 'Пользователь не может арендовать свой транспорт.')

	# проверка существования аренды
	r = Rent.query.get(rent_id)
	if not r:
		abort(HTTPStatus.NOT_FOUND, f'Аренда с id = {rent_id} не найдена.')


	# обнволение аренды
	r.transport_id = transport_id
	r.user_id = user_id
	r.time_start = time_start
	r.price_of_unit = price_of_unit
	r.price_type = price_type

	# последовательность важна!
	# сначала проверяем вручную установленную общую стоимость,
	# затем время окончания аренды.
	# если финальная стоимость не задана, то
	# она считается на основе времени окончания аренды.

	if final_price:
		r.final_price = final_price

	if time_end:
		r.time_end = time_end

	# сохранить модель для последующей обработки расчёта финальной стоимости
	r.save()

	if not final_price and time_end:
		r.calculate_final_price(time_end)
		r.save()


def process_admin_get_rent_info(rent_id: int):
	r = Rent.query.get(rent_id)
	if not r:
		abort(HTTPStatus.NOT_FOUND, f'Аренда с id = {rent_id} не найдена.')

	return r


def process_admin_get_user_rent_history(user_id: int):
	rs = Rent.query.filter_by(user_id=user_id).all()
	return rs


def process_admin_get_transport_rent_history(transport_id: int):
	rs = Rent.query.filter_by(transport_id=transport_id).all()
	return rs


def process_admin_end_user_rent(rent_id: int, latitude: float, longitude: float):
	rent_time_end = datetime.utcnow()
	r = Rent.query.get(rent_id)
	if not r:
		abort(HTTPStatus.NOT_FOUND, f'Нет аренды с id = {rent_id}')

	if r.time_end:
		abort(HTTPStatus.CONFLICT, f'Аренда с id = {rent_id} завершится в {datetime.isoformat(r.time_end)}.')

	t = Transport.query.get(r.transport_id)
	t.latitude = latitude
	t.longitude = longitude
	t.save()

	r.calculate_final_price(rent_time_end)
	r.save()


def process_admin_delete_rent(rent_id: int):
	r = Rent.query.get(rent_id)
	if not r:
		abort(HTTPStatus.NOT_FOUND, f'Аренда с id = {rent_id} не найдена.')

	db.session.delete(r)
	db.session.commit()
