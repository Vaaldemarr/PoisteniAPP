# from insurance import InsuredPerson, InsurancePolicy
from insured_person import InsuredPerson
from policy import InsurancePolicy

from persons import Persons
from policies import Policies

from database import DatabaseInsurances

class DatabaseInterface():
    """
    Třída implementuje spojení mezi databází a sbírkami pojištěnců a pojištění.

    Attributes:
        db_name (str): Cesta k databázi.
    """

    _db_name = None

    def __init__(self, db_name):
        self._db_name = db_name

    @property
    def db_name(self):
        return self._db_name

    def create_tables(self):
        """Vytváří tabulky pro ukládání záznamů s údaji o pojištěncích a pojištění."""
        db = DatabaseInsurances(self._db_name)
        db.create_tables()

    def load_persons(self):
        """Načte sbírky pojištěnců a pojištění z databáze do objektu Persons."""
        db = DatabaseInsurances(self._db_name)

        persons = Persons()

        insured_persons_data = db.fetch_all_insured_persons()
        for row in insured_persons_data:
            person_id, first_name, last_name, email, phone, street, city, postal_code = row
            person = InsuredPerson(first_name, last_name, email, phone, street, city, postal_code)

            policies = Policies()
            policies_data = db.fetch_insurance_policies_by_person(person_id)
            for policy_data in policies_data:
                policy_id, title, insured_amount, insured_object, start_date, end_date = policy_data
                policy = InsurancePolicy(title, insured_amount, insured_object, start_date, end_date)
                policies[policy_id] = policy
            
            person.policies = policies
            persons[person_id] = person

        return persons

    def add_insured_person_to_db(self, person):
        """
        Přidání pojištěného do databáze.

        Args:
            person (InsuredPerson): pojištěnec.

        Returns:
            int: Identifikátor nového záznamu pojištěnce.
        """        
        db = DatabaseInsurances(self._db_name)
        person_id = db.insert_insured_person(
            person.first_name, person.last_name, person.email, person.phone,
            person.street, person.city, person.postal_code
        )
        return person_id

    def add_insurance_policy_to_db(self, policy):
        """
        Vytvoření pojištění v databázi.

        Args:
            policy (InsurancePolicy): Pojištění.

        Returns:
            int: Identifikátor nového záznamu pojištění.
        """        
        db = DatabaseInsurances(self._db_name)
        policy_id = db.insert_insurance_policy(
            policy.title, policy.insured_amount, policy.insured_object,
            policy.start_date, policy.end_date
        )
        return policy_id

    def find_insured_person_by_id(self, person_id):
        """
        Hledání pojištěného podle ID.

        Args:
            person_id (int): Identifikátor pojištěnce.

        Returns:
            InsuredPerson: pojištěnec nebo None.
        """        
        db = DatabaseInsurances(self._db_name)
        person_data = db.fetch_insured_person(person_id)
        if person_data:
            return InsuredPerson(
                person_data[0], person_data[1], person_data[2],
                person_data[3], person_data[4], person_data[5], person_data[6])
        return None

    def find_insurance_policies_by_person_id(self, person_id):
        """
        Získání pojištění podle ID pojištěnce.

        Args:
            person_id (int, str): Identifikátor pojištěnce.

        Returns:
            dict[int: InsurancePolicy]: Všechna Sjednaná pojištění pojištěncu.
        """        
        db = DatabaseInsurances(self._db_name)
        policies_data = db.fetch_insurance_policies_by_person(person_id)
        policies = {}
        for policy_data in policies_data:
            policy = InsurancePolicy(
                title=policy_data[1],
                insured_amount=policy_data[2],
                insured_object=policy_data[3],
                start_date=policy_data[4],
                end_date=policy_data[5]
            )
            policies[policy_data[0]]=policy
        return policies

    def find_insurance_policy_by_id(self, id):
        """
        Hledání pojištění podle ID.

        Args:
            id (int): Identifikátor pojištění.

        Returns:
            InsurancePolicy: Nalezené pojištění nebo None.
        """        
        db = DatabaseInsurances(self._db_name)
        policy_data = db.fetch_insurance_policy_by_id(id)
        if policy_data:
            return InsurancePolicy(
                title=policy_data[1],
                insured_amount=policy_data[2],
                insured_object=policy_data[3],
                start_date=policy_data[4],
                end_date=policy_data[5]
            )
        return None

    def get_all_insured_persons(self):
        """
        Získání všech pojištěných.

        Returns:
            dict[int: InsuredPerson]: Všichni pojištěnci z databáze.
        """        
        db = DatabaseInsurances(self._db_name)
        persons_data = db.fetch_all_insured_persons()
        persons = {}
        for person_data in persons_data:
            persons[person_data[0]]=InsuredPerson(
                person_data[1], person_data[2], person_data[3],
                person_data[4], person_data[5], person_data[6], person_data[7]
            )
        return persons

    def get_all_insurance_policies(self):
        """
        Získání všech pojištění.

        Returns:
            dict[int: InsurancePolicy]: Všechna pojištění z databáze.
        """        
        db = DatabaseInsurances(self._db_name)
        policies_data = db.fetch_all_insurance_policies()
        policies = {}
        for policy_data in policies_data:
            policy = InsurancePolicy(
                title=policy_data[1],
                insured_amount=policy_data[2],
                insured_object=policy_data[3],
                start_date=policy_data[4],
                end_date=policy_data[5]
            )
            policies[policy_data[0]]=(policy, policy_data[6])
        return policies

    def get_all_unused_insurance_policies(self):
        """
        Získání všech nesjednaných pojištění.

        Returns:
            dict[int: InsurancePolicy]: Všechna bezplatná pojištění z databáze.
        """        
        db = DatabaseInsurances(self._db_name)
        policies_data = db.fetch_all_unused_insurance_policies()
        policies = {}
        for policy_data in policies_data:
            policy = InsurancePolicy(
                title=policy_data[1],
                insured_amount=policy_data[2],
                insured_object=policy_data[3],
                start_date=policy_data[4],
                end_date=policy_data[5]
            )
            policies[policy_data[0]]=policy
        return policies

    def update_insured_person_in_db(self, person_id, person):
        """
        Editace pojištěnce v databázi.

        Args:
        person_id (int): Identifikátor pojištěnce.
        person (InsuredPerson): pojištěnec.
        """        
        db = DatabaseInsurances(self._db_name)
        db.update_insured_person(
            person_id, person.first_name, person.last_name, person.email,
            person.phone, person.street, person.city, person.postal_code
        )

    def update_insurance_policy_in_db(self, policy_id, policy):
        """
        Editace pojištění v databázi.

        Args:
        policy_id (int): Identifikátor pojištění.
        policy (InsurancePolicy): Pojištění.
        """        
        db = DatabaseInsurances(self._db_name)
        db.update_insurance_policy(
            policy_id, policy.title, policy.insured_amount, policy.insured_object,
            policy.start_date, policy.end_date
        )

    def is_person_exists(self, person):
        """
        Hledá pojištěnce podle jména, příjmení a e-mailu.

        Args:
            person (InsuredPerson): pojištěnec.

        Returns:
            int: Počet nalezených pojištěnců.
        """        
        db = DatabaseInsurances(self._db_name)
        persons_count = db.insured_person_exist(person.first_name, person.last_name, person.email)
        return persons_count[0]

    def is_policy_title_unique(self, title, policy_id):
        """
        Ověřuje, zda již existuje pojištění s tímto názvem, ale jiným identifikátorem v databázi.

        Args:
            title (str): Název pojištění.
            policy_id (int): Identifikátor pojištění.

        Returns:
            bool: True pokud existuje, jinak False.
        """        
        db = DatabaseInsurances(self._db_name)
        found_ids = db.find_insurance_policy_id_by_name(title)
        for id in found_ids:
            if int(policy_id) != id[0]:
                return False
        return True

    def is_policy_title_exist(self, title):
        """
        Ověřuje, zda již existuje pojištění s tímto názvem v databázi.

        Args:
            title (str): Název pojištění.

        Returns:
            int: Počet nalezených pojištění.
        """        
        db = DatabaseInsurances(self._db_name)
        policies_count = db.find_insurance_policy_by_name(title)[0]
        return policies_count>0
