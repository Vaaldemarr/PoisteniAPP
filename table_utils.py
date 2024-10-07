from database import DatabaseInsurances

class Pagination:
    """Obsahuje statické metody pro výpočet stránek tabulky"""

    @staticmethod
    def chek_policies_page(my_db, page):
        """
        Kontroluje, zda aktuální stránka tabulky pojištění nevybočuje z rozsahu stránek.

        Args:
            page (int): Aktuální stránka.

        Returns:
            int: Aktuální stránka.
        """        
        page = int(page)
        db = DatabaseInsurances(my_db.db_name)
        total_policies = db.insurance_policies_count()[0]
        total_pages = (total_policies + 2) // 3
        return page if page<=total_pages else total_pages

    @staticmethod
    def chek_persons_page(my_db, page):
        """
        Kontroluje, zda aktuální stránka tabulky pojištěnců nevybočuje z rozsahu stránek.

        Args:
            page (int): Aktuální stránka.

        Returns:
            int: Aktuální stránka.
        """        
        page = int(page)
        db = DatabaseInsurances(my_db.db_name)
        total_persons = db.insured_persons_count()[0]
        total_pages = (total_persons + 2) // 3
        return page if page<=total_pages else total_pages

    @staticmethod
    def calculate_table_pages(my_db, table_name, per_page, page):
        """
        Výpočet aktuální stránky tabulky k zobrazení.

        Args:
            table_name (str): Název tabulky (policies nebo persons).
            per_page (int): Počet řádků v tabulce.
            page (int): Aktuální stránka.

        Returns:
            tuple: řez kolekce pro zobrazení, číslo stránky, celkem stránek.
        """        
        to_show=[]

        if table_name=='persons':
            insured_persons = my_db.get_all_insured_persons()
            for id, next_person in insured_persons.items():
                to_show.append((f"{next_person.first_name} {next_person.last_name}",f"{next_person.street}, {next_person.city}", id))

        elif table_name=='policies':
            policies = my_db.get_all_insurance_policies()
            for id, policy_info in policies.items():
                policy=policy_info[0]
                persons=policy_info[1]
                to_show.append((str(id), policy.title, policy.insured_amount, persons))

        total_pages = (len(to_show) + per_page - 1) // per_page
        start = (page - 1) * per_page
        end = start + per_page

        to_show_slice = to_show[start:end]

        if table_name=='persons':
            page = Pagination.chek_persons_page(my_db, page)
        elif table_name=='policies':
            page = Pagination.chek_policies_page(my_db, page)

        if page==total_pages==0:
            page=total_pages=1

        return (to_show_slice, page, total_pages)

    @staticmethod
    def total_table_pages(my_db, table_name, per_page):
        """
        Vypočítá celkový počet stránek tabulky podle počtu řádků v tabulce.

        Args:
            table_name (str): Název tabulky (policies nebo persons).
            per_page (int): Počet řádků v tabulce.

        Returns:
            int: Počet stránek.
        """        
        db = DatabaseInsurances(my_db.db_name)
        if table_name == 'policies':
            total_items = db.insurance_policies_count()[0]
        elif table_name == 'persons':
            total_items = db.insured_persons_count()[0]
        return (total_items + 2) // per_page  # Výpočet počtu stránek

