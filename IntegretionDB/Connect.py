import psycopg2
from psycopg2 import OperationalError


def create_connect(name_db, user_db, password_db, host_db, port_db):
    connection_db = None
    try:
        connection_db = psycopg2.connect(
            database=name_db,
            user=user_db,
            password=password_db,
            host=host_db,
            port=port_db
        )
        print("Connection to vkinder_db successful")
    except OperationalError as e:
        print(f'Error{e}')
    return connection_db


connection = create_connect('vkinder_db', 'developer', 'qwerty123', 'localhost', '5432')
print(connection)
