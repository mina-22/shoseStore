from flask import Flask, render_template, request, redirect, url_for, session, flash
import database as db
import utils
app = Flask(__name__)
connection = db.connect_to_database()

app.secret_key = "SUPER-SECRET"
@app.route('/')
def index():
    if 'username' in session:
        if session['username'] == 'momen':
            return("hellow")
        else:
            return render_template('index.html')
    return render_template('Register.html')

@app.route('/Login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.get_user(connection, username)
        if user:
            if utils.is_password_match(password, user[2]):
                session['username'] = user[1]
                return redirect(url_for('index'))
            else:
                flash("Invalid username or password", "danger")
                return render_template('Login.html')
        else:
            flash("Invalid username or password", "danger")
            return render_template('Login.html')
    else:
        
        return render_template("Login.html")    
@app.route('/Register', methods=['GET', 'POST'])
def Register():
    if request.method == 'POST':
        
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if not utils.is_strong_password(password):
            flash(
                "Sorry You Entered a weak Password Please Choose a stronger one", "danger")
            return render_template('Register.html')

        user = db.get_user(connection, username)
        if user:
            flash(
                "Username already exists. Please choose a different username.", "danger")
            return render_template('Register.html')
        else:
            db.add_user(connection,email,username,password)
            return redirect(url_for('Login'))
    else:
        return render_template('Register.html')
     