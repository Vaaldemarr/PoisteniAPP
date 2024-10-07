from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

from insured_person import InsuredPerson
from policy import InsurancePolicy
from persons import Persons
from policies import Policies

from interface_to_db import DatabaseInterface
from database import DatabaseInsurances

from table_utils import Pagination


class FlaskInterface:
    """
    Třída implementuje webové rozhraní pro databázi pojištěnců na lokálním serveru.
    Obsahuje informace o pojištěnci a kolekci jeho pojištění.

    Attributes:
        my_db (DatabaseInterface): Rozhraní do databáze.
        insured (Persons): kolekce pojištěných.
    """

    def __init__(self, my_db: DatabaseInterface, persons: Persons) -> None:
        """
        Konstruktér třídy. Propojuje trasy se svými třídními metodami.

        Args:
            my_db (DatabaseInterface): Rozhraní do databáze.
            persons (Persons): kolekce pojištěných.
        """
        self.my_db = my_db
        self.insured = persons

        # Registrace tras uvnitř konstruktoru
        app.add_url_rule('/', view_func=self.index, methods=['GET'])
        app.add_url_rule('/persons', view_func=self.persons, methods=['GET'])
        app.add_url_rule('/policies', view_func=self.policies, methods=['GET'])
        app.add_url_rule('/new', view_func=self.new_person, methods=['GET', 'POST'])
        app.add_url_rule('/new2', view_func=self.new2_policy, methods=['GET', 'POST'])
        app.add_url_rule('/delete_person/<person_id>', view_func=self.delete_person, methods=['GET'])
        app.add_url_rule('/edit_person/<person_id>/<source>/<page>', view_func=self.edit_person, methods=['GET', 'POST'])
        app.add_url_rule('/person/<person_id>', view_func=self.person, methods=['GET'])
        app.add_url_rule('/delete_policy/<policy_id>/<current_page>', view_func=self.delete_policy, methods=['GET'])
        app.add_url_rule('/edit_policy/<policy_id>/<source>/<page>', view_func=self.edit_policy, methods=['GET', 'POST'])
        app.add_url_rule('/delete_person_policy/<person_id>/<policy_id>', view_func=self.delete_person_policy, methods=['GET'])
        app.add_url_rule('/add_person_policy/<person_id>', view_func=self.add_person_policy, methods=['GET', 'POST'])
        app.add_url_rule('/about', view_func=self.about_project, methods=['GET'])
        app.add_url_rule('/show_persons', view_func=self.show_persons, methods=['GET'])

    def start(self):
        """
            Spustí webový server flask na adrese
            http://127.0.0.1:5000
        """
        app.run(debug=True)

    def index(self):
        """Domovská stránka"""
        return redirect(url_for('persons'))

    def persons(self):
        """Webová stránka: Seznam pojištěnců"""
        page = int(request.args.get('page', 1))
        saved = request.args.get('saved', '0') == '1'
        saved_text = request.args.get('saved_text', '')

        to_show, page, total_pages  = Pagination.calculate_table_pages(self.my_db, 'persons', 3, page)

        return render_template('persons.html', persons=to_show, saved=saved, saved_text=saved_text,
                            page=page, previous_page=page - 1 if page > 1 else 1,
                            next_page=page + 1 if page < total_pages else total_pages + 1,
                            total_pages=total_pages)

    def policies(self):
        """Webová stránka: Seznam pojištění"""
        page = int(request.args.get('page', 1))
        saved = request.args.get('saved', '0') == '1'
        saved_text = request.args.get('saved_text', '')

        to_show, page, total_pages  = Pagination.calculate_table_pages(self.my_db, 'policies', 3, page)

        return render_template('policies.html', policies=to_show,
                            saved=saved, saved_text=saved_text, page=page, 
                            previous_page=page - 1 if page > 1 else 0,
                            next_page=page + 1 if page < total_pages else total_pages + 1,
                            total_pages=total_pages)

    def new_person(self):
        """Webová stránka: Vytvoření nového pojištěnce"""
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = request.form['phone']
            street = request.form['street']
            city = request.form['city']
            postal_code = request.form['postal_code']

            new_insured = InsuredPerson(first_name, last_name, email, phone, street, city, postal_code)

            check_data = new_insured.check_valid_data()
            
            if check_data != '':
                return render_template('new_person.html', err_msg=check_data, person=new_insured)
            if self.my_db.is_person_exists(new_insured)>0:
                err_msg = f"Tento pojištěnec již existuje: {first_name} {last_name}"
                return render_template('new_person.html', err_msg=err_msg, person=new_insured)

            person_id = self.my_db.add_insured_person_to_db(new_insured)
            self.insured[person_id] = new_insured

            return redirect(url_for('persons', 
                                    page=Pagination.total_table_pages(self.my_db, 'persons', 3), 
                                    saved=True, saved_text="Pojištěnec byl uložen."))
        
        return render_template('new_person.html', err_msg=None, person=InsuredPerson("","","","","","",""))

    def new2_policy(self):
        """Webová stránka: Vytvoření nového pojištění"""
        if request.method == 'POST':
            title = request.form['title']
            insured_amount = request.form['insured_amount']
            insured_object = request.form['insured_object']
            start_date = request.form['start_date']
            end_date = request.form['end_date']

            policy = InsurancePolicy(title, insured_amount, insured_object, start_date, end_date)
            check_data = policy.check_valid_data()
            if check_data != '':
                return render_template('new_policy.html', err_msg=check_data, policy=policy)
            if self.my_db.is_policy_title_exist(title):
                return render_template('new_policy.html', err_msg=f"Tento Jméno již existuje: {title}", policy=policy)

            self.my_db.add_insurance_policy_to_db(policy)

            return redirect(url_for('policies', 
                                    page=Pagination.total_table_pages(self.my_db, 'policies', 3), 
                                    saved=True, saved_text="Pojištění bylo uloženo."))

        return render_template('new_policy.html', err_msg=None, policy=InsurancePolicy("","","","",""))

    def delete_person(self, person_id):
        """
        Odstranění pojištěného.

        Args:
            person_id (int): Identifikátor pojištěného.
        """        
        
        db = DatabaseInsurances(self.my_db.db_name)
        db.delete_insured_person(person_id)
        del self.insured[int(person_id)]

        total_pages = Pagination.total_table_pages(self.my_db, 'persons', 3)

        return redirect(url_for('persons', page=total_pages, saved=True, saved_text="Pojištěnec byl odstraněn."))

    def edit_person(self, person_id, source, page):
        """
        Webová stránka: Editování pojištěného.

        Args:
            person_id (str): Identifikátor pojištěného.
            source (str): Zdrojová trasa pro návrat, kam je uživatel přesměrován.
            page (str): Zdrojové číslo stránky pro návrat.
        """        
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = request.form['phone']
            street = request.form['street']
            city = request.form['city']
            postal_code = request.form['postal_code']

            edited_insured = InsuredPerson(first_name, last_name, email, phone, street, city, postal_code)
            check_data = edited_insured.check_valid_data()
            if check_data != '':
                return render_template('edit_person.html', person_id=person_id, person=edited_insured, source=source, page=page, err_msg=check_data)

            # Aktualizovat kolekce
            for policy_id, policy in self.insured[int(person_id)].policies:
                edited_insured.policies[policy_id] = policy
            self.insured[int(person_id)] = edited_insured
            self.my_db.update_insured_person_in_db(person_id, edited_insured)
            
            if source=='persons':
                return redirect(url_for('persons', 
                                        page=Pagination.chek_persons_page(self.my_db, page), 
                                        saved=True, saved_text="Pojištěnec byl upraven."))
            else:
                return redirect(url_for('person', person_id=person_id))

        person = self.my_db.find_insured_person_by_id(person_id)
        if person==None:
            return "Pojištěnec ID: {person_id} nenalezen v database!"
        return render_template('edit_person.html', person_id=person_id, person=person, source=source, page=page, err_msg=None)

    def person(self, person_id):
        """
        Webová stránka: Přehled pojištěného a jeho pojištění.

        Args:
            person_id (str): Identifikátor pojištěného.
        """
        person = self.my_db.find_insured_person_by_id(person_id)
        policies_dic = self.my_db.find_insurance_policies_by_person_id(person_id)

        # Aktualizovat kolekce
        policies_replace = Policies()
        for id, policy in policies_dic.items():
            policies_replace[id]=policy
        person.policies = policies_replace
        self.insured[int(person_id)] = person

        person_policies = [(id, policy) for id, policy in policies_dic.items()]

        return render_template('person.html', person_id=person_id, person=person, policies=person_policies)

    def delete_policy(self, policy_id, current_page):
        """
        Odstranění pojištěného.

        Args:
            policy_id (str): Identifikátor pojištění.
            current_page (str): Číslo stránky v tabulce pojištěnců pro vrácení.
        """
        db = DatabaseInsurances(self.my_db.db_name)
        db.delete_insurance_policy(policy_id)
        self.insured.delete_policy(policy_id)

        return redirect(url_for('policies', page=Pagination.chek_policies_page(self.my_db, current_page)))

    def edit_policy(self, policy_id, source, page):
        """
        Webová stránka: Editování pojištění.

        Args:
            policy_id (str): Identifikátor pojištění.
            source (str): Zdrojová trasa pro návrat, kam je uživatel přesměrován.
            page (str): Zdrojové číslo stránky pro návrat.
        """
        if request.method == 'POST':
            title = request.form['title']
            insured_amount = request.form['insured_amount']
            insured_object = request.form['insured_object']
            start_date = request.form['start_date']
            end_date = request.form['end_date']

            policy = InsurancePolicy(title, insured_amount, insured_object, start_date, end_date)
            check_data = policy.check_valid_data()
            if check_data != '':
                return render_template('edit_policy.html', policy_id=policy_id, policy=policy, source=source, page=page, err_msg=check_data)

            if not self.my_db.is_policy_title_unique(title, policy_id):
                return render_template('edit_policy.html', policy_id=policy_id, policy=policy, source=source, page=page, err_msg=f"Tento Jméno již existuje: {title}")
                
            self.insured.replace_policy(int(policy_id), policy)
            self.my_db.update_insurance_policy_in_db(policy_id, policy)

            if source=='policies':
                return redirect(url_for('policies', page=Pagination.chek_policies_page(self.my_db, page), 
                                        saved=True, saved_text=f"'{title}' bylo upraveno."))
            else:
                return redirect(url_for('person', person_id=source))
        
        policy = self.my_db.find_insurance_policy_by_id(policy_id)
        if policy==None:
            return "Pojištění ID: {policy_id} nenalezeno"
        return render_template('edit_policy.html', policy_id=policy_id, policy=policy, source=source, page=page, err_msg=None)

    def delete_person_policy(self, person_id, policy_id):
        """
        Webová stránka: Odpojit pojištění od pojištěného.

        Args:
            person_id (str): Identifikátor pojištěného.
            policy_id (str): Identifikátor pojištění.
        """
        db = DatabaseInsurances(self.my_db.db_name)
        db.delete_person_insurance_policy(person_id, policy_id)
        del self.insured[int(person_id)].policies[int(policy_id)]
        return redirect(url_for('person', person_id=person_id))

    def add_person_policy(self, person_id):
        """
        Webová stránka: Spojte pojištění s pojištěním.

        Args:
            person_id (str): Identifikátor pojištěného.
        """
        if request.method == 'POST':
            policy_id = request.form['policySelect']
            policy = self.my_db.find_insurance_policy_by_id(policy_id)
            if policy==None:
                return "Pojištění ID: {policy_id} nenalezeno"
            self.insured[int(person_id)].policies[int(policy_id)]=policy
            db = DatabaseInsurances(self.my_db.db_name)
            db.insert_person_insurance_policy(person_id, policy_id)
            return redirect(url_for('person', person_id=person_id))
        
        person = self.my_db.find_insured_person_by_id(person_id)
        unused_policies = self.my_db.get_all_unused_insurance_policies()
        select_data = []
        policies = []
        for id, policy in unused_policies.items():
            select_data.append((id, policy.title))
            policy_dic = {
                'title': policy.title,
                'insured_amount': policy.insured_amount,
                'insured_object': policy.insured_object,
                'start_date': policy.start_date,
                'end_date': policy.end_date,
            }
            policies.append(policy_dic)

        return render_template('person_policy.html', person_name=f"{person.first_name} {person.last_name}", select_data=select_data, policies=policies, person_id=person_id)

    def about_project(self):
        """Webová stránka: Informace o programu"""
        return render_template('about.html')

    def show_persons(self):
        """Webová stránka: Servisní stránka"""
        result = '<a href="/">PojištěníApp</a><br>\n'
        for id, _ in self.insured:
            result += f'<h4>{id}. {self.insured[id]}: <br></h4>\n<ul>'
            for id2, policy in self.insured[id].policies:
                result += f'<li>\t{id2}. {policy}</li>\n'
            result += f'</ul>\n'
        return result

