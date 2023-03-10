import statistics, sqlite3
from modules.student import Students

DB_FILE_NAME = "data.db"

class Course():
    def __init__(self, name, teacher_name, teacher_email, students_number, average_grade, passed_percentage):
        self.name = name  
        self.teacher_name = teacher_name
        self.teacher_email = teacher_email
        self.students_number = students_number
        self.average_grade = average_grade
        self.passed_percentage = passed_percentage

    def __str__(self):
        return(f"{self.name}, {self.teacher_name}, {self.teacher_email}, {self.students_number}, {self.average_grade}, {self.passed_percentage}")
                   
    def __repr__(self):
        return self.__str__()

class Courses():
    def __init__(self):
        self.courses_obj = []
        self.courses = []
        student_data = Students()
        self.students = student_data.students_obj
        self.create_courses_table()
        self.create_courses()
        self.course_members = self.courses_members()        
        self.course_statistics = self.merge_dictionary(self.number_each_course(), self.average_grade(), self.passed_percentage())
        self.most_popular_course = self.most_popular()
        
    def create_courses_table(self):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            mycursor.execute("CREATE TABLE IF NOT EXISTS \
            courses(CourseName TEXT UNIQUE, \
            TeacherName TEXT NOT NULL, \
            TeacherEmail TEXT NOT NULL, \
            StudentsNumber INTEGER NOT NULL, \
            AverageGrade INTEGER NOT NULL, \
            PassedPercentage INTEGER NOT NULL, \
            CONSTRAINT MY_Check CHECK(CourseName !='' \
            AND TeacherName !='' \
            AND TeacherEmail !='' \
            AND StudentsNumber >= 0 \
            AND AverageGrade >= 0 AND AverageGrade <= 100 \
            AND PassedPercentage >= 0 AND PassedPercentage <= 100))")

    def create_courses(self):
        self.courses_obj = []
        self.courses = []
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            courses_data = [c for c in mycursor.execute("SELECT * FROM courses")]
            for c in courses_data:
                self.courses_obj.append(Course(name = c[0], teacher_name = c[1], teacher_email = c[2], students_number = c[3], average_grade = c[4], passed_percentage = c[5]))
            for c in self.courses_obj:
                self.courses.append((c.name, c.teacher_name, c.teacher_email, c.students_number, c.average_grade, c.passed_percentage))
        return self.courses 

    def add(self, course_data):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            mycursor.execute(f"INSERT INTO courses VALUES \
            ('{course_data['course_name']}', '{course_data['teacher_name']}', '{course_data['teacher_email']}', 0, 0, 0)")   
            conn.commit() 

    def edit(self, new_teacher_name, new_taecher_email, course_name):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            mycursor.execute(f"UPDATE courses SET TeacherName = '{new_teacher_name}', TeacherEmail = '{new_taecher_email}' WHERE CourseName = '{course_name}'")
            conn.commit()

    def delete(self, course_name):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            mycursor.execute(f"DELETE FROM courses WHERE CourseName = '{course_name}'")
            conn.commit()

    def delete_all(self):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()  
            mycursor.execute("DELETE FROM courses") 

    def sorting(self, sort_by):
        self.create_courses()
        if sort_by == "Name":
            courses = sorted(self.courses, key = lambda x: x[0], reverse=False)
        elif sort_by == "Number↑":
            courses = sorted(self.courses, key = lambda x: x[3], reverse=True)
        elif sort_by == "Number↓":
            courses = sorted(self.courses, key = lambda x: x[3], reverse=False)     
        elif sort_by == "Grade↑":
            courses = sorted(self.courses, key = lambda x: x[4], reverse=True)
        elif sort_by == "Grade↓":
            courses = sorted(self.courses, key = lambda x: x[4], reverse=False)
        elif sort_by == "Passed↑":
            courses = sorted(self.courses, key = lambda x: x[5], reverse=True)
        elif sort_by == "Passed↓":
            courses = sorted(self.courses, key = lambda x: x[5], reverse=False)       
        else:
            None      
        return courses

    def update_courses(self, course_name, column, val):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            mycursor.execute(f"UPDATE courses SET '{column}' = '{val}' WHERE CourseName = '{course_name}'")
            conn.commit()

    def courses_members(self):
        course_members = {}  
        for student1 in self.students:
            names = []
            for student2 in self.students:
                if student1.course == student2.course:
                   names.append(student2.name) 
            course_members[student1.course] = (names)      
        return dict(sorted(course_members.items()))   
    
    def course_grades(self):
        course_grades = {}
        for student1 in self.students:
            grades = []
            for student2 in self.students:
                if student1.course == student2.course:
                   grades.append(int(student2.grade)) 
            course_grades[student1.course] = (grades)   
        return course_grades

    def average_grade(self):
        average_grade = {}
        for c,g in self.course_grades().items():
            average_grade[c] = round(statistics.mean(g), 2)
            self.update_courses(c, 'AverageGrade', round(statistics.mean(g), 2))        
        return dict(sorted(average_grade.items(), key = lambda x:x[1])) 

    def number_each_course(self):
        number_course = {}       
        for c,n in self.course_members.items():
            number_course[c] = len(n)
            self.update_courses(c, 'StudentsNumber', len(n))
        return dict(sorted(number_course.items(), key = lambda x:x[1])) 

    def passed_percentage(self): 
        passed = {}      
        for k,v in self.course_grades().items():
            val = v
            yes = no = 0
            for n in val:             
                if n >= 60:
                    yes += 1
                else:
                    no += 1
            passed[k] = round((yes/(yes+no)*100), 2)
            self.update_courses(k, 'PassedPercentage', round((yes/(yes+no)*100), 2))
        return passed
               
    def merge_dictionary(self, dict_1, dict_2, dict_3):
        total = {**dict_1, **dict_2, **dict_3}   
        for k,v in total.items():
            if k in dict_1 and k in dict_2 and k in dict_3:
                total[k] = [dict_1[k], dict_2[k], dict_3[k]]
        return total   

    def most_popular(self):
        try:
            for k1,v1 in self.number_each_course().items():
                for k1,v2 in self.number_each_course().items():
                    if v1>v2:
                        v = v1
                    elif v2>v1:
                        v = v2
                    else:
                        None
            return [key for key,value in self.number_each_course().items() if value == v][0]
        except:
            return ""

    def check_courses(self, email):
        courses_list = []
        for c in self.courses_obj:
            if c.teacher_email == email:
                courses_list.append(c.name)
            else:
                None
        return courses_list