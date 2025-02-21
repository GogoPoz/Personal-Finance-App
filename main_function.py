from class_transactions import *
from db_functions import *
from datetime import datetime


def main():
    setup_database()
    connection = open_connection()
    transaction = Transactions(connection)
    transaction.load_monthly()

    while True:
        print("Τι ενέργεια επιθυμείτε; \n1) Καταχώρηση/Τροποποίηση/Διαγραφή \n2)Εκτύπωση συναλλαγών \n"
              "3)Εκτύπωση συνολικού ποσού")
        action = input("Επιλέξτε την ενέργεια (1/2/3) ή '4' για έξοδο: ")

        if not action.isdigit() or int(action) not in [1, 2, 3, 4]:
            print("Μη έγκυρη επιλογή, παρακαλώ προσπαθήστε ξανά.")
            continue

        action = int(action)

        if action == 4:
            break
        elif action == 1:
            while True:
                print("1) Καταχώρηση \n2) Τροποποίηση \n3) Διαγραφή")
                sub_action = input("Επιλέξτε την ενέργεια (1/2/3) ή '4' για επιστροφή: ")

                if not sub_action.isdigit() or int(sub_action) not in [1, 2, 3, 4]:
                    print("Μη έγκυρη επιλογή, παρακαλώ προσπαθήστε ξανά.")
                    continue

                sub_action = int(sub_action)

                if sub_action == 4:
                    break
                elif sub_action == 1:
                    transaction.create_transaction()
                elif sub_action == 2:
                    transaction.update_transaction()
                elif sub_action == 3:
                    transaction.delete_transaction()
                else:
                    print("Μη έγκυρη επιλογή, παρακαλώ προσπαθήστε ξανά.")
        elif action == 2:
            transaction.print_transactions()
        elif action == 3:
            transaction.print_total()

    close_connection(connection)  # Διακοπή σύνδεσης με την βάση


if __name__ == "__main__":
    main()
