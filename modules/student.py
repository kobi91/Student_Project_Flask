import sqlite3

DB_FILE_NAME = "data.db"

class Student():
    def __init__(self, name, age, id_, address, phone, email, course, grade, missing):
        self.name = name   
        self.age = age
        self.id_ = id_
        self.address = address
        self.phone = phone
        self.email = email
        self.course = course
        self.grade = grade
        self.missing = missing

    def __str__(self):
        return(f"{self.name}, {self.age}, {self.id_}, {self.address}, {self.phone}, {self.email}, {self.course}, {self.grade}, {self.missing}")
                   
    def __repr__(self):
        return self.__str__()

class Students():
    def __init__(self):
        self.students_obj = []
        self.students = []
        self.students_list = []
        self.create_students_table()
        self.create_students()
        self.list_of_students()
        self.update_missing()

    def create_students_table(self):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            mycursor.execute("CREATE TABLE IF NOT EXISTS \
            students(StudentName TEXT UNIQUE, \
            Age INTEGER NOT NULL, \
            ID TEXT UNIQUE, \
            Address TEXT NOT NULL, \
            Phone TEXT UNIQUE, \
            Email TEXT UNIQUE, \
            Course TEXT NOT NULL, \
            Grade INTEGER, \
            MissingLessons INTEGER, \
            CONSTRAINT my_Check CHECK(StudentName !='' \
            AND Age !='' AND Age > 20 AND Age < 60 \
            AND ID !='' \
            AND Address !='' \
            AND Phone !='' \
            AND Email !='' \
            AND Course !='' AND Course != 'Select' \
            AND Grade >= 0 AND Grade <= 100 \
            AND MissingLessons >= 0))")
                 
    def create_students(self):
        self.students_obj = []
        self.students = []
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            students_data = [s for s in mycursor.execute("SELECT * FROM students")]
            for s in students_data:
                self.students_obj.append(Student(name = s[0], age = s[1], id_ = s[2], address = s[3], phone = s[4], email = s[5], course = s[6], grade = s[7], missing = s[8]))
            for s in self.students_obj:
                self.students.append((s.name, s.age, s.id_, s.address, s.phone, s.email, s.course, s.grade, s.missing))
        return self.students

    def list_of_students(self):
        temp_list = []
        for student in self.students_obj:
            temp_list.append(student.name)
            self.students_list = sorted(temp_list) 
        return self.students_list  

    def add(self, student_data):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            mycursor.execute(f"INSERT INTO students VALUES \
            ('{student_data['name']}', '{student_data['age']}', '{student_data['id_']}',\
            '{student_data['address']}', '{student_data['phone']}', '{student_data['email']}',\
            '{student_data['course']}', 0, 0)")   
            conn.commit() 
       
    def update_grade(self, updated_grade, id_num):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            mycursor.execute(f"UPDATE students SET Grade = '{updated_grade}' WHERE ID = '{id_num}'")
            conn.commit()
    
    def update_missing(self):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            attendance_data = [a for a in mycursor.execute("SELECT * FROM attendance")]
            for student in attendance_data:
                updated_missing = 0
                for val in student:
                    if val == "Yes":
                        updated_missing += 1
                    mycursor.execute(f"UPDATE students SET MissingLessons = '{updated_missing}' WHERE StudentName = '{student[0]}'")
                    conn.commit()
            else:
                None

    def delete(self, student_id):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            mycursor.execute(f"DELETE FROM students WHERE ID = '{student_id}'")
            conn.commit()

    def delete_all(self):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()  
            mycursor.execute("DELETE FROM students")
            conn.commit()

    def sorting(self, sort_by):
        self.create_students()
        if sort_by == "Name":
            students = sorted(self.students, key = lambda x: x[0], reverse=False)
        elif sort_by == "Grade↑":
            students = sorted(self.students, key = lambda x: x[7], reverse=True)
        elif sort_by == "Grade↓":
            students = sorted(self.students, key = lambda x: x[7], reverse=False)
        elif sort_by == "Course":
            students = sorted(self.students, key = lambda x: x[6], reverse=False)  
        else:
            None      
        return students
    
    def student_attendance(self, date, attendance, student_name):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            student_course = [s.course for s in self.students_obj if s.name == student_name][0]
            mycursor.execute("CREATE TABLE IF NOT EXISTS attendance(StudentName TEXT UNIQUE, Course TEXT NOT NULL)")
            conn.commit()
            columns = [c[1] for c in mycursor.execute("PRAGMA table_info(attendance)")]
            if date not in columns:
                mycursor.execute(f"ALTER TABLE attendance ADD COLUMN '{date}' TEXT")
                conn.commit()
            else:
                None
            mycursor.execute(f"INSERT OR IGNORE INTO attendance (StudentName, Course) VALUES ('{student_name}', '{student_course}')")
            conn.commit()
            mycursor.execute(f"UPDATE attendance SET '{date}' = '{attendance}' WHERE StudentName = '{student_name}'")
            conn.commit()
            
    def create_attendance_list(self, teacher_courses, selected_date):
        if selected_date != "Select":
            with sqlite3.connect(DB_FILE_NAME) as conn:
                mycursor = conn.cursor()
                attendance_list = [a for a in mycursor.execute(f'SELECT StudentName, Course, "{selected_date}" FROM attendance WHERE "{selected_date}" IS NOT NULL') if a[1] in teacher_courses]
            return sorted(attendance_list, key = lambda x: x[1])
        else:
            return []
            
    def delete_attendance_list(self, selected_date):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            mycursor.execute(f'ALTER TABLE attendance DROP COLUMN "{selected_date}"')
            conn.commit()
        
    def get_dates(self):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            dates = [c[1] for c in mycursor.execute("PRAGMA table_info(attendance)") if c[1] not in ['StudentName', 'Course']]
        return dates

