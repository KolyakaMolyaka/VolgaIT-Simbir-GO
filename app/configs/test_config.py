class TestConfig:
	SQLALCHEMY_DATABASE_URI = 'sqlite://'
	SECRET_KEY = 'test_secret_key'
	JWT_SECRET_KEY = 'test_jwt_secret_key'
	DEBUG = True
	# magic of propagation exception:
	# https://github.com/vimalloc/flask-jwt-extended/issues/86#issuecomment-444984295
	PROPAGATE_EXCEPTION = True
