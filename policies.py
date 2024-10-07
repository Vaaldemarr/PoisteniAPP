from policy import InsurancePolicy

class Policies:
    """
    Kolekce pojištění. 
    Obsahuje slovník, kde klíč je identifikátor pojištění a hodnota je objekt typu InsurancePolicy.
    Umožňuje přistupovat k prvkům kolekce podle klíče ve slovníku jako podle indexu.
    """

    def __init__(self):
        """Konstruktor třídy Policies. Vytvoří slovník pro uložení pojištění"""
        self._policies = {}

    # Přidání pojištění
    def __setitem__(self, _id, policy):
        # if _id in self._policies:
        #     raise ValueError(f"Policy with ID {_id} already exists.")
        if not isinstance(policy, InsurancePolicy):
            raise TypeError("Policy must be an instance of InsurancePolicy.")
        self._policies[_id] = policy

    # Získání pojištění podle identifikátoru _id
    def __getitem__(self, _id):
        return self._policies.get(_id, None)

    # Odstranění pojištění podle identifikátoru _id
    def __delitem__(self, _id):
        if _id in self._policies.keys():
            del self._policies[_id]
        else:
            raise KeyError(f"Policy with ID {_id} does not exist.")

    # Kontrola přítomnosti pojištění podle identifikátoru _id
    def __contains__(self, _id):
        return _id in self._policies

    # Magická metoda pro získání množství
    def __len__(self):
        return len(self._policies)

    # Magická metoda pro iteraci
    def __iter__(self):
        return iter(self._policies.items())

