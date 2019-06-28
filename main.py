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
        self.options = {1: {1: self.get_courses,
                            0: self.quit},
                        2: {0: self.quit},
                        3: {0: self.quit}}

    def get_choices(self):
        if self.user_type is 1:
            self.choices = {1: "Mogelijke keuzevakken",
                            0: "Uitloggen"}
        elif self.user_type is 2:
            self.choices = {0: "Uitloggen"}
        elif self.user_type is 3:
            self.choices = {0: "Uitloggen"}

    def start_option(self):
        self.get_choices()
        print("\nKies een van de onderstaande opties.")
        choice = choice_menu(self.choices)
        option = self.options[self.user_type].get(choice)
        option()

    def get_courses(self):
        period = (self.user.student.get('Period'))
        year = (self.user.student.get('Year'))
        print("\nBekijk hieronder je beschikbare vakken voor elk blok.")
        while period != 5:
            query = "SELECT course_id, course_name FROM COURSES WHERE(period = ? OR period is NULL) AND year = ?"
            courses = self.data.execute_query(query, period, year)
            print("\n## Blok", period, "##")
            for course in courses:
                print('{:8}{:35}'.format(course[0], course[1]))
            period += 1

    def quit(self):
        self.done = True


class Login:
    def __init__(self, database):
        self.data = database
        self.type = None
        self.student = None
        self.exit = False
        self.choose_type()
        super().__init__()

    def choose_type(self):
        choices = {1: "Student",
                   2: "SLB'er",
                   3: "Examencommissie",
                   0: "Programma afsluiten"}
        print("\nKies een van de onderstaande opties.")
        choice = choice_menu(choices)
        if choice is 1:
            self.type = choice
            self.choose_student()
        else:
            self.type = choice

    def choose_student(self):
        query = "SELECT surname, last_name FROM STUDENTS"
        students = self.data.execute_query(query)
        choices = {}
        n = 1
        print("\nWat is je naam?")
        for student in students:
            choices.update({n: student[0] + ' ' + student[1]})
            n += 1
        choice = choice_menu(choices)
        self.get_student_info(choice)

    def get_student_info(self, student_id):
        query = "SELECT * FROM STUDENTS WHERE student_id = ?"
        student = self.data.execute_query(query, student_id)
        student = student[0]
        self.student = {'Name': student[1] + ' ' + student[2],
                        'Year': int(student[3]),
                        'Period': int(student[4]),
                        'SLB': int(student[5])}


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
                print("\nDat is geen geldige keuze. Probeer het opnieuw.")
        except ValueError:
            print("\nDat is geen geldige keuze. Probeer het opnieuw.")


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
