from insured_person import InsuredPerson

class Persons:
    """
    Kolekce pojištěnce. 
    Obsahuje slovník, kde klíč je identifikátor pojištěného a hodnota je objekt typu InsuredPerson.
    Umožňuje přistupovat k prvkům kolekce podle klíče ve slovníku jako podle indexu.
    """

    def __init__(self):
        """Konstruktor třídy Persons. Vytvoří slovník pro uložení pojištěnců."""
        self._persons = {}

    # Přidání pojištěnce
    def __setitem__(self, _id, person):
        # if _id in self._persons:
        #     raise ValueError(f"Person with ID {_id} already exists.")
        if not isinstance(person, InsuredPerson):
            raise TypeError("Person must be an instance of InsuredPerson.")
        self._persons[_id] = person

    # Získání pojištěnce podle identifikátoru _id
    def __getitem__(self, _id):
        return self._persons.get(_id, None)

    # Odstranění pojištěnce podle identifikátoru _id
    def __delitem__(self, _id):
        if _id in self._persons.keys():
            del self._persons[_id]
        else:
            raise KeyError(f"Person with ID {_id} does not exist.")

    # Kontrola přítomnosti pojištěnce podle identifikátoru _id
    def __contains__(self, _id):
        _id = int(_id)
        return _id in self._persons

    # Magická metoda pro získání množství
    def __len__(self):
        return len(self._persons)

    # Magická metoda pro iteraci 
    def __iter__(self):
        return iter(self._persons.items())

    def replace_policy(self, policy_id, policy):
        """
        Vyhledá pojištění podle ID pojištění každého pojištěnce a nahradí novém.

        Args:
            policy_id (int): Identifikátor pojištění.
            policy (InsurancePolicy): pojištění.
        """
        for id, person in self._persons.items():
            if policy_id in person.policies:
                self._persons[id].policies[policy_id]=policy

    def delete_policy(self, policy_id):
        """
        Vyhledá pojištění podle ID pojištění každého pojištěnce a odstraní je.

        Args:
            policy_id (int): Identifikátor pojištění.
        """
        policy_id = int(policy_id)
        for id, person in self._persons.items():
            if policy_id in person.policies:
                del self._persons[id].policies[policy_id]

