from utils import Check
class Person:
    """
    Základní třída pojištěnce.

    Attributes:
        first_name (str): Jméno.
        last_name (str): Příjmení.
        email (str): Email.
        phone (str): Telefon.
        street (str): Ulice a číslo popisné.
        city (str): Město.
        postal_code (str): PSČ.
    """

    def __init__(self, first_name, last_name, email, phone, street, city, postal_code):
        """Konstruktor třídy Person"""
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._phone = phone
        self._street = street
        self._city = city
        self._postal_code = postal_code

    def __str__(self) -> str:
        return f'{self._first_name} {self._last_name}. {self._street}, {self._city}.'

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = value

    @property
    def street(self):
        return self._street

    @street.setter
    def street(self, value):
        self._street = value

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        self._city = value

    @property
    def postal_code(self):
        return self._postal_code

    @postal_code.setter
    def postal_code(self, value):
        self._postal_code = value

    def check_valid_data(self):
        """
        Zkontroluje, zda jsou všechny jeho atributy správné.

        Returns:
            str: Text popisující chybu nebo prázdný řádek, pokud jsou všechny hodnoty správně vyplněny.
        """
        result = ""

        if len(self._first_name.strip()) == 0:
            result="Jméno není vyplněno"
        elif len(self._last_name.strip()) == 0:
            result="Příjmení není vyplněno"
        elif not Check.email(self._email):
            result="E-mailová adresa není vyplněna nebo neodpovídá formátu"
        elif not Check.phone(self._phone):
            result="Telefon není vyplněn nebo neodpovídá formátu"
        elif len(self._street.strip()) == 0:
            result="Ulice a číslo popisné nejsou vyplněny"
        elif len(self._city.strip()) == 0:
            result="Město není vyplněno"
        elif not Check.postal_code(self._postal_code):
            result="PSČ není vyplněno nebo obsahuje neplatné znaky."

        return result
