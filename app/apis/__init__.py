from flask_restx import Api

authorizations = {
	'JWT': {
		'type': 'apiKey',
		'in': 'header',
		'name': 'Authorization'
	}
}

api = Api(
	prefix='/api/',
	title='Volga IT Simbir.GO приложение',
	description= \
		'Сервис по аренде автомобилей под названием Simbir.GO. Сервис предлагает '
		'аренду не только автомобилей, но и мотоциклов и самокатов. Также вы можете '
		'выбрать срок аренды транспортного средства, например 1 минуту или 1 день.',
	version='1.0',
	authorizations=authorizations
)

# инициализация моделей
from app.apis.accounts.dto import user_model

api.models[user_model.name] = user_model

from app.apis.transports.dto import user_transport_model, edit_transport_model, owner_transport_model

api.models[user_transport_model.name] = user_transport_model
api.models[edit_transport_model.name] = edit_transport_model
api.models[owner_transport_model.name] = owner_transport_model

from app.apis.rents.dto import rent_model
api.models[rent_model.name] = rent_model

# привязка Namespaces
from app.apis.accounts.user_accounts_ns import user_accounts_ns
api.add_namespace(user_accounts_ns)

from app.apis.accounts.admin_accounts_ns import admin_accounts_ns
api.add_namespace(admin_accounts_ns)

from app.apis.payments.payments_ns import payments_ns
api.add_namespace(payments_ns)

from app.apis.transports.user_transports_ns import user_transport_ns
api.add_namespace(user_transport_ns)

from app.apis.transports.admin_transport_ns import admin_transport_ns
api.add_namespace(admin_transport_ns)

from app.apis.rents.rents_ns import rents_ns
api.add_namespace(rents_ns)

from app.apis.rents.admin_rents_controller import admin_rents_ns
api.add_namespace(admin_rents_ns)

