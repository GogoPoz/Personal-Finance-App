import mysql.connector

MYSQL = mysql.connector


def open_connection_without_database():
    try:
        return MYSQL.connect(
            host="localhost",
            user="root",
            password="1234qazwsx4321"
        )
    except MYSQL.Error as e:
        print("Error" + str(e))
        return None


def open_connection():
    try:
        return MYSQL.connect(
            host="localhost",
            user="root",
            password="1234qazwsx4321",
            database="transactionsdb"
        )
    except MYSQL.Error as e:
        print("Error" + str(e))
        return None


def close_connection(connection):
    try:
        connection.close()
    except MYSQL.Error as e:
        print("Error" + str(e))


def import_sql_file(sql_file, connection):
    try:
        with open(sql_file, 'r') as f:
            cursor = connection.cursor()
            sql_script = f.read()
            sql_commands = sql_script.split(";")
            for command in sql_commands:
                try:
                    cursor.execute(command)
                    connection.commit()
                except MYSQL.Error as e:
                    print("Command skipped: ", e)
            cursor.close()
    except FileNotFoundError:
        print("Το αρχείο SQL δεν βρέθηκε.")
        return None
    except Exception as e:
        print("Σφάλμα κατά την ανάγνωση του αρχείου SQL:", e)
        return None


def check_if_database_exists(connection, db_name):
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES LIKE %s", (db_name,))
    result = cursor.fetchone()
    cursor.close()
    return result is not None


def setup_database():
    db_name = "transactionsdb"

    connection = open_connection_without_database()
    if connection is None:
        print("Failed to connect to the database server.")
        return

    if not check_if_database_exists(connection, db_name):
        try:
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE {db_name}")
            connection.commit()
            cursor.close()
        except MYSQL.Error as e:
            print("Error: " + str(e))
        finally:
            close_connection(connection)

        connection = open_connection()
        if connection is None:
            print("Failed to connect to the database server.")
            return

        import_sql_file("transactions.sql", connection)
        close_connection(connection)
    else:
        close_connection(connection)


def insert_data(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    lastrowid = None
    if cursor.lastrowid:
        lastrowid = cursor.lastrowid
    cursor.close()
    return lastrowid


def delete_or_update_data(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.close()


def query_fetch_all(connection, query):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except MYSQL.Error as e:
        print("Error" + str(e))
