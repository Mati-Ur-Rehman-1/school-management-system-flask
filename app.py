from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash

import database

app = Flask(__name__)
app.secret_key = "any_random_secret_key"


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        database.create_user(username, email, password)
        flash("Account created! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = database.get_user_by_email(email)

        if user is None:
            flash("Email not found", "danger")
            return redirect(url_for("login"))

        # user[3] = password hash from DB
        if not check_password_hash(user[3], password):
            flash("Incorrect password!", "danger")
            return redirect(url_for("login"))

        # Save user in session
        session["user_id"] = user[0]
        session["username"] = user[1]

        return redirect(url_for("home"))

    return render_template("login.html")


database.create_table()



@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    students = database.get_all_students()
    return render_template("home.html", students=students, username=session["username"])


@app.route("/insert", methods=["GET", "POST"])
def insert():
    if request.method == "POST":
        roll_no = request.form["roll_no"]
        name = request.form["name"]
        f_name = request.form["f_name"]
        class_name = request.form["class_name"]
        subject = request.form["subject"]
        grade = request.form["grade"]

        database.insert_student(roll_no, name, f_name, class_name, subject, grade)
        return redirect(url_for("view_students"))

    return render_template("insert.html")


@app.route("/view")
def view_students():
    page = request.args.get('page', 1, type=int)
    per_page = 20


    all_students = database.get_all_students()


    total_records = len(all_students)
    total_pages = (total_records + per_page - 1) // per_page


    start = (page - 1) * per_page
    end = start + per_page
    students = all_students[start:end]


    unique_classes = sorted(list({s[3] for s in all_students}))

    return render_template(
        "view.html",
        students=students,
        page=page,
        total_pages=total_pages,
        unique_classes=unique_classes
    )




@app.route("/update/<roll_no>", methods=["GET", "POST"])
def update(roll_no):
    student = database.get_student(roll_no)

    if request.method == "POST":
        name = request.form["name"]
        f_name = request.form["f_name"]
        class_name = request.form["class_name"]
        subject = request.form["subject"]
        grade = request.form["grade"]

        database.update_student(roll_no, name, f_name, class_name, subject, grade)
        return redirect(url_for("view_students"))

    return render_template("update.html", student=student)


@app.route("/delete/<roll_no>")
def delete(roll_no):
    database.delete_student(roll_no)
    return redirect(url_for("view_students"))



@app.route("/filter/<class_name>")
def filter_class(class_name):
    page = request.args.get("page", 1, type=int)
    per_page = 10

    offset = (page - 1) * per_page

    students = database.filter_class_paginated(class_name, offset, per_page)
    total_filtered = database.count_students_filtered(class_name)
    total_pages = (total_filtered + per_page - 1) // per_page

    unique_classes = database.get_unique_classes()

    return render_template(
        "view.html",
        students=students,
        unique_classes=unique_classes,
        filtered_class=class_name,
        current_page=page,
        total_pages=total_pages
    )





@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)


