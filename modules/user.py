import sqlite3

DB_FILE_NAME = "data.db"

class User():
    def __init__(self, username , password, email, authorization):
        self.username = username  
        self.password = password
        self.email = email
        self.authorization = authorization

    def __str__(self):
        return(f"{self.username}, {self.password}, {self.email}, {self.authorization}")
                   
    def __repr__(self):
        return self.__str__()

class Users():
    def __init__(self):
        self.users_obj = []
        self.users = []
        self.default_settings()
        self.create_users()
        self.register_code()
        self.teacher_code
        self.student_code

    def default_settings(self):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            mycursor.execute("CREATE TABLE IF NOT EXISTS \
            users(username TEXT UNIQUE, \
            password TEXT NOT NULL, \
            email TEXT UNIQUE, \
            authorization NOT NULL, \
            CONSTRAINT My_Check CHECK(username !='' \
            AND password !='' \
            AND email !='' \
            AND authorization != 'Select'))")
            mycursor.execute("INSERT OR IGNORE INTO users VALUES ('manager', '1234', 'manager@manager.com', 'master')") 
            conn.commit() 
            mycursor.execute("CREATE TABLE IF NOT EXISTS registration(authorization UNIQUE, code UNIQUE)")
            mycursor.execute("INSERT OR IGNORE INTO registration VALUES ('student', '1111'), ('teacher', '2222')")
            conn.commit()              

    def create_users(self):
        self.users_obj = []
        self.users = []
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            users_data = [u for u in mycursor.execute("SELECT * FROM users")]
            for u in users_data:
                self.users_obj.append(User(username = u[0], password = u[1], email = u[2], authorization = u[3]))
            for u in self.users_obj:
                self.users.append((u.username, u.password, u.email, u.authorization))
        return self.users

    def register_code(self):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            self.teacher_code = mycursor.execute("SELECT code FROM registration WHERE authorization = 'teacher'").fetchall()[0][0]
            self.student_code = mycursor.execute("SELECT code FROM registration WHERE authorization = 'student'").fetchall()[0][0]

    def registeration(self, username, password, email, reg_code):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            if reg_code == self.teacher_code:
                mycursor.execute(f"INSERT INTO users VALUES ('{username}', '{password}', '{email}', 'teacher')")
                conn.commit()
                self.create_users()
                return "successfully.html", username
            elif reg_code == self.student_code:
                mycursor.execute(f"INSERT INTO users VALUES ('{username}', '{password}', '{email}', 'student')")
                conn.commit()
                self.create_users()
                return "successfully.html", username    
            else:
                error = "Please make sure all fields are filled in correctly."
                return "register.html", error          
    
    def set_registration_code(self, set_code, authorization):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            mycursor.execute(f"UPDATE registration SET code = '{set_code}' WHERE authorization = '{authorization}'") 
            conn.commit()  

    def add(self, username, password, email, authorization):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            mycursor.execute(f"INSERT INTO users VALUES ('{username}', '{password}', '{email}', '{authorization}')")
            conn.commit()    

    def edit(self, new_user, new_pass, new_email, new_authorization, user_name):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            mycursor.execute(f"UPDATE users SET username = '{new_user}', password = '{new_pass}', email = '{new_email}', authorization = '{new_authorization}' WHERE username = '{user_name}'")
            conn.commit()

    def user_login(self, username, password):
        for u,p,e,a in self.users:
            if username == u and password == p and a == "master":
                return "manager", e
            elif username == u and password == p and a == "teacher":
                return "teacher", e     
            elif username == u and password == p and a == "student":
                return "students", e
        else: 
            return None

    def delete(self, username):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            mycursor.execute(f"DELETE FROM users WHERE username = '{username}'")
            conn.commit()

    def delete_all(self):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()  
            mycursor.execute("DELETE FROM users")
            conn.commit()

    def sorting(self, sort_by):
        self.create_users()
        if sort_by == "Name":
            users = sorted(self.users, key = lambda x: x[0])
        elif sort_by == "Authorization":
            users = sorted(self.users, key = lambda x: x[3])
        else:
            None  
        return users





