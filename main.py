# Casusgroep 12 - Alain Lardinois & Peter Roijen
import sqlite3
import os
import time


class SqliteDBConnection:
    def __init__(self, type_db):
        self.connect_to_db = sqlite3.connect(type_db)
        self.cursor = self.connect_to_db.cursor()

    def execute_query(self, input_query, *arg):
        self.cursor.execute(input_query, arg)
        return self.cursor.fetchall()

    def modify_table_values(self, modify_value_query, *arg):
        self.cursor.execute(modify_value_query, arg)


class Login(SqliteDBConnection):
    def __init__(self):
        self.login_db_path = os.path.join(os.path.dirname(__file__), 'login_db.db')
        super().__init__(self.login_db_path)
        self.find_user = {1: "SELECT * FROM login_student WHERE username = ? AND password = ?",
                          2: "SELECT * FROM login_slber WHERE username = ? AND password = ?",
                          3: "SELECT * FROM login_management WHERE username = ? AND password = ?"}
        self.logged_in = False

    def search_user(self, choice_user, username, password):
        return self.execute_query(self.find_user[choice_user], username, password)


class SPA(SqliteDBConnection):
    def __init__(self, type_user, user_id):
        self.spa_db_path = os.path.join(os.path.dirname(__file__), 'spa_data.db')
        super().__init__(self.spa_db_path)
        self.choice_menu = {1: {0: self.close_program},
                            2: {0: self.close_program},
                            3: {0: self.close_program}}
        self.choice_app = []
        self.user_type = type_user
        self.userID = user_id
        self.done_with_app = False

    def display_menu(self):
        if self.user_type is 1:
            print("\nKies een van de onderstaande taken die u wilt uitvoeren.\n"
                  "1. "
                  "0. Sluit de applicatie af")
            self.choice_app = [0]
        if self.user_type is 2:
            print("\nKies een van de onderstaande taken die u wilt uitvoeren.\n"
                  "1. "
                  "0. Sluit de applicatie af")
            self.choice_app = [0]
        if self.user_type is 3:
            print("\nKies een van de onderstaande taken die u wilt uitvoeren.\n"
                  "1. "
                  "0. Sluit de applicatie af")
            self.choice_app = [0]

    def app_choice(self):
        valid_menu_choice = False
        while not valid_menu_choice:
            try:
                self.display_menu()
                choice_app = int(input("\nWat is uw keuze?: "))
                if choice_app in self.choice_app:
                    action = self.choice_menu[self.user_type].get(choice_app)
                    action()
                    valid_menu_choice = True
                else:
                    print("\n{} is geen geldige keuze, probeer het nog eens.".format(choice_app))
            except ValueError:
                print("\nU heeft een ongeldig karakter ingevuld, probeer het nog eens.")

    def close_program(self):
        print("\nWij wensen u een fijne dag!")
        time.sleep(2)
        self.done_with_app = True


def login(choice_user, username, password):
    login_user = Login()
    users = login_user.search_user(choice_user, username, password)
    if len(users) > 0:
        print("\nWelkom {} {}.".format(users[0][2], users[0][3]))
        return True, users
    else:
        print("\nDe opgegeven credentials zijn niet bekend in het systeem, probeer het nog eens.")
        return False


def user_credentials():
    print("\nKies een van de onderstaande gebruikers waar u op wilt inloggen.\n"
          "1. Student\n"
          "2. SLB'er\n"
          "3. Management")
    valid_input = False
    while not valid_input:
        try:
            choice_user = int(input("\nWat is uw keuze?: "))
            username = input("\nWat is uw gebruikersnaam?: ")
            password = input("Wat is uw wachtwoord?: ")
            valid_input = True
            return choice_user, username, password
        except ValueError:
            print("De keuze dat u heeft gemaakt is niet mogelijk, probeer het nog eens.")


def main():
    connect_login_db = Login()

    while not connect_login_db.logged_in:
        credentials = user_credentials()
        check_if_logged_in = login(credentials[0], credentials[1], credentials[2])
        try:
            is_logged_in = check_if_logged_in[0]
        except TypeError:
            is_logged_in = check_if_logged_in

        if is_logged_in is True:
            connect_login_db.logged_in = is_logged_in
        else:
            connect_login_db.logged_in = is_logged_in

    use_apps = SPA(credentials[0], check_if_logged_in[1][0][0])

    while not use_apps.done_with_app:
        use_apps.app_choice()


if __name__ == "__main__":
    main()
