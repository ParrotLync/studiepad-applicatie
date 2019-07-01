# Casusgroep 12 - Alain Lardinois & Peter Roijen
import sqlite3
import os


class SqliteDBConnection:
    def __init__(self):
        self.database_path = os.path.join(os.path.dirname('__file__'), 'spa_data.db')
        self.connect_to_db = sqlite3.connect(self.database_path)
        self.cursor = self.connect_to_db.cursor()

    def execute_query(self, input_query, *arg):
        self.cursor.execute(input_query, arg)
        return self.cursor.fetchall()

    def modify_table_values(self, modify_value_query, *arg):
        self.cursor.execute(modify_value_query, arg)


class SPA:
    def __init__(self, database, user):
        self.user = user
        self.data = database
        self.done = False
        self.user_type = user.type
        self.choices = {}
        self.options = {1: {1: self.student_get_all_courses,
                            2: self.change_sp,
                            3: self.student_get_sp,
                            0: self.quit},
                        2: {1: self.list_sp,
                            2: self.assess_sp,
                            3: self.generate_report,
                            0: self.quit},
                        3: {1: self.list_sp,
                            2: self.assess_sp,
                            3: self.change_sp,
                            4: self.generate_report,
                            0: self.quit}}

    def get_choices(self):
        if self.user_type is 1:
            self.choices = {1: "Bekijk alle beschikbare vakken per leerjaar.",
                            2: "Kies je studiepad per leerjaar",
                            3: "Bekijk een overzicht van je studiepad",
                            0: "Uitloggen"}
        elif self.user_type is 2:
            self.choices = {1: "Bekijk de studiepaden van je studenten.",
                            2: "Studiepaden af- en goedkeuren.",
                            3: "Genereer een rapport met de studiepaden van je studenten.",
                            0: "Uitloggen"}
        elif self.user_type is 3:
            self.choices = {1: "Bekijk alle studiepaden per student",
                            2: "Studiepaden af- en goedkeuren.",
                            3: "Studiepaden aanpassen.",
                            4: "Genereer een rapport.",
                            0: "Uitloggen"}

    def start_option(self):
        self.get_choices()
        message("Kies een van de onderstaande opties.")
        choice = choice_menu(self.choices)
        option = self.options[self.user_type].get(choice)
        option()

    def student_get_all_courses(self)
        # TODO: Kijken of we volgende leerjaar doen of gewoon kiezen per leerjaar
        period = self.user.student.get('Period')
        year_choice = False
        year = 0
        while not year_choice:
            try:
                year = int(input("Kies een leerjaar (1/2/3/4): "))
                if 1 <= year <= 4:
                    year_choice = True
                else:
                    warning("Dat is geen geldige keuze. Probeer het opnieuw.")
            except ValueError:
                warning("Dat is geen geldige keuze. Probeer het opnieuw.")

        message("Bekijk hieronder je beschikbare vakken voor elk blok.")
        while period != 5:
            query = "SELECT course_id, course_name FROM COURSES WHERE(period = ? OR period is NULL) AND year = ?"
            courses = self.data.execute_query(query, period, year)
            print("\n## Blok", period, "##")
            for course in courses:
                print('{:8}{:35}'.format(course[0], course[1]))
            period += 1

    def slb_list_sp(self):
        # TODO: Finish function
        students = self.user.slb.get('Students')
        print(students)

    def quit(self):
        self.done = True


class Login:
    def __init__(self, database):
        self.data = database
        self.type = None
        self.student = None
        self.slb = None
        self.exit = False
        self.choose_type()

    def choose_type(self):
        choices = {1: "Student",
                   2: "SLB'er",
                   3: "Examencommissie",
                   0: "Programma afsluiten"}
        message("Kies een van de onderstaande opties.")
        choice = choice_menu(choices)
        if choice is 1:
            self.type = choice
            self.choose_user()
        elif choice is 2:
            self.type = choice
            self.choose_user()
        else:
            self.type = choice

    def choose_user(self):
        if self.type is 1:
            query = "SELECT surname, last_name FROM STUDENTS"
        elif self.type is 2:
            query = "SELECT surname, last_name from TEACHERS"
        users = self.data.execute_query(query)
        choices = {}
        n = 1
        message("Wat is je naam?")
        for user in users:
            choices.update({n: user[0] + ' ' + user[1]})
            n += 1
        choice = choice_menu(choices)
        if self.type is 1:
            self.get_student_info(choice)
        elif self.type is 2:
            self.get_slb_info(choice)

    def get_student_info(self, student_id):
        query = "SELECT * FROM STUDENTS WHERE student_id = ?"
        student = self.data.execute_query(query, student_id)
        student = student[0]
        self.student = {'Name': student[1] + ' ' + student[2],
                        'Year': int(student[3]),
                        'Period': int(student[4]),
                        'SLB': int(student[5]),
                        'ID': int(student[0])}

    def get_slb_info(self, slb_id):
        query = "SELECT * FROM TEACHERS WHERE teacher_id = ?"
        subquery = "SELECT student_id FROM STUDENTS where slb_id = ?"
        slb = self.data.execute_query(query, slb_id)
        slb_students = self.data.execute_query(subquery, slb_id)
        slb = slb[0]
        slb_students = [int(str(slb_students[0])[1]), int(str(slb_students[1])[1])]
        self.slb = {'Name': slb[1] + ' ' + slb[2],
                    'Students': slb_students}


def choice_menu(choices):
    valid_choice = False
    while not valid_choice:
        for x in choices:
            print(str(x) + '.', choices.get(x))
        try:
            choice = int(input(">> "))
            if choice in choices:
                return choice
            else:
                warning("Dat is geen geldige keuze. Probeer het opnieuw.")
        except ValueError:
            warning("Dat is geen geldige keuze. Probeer het opnieuw.")


def warning(msg):
    msg = '[!] ' + msg
    print('\n' + '\033[1;31m' + msg + '\033[37m')


def message(msg):
    print('\n' + '\033[1;32m' + msg + '\033[37m')


if __name__ == "__main__":
    data = SqliteDBConnection()
    done = False
    while not done:
        login = Login(data)
        if login.type is 0:
            done = True
        else:
            app = SPA(data, login)
            while not app.done:
                app.start_option()
