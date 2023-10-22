from datetime import datetime
from http import HTTPStatus
from flask import abort
from flask_jwt_extended import current_user
from app.extensions.database.models import Transport, Rent


def process_get_free_transport_for_rent_list(latitude: float, longitude: float, radius: float, type: str = 'All'):
	# фильтруем по местоположению
	ts = Transport.get_transport_by_cords(latitude, longitude, radius, return_cursor=True)

	# фильтрация по определенному типу транспорта (если необходимо)
	if type != 'All':
		ts = ts.filter(Transport.transport_type == type)

	# исключаем транспорт, который уже арендован
	rented_ts = Rent.rented_transports()
	rented_ts_ids = map(lambda r: r.transport_id, rented_ts)
	ts = [t for t in ts if t.id not in rented_ts_ids]

	# исключаем транспорт, у которого неизвестна невозможно вычислить цену аренды
	ts = [t for t in ts if t.can_calculate_price()]

	return ts


def process_user_rents_transport(transport_id: int, rent_type: str):
	t = Transport.query.get(transport_id)
	if not t:
		abort(HTTPStatus.NOT_FOUND, f'Транспорт с id = {transport_id} не найден.')

	# проверка, что пользователь не является владельцем транспорта
	if current_user.id == t.owner_id:
		abort(HTTPStatus.CONFLICT, 'Вы не можете арендовать свой транспорт.')

	# проверка, что у транспорта можно вычислить стоимость аренды
	if not t.can_calculate_price():
		abort(HTTPStatus.CONFLICT, f'У транспорта недостаточно данных для определения стоимости аренды.')

	busy_transport_ids = set((r.transport_id for r in Rent.rented_transports()))

	if transport_id in busy_transport_ids:
		abort(HTTPStatus.CONFLICT, f'Транспорт с id = {transport_id} уже арендован.')

	# создание аренды
	rent_price_of_unit = t.day_price if rent_type == 'Days' else t.minute_price
	new_r = Rent(
		time_start=datetime.utcnow(),
		price_of_unit=rent_price_of_unit,
		price_type=rent_type,
		transport_id=transport_id,
		user_id=current_user.id
	)
	new_r.save()


def process_user_end_rents_transport(latitude: float, longitude: float, rent_id: int):
	rent_time_end = datetime.utcnow()
	r = Rent.query.get(rent_id)
	if not r:
		abort(HTTPStatus.NOT_FOUND, f'Нет аренды с id = {rent_id}.')

	if r.time_end != None:
		abort(HTTPStatus.CONFLICT, f'Аренда c id = {rent_id} уже была завершена.')

	if current_user.id != r.user_id:
		abort(HTTPStatus.FORBIDDEN, f'Вы не являетесь арендатором.')

	# Расчет стоимости аренды
	r.calculate_final_price(rent_time_end)
	r.save()

	# Обновление положения машины
	t = Transport.query.get(r.transport_id)
	t.latitude = latitude
	t.longitude = longitude
	t.save()


def process_user_get_rents_history():
	rs = Rent.query.filter_by(user_id=current_user.id).all()
	return rs


def process_user_get_rent_info(rent_id: int):
	r = Rent.query.get(rent_id)
	if not r:
		abort(HTTPStatus.NOT_FOUND, f'Аренда с id = {rent_id} не найдена.')

	t = Transport.query.get(r.transport_id)

	if current_user.id not in (t.owner_id, r.user_id):
		abort(HTTPStatus.FORBIDDEN, 'Вы не являетесь владельцем транспорта или арендатором.')

	return r

def process_user_get_transports_history(transport_id: int):
	t = Transport.query.get(transport_id)
	if not t:
		abort(HTTPStatus.NOT_FOUND, f'Транспорт с id = {transport_id} не найден.')

	if not current_user.id == t.owner_id:
		abort(HTTPStatus.FORBIDDEN, 'Вы не являетесь владельцем транспорта.')

	rs = Rent.query.filter_by(transport_id=transport_id).all()

	return rs