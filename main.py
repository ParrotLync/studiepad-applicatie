# Casusgroep 12 - Alain Lardinois & Peter Roijen
import sqlite3
import os
import time


class SqliteDBConnection:
    def __init__(self):
        self.database_path = os.path.join(os.path.dirname('__file__'), 'spa_data.db')
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()

    def execute_query(self, input_query, *arg):
        self.cursor.execute(input_query, arg)
        return self.cursor.fetchall()

    def modify_value(self, modify_value_query, *arg):
        self.cursor.execute(modify_value_query, arg)
        self.connection.commit()


class SPA:
    def __init__(self, database, user):
        self.user = user
        self.data = database
        self.done = False
        self.student_info = None
        self.user_type = user.type
        self.choices = {}
        self.options = {1: {1: self.student_see_sp,
                            2: self.student_change_sp,
                            0: self.quit},
                        2: {1: self.slb_list_sp,
                            2: self.assess_sp,
                            3: 'self.generate_report',
                            0: self.quit}}

    def get_choices(self):
        if self.user_type is 1:
            self.choices = {1: "Bekijk je huidige studiepad",
                            2: "Werk je studiepad bij.",
                            0: "Uitloggen"}
        elif self.user_type is 2:
            self.choices = {1: "Bekijk de studiepaden van je studenten.",
                            2: "Studiepaden af- en goedkeuren.",
                            3: "Genereer een rapport met de studiepaden van je studenten.",
                            0: "Uitloggen"}

    def start_option(self):
        if self.user_type is 1:
            self.check_path(self.user.student.get('ID'))
        self.get_choices()
        message("header", "\nKies een van de onderstaande opties.")
        choice = choice_menu(self.choices)
        option = self.options[self.user_type].get(choice)
        option()

    def student_see_sp(self):
        self.user.get_student_info(self.user.student.get('ID'))
        period = self.user.student.get('Period')
        year = self.user.student.get('Year') + 1
        profile = self.user.student.get('Profile')
        if year != 1 and profile is 1:
            message("warning", "\n[!] Je hebt nog geen profiel gekozen! Kies eerst je studiepad en kom dan terug.")
        else:
            while period != 5:
                studiepunten = 0
                query = "SELECT course_id, course_name, amount_ec FROM COURSES WHERE (profile = ? OR profile = 1) AND (period = ? OR period is NULL) AND year = ?"
                courses = self.data.execute_query(query, profile, period, year)
                print("\n## Blok", period, "##")
                for course in courses:
                    print('{:8}{:35}{:5}{:20}'.format(course[0], course[1], course[2], ' studiepunten'))
                    studiepunten += int(course[2])
                msg = "Totaal aantal studiepunten: " + str(studiepunten)
                message("note", msg)
                period += 1

    def student_change_sp(self):
        year = self.user.student.get('Year') + 1
        if year is 2:
            choices = {1: "IT Services",
                       2: "IT Development",
                       3: "Business Intelligence"}
            message("header", "\nKies een profiel.")
            choice = choice_menu(choices) + 1
            year2_profile_query = "UPDATE STUDENT_PROFILE_CHOICE SET profile_id = ? WHERE student_id = ?"
            self.data.modify_value(year2_profile_query, choice, self.user.student.get('ID'))
            herkansingen = []
            herkansingen_done = False
            print("\nMoet je nog vakken opnieuw volgen? Vul dan de vakcode in (bijv. B1A03)")
            print("Indien dit niet nodig is, vul dan 'n' in.")
            while not herkansingen_done:
                # Herkansingen worden nog niet meegenomen in het studieplan
                try:
                    herkansing = (input(">> "))
                    if herkansing == 'n':
                        herkansingen_done = True
                    else:
                        herkansingen.append(herkansing)
                except ValueError:
                    message("warning", "\n[!] Dat is geen geldige keuze. Probeer het opnieuw.")
            message("note", "\nEen ogenblik geduld alstublieft, je studiepad wordt ingestuurd...")
            time.sleep(2)

    def check_path(self, student_id):
        # TODO: Add database connection to get status
        self.user.get_student_info(student_id)
        year = self.user.student.get('Year') + 1
        profile = self.user.student.get('Profile')
        query = "SELECT path_approved_by_slber FROM STUDY_PATHS WHERE student_id is ?"
        goedgekeurd = data.execute_query(query, student_id)
        goedgekeurd = int(goedgekeurd[0][0])
        status = None
        if year is 1 and goedgekeurd is 1:
            status = 3
        if year is 1 and goedgekeurd is 0:
            status = 2
        if year is 2 and profile is 1 and goedgekeurd is 0:
            status = 1
        elif year is 2 and profile != 1 and goedgekeurd is 0:
            status = 2
        elif year is 2 and profile != 1 and goedgekeurd is 1:
            status = 3

        if status is 1:
            message("error", "\n✘ Je studiepad is nog niet ingevuld")
            message("error", "✘ Je studiepad is nog niet goedgekeurd")
            return False
        elif status is 2:
            message("success", "\n✔ Je studiepad is ingevuld.")
            message("error", "✘ Je studiepad is nog niet goedgekeurd")
            return False
        elif status is 3:
            message("success", "\n✔ Je studiepad is ingevuld.")
            message("success", "✔ Je studiepad is goedgekeurd.")
            return True

    def slb_list_sp(self):
        # TODO: Finish function
        students = self.user.slb.get('Students')
        print(students)

    def assess_sp(self):
        # TODO: Finish function
        self.choose_student()
        approved = None
        choices = {1: 'Studiepad goedkeuren',
                   2: 'Studiepad afkeuren'}
        message("header", "\nKies aan actie.")
        choice = choice_menu(choices)
        if choice is 1:
            approved = True
        elif choice is 2:
            approved = False
        update_query = "UPDATE STUDY_PATHS SET path_approved_by_slber = ? WHERE student_id = ?"
        self.data.modify_value(update_query, approved, self.user.student.get('ID'))
        message("note", "\nEen ogenblik geduld alstublieft, het studiepad wordt bijgewerkt...")
        time.sleep(2)

    def choose_student(self):
        query = "SELECT surname, last_name FROM STUDENTS WHERE SLB_ID = ?"
        students = self.data.execute_query(query, self.user.slb.get('ID'))
        student_choices = {}
        n = 1
        message("header", "\nKies een student.")
        for student in students:
            student_choices.update({n: student[0] + ' ' + student[1]})
            n += 1
        student_id = choice_menu(student_choices)
        self.student_info = self.user.get_student_info(student_id)

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
                   0: "Programma afsluiten"}
        message("header", "\nKies een van de onderstaande opties.")
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
        message("header", "\nWat is je naam?")
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
        subquery = "SELECT profile_id FROM STUDENT_PROFILE_CHOICE WHERE student_id = ?"
        student = self.data.execute_query(query, student_id)
        profile = self.data.execute_query(subquery, student_id)
        profile = str(profile[0])[1]
        student = student[0]
        self.student = {'Name': student[1] + ' ' + student[2],
                        'Year': int(student[3]),
                        'Period': int(student[4]),
                        'SLB': int(student[5]),
                        'ID': int(student[0]),
                        'Profile': int(profile)}

    def get_slb_info(self, slb_id):
        query = "SELECT * FROM TEACHERS WHERE teacher_id = ?"
        subquery = "SELECT student_id FROM STUDENTS where slb_id = ?"
        slb = self.data.execute_query(query, slb_id)
        slb_students = self.data.execute_query(subquery, slb_id)
        slb = slb[0]
        slb_students = [int(str(slb_students[0])[1]), int(str(slb_students[1])[1])]
        self.slb = {'Name': slb[1] + ' ' + slb[2],
                    'Students': slb_students,
                    'ID': int(slb[0])}


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
                message("warning", "[!] Dat is geen geldige keuze. Probeer het opnieuw.")
        except ValueError:
            message("warning", "[!] Dat is geen geldige keuze. Probeer het opnieuw.")


def message(msg_type, msg):
    types = {'warning': '\033[1;31m',
             'error': '\033[31m',
             'success': '\033[32m',
             'header': '\033[34m',
             'note': '\033[36m'}
    print(types.get(msg_type) + msg + '\033[0;0m')


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
    data.connection.close()
