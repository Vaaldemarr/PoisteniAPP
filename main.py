from interface_to_db import DatabaseInterface
from flask_interface import FlaskInterface


if __name__ == '__main__':
    my_db = DatabaseInterface('insurance.db')
    my_db.create_tables()
    persons = my_db.load_persons()
    web_interface = FlaskInterface(my_db, persons)
    web_interface.start()
