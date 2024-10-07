from utils import Check

class InsurancePolicy:
    """
    Třída pojištění. Obsahuje údaje o pojištění.

    Attributes:
        title (str): Jméno.
        insured_amount (int): Částka.
        insured_object (str): Předmět pojištění.
        start_date (str): Platnost od.
        end_date (str): Platnost do.
    """

    def __init__(self, title, insured_amount, insured_object, start_date, end_date):
        """Konstruktor třídy InsurancePolicy"""
        self._title = title
        self._insured_amount = insured_amount
        self._insured_object = insured_object
        self._start_date = start_date
        self._end_date = end_date

    def __str__(self) -> str:
        return f'{self._title}, {self._insured_amount}'

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def insured_amount(self):
        return self._insured_amount

    @insured_amount.setter
    def insured_amount(self, value):
        self._insured_amount = value

    @property
    def insured_object(self):
        return self._insured_object

    @insured_object.setter
    def insured_object(self, value):
        self._insured_object = value

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        self._start_date = value

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        self._end_date = value

    def check_valid_data(self):
        """
        Zkontroluje, zda jsou všechny jeho atributy správné.

        Returns:
            str: Text popisující chybu nebo prázdný řádek, pokud jsou všechny hodnoty správně vyplněny.
        """        
        result=""
        if len(self._title.strip()) == 0:
            result = "Zadejte hodnotu: Jméno"
        elif len(self._insured_object.strip()) == 0:
            result = "Zadejte hodnotu: Předmět pojištění"
        elif not Check.positive_number(self._insured_amount):
            result = "Neplatná hodnota: Částka"
        elif self._start_date > self._end_date:
            result = "Platnost od by mělo být dříve než Platnost do"
            
        return result
