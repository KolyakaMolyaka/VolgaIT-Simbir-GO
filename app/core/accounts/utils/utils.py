from random import choice, randint
import logging
from app.core.accounts.accounts_logic import process_registration_request
from app.core.accounts.admin_accounts_logic import process_admin_create_user


def generate_n_users(n: int, username_len=16, password_len=8) -> None:
	"""
	Генерирование n пользователей в БД
	:return:
	"""
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	for _ in range(n):

		username = ''.join(choice(alphabet) for _ in range(username_len))
		password = ''.join(choice(alphabet) for _ in range(password_len))
		try:
			process_registration_request(username, password)
		except Exception as e:
			logging.log(level=logging.DEBUG, msg=f'Ошибка создания пользователя. Пользователь {username} уже существует.')
		else:
			logging.log(level=logging.DEBUG, msg=f'Пользователь "{username}" с паролем "{password}" добавлен в БД.')


first_generate = True
def generate_n_admins(n: int, username_len=16, password_len=8) -> None:
	"""
	Генерирование n администраторов в БД
	:return:
	"""
	global first_generate
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	if first_generate:
		process_admin_create_user('admin', 'admin', True, 10_000_000)
		first_generate = False
	for _ in range(n):
		username = ''.join(choice(alphabet) for _ in range(username_len))
		password = ''.join(choice(alphabet) for _ in range(password_len))
		balance = float(randint(0, 100_000))
		try:
			process_admin_create_user(username, password, True, balance)
		except Exception as e:
			logging.log(level=logging.DEBUG, msg=f'Ошибка добавления админа...Пользователь уже существует.')
		else:
			logging.log(level=logging.DEBUG, msg=f'Админ "{username}" с паролем "{password}" добавлен в БД, баланс = {balance} рублей.')

