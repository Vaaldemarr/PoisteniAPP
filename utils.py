import re

class Check:
    """Obsahuje statické metody pro kontrolu hodnot atributů"""

    @staticmethod
    def email(text):
        '''kontroluje e-mail pomocí regulárního výrazu.

        Args:
            text (str): E-mailová adresa

        Returns:
            bool: True, pokud e-mailová adresa odpovídá šabloně, jinak False.
        '''
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$"

        if re.match(regex, text):
            return True
        return False

    @staticmethod
    def phone(text):
        """kontroluje telefonní číslo pomocí regulárního výrazu.

        Args:
            text (str): Telefonní číslo pro ověření.

        Returns:
            bool: True, pokud telefonní číslo odpovídá šabloně, jinak False.
        """

        # 1. Jen čísla
        regex_digits_only = r"^\d+$"

        # 2. Jen čísla a vnitřní znaky "-"
        regex_digits_and_hyphens = r"^\d+(-\d+)*$"

        # 3. "("" pak jen čísla, pak "")"" pak jen čísla a uvnitř znaky "-" s mezerou
        regex_with_parentheses = r"^(\d+)\s?\d+(-\d+)*$"

        if (re.match(regex_digits_only, text)
            or re.match(regex_digits_and_hyphens, text)
            or re.match(regex_with_parentheses, text)):
            return True
        else:
            return False

    @staticmethod
    def postal_code(text):
        """kontroluje poštovní směrovací číslo pomocí regulárního výrazu.

        Args:
            text (str): Poštovní směrovací číslo pro ověření.

        Returns:
            bool: True, pokud poštovní směrovací číslo odpovídá šabloně, jinak False.
        """

        regex_postal_code = r"^[A-Za-z\d][A-Za-z\d\s-]*$"
        if re.match(regex_postal_code, text):
            return True
        return False

    @staticmethod
    def positive_number(value):
        """kontroluje, zda je hodnota kladné číslo

        Args:
            value: Kontrolovaná hodnota

        Returns:
            bool: True, pokud je číslo kladné, jinak False.
        """

        try:
            value=float(value)
            return value > 0
        except:
            return False
        
