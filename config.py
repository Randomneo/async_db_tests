from pyconfiger import configer
from pyconfiger import key_builder


def database_url_builder(user, password, db_host, port, db_name):
    return f'postgresql+asyncpg://{user}:{password}@{db_host}:{port}/{db_name}'


@key_builder(use=(
    'POSTGRES_USER',
    'POSTGRES_PASSWORD',
    'DB_HOST',
    'POSTGRES_PORT',
    'POSTGRES_DB',
))
def database_url(*args):
    return database_url_builder(*args)


@key_builder(use=(
    'POSTGRES_USER',
    'POSTGRES_PASSWORD',
    'DB_HOST',
    'POSTGRES_PORT',
    'POSTGRES_TEST_DB',
))
def database_test_url(*args):
    return database_url_builder(*args)


@key_builder(use=(
    'POSTGRES_USER',
    'POSTGRES_PASSWORD',
    'DB_HOST',
    'POSTGRES_PORT',
))
def database_default_url(*args):
    return database_url_builder(*args, 'postgres')


configer.required_keys = (
    'POSTGRES_DB',
    'POSTGRES_USER',
    'POSTGRES_PASSWORD',
    'POSTGRES_PORT',
    'DB_HOST',
)
configer.built_keys['DATABASE_URL'] = database_url
configer.built_keys['DATABASE_TEST_URL'] = database_test_url
configer.built_keys['DATABASE_DEFAULT_URL'] = database_default_url


DATABASE_URL = configer.get('DATABASE_URL')
