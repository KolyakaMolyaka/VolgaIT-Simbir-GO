from http import HTTPStatus


def new_user_payload_created_by_admin(i: int = None):
	"""
	Создание информации о новом пользователе администратором
	:param i:int номер пользователя
	:return: информация о пользователе
	"""
	name = 'markeeff'
	if i: name += str(i)

	pwd = 'password'
	is_admin = False
	balance = 123

	payload = {
		'username': name,
		'password': pwd,
		'isAdmin': is_admin,
		'balance': balance
	}
	return payload

def register_users(client: 'flask_test_client', num: int):
	"""
	Добавление в базу данных X пользователей
	:param num: кол-во пользователей
	"""
	for i in range(num):
		u = new_user_payload(i)
		register_new_user(client, u)

def new_user_payload(i: int = None):
	"""
	Создание информации о новом пользователе.
	:param: i:int номер пользователя
	"""
	name, pwd = 'markeeff', 'password'
	if i:
		name += str(i)
	payload = {
		'username': name,
		'password': pwd
	}

	return payload


def login_by_json(client: 'flask_test_client', user: dict):
	"""
	Авторизация существующего пользователя
	:param user:dict данные о пользователе
	:return: access_token и заголовок авторизации
	"""
	login_response = login_user(client, user)
	access_token = login_response.json.get('access_token')
	AUTH_HEADER = {'Authorization': f'Bearer {access_token}'}
	return access_token, AUTH_HEADER


def register_new_user(client: 'flask_test_client', user: dict):
	"""
	Регистрация нового пользователя
	:param user:dict данные о пользователе
	:return: response сервера
	"""
	return client.post('/api/account/signup', json=user)


def login_user(client: 'flask_test_client', user: dict):
	"""
	Авторизация пользователя
	:param user:dict данные о пользователе
	:return: response сервера
	"""
	return client.post('/api/account/signin', json=user)


def register_and_login_user(client: 'flask_test_client', user_json: dict):
	"""
	Регистрация и авторизация нового пользователя.
	:param user_json:dict информация о пользователе
	:return: ответ сервера об авторизации
	"""
	register_response = register_new_user(client, user_json)
	assert register_response.status_code == int(HTTPStatus.CREATED), \
		'Пользователь не может быть зарегистрирован (возможно он уже существует).'
	# получение JWT токена для авторизации
	login_response = login_user(client, user_json)
	return login_response


def get_access_token_and_auth_header(client, user_json: dict):
	"""
	Получение access_token и заголовка авторизации для пользователя user_json
	:param: user_json:dict информация о пользователе
	:return: access_token и {'Authorization': 'Bearer {access_token}'}
	"""
	login_response = register_and_login_user(client, user_json)
	access_token = login_response.json.get('access_token')
	AUTH_HEADER = {'Authorization': f'Bearer {access_token}'}
	return access_token, AUTH_HEADER
