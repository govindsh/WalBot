from flask import Flask, render_template, request, redirect, url_for, session
import os
import requests
import sqlite3 as sqllite

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("home_page.html")


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for("home_page"))


@app.route("/profile", methods=['POST', 'GET'])
def login_page():
    error = None
    login_success = False
    product_details = []
    if request.method == 'POST':
        with sqllite.connect("walbot.db") as conn:
            cursor = conn.cursor()
            cursor.execute("select email, password, fullname, id from users")
            content = cursor.fetchall()
            for row in content:
                print(row)
                print(request.form['email'])
                print(request.form['password'])
                email = str(row[0]).strip("[(',)]")
                print(email)
                name = str(row[2]).strip("[(',)]")
                print(name)
                password = str(row[1]).strip("[(',)]")
                print(password)
                if email == request.form['email'] and password == request.form['password']:
                    login_success = True
                    session['logged_in'] = True

                    # Get the user id from db
                    user_id = row[3]
                    print(user_id)

                    # Now we need to retrieve recently viewed products
                    query = "select item_id, user_id, item_status from item_status where user_id={}".format(str(user_id))
                    print(query)

                    cursor.execute(query)
                    content = cursor.fetchall()

                    for row in content:
                        product_id = str(row[0]).strip("[(',)]")
                        query = "select name, cost, image from products where id={}".format(product_id)
                        cursor.execute(query)
                        product_details = cursor.fetchall()

                    return render_template("profile.html", name=name, email=email, product_details=product_details)

            if not login_success:
                error = "Username and password do not match our records, try again!"
                return render_template('login.html', message=error)

        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('/'))
    return render_template('login.html', error=error)


@app.route("/signup", methods=['POST', 'GET'])
def sign_up():
    error = request.args.get('error')
    return render_template("signup.html", error=error)


@app.route("/user_registration", methods=['POST', 'GET'])
def user_registration():
    message = None

    if request.form['password'] != request.form['confirm-password']:
        return redirect(url_for("sign_up", error="Passwords do not match!"))

    with sqllite.connect('walbot.db') as conn:
        cursor = conn.cursor()

        # Check if user exists
        query = "select email from users"
        cursor.execute(query)
        content = cursor.fetchall()
        for email in content:
            email = str(email).strip("(''),")
            # print(email)
            if email == request.form['email']:
                error = "Account with that email already exists!"
                return redirect(url_for("sign_up", error=error))

        # id = uuid.uuid1()
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        image = "/static/images/pavlo.jpg"
        query = "insert into users (fullname, email, password, image) VALUES('{0}', '{1}','{2}','{3}')".format(fullname, email, password, image)

        cursor.execute(query)
        message = "User registration success, please login now!"
    return render_template("login.html", message=message)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = "team_enigma"
    app.run("localhost", port=5000)
