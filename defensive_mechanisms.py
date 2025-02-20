import datetime
import calendar


def check_description(message=None):
    """ H συνάρτηση ελέγχει αν η ονομασία της συναλλαγής είναι έγκυρη(να μην είναι κενό string και να περιέχει μόνο
    γράμματα ή αριθμούς - όχι ειδικούς χαρακτήρες)"""
    while True:
        # έλεγχος για σκέτο enter η input που περιέχει μόνο κενά
        description_input = input(message)
        if description_input.strip() == "":
            print("Λάθος είσοδος. Παρακαλώ προσπαθήστε ξανά")
            continue
        # περιορισμός να περιέχει μόνο γράμματα και αριθμούς
        elif not description_input.isalnum():
            print("Παρακαλώ εισάγετε μόνο γράμματα ή αριθμούς.")
            continue
        return description_input


def check_amount(message=None):
    """ Η συνάρτηση παίρνει ένα ποσό από το input, ελέγχει αν αυτό το ποσό είναι int η float και αν είναι το επιστρέφει
    Το όρισμα message είναι None ώστε όταν καλείται η check_amount να παίρνει όρισμα το εκάστοτε μήνυμα που
    θέλουμε να εμφανίσουμε """
    while True:
        amount_input = input(message)
        # Έλεγχος αν το ποσό που εισάχθηκε είναι int η float μεγαλύτερα του μηδενός
        if amount_input.replace('.', '', 1).isdigit():
            amount_input = float(amount_input)
            if amount_input > 0:
                break
            else:  # όταν εισάγεται 0 η αρνητικός αριθμός
                print("Παρακαλώ εισάγετε ένα ποσό μεγαλύτερο του μηδενός.")
                continue
        else:  # όταν εισάγεται οτιδήποτε άλλο εκτός float η int
            print("Λάθος είσοδος. Παρακαλώ προσπαθήστε ξανά")
            continue
    return amount_input


def add_one_month(orig_date):
    new_year = orig_date.year
    # προσθέτει έναν μήνα στην αρχική ημερομηνία
    new_month = orig_date.month + 1
    # περίπτωση που αυτός ο μήνας είναι ο Δεκέμβριος ώστε να αλλάξει η χρονιά
    if new_month > 12:
        new_year += 1
        new_month -= 12

    # αποθηκεύει την τελευταία ημέρα του καινούριου μήνα ώστε να γίνει η κατάλληλη αλλαγή (περίπτωση που η αρχική ημέρα
    # βρίσκεται στο τέλος του μήνα πχ 31)
    last_day_of_month = calendar.monthrange(new_year, new_month)[1]
    new_day = min(orig_date.day, last_day_of_month)

    return orig_date.replace(year=new_year, month=new_month, day=new_day)
