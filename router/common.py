import random
from models.registation import Registation
from View import db, app
from helper import utility
from View.configuration import config
from flask import Flask, render_template, redirect, url_for, session
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from View.form import forgetpasswordform


@app.route('/')   # user
def Login():
    return render_template('Login.html')


@app.route('/Login1', methods={'POST', 'GET'})  # user
def Login1():

    email = request.form.get('email', '')
    password = request.form.get('password', '')
    record = Registation.query.filter_by(Email=email).first()
    if record is not None:
        # if  pbkdf2_sha256.verify(password, record.Password) :
        if check_password_hash(record.Password, password):
            session["authenticated"] = True
            session["email"] = email
            return redirect(url_for('home'))
        else:
            session["authenticated"] = False
            session["email"] = ""
            Error = "incorrect password or email"
            return render_template('Login.html', error=Error)
    else:
        Error = "enter valid email"
        return render_template('Login.html', error=Error)


@app.route('/Register', methods={'GET', 'POST'})  # user
def Register():

    message = ""
    if(request.method == 'POST'):
        # add entry to the database...
        first_name = request.form.get('fname')
        last_name = request.form.get('lname')
        dob = request.form.get('dob')
        email = request.form.get('email')
        password = request.form.get('fp')

        # hased_pawd = pbkdf2_sha256.hash(password)
        hash = generate_password_hash(password)
        # pw_hash = bcrypt.generate_password_hash(password)
        Otp = random.randint(1000, 9999)

        try:
            register = Registation(
                First_Name=first_name, Last_Name=last_name, Dob=dob,
                Email=email, Password=hash, otp=Otp
                )
            db.session.add(register)
            db.session.commit()
            message = "<div class='text-success'>Your Account has been Created</div>"
            subject = "Registation Deatil"
            recipients = [email, ]
            mailbody = "your registation is done. "
            utility.send_mail(subject, recipients, mailbody)
        except Exception as E:
            print(E.args)
            message = "<div class='text-danger'>" + str(E)+"</div>"
    return render_template('Register.html', Error=message)


@app.route('/fpassword', methods={'GET', 'POST'})  # user
def fpassword():

    if request.method == "GET":
        print("Page Loaded")
        form = forgetpasswordform()
        return render_template('fpassword.html', form=form)
    else:
        # 1. User ne kya email dala
        email = request.form.get('email', '')
    # 2. Search in database
        Otp = random.randint(1000, 9999)
        print(Otp)
        admin = Registation.query.filter_by(Email=email).update(dict(otp=Otp))
        db.session.commit()
        subject = "Otp"
        recipients = [email, ]
        # update OTP in data base for that email address
        mailbody = "your otp is: {} <br> <a href='{}/Epassword'>  \
        Please click here</a>".format(str(Otp), config.BASE_URL)
        utility.send_mail(
             subject=subject, recipients=recipients, mailbody=mailbody
             )
        # same order mai chahie , warna aihse likho
        form = forgetpasswordform()
        error = "<b>Pleace cheak the mailbox</b>"
        return render_template('fpassword.html', form=form, Error=error)  
