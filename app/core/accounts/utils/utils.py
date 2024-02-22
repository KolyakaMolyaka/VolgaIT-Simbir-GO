from random import choice


def generate_n_users(n: int, username_len=16, password_len=8) -> list:
	"""
	Генерирование n пользователей
	:return: список n пользователей 
	"""
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	users = []
	for _ in range(n):

		username = ''.join(choice(alphabet) for _ in range(username_len))
		password = ''.join(choice(alphabet) for _ in range(password_len))
		users.append((username, password))

	return users
