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

        # έξοδος
        if action == 4:
            break
        # Εισαγωγή/ τροποποίηση / διαγραφή
        elif action == 1:
            while True:
                print("1) Καταχώρηση \n2) Τροποποίηση \n3) Διαγραφή")
                sub_action = input("Επιλέξτε την ενέργεια (1/2/3) ή '4' για επιστροφή: ")

                if not sub_action.isdigit() or int(sub_action) not in [1, 2, 3, 4]:
                    print("Μη έγκυρη επιλογή, παρακαλώ προσπαθήστε ξανά.")
                    continue

                sub_action = int(sub_action)

                # Επιστροσή στο αρχικό μενού
                if sub_action == 4:
                    break
                # Καταχώρηση
                elif sub_action == 1:
                    transaction.create_transaction()
                # Τροποποίηση
                elif sub_action == 2:
                    transaction.update_transaction()
                # Διαγραφή
                elif sub_action == 3:
                    transaction.delete_transaction()
                else:
                    print("Μη έγκυρη επιλογή, παρακαλώ προσπαθήστε ξανά.")
        # Εμφάνιση συναλλαγών
        elif action == 2:
            transaction.print_transactions()
        # Εμφάνιση συνολικού ποσού
        elif action == 3:
            transaction.print_total()

    close_connection(connection)


if __name__ == "__main__":
    main()
