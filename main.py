from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask import session, request, jsonify
from flaskext.mysql import MySQL
import re
import os
import random
import hashlib
import pybase64
import json
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from jsonschema import validate
import pandas as pd



app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))

app.secret_key = 'financexyz$test7972#'

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD	'] = ''
app.config['MYSQL_DATABASE_DB'] = 'finpeer'

# Intialize MySQL
mysql = MySQL(autocommit=True)
mysql.init_app(app)

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True


schema = {
    "type" : "string",
    "properties" : {
        "description" : {"type" : "string"},
        "value_a" : {"type" : "number"},
        "value_b" : {"type" : "number"},
    },
}

@app.route('/')
def index():
    if 'loggedin' not in session:
        return render_template('index.html')
    else:
        return home()

@app.route('/dashboard')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])

        account = cursor.fetchone()
        cursor1 = mysql.get_db().cursor()
        records = cursor.execute('SELECT * FROM users')
        return render_template('dashboard.html', account = account, num = records)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# Account information visible inside dashboard
@app.route('/myaccount')
def myaccount():
    if 'loggedin' in session:
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('myaccount.html', account=account)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'loggedin' not in session:
    # Output message if something goes wrong...
        msg = None
        # Check if "username" and "password" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            if(username and password):
            # Check if account exists using MySQL
                cursor = mysql.get_db().cursor()
                cursor.execute('SELECT * FROM users WHERE Username = %s', (username))
                # Fetch one record and return result
                account = cursor.fetchone()
                # If account exists in accounts table in out database
                if account:
                    if check_password_hash(account[2], password):
                        # Create session data, we can access this data in other routes
                        session['loggedin'] = True
                        session['id'] = account[0]
                        session['username'] = account[1]
                        # Redirect to dashboard
                        return home()
                    else:
                        # Account doesnt exist or username/password incorrect
                        msg = 'Incorrect username/password!'
                        flash(msg)
                else:
                    # Account doesnt exist or username/password incorrect
                    msg = 'Incorrect username/password!'
                    flash(msg)
            else:
                msg = 'Please provide both username and password!'
                flash(msg)
        # Show the login form with message (if any)
    else:
        return home()
    return render_template('userlogin.html', msg=msg)

#User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    if('loggedin' not in session):
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            full_name = request.form['full_name']
            if(username and password and email and full_name):
                # Check if account exists using MySQL
                cursor = mysql.get_db().cursor()
                cursor.execute('SELECT * FROM users WHERE Username = %s', (username))
                account = cursor.fetchone()
                # If account exists show error and validation checks
                if account:
                    msg = 'Account already exists!'
                    flash(msg)
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    msg = 'Invalid email address!'
                    flash(msg)
                elif not re.match(r'[A-Za-z0-9]+', username):
                    msg = 'Username must contain only characters and numbers!'
                    flash(msg)
                else:
                    # Account doesnt exists and the form data is valid, now insert new account into users table
                    apistr = username
                    hashed_password = generate_password_hash(password)
                    cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s)', (username, hashed_password, email, full_name))
                    cursor.execute('SELECT * FROM users WHERE Username = %s', (username))
                    # Fetch one record and return result
                    account = cursor.fetchone()
                    session['loggedin'] = True
                    session['id'] = account[0]
                    session['username'] = account[1]
                    msg = 'You have successfully registered!'
                    return home()
            else:
                msg = 'Please fill out the form!'
                flash(msg)
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
        # Show registration form with message (if any)
    else:
        return home()
    return render_template('userlogin.html', msg=msg)


@app.route('/jsonupload', methods=['GET','POST'])
def jsonuploader():
    if 'loggedin' in session:
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('jsonpanel.html', account=account)
    return redirect(url_for('login'))

@app.route('/uploadsuccess',methods=['GET','POST'])
def jsonup():
    if 'loggedin' in session:
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])
        account = cursor.fetchone()
        username = account[1]
        if request.method == 'POST':
            f = request.files['file']

            try:
                data = json.load(f)
                success = True
            except:
                success = False
                return render_template('jsonproceed.html',account=account,success=success)
            
        

            df = pd.DataFrame(data)
            userid = []
            dfsize = len(df)
            for i in range(dfsize):
                userid.append(str(username))
            

            # print for debug
            df["userids"] = userid


            cols = "`,`".join([str(i) for i in df.columns.tolist()])



            # Insert DataFrame recrds one by one.
            for i,row in df.iterrows():
                sql = "INSERT INTO `jsonuser` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
                cursor.execute(sql, tuple(row))


            return render_template('jsonproceed.html',account=account,success=success)
    return redirect(url_for('login'))


@app.route('/jsonview',methods=['GET','POST'])
def jsonview():
    if 'loggedin' in session:
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])
        account = cursor.fetchone()
        username = account[1]

        cursor2 = mysql.get_db().cursor()
        cursor2.execute('SELECT * FROM jsonuser WHERE userids=%s',[username])
        data = cursor2.fetchall()
        return render_template('JsonView.html',account=account,data=data)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
   # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('index'))

app.run()