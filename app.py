from flask import Flask, request, session
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_bootstrap import Bootstrap
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp
from datetime import timedelta

from db import Database

app = Flask(__name__)
app.config['SECRET_KEY'] = "APP_SECRET_KEY"
Bootstrap(app)
db = Database()

# homepage route
@app.route("/")
def index():
    print(session.get('logged_in'))
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    return "<h1>Hellooo World!!!</h1>"

# login route
@app.route("/login")
def login():
    return render_template("login.html")

# login POST method
@app.route("/login", methods=["POST"])
def login_form():
    db_user_phone_list = db.select_all_phone()
    
    # get from data
    phone = request.form.get("phone")
    password = request.form.get("password")

    if phone not in db_user_phone_list:
        flash("You have not yet registered", "danger")
        return redirect(url_for("login"))
    else:
        password_hash = db.select_password(phone)
        if not check_password_hash(password_hash, password):
            flash("Wrong password", "danger")
            return redirect(url_for("login"))
        else:
            flash("Logged in successfully", "success")
            return redirect(url_for("login_2fa", phone=phone))

# login_2fa route
@app.route("/login_2fa")
def login_2fa():
    return render_template("login_2fa.html", phone=request.args.get('phone'))

# login_2fa POST method
@app.route("/login_2fa", methods=["POST"])
def login_2fa_form():
    phone = request.args.get('phone')
    secret = db.select_secret_key(phone)
    otp = int(request.form.get("otp"))

    if pyotp.TOTP(secret).verify(otp):
        flash("The TOTP 2FA token is valid", "success")
        print("SUCCESS")
        # Set session
        session["logged_in"] = True
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=1)
        return redirect(url_for("index"))
    else:
        flash("You have supplied an invalid 2FA token! Please try again", "danger")
        print("FAILED")
        return redirect(url_for("login_2fa", phone=phone))

# register route
@app.route("/register")
def register():
    return render_template("register.html")

# register POST method
@app.route("/register", methods=["POST"])
def register_form():
    user_phone_list = ["852 69959681", "852 87654321"]  # Google sheet phone list
    phone = request.form.get("phone")
    password = request.form.get("password")
    confirm_password = request.form.get("confirmPassword")

    if phone not in user_phone_list:
        flash("You are not telegram bot user", "danger")
        print("FAILED")
        return redirect(url_for("register"))
    elif password != confirm_password:
        flash("Passwords are not the same", "danger")
        print("FAILED")
        return redirect(url_for("register"))
    else:
        password_hash = generate_password_hash(password)
        print("SUCCESS")
        
        db_user_phone_list = db.select_all_phone()
        if phone in db_user_phone_list:
            # Get secret key from database
            secret = db.select_secret_key(phone)
        else:
            # Add user input to database
            secret = pyotp.random_base32()
            db.insert_values("user", {'phone': phone, 'password': password_hash, 'secret': secret})
        # output corresponding qr code
        qr_url = pyotp.totp.TOTP(secret).provisioning_uri(name=phone, issuer_name="QuantRaiser")
        print(qr_url)
        return redirect(url_for("register2fa", qr_url=qr_url))


# register 2fa route
@app.route("/register2fa")
def register2fa():
    return render_template("register2fa.html", qr_url=request.args.get("qr_url"))

if __name__ == "__main__":
    app.run(debug=True)