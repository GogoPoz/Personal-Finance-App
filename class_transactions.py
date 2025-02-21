from db_functions import *
from defensive_mechanisms import *
from datetime import date
import calendar


class Transactions:
    def __init__(self, connector):
        self.type = None
        self.monthly = None
        self.category = None
        self.description = None
        self.amount = None
        self.insert_date = None
        self.total = None
        self.original_date = None
        self.connector = connector

    def load_transaction(self, description):
        results = query_fetch_all(self.connector,
                                  "SELECT * FROM transactions WHERE descr_of_trans='" + str(description) + "'")
        if results:
            data = results[0]
            self.type = data["type_of_trans"]
            self.monthly = data["sub_type_of_trans"]
            self.category = data["category"]
            self.description = data["descr_of_trans"]
            self.amount = data["amount"]
            self.insert_date = data["insert_date"]
            return self
        else:
            return None

    def add_to_total(self, amount):
        results = query_fetch_all(self.connector, "SELECT * FROM total_amount")
        if results:
            data = results[0]
            self.total = data["total"]
            self.total += amount
            delete_or_update_data(self.connector, f"UPDATE total_amount SET total={self.total}")
            self.connector.commit()
        else:
            self.total = amount
            query = f"INSERT INTO total_amount (total) VALUES ({self.total})"
            insert_data(self.connector, query)
            self.connector.commit()

    def subtract_from_total(self, amount):
        results = query_fetch_all(self.connector, "SELECT * FROM total_amount")
        if results:
            data = results[0]
            self.total = data["total"]
            self.total -= amount
            delete_or_update_data(self.connector, f"UPDATE total_amount SET total={self.total}")
            self.connector.commit()
        else:
            self.total = -amount
            query = f"INSERT INTO total_amount (total) VALUES ({self.total})"
            insert_data(self.connector, query)
            self.connector.commit()

    def load_monthly(self):
        results = query_fetch_all(self.connector, "SELECT * FROM transactions WHERE sub_type_of_trans=1")
        monthly_transactions = []
        if results:
            for result in results:
                transaction = Transactions(self.connector)
                transaction.type = result["type_of_trans"]
                transaction.description = result["descr_of_trans"]
                transaction.amount = result["amount"]
                transaction.insert_date = result["insert_date"]
                transaction.original_date = result["original_date"]
                monthly_transactions.append(transaction)

        amount_to_add = 0
        amount_to_subtract = 0

        for transaction in monthly_transactions:
            old_date = transaction.insert_date
            today = date.today()
            if transaction.type == 1:
                while (old_date.year < today.year) or (
                        old_date.year == today.year and old_date.month < today.month):
                    if old_date.month == today.month - 1 and old_date.day > today.day:
                        break
                    else:
                        old_date = add_one_month(old_date)
                        amount_to_add += transaction.amount
                        transaction.insert_date = old_date
            elif transaction.type == 2:
                while (old_date.year < today.year) or (
                        old_date.year == today.year and old_date.month < today.month):
                    if old_date.month == today.month - 1 and old_date.day > today.day:
                        break
                    else:
                        old_date = add_one_month(old_date)
                        amount_to_subtract += transaction.amount
                        transaction.insert_date = old_date

            original_day = transaction.original_date.day
            last_day_of_current_month = calendar.monthrange(transaction.insert_date.year, transaction.insert_date.month)[1]
            if original_day > last_day_of_current_month:
                transaction.insert_date = transaction.insert_date.replace(day=last_day_of_current_month)
            elif original_day <= last_day_of_current_month:
                transaction.insert_date = transaction.insert_date.replace(day=original_day)
            delete_or_update_data(self.connector, f"UPDATE transactions SET "
                                                  f"insert_date='{transaction.insert_date}' "
                                                  f"WHERE descr_of_trans='{transaction.description}'")

            self.connector.commit()
        self.add_to_total(amount_to_add)
        self.subtract_from_total(amount_to_subtract)

    def create_transaction(self):
        self.category = check_description("Εισάγετε την κατηγορία της συναλλαγής που θέλετε να καταχωρήσετε: ")
        self.description = check_description("Εισάγετε το όνομα της συναλλαγής που θέλετε να καταχωρήσετε: ")
        results = self.load_transaction(self.description)
        if results:
            print("Η συναλλαγή υπάρχει ήδη. Παρακαλώ επιλέξτε άλλο όνομα.")
            return
        elif results is None:
            while True:
                action_monthly = input("Πρόκειται για μηνιαία συναλλαγή (1-μηνιαία, 2-άλλο);")
                if action_monthly in ["1", "2"]:
                    break
                elif not action_monthly.isdigit() or int(action_monthly) not in [1, 2]:
                    print("Μη έγκυρη επιλογή, παρακαλώ προσπαθήστε ξανά.")

            self.monthly = int(action_monthly)
            while True:
                action_type = input("H συναλλαγή σας αφορά έσοδο η έξοδο (1-έσοδο, 2-έξοδο);")
                if action_type in ["1", "2"]:
                    break
                elif not action_type.isdigit() or int(action_type) not in [1, 2]:
                    print("Μη έγκυρη επιλογή, παρακαλώ προσπαθήστε ξανά.")
                continue
            self.type = int(action_type)
            self.amount = check_amount("Εισάγετε το ποσό της συναλλαγής: ")
            self.insert_date = date.today()
            self.original_date = date.today()
        query = f"""INSERT INTO transactions (type_of_trans, sub_type_of_trans, category, descr_of_trans, amount,
                                    insert_date, original_date)
                                    VALUES ({self.type}, {self.monthly}, '{self.category}', '{self.description}', {self.amount}, 
                                    '{self.insert_date}', '{self.original_date}')"""
        insert_data(self.connector, query)
        self.connector.commit()

        if self.type == 1:
            self.add_to_total(self.amount)
        elif self.type == 2:
            self.subtract_from_total(self.amount)
        print("Η συναλλαγή σας αποθηκεύτηκε επιτυχώς.")

    def update_transaction(self):
        """H μέθοδος ψάχνει συναλλαγή με το συγκεκριμένο description(όνομα) και την τροποποιεί αν αυτή υπάρχει"""
        description = check_description("Εισάγετε το όνομα της συναλλαγής που θέλετε να τροποποιήσετε: ")
        results = self.load_transaction(description)
        if results is None:
            print(f"Δεν βρέθηκε συναλλαγή με όνομα {description}. Παρακαλώ δοκιμάστε ξανά.")
            return
        while True:
            if results:
                choice = int(input("Επιλέξτε το στοιχείο προς τροποποίηση ή έξοδο στην περίπτωση που δεν θέλετε "
                                   "να τροποποιήσετε κάτι:\n1)Ποσό\n2)Όνομα\n3)Κατηγορία\n"
                                   "4)Πρόσθεση/αφαίρεση από τις μηνιαίες συναλλαγές\n5)Έξοδος\n"))

                if choice == 1:
                    new_amount = check_amount("Εισάγετε το νέο ποσό: ")
                    if new_amount != self.amount:
                        if self.type == 1:
                            if new_amount > self.amount:
                                amount_to_add = new_amount - self.amount
                                self.amount = new_amount
                                self.add_to_total(amount_to_add)
                            elif new_amount < self.amount:
                                amount_to_subtract = self.amount - new_amount
                                self.amount = new_amount
                                self.subtract_from_total(amount_to_subtract)
                        elif self.type == 2:
                            if new_amount > self.amount:
                                amount_to_subtract = new_amount - self.amount
                                self.amount = new_amount
                                self.subtract_from_total(amount_to_subtract)
                            elif new_amount < self.amount:
                                amount_to_add = self.amount - new_amount
                                self.amount = new_amount
                                self.add_to_total(amount_to_add)
                    delete_or_update_data(self.connector, f"UPDATE transactions SET amount={new_amount} "
                                                          f"WHERE descr_of_trans='{self.description}'")

                    self.connector.commit()
                    print("Το ποσό άλλαξε επιτυχώς.")
                elif choice == 2:
                    new_description = check_description("Εισάγετε το νέο όνομα: ")
                    delete_or_update_data(self.connector, f"UPDATE transactions "
                                                          f"SET descr_of_trans='{new_description}' "
                                                          f"WHERE descr_of_trans='{self.description}'")
                    self.connector.commit()
                    self.description = new_description
                    print("Το όνομα άλλαξε επιτυχώς.")
                elif choice == 3:
                    new_category = check_description("Εισάγετε την νέα κατηγορία: ")
                    delete_or_update_data(self.connector, f"UPDATE transactions "
                                                          f"SET category='{new_category}' "
                                                          f"WHERE descr_of_trans='{self.description}'")
                    self.connector.commit()
                    self.category = new_category
                    print("Η κατηγορία άλλαξε επιτυχώς.")
                elif choice == 4:
                    if self.monthly == 1:
                        delete_or_update_data(self.connector, f"UPDATE transactions SET sub_type_of_trans=2 "
                                                              f"WHERE descr_of_trans='{self.description}'")
                        self.monthly = 2
                        print("Αφαιρέθηκε από τις μηνιαίες συναλλαγές επιτυχώς.")
                        self.connector.commit()
                    elif self.monthly == 2:
                        delete_or_update_data(self.connector, f"UPDATE transactions SET sub_type_of_trans=1 "
                                                              f"WHERE descr_of_trans='{self.description}'")
                        self.monthly = 1
                        print("Προστέθηκε στις μηνιαίες συναλλαγές επιτυχώς.")
                        self.connector.commit()
                else:
                    break

    def delete_transaction(self):
        description = check_description("Εισάγετε το όνομα της συναλλαγής που θέλετε να διαγράψετε: ")
        results = self.load_transaction(description)

        if results is None:
            print(f"Δεν βρέθηκε συναλλαγή με όνομα {description}. Παρακαλώ δοκιμάστε ξανά.")
            return
        else:
            query = f"DELETE FROM transactions WHERE descr_of_trans='{self.description}'"
            delete_or_update_data(self.connector, query)
            if self.type == 1:
                self.subtract_from_total(self.amount)
            elif self.type == 2:
                self.add_to_total(self.amount)
            self.connector.commit()
            print("Η συναλλαγή διαγράφηκε επιτυχώς.")

    def print_transactions(self):
        results = query_fetch_all(self.connector, "SELECT * FROM transactions")
        print_transactions = []

        if results:
            for result in results:
                transaction = Transactions(self.connector)
                transaction.type = result["type_of_trans"]
                transaction.monthly = result["sub_type_of_trans"]
                transaction.category = result["category"]
                transaction.description = result["descr_of_trans"]
                transaction.amount = result["amount"]
                transaction.insert_date = result["insert_date"]
                print_transactions.append(transaction)
        else:
            print("Δεν βρέθηκαν συναλλαγές.")

        for transaction in print_transactions:
            st = ""
            st += f"Κατηγορία: {transaction.category}, Όνομα συναλλαγής: {transaction.description}, Τύπος συναλλαγής: "
            if transaction.type == 1:
                st += "Έσοδο, "
            elif transaction.type == 2:
                st += "Έξοδο, "
            st += "Μηνιαία συναλλαγή: "
            if transaction.monthly == 1:
                st += "Ναι, "
            elif transaction.monthly == 2:
                st += "Όχι, "
            st += f"Ποσό: {transaction.amount}, Ημερομηνία συναλλαγής: {transaction.insert_date}."
            print(st)

    def print_total(self):
        results = query_fetch_all(self.connector, "SELECT * FROM total_amount")
        if results:
            transaction = Transactions(self.connector)
            transaction.total = results[0]["total"]
            print(f"Συνολικό ποσό: {transaction.total}")
        else:
            print("Δεν βρέθηκαν χρήματα στο συνολικό ποσό.")
