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
        self.choice_menu = {1: {1: self.choose_courses,
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
                print("\nU heeft een ongeldig karakter ingevuld, probeer het nog eens.")

    def choose_courses(self):
        # TODO: Werkt niet, aanpassen
        done_with_choice_courses = False
        while not done_with_choice_courses:
            print("\nWie van onderstaande studenten bent u?\n"
                  "1. Peter Roijen\n"
                  "2. Alain Lardinois\n"
                  "3. Pietje Driekhoek\n"
                  "4. Marissa Shadow")
            student_id = input("Wat is uw keuze?: ")
            if student_id in ["1", "2", "3", "4"]:
                print("\nKies een van onderstaande taken die u wilt uitvoeren.\n"
                      "1. Huidig studieplan inzien\n"
                      "2. Studieplan bijwerken\n"
                      "0. Applicatie afsluiten")
                choice_menu = input("\nWat is uw keuze?")
                if choice_menu is "0":
                    done_with_choice_courses = True
                elif choice_menu is "1":
                    done = False
                    while not done:
                        period = input("\nVoor welke periode wilt u het studiepad inzien?: ")
                        if period in ["1", "2", "3", "4"]:
                            self.current_student_courses(student_id, period)
                            done = True
                        else:
                            print("\n{} is geen geldige periode, probeer het nog eens.".format(period))
                elif choice_menu is "2":
                    done_with_studypath_change = False
                    while not done_with_studypath_change:
                        period = input("\nVoor welke periode wilt u het studiepad inzien?: ")
                        if period in ["1", "2", "3", "4"]:
                            available_courses = self.available_courses(student_id, period)
                            choice_course = input("\nWelk vak wilt u toevoegen aan uw studiepad? (vul het vak ID in): ")
                            if choice_course in available_courses:

                                done_with_studypath_change = True
                            else:
                                print("\n{} is geen geldige keuze, probeer het nog eens.".format(choice_course))
                        else:
                            print("\n{} is geen geldige periode, probeer het nog eens.".format(period))
                else:
                    print("\n{} is geen geldige keuze, probeer het nog eens.".format(choice_menu))
            else:
                print("\n{} is geen geldige keuze, probeer het nog eens.".format(student_id))

    def current_student_courses(self, student_id, period):
        amount_ec = []
        student_courses_query = "SELECT SPC.course_id, C.course_name, C.amount_ec " \
                                "FROM study_paths SP " \
                                "JOIN study_path_courses SPC on SP.path_id = SPC.path_id " \
                                "JOIN courses C on SPC.course_id = C.course_id " \
                                "WHERE SP.student_id = ? AND SP.period = ?"
        show_courses_student = self.execute_query(student_courses_query, student_id, period)
        for row in show_courses_student:
            print("{:<10}".format(row[0]), "{:<10}".format(row[1]))
        for amount in show_courses_student:
            amount_ec.append(amount[2])
        print("\nHet aantal EC's van deze periode is {}".format(sum(amount_ec)))

    def available_courses(self, student_id, period):
        available_course_query = "SELECT C.course_id, C.course_name, C.amount_ec " \
                                 "FROM courses C " \
                                 "JOIN course_profile CP ON C.course_id = CP.course_id " \
                                 "JOIN profiles P ON CP.profile_id = P.profile_id " \
                                 "JOIN student_profile_choice SPC ON P.profile_id = SPC.profile_id " \
                                 "JOIN students S ON SPC.student_id = S.student_id " \
                                 "JOIN study_paths SP ON " \
                                 "WHERE SPC.student_id = ? AND C.period = ? " \
                                 "AND AND C.grade = S.grade AND CP.profile_id = SPC.profile_id"
        show_available_courses = self.execute_query(available_course_query, student_id, period)
        for row in show_available_courses:
            print("{:<10}".format(row[0]), "{:<10}".format(row[1]), "{:<10}".format(row[2]))
        return show_available_courses[0]

    def insert_courses(self):
        pass

    def close_spa_program(self):
        print("\nU wordt nu uitgelogd. Wij wensen u een fijne dag!")
        self.done_with_app = True


def user_credentials():
    choices = [0, 1, 2, 3]
    print("\nKies een van de onderstaande opties.\n"
          "1. Inloggen student\n"
          "2. Inloggen SLBer\n"
          "3. Inloggen exaemen commisie\n"
          "0. Applicatie afsluiten")
    while True:
        try:
            choice_user = int(input("\nWat is uw keuze?: "))
            if choice_user in choices:
                return choice_user
        except ValueError:
            print("De keuze dat u heeft gemaakt is niet mogelijk, probeer het nog eens.")


def main():
    done = False
    while not done:
        type_user = user_credentials()
        if type_user is 0:
            done = True
        else:
            use_apps = SPA(type_user)
            while not use_apps.done_with_app:
                use_apps.app_choice()


if __name__ == "__main__":
    main()
