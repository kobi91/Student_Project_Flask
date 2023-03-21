from flask import Flask, redirect, url_for, render_template, request, make_response, session, abort, flash, jsonify
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
import sqlite3
from datetime import datetime
from modules.user import Users
from modules.student import Students
from modules.course import Courses
from modules.home import HomePage

app = Flask(__name__)
app.secret_key = 'kobitamam'

DB_FILE_NAME = "data.db"

today = datetime.today().strftime('%d-%m-%Y')

unauthorized_paths = ["home_messages", "home", "search", "attendance_table", "show_course", "students_table", "courses_table", "statistics_table", "about", "login", "user_login", "register", "successfully_reg", "static"]


#------------------ H O M E  W E B ---------------------#  

@app.route("/messages")
def home_messages():
    messages = [s[1] for s in home_page.messages]
    return messages

@app.route("/")
def home():
    course = Courses()
    return render_template("home.html", most_popular_course = course.most_popular_course)

@app.route("/students_list")
def students_table():
    student = Students()
    return render_template("students_table.html", students_list = student.students_list)

@app.route("/courses")
def courses_table():
    course = Courses()  
    return render_template("courses_table.html", course_members = course.course_members, courses = course.courses)     

@app.route("/statistics")
def statistics_table():
    course = Courses()  
    return render_template("statistics_table.html", course_statistics = course.course_statistics)   

@app.route("/about")
def about():  
    return render_template("about.html")

@app.route("/courses/<name>")
def show_course(name):
    course = Courses() 
    student_name = None
    for k,v in course.course_members.items():
        if name in v:
           student_name = v[0].title()
           name = k
    course_details = [c for c in course.courses if c[0] == name or c[1] == name]
    return render_template("show_course.html", course_details = course_details, student_name = student_name)

@app.route("/search", methods = ["POST"])
def search():
    search_value = request.form["search"]
    courses_checkbox = request.form.get("courses_check")
    teachers_checkbox = request.form.get("teachers_check")
    students_checkbox = request.form.get("students_check")
    if search_value != "":
        courses_list, students_list, teacher_list = home_page.search(courses_checkbox, teachers_checkbox, students_checkbox, search_value)
    else:
        return redirect(url_for('home'))    
    return render_template("search.html", courses = courses_list, students = students_list, teachers = teacher_list, search_value = search_value)


#--------------- L O G I N / L O G O U T ---------------#

@app.route("/login", methods = ["POST", "GET"])
def login():
    error = None
    user.create_users()
    if request.method=='POST':
        username = request.form["username"]
        password = request.form["password"]
        try:
            global teacher_courses
            global student_email     
            route, email = user.user_login(username, password)
            student_email = email
            teacher_courses = course.check_courses(email)
            session['username'] = username
            return redirect(url_for(route))   
        except:
            error = "Invalid username or password. Please try again!"          
    return render_template("login.html", error = error)

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

def is_logged_in():
    return 'username' in session

@app.before_request
def auth():
    if not is_logged_in() and request.endpoint not in unauthorized_paths:
        return redirect(url_for('login'))

                                                        
#-------------- R E G I S T E R A T I O N --------------#

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register/successfully", methods=["POST"])
def successfully_reg():
    error = None
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]
    reg_code = request.form["reg_code"]
    try:  
        url, val = user.registeration(username, password, email.title(), reg_code)
        user.create_users()
        return render_template(url, val = val)
    except sqlite3.Error:
        error = "Username or Email already exists. Please try again!"
        return render_template("register.html", val = error)


#-------------- M A N A G E R  P A N E L ---------------#

@app.route("/manager")
def manager():
    return render_template("manager.html")

@app.route("/manager/manage_home", methods = ["POST", "GET"])
def manage_home_page():
    if request.method=='POST':
        message = request.form["message"]
        home_page.add_message(message)
    messages = home_page.create_messages_list()      
    return render_template("manage_home.html", messages = messages)

@app.route("/manage_home/delete_message", methods = ["POST"])
def delete_message():
    message_id = request.form["message_id"]
    try:
        home_page.delete(message_id)
        return redirect(url_for('manage_home_page'))
    except:
        return redirect(url_for('manage_home_page')) 

@app.route("/manage_home/delete_messages")
def delete_messages():
    try:
        home_page.delete_all()
        return redirect(url_for('manage_home_page'))  
    except:
        return redirect(url_for('manage_home_page'))
    
@app.route("/manager/manage_users")
def manage_users(): 
    try:
        user = Users()
        return render_template("manage_users.html", users = user.users) 
    except:
        return render_template("manage_users.html")

@app.route("/manage_users/add_user", methods = ["POST"])
def add_user(): 
    username = request.form["user_name"]
    password = request.form["user_pass"]
    email = request.form["user_email"]
    authorization = request.form["authorization"]
    try:      
        user.add(username, password, email.title(), authorization)                   
        return redirect(url_for('manage_users'))           
    except sqlite3.Error as error:
        print("An error accurred:", error)
        return redirect(url_for('manage_users'))

@app.route("/manager/manage_users/edit_u", methods = ["POST"])
def edit_u():
    global user_name 
    username = request.form["user"]
    password = request.form["pass"]
    email = request.form["email"]
    authorization = request.form["authorization1"]
    user_name = username
    return render_template("edit_user.html", old_user = username, old_pass = password, old_email = email, old_authorization = authorization)

@app.route("/manage_users/edit_user", methods = ["POST"])
def edit_user():
    error = None
    new_user = request.form["new_user"]
    new_pass = request.form["new_pass"]
    new_email = request.form["new_email"]
    new_authorization = request.form["new_authorization"]
    try:              
        user.edit(new_user, new_pass, new_email.title(), new_authorization, user_name)      
        return redirect(url_for('manage_users'))                     
    except sqlite3.Error:
        error = "Please make sure all fields are filled in correctly."
        return render_template("edit_user.html", error = error)

@app.route("/manage_users/delete_user", methods = ["POST"])
def delete_user():
    username = request.form["user"]
    try:
        user.delete(username)
        return redirect(url_for('manage_users'))
    except:
        return redirect(url_for('manage_users')) 

@app.route("/manage_users/delete_users")
def delete_users():
    try:
        user.delete_all()
        return redirect(url_for('manage_users'))  
    except:
        return redirect(url_for('manage_users'))

@app.route("/manage_users/sorting_users", methods = ["POST"])
def sorting_users():
    sort_by = request.form["sortedby"]
    try:    
        return render_template("manage_users.html", users = user.sorting(sort_by))  
    except:
        return redirect(url_for('manage_users'))          

@app.route("/manager/manage_users/registration_code")
def registration_code():
    return render_template("registration_code.html")

@app.route("/manage_users/set_registration_code", methods = ["POST"])
def set_registration_code():
    choose_authorization = request.form["choose_authorization"]
    set_code = request.form["set_code"]
    try:
        user.set_registration_code(set_code, choose_authorization)
        return redirect(url_for('registration_code'))
    except sqlite3.Error as error:
        print("An error accurred:", error)
        return redirect(url_for('registration_code'))
    
@app.route("/manager/manage_students")
def manage_students():  
    try:
        student = Students()    
        return render_template("manage_students.html", students = student.students, courses = course.create_courses()) 
    except:
        return render_template("manage_students.html")

@app.route("/manage_students/add_student", methods = ["POST"])
def add_student():  
    student_data = {k:v.title() for k,v in request.form.items()}
    try:  
        student.add(student_data) 
        return redirect(url_for('manage_students'))    
    except sqlite3.Error as error:
        print("An error accurred:", error)
        return redirect(url_for('manage_students'))

@app.route("/manage_students/delete_student", methods = ["POST"])
def delete_student():
    student_id = request.form["student"]
    try:
        student.delete(student_id)
        return redirect(url_for('manage_students'))
    except:
        return redirect(url_for('manage_students'))         

@app.route("/manage_students/delete_students")
def delete_students():
    try:
        student.delete_all()
        return redirect(url_for('manage_students'))  
    except:
        return redirect(url_for('manage_students'))

@app.route("/manage_students/sorting_students", methods = ["POST"])
def manager_sorting_students():
    sort_by = request.form["sortedby"]
    try: 
        return render_template("manage_students.html", students = student.sorting(sort_by), courses = course.create_courses()) 
    except:
        return redirect(url_for('manage_students'))          

@app.route("/manager/manage_courses")
def manage_courses():   
    try:
        course = Courses()    
        return render_template("manage_courses.html", courses = course.courses) 
    except:
        return render_template("manage_courses.html") 

@app.route("/manage_courses/add_course", methods = ["POST"])
def add_course():  
    course_data = {k:v.title() for k,v in request.form.items()}
    try:  
        course.add(course_data) 
        return redirect(url_for('manage_courses'))    
    except sqlite3.Error as error:
        print("An error accurred:", error)
        return redirect(url_for('manage_courses')) 

@app.route("/manage_courses/delete_course", methods = ["POST"])
def delete_course():
    course_name = request.form["course_name"]
    try:
        course.delete(course_name)
        return redirect(url_for('manage_courses'))
    except:
        return redirect(url_for('manage_courses'))         

@app.route("/manage_courses/delete_courses")
def delete_courses():
    try:
        course.delete_all()
        return redirect(url_for('manage_courses'))  
    except:
        return redirect(url_for('manage_courses'))

@app.route("/manager/manage_courses/edit_c", methods = ["POST"])
def edit_c():
    global course_name 
    course_name = request.form["name"]
    teacher_name = request.form["teacher_name"]
    teacher_email = request.form["teacher_email"]
    return render_template("edit_course.html", course_name = course_name, old_t_name = teacher_name, old_email = teacher_email)

@app.route("/manage_courses/edit_course", methods = ["POST"])
def edit_course():
    error = None
    new_teacher_name = request.form["teacher_name"]
    new_taecher_email = request.form["teacher_email"]
    try:              
        course.edit(new_teacher_name.title(), new_taecher_email.title(), course_name.title())      
        return redirect(url_for('manage_courses'))                     
    except sqlite3.Error:
        error = "Please make sure all fields are filled in correctly."
        return render_template("edit_course.html", error = error)

@app.route("/manage_courses/sorting_courses", methods = ["POST"])
def sorting_courses():
    sort_by = request.form["sortedby"]
    try: 
        return render_template("manage_courses.html", courses = course.sorting(sort_by)) 
    except:
        return redirect(url_for('manage_courses')) 


#-------------- T E A C H E R  P A N E L ---------------#

@app.route("/teacher")
def teacher():
    try:
        student = Students()
        course = Courses()
        students = [s for s in student.students if s[6] in teacher_courses]
        course_statistics = {k:v for k,v in course.course_statistics.items() if k in teacher_courses}
        return render_template("teacher.html", students = students, course_statistics = course_statistics) 
    except:
        return render_template("teacher.html")   

@app.route("/teacher/edit_s", methods = ["POST"])
def edit_s():
    global id_num
    s_id = request.form["id"]
    s_grade = request.form["grade"]
    id_num = s_id
    return render_template("edit_student.html", s_grade = s_grade)

@app.route("/teacher/edit_student", methods = ["POST"])
def edit_student():
    error = None
    updated_grade = request.form["grade"]
    try:
        student.update_grade(updated_grade, id_num)
        return redirect(url_for('teacher'))                     
    except sqlite3.Error:
        error = "Please make sure all fields are filled in correctly."
        return render_template("edit_student.html", error = error)

@app.route("/teacher/sorting_students", methods = ["POST"])
def teacher_sorting_students():
    sort_by = request.form["sortedby"]
    try: 
        students = [s for s in student.sorting(sort_by) if s[6] in teacher_courses]
        return render_template("teacher.html", students = students) 
    except:
        return redirect(url_for('teacher'))
    
@app.route("/teacher/attendance", methods = ["POST", "GET"])
def student_attendance():
    student = Students()
    course = Courses() 
    course_members = {k:v for k,v in course.course_members.items() if k in teacher_courses}
    if request.args.get("attendance"):
        data = request.args.get("attendance").split(",")
        attendance = data[0]
        student_name = data[1] 
        student.student_attendance(today, attendance, student_name)
    return render_template("student_attendance.html", course_members = course_members, date = today)

@app.route("/teacher/attendance_list", methods = ["POST", "GET"])
def attendance_list():
    dates = student.get_dates()
    selected_date = request.args.get("date")
    if selected_date:
        attendance_list = student.create_attendance_list(teacher_courses, selected_date)
        return attendance_list
    if request.method=='POST':
        try:
            delete_date = request.get_json()
            student.delete_attendance_list(delete_date)   
            return redirect(url_for('attendance_list'))
        except:
            return redirect(url_for('attendance_list'))     
    return render_template("attendance_list.html", dates = dates)

@app.route("/teacher/course_attendance", methods = ["GET"])
def course_attendance():
    course = Courses() 
    student_list = []
    selected_course = request.args.get("course")
    if selected_course:
        student_list = course.course_members.get(selected_course)
    return student_list


#------------- S T U D E N T  P A N E L ----------------# 

@app.route("/students")
def students():
    student = Students()
    return render_template("students.html", student_statistics = [s for s in student.students if s[5] == student_email])

        
#-------------------------------------------------------#          

if __name__ == "__main__":
    user = Users()
    student = Students()
    course = Courses()
    home_page = HomePage()
    app.run(debug = True, port = 5000)
