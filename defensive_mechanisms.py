import datetime
import calendar


def check_description(message=None):
    while True:
        description_input = input(message)
        if description_input.strip() == "":
            print("Λάθος είσοδος. Παρακαλώ προσπαθήστε ξανά")
            continue
        elif not description_input.isalnum():
            print("Παρακαλώ εισάγετε μόνο γράμματα ή αριθμούς.")
            continue
        return description_input


def check_amount(message=None):
    while True:
        amount_input = input(message)
        if amount_input.replace('.', '', 1).isdigit():
            amount_input = float(amount_input)
            if amount_input > 0:
                break
            else:
                print("Παρακαλώ εισάγετε ένα ποσό μεγαλύτερο του μηδενός.")
                continue
        else:
            print("Λάθος είσοδος. Παρακαλώ προσπαθήστε ξανά")
            continue
    return amount_input


def add_one_month(orig_date):
    new_year = orig_date.year
    new_month = orig_date.month + 1

    if new_month > 12:
        new_year += 1
        new_month -= 12

    last_day_of_month = calendar.monthrange(new_year, new_month)[1]
    new_day = min(orig_date.day, last_day_of_month)

    return orig_date.replace(year=new_year, month=new_month, day=new_day)
