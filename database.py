import sqlite3

class DatabaseInsurances():
    """
    Třída pro práci s databází SQLite.

    Poskytuje vytváření, čtení, zápis a mazání pojištěných v databázi
    """

    def __init__(self, db_name):
        """Vytvoří spojení s databází"""
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def create_tables(self):
        """Vytváří tabulky pro ukládání záznamů s údaji o pojištěncích a pojištění."""
            
        # Vytvoření tabulky pojištěnců
        query_text = '''
            CREATE TABLE IF NOT EXISTS InsuredPersons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                street TEXT NOT NULL,
                city TEXT NOT NULL,
                postal_code TEXT NOT NULL
            )
        '''
        self.cursor.execute(query_text)

        # Vytvoření tabulky pojištění
        query_text = '''
            CREATE TABLE IF NOT EXISTS InsurancePolicies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                insured_amount REAL NOT NULL,
                insured_object TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL
            )
        '''
        self.cursor.execute(query_text)

        # Vytvoření tabulky pro vztah M:N mezi pojištěnců a pojištění
        query_text = '''
            CREATE TABLE IF NOT EXISTS PersonInsurancePolicies (
                person_id INTEGER,
                policy_id INTEGER,
                FOREIGN KEY (person_id) REFERENCES InsuredPersons(id) ON DELETE CASCADE,
                FOREIGN KEY (policy_id) REFERENCES InsurancePolicies(id) ON DELETE CASCADE,
                PRIMARY KEY (person_id, policy_id)
            )
        '''
        self.cursor.execute(query_text)

        self.connection.commit()

    def insert_insured_person(self, first_name, last_name, email, phone, street, city, postal_code):
        """
        Záznam pojištěnce do databáze.

        Args:
            first_name (str): Jméno.
            last_name (str): Příjmení.
            email (str): Email.
            phone (str): Telefon.
            street (str): Ulice a číslo popisné.
            city (str): Město.
            postal_code (str): PSČ.
        """        
        self.cursor.execute('''
            INSERT INTO InsuredPersons (first_name, last_name, email, phone, street, city, postal_code)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, phone, street, city, postal_code))
        self.connection.commit()
        return self.cursor.lastrowid

    def insert_insurance_policy(self, title, insured_amount, insured_object, start_date, end_date):
        """
        Záznam pojištění do databáze.

        Args:
            title (str): Jméno.
            insured_amount (int): Částka.
            insured_object (str): Předmět pojištění.
            start_date (str): Platnost od.
            end_date (str): Platnost do.
        """
        self.cursor.execute('''
            INSERT INTO InsurancePolicies (title, insured_amount, insured_object, start_date, end_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, insured_amount, insured_object, start_date, end_date))
        self.connection.commit()
        return self.cursor.lastrowid

    def insert_person_insurance_policy(self, person_id, policy_id):
        """
        Záznam do databáze vztahu mezi pojištěným a pojištěním do databáze

        Args:
            person_id (int): Identifikátor pojištěného.
            policy_id (int): Identifikátor pojištění.
        """
        self.cursor.execute('''
            INSERT INTO PersonInsurancePolicies (person_id, policy_id)
            VALUES (?, ?)
        ''', (person_id, policy_id))
        self.connection.commit()

    def fetch_insured_person(self, person_id):
        """
        Hledejte pojištěnce podle ID

        Args:
            person_id (int): Identifikátor pojištěného.

        Returns:
            tuple: Pole nalezeného záznamu databáze nebo None.
        """
        result = self.cursor.execute('''
            SELECT first_name, last_name, email, phone, street, city, postal_code
            FROM InsuredPersons WHERE id = ?
        ''', (person_id,))
        return result.fetchone()

    def insured_persons_count(self):
        """
        Získejte počet pojištěnce

        Returns:
            tuple: Celkový počet pojištěnců.
        """
        result = self.cursor.execute('''
            SELECT count(id)
            FROM InsuredPersons
        ''')
        return result.fetchone()

    def insured_person_exist(self, first_name, last_name, email):
        """
        Získejte počet pojištěnce odpovídající předaným parametrům

        Args:
            first_name (str): Jméno.
            last_name (str): Příjmení.
            email (str): Email.

        Returns:
            tuple: počet nalezených pojištěnců.
        """
        result = self.cursor.execute('''
            SELECT count(id)
            FROM InsuredPersons
            WHERE first_name=? and last_name=? and email=?
        ''', (first_name, last_name, email))
        return result.fetchone()

    def insurance_policies_count(self):
        """
        Získejte počet Pojištění

        Returns:
            tuple: Celkový počet pojištění.
        """
        result = self.cursor.execute('''
            SELECT count(id)
            FROM InsurancePolicies
        ''')
        return result.fetchone()

    def find_insurance_policy_by_name(self, text):
        """
        Získejte počet pojištění podle názvu

        Args:
            text (str): Název pojištění.

        Returns:
            tuple: počet Pojištění odpovídající předaným parametrům.
        """
        result = self.cursor.execute('''
            SELECT count(id)
            FROM InsurancePolicies
            WHERE title = ?
        ''', (text,))
        return result.fetchone()

    def find_insurance_policy_id_by_name(self, text):
        """
        Najít všechny id pojištění podle názvu

        Args:
            text (str): Název pojištění.

        Returns:
            list[tuple]: Seznam nalezených identifikátorů Pojištění.
        """
        result = self.cursor.execute('''
            SELECT id
            FROM InsurancePolicies
            WHERE title = ?
        ''', (text,))
        return result.fetchall()

    def fetch_insurance_policies_by_person(self, person_id):
        """
        Vyhledejte pojištění podle ID pojištěného

        Args:
            person_id (int): Identifikátor pojištěného.

        Returns:
            list[tuple]: Seznam všech polí nalezených v záznamu Pojištění.
        """
        result = self.cursor.execute('''
            SELECT ip.id, ip.title, ip.insured_amount, ip.insured_object, ip.start_date, ip.end_date
            FROM InsurancePolicies ip
            JOIN PersonInsurancePolicies pip ON ip.id = pip.policy_id
            WHERE pip.person_id = ?
        ''', (person_id,))
        return result.fetchall()

    def fetch_insurance_policy_by_id(self, id):
        """
        Vyhledejte pojištění podle id

        Args:
            id (int): Identifikátor pojištění.

        Returns:
            tuple: Všechna pole nalezeného záznamu Pojištění.
        """
        result = self.cursor.execute('''
            SELECT id, title, insured_amount, insured_object, start_date, end_date
            FROM InsurancePolicies
            WHERE id = ?
        ''', (id,))
        return result.fetchone()

    def fetch_all_insured_persons(self):
        """
        Získejte všechny pojištěnce

        Returns:
            list[tuple]: Seznam všech polí nalezených v záznamu Pojištěncu.
        """
        result = self.cursor.execute('''
            SELECT id, first_name, last_name, email, phone, street, city, postal_code
            FROM InsuredPersons
        ''')
        return result.fetchall()

    def fetch_all_insurance_policies(self):
        """
        Získání všech pojištění

        Returns:
            list[tuple]: Seznam všech polí nalezených v záznamu pojištění.
        """
        result = self.cursor.execute('''
            SELECT id, title, insured_amount, insured_object, start_date, end_date, persons
            FROM InsurancePolicies
            LEFT JOIN (SELECT count(person_id) As persons, policy_id
                    FROM PersonInsurancePolicies
                    GROUP by policy_id) As LPolicies
            ON id=LPolicies.policy_id
        ''')
        return result.fetchall()

    def fetch_all_unused_insurance_policies(self):
        """
        Získejte všechna nesjednaná pojištění

        Returns:
            list[tuple]: Seznam všech polí nalezených v záznamu pojištění.
        """
        result = self.cursor.execute('''
            SELECT id, title, insured_amount, insured_object, start_date, end_date
            FROM InsurancePolicies
            WHERE id NOT in(SELECT DISTINCT policy_id FROM PersonInsurancePolicies)
        ''')
        return result.fetchall()

    def update_insured_person(self, person_id, first_name, last_name, email, phone, street, city, postal_code):
        """
        Aktualizace údajů pojištěnce.

        Args:
            person_id (int): Identifikátor pojištěného.
            first_name (str): Jméno.
            last_name (str): Příjmení.
            email (str): Email.
            phone (str): Telefon.
            street (str): Ulice a číslo popisné.
            city (str): Město.
            postal_code (str): PSČ.
        """
        self.cursor.execute('''
            UPDATE InsuredPersons
            SET first_name = ?, last_name = ?, email = ?, phone = ?, street = ?, city = ?, postal_code = ?
            WHERE id = ?
        ''', (first_name, last_name, email, phone, street, city, postal_code, person_id))
        self.connection.commit()

    def update_insurance_policy(self, policy_id, title, insured_amount, insured_object, start_date, end_date):
        """
        Aktualizace údajů pojištění.

        Args:
            policy_id (int): Identifikátor pojištění.
            title (str): Jméno.
            insured_amount (int): Částka.
            insured_object (str): Předmět pojištění.
            start_date (str): Platnost od.
            end_date (str): Platnost do.
        """
        self.cursor.execute('''
            UPDATE InsurancePolicies
            SET title = ?, insured_amount = ?, insured_object = ?, start_date = ?, end_date = ?
            WHERE id = ?
        ''', (title, insured_amount, insured_object, start_date, end_date, policy_id))
        self.connection.commit()

    def delete_insured_person(self, person_id):
        """
        Odstranění pojištěnce z databáze.

        Args:
            person_id (int): Identifikátor pojištěného.
        """
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        self.cursor.execute('''
            DELETE FROM InsuredPersons WHERE id = ?
        ''', (person_id,))
        self.connection.commit()

    def delete_insurance_policy(self, policy_id):
        """
        Odstranění pojištění z databáze.

        Args:
            policy_id (int): Identifikátor pojištění.
        """
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        self.cursor.execute('''
            DELETE FROM InsurancePolicies WHERE id = ?
        ''', (policy_id,))
        self.connection.commit()

    def delete_person_insurance_policy(self, person_id, policy_id):
        """
        Odstranění spojení mezi pojištěním a pojištěným.

        Args:
            person_id (int): Identifikátor pojištěného.
            policy_id (int): Identifikátor pojištění.
        """
        self.cursor.execute('''
            DELETE FROM PersonInsurancePolicies WHERE person_id = ? AND policy_id=?
        ''', (person_id, policy_id))
        self.connection.commit()
