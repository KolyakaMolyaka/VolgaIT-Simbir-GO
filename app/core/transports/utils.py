from random import choice, randint


def generate_n_transports(n: int):
	"""
	Создание n ТС
	:param n: количество транспортных средст
	:return:
	"""
	def gen_random_identifier():
		parts = 'авекмнорстух'
		number = str(randint(0, 999)).ljust(3, '0')
		region = str(randint(1, 999))
		identifier = [
			choice(parts), number, choice(parts), choice(parts), region
		]
		return ''.join(identifier)

	transports = []
	for _ in range(n):
		can_be_rented = True
		transport_type = choice(['Car', 'Bike', 'Scooter'])
		model = choice(['BMW', 'LADA', 'Volvo', 'KAMAZ', 'Mazda', 'Audi'])
		color = choice(['black', 'red', 'white', 'blue', 'green', 'orange', 'yellow'])

		identifier = gen_random_identifier()
		description = f'My super {model} {transport_type} with cool {identifier} number!'
		latitude = float(randint(0, 90))
		longitude = float(randint(0, 180))
		minute_price = float(randint(1000, 3000))
		day_price = float(randint(minute_price * 60 * 9, minute_price * 60 * 12))

		from app.extensions.database.models import Transport
		import random

		transport = Transport(
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
			owner_id=random.randint(0, 2000)
		)
		transport.save()

		transports.append(transport)

	return transports
