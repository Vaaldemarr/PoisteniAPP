from person import Person
from policies import Policies

class InsuredPerson(Person):
    """
    Rozšířená třída pojištěného. Dědí se ze třídy Person.
    Obsahuje informace o pojištěném a kolekce jeho pojištění

    Attributes:
        first_name (str): Jméno.
        last_name (str): Příjmení.
        email (str): Email.
        phone (str): Telefon.
        street (str): Ulice a číslo popisné.
        city (str): Město.
        postal_code (str): PSČ.
        policies (Policies): kolekce pojištění
    """

    _policies = Policies()

    def __init__(self, first_name, last_name, email, phone, street, city, postal_code):
        """Konstruktor třídy InsuredPerson"""
        super().__init__(first_name, last_name, email, phone, street, city, postal_code)

    @property
    def policies(self):
        return self._policies

    @policies.setter
    def policies(self, value):
        if not isinstance(value, Policies):
            raise TypeError("Policies must be an instance of Policies class")
        self._policies = value

    @policies.deleter
    def policies(self):
        del self._policies
