# Casusgroep 12 - Alain Lardinois & Peter Roijen
import sqlite3
import os


class SqliteDBConnection:
    def __init__(self, type_db):
        self.connect_to_db = sqlite3.connect(type_db)
        self.cursor = self.connect_to_db.cursor()

    def execute_query(self, input_query, *arg):
        self.cursor.execute(input_query, arg)
        return self.cursor.fetchall()

    def modify_table_values(self, modify_value_query, *arg):
        self.cursor.execute(modify_value_query, arg)


class SPA(SqliteDBConnection):
    def __init__(self, type_user):
        self.spa_db_path = os.path.join(os.path.dirname(__file__), 'spa_data.db')
        super().__init__(self.spa_db_path)
        self.choice_menu = {1: {1: self.print_available_courses,
                                0: self.close_spa_program},
                            2: {0: self.close_spa_program},
                            3: {0: self.close_spa_program}}
        self.choice_app_list = []
        self.user_type = type_user
        self.done_with_app = False

    def display_menu(self):
        if self.user_type is 1:
            print("\nKies een van de onderstaande taken die u wilt uitvoeren.\n"
                  "1. Mogelijke keuzevakken\n"
                  "0. Uitloggen")
            self.choice_app_list = [1, 0]
        if self.user_type is 2:
            print("\nKies een van de onderstaande taken die u wilt uitvoeren.\n"
                  "1. niets 1\n"
                  "0. Uitloggen")
            self.choice_app_list = [0]
        if self.user_type is 3:
            print("\nKies een van de onderstaande taken die u wilt uitvoeren.\n"
                  "1. niets 2\n"
                  "0. Uitloggen")
            self.choice_app_list = [0]

    def app_choice(self):
        valid_menu_choice = False
        while not valid_menu_choice:
            try:
                self.display_menu()
                choice_app = int(input("\nWat is uw keuze?: "))
                if choice_app in self.choice_app_list:
                    action = self.choice_menu[self.user_type].get(choice_app)
                    action()
                    valid_menu_choice = True
                else:
                    print("\n{} is geen geldige keuze, probeer het nog eens.".format(choice_app))
            except ValueError:
                print("\nDat is geen geldige keuze. Probeer het opnieuw.")

    def print_available_courses(self):
        # TODO: Werkt niet, aanpassen
        courses_query = "SELECT * FROM COURSES"
        print(self.cursor.description)
        print(self.execute_query(courses_query))

    def close_spa_program(self):
        print("\nU wordt nu uitgelogd. Wij wensen u een fijne dag!")
        self.done_with_app = True


def user_credentials():
    choices = [1, 2, 3, 0]
    print("\nKies een van de onderstaande opties.\n"
          "1. Inloggen student\n"
          "2. Inloggen SLBer\n"
          "3. Inloggen examencommissie\n"
          "0. Applicatie afsluiten")
    while True:
        try:
            choice_user = int(input("\nWat is uw keuze?: "))
            if choice_user in choices:
                return choice_user
            else:
                print("Dat is geen geldige keuze. Probeer het opnieuw.")
        except ValueError:
            print("Dat is geen geldige keuze. Probeer het opnieuw.")


def main():
    done = False
    while not done:
        credentials = user_credentials()
        if credentials is 0:
            done = True
        else:
            use_apps = SPA(credentials)
            while not use_apps.done_with_app:
                use_apps.app_choice()


if __name__ == "__main__":
    main()
