import random
import os
from helper import utility
from View import app, db
from flask import Flask, render_template, redirect, url_for, session
from models.registation import Registation
from models.Contacts import Contacts
from models.Posts import Posts
from flask import request 
from View.form import forgetpasswordform, RPassword, EditProfile, epassword
from passlib.hash import pbkdf2_sha256 
from werkzeug.security import generate_password_hash, check_password_hash  
from View.configuration import config  


@app.route('/home')
def home():
    if session.get("authenticated", '') is True:
        post = Posts.query.all()
        return render_template('index.html', record=post)
    else:
        return redirect(url_for('Login'))


@app.route('/about')
def about():
    if session.get("authenticated", '') is True:
        return render_template('about.html')
    else:
        return redirect(url_for('Login'))


@app.route('/post')  # post
def post():
    if session.get("authenticated", '') is True:
        return render_template('post.html')
    else:
        return redirect(url_for('Login'))


@app.route('/createpost', methods={'GET', 'POST'})  # post
def createpost():
    if session.get("authenticated", '') is True:
        if(request.method == 'POST'):
            # add entry to the database...
            title = request.form.get('title')
            description = request.form.get('description')
            record = Posts(tittle=title, Description=description, date="234")
            db.session.add(record)
            db.session.commit()
        return render_template('createpost.html')
    else:
        return redirect(url_for('Login'))


@app.route('/allcontact')
def allcontact():
    if session.get("authenticated", '') is True:
        data = Contacts.query.all()  # 2 record
        print(data)
        print(data[0])
        print(data[0].email)
        return render_template('allcontact.html', record=data)
    else:
        return redirect(url_for('Login'))


@app.route('/Logout')  # user
def Logout():
    session["authenticated"] = False
    session["email"] = ""
    return redirect(url_for('Login'))


@app.route('/ResetPassword', methods=['GET', 'POST'])  # user
def ResetPassword():
    error = ""
    form = RPassword()
    print(request.method)
    if request.method == "POST":
        oldpassword = request.form.get('password', '')
        newpassword = request.form.get('newpassword', '')
        # get old password from form
        print(" old password is : ", oldpassword)
        # get new password from form
        print("new password is: ", newpassword)
        Email = session["email"]
        print(Email)
        record = Registation.query.filter_by(Email=Email).first()
        print(record.Password)
        admin = Registation.query.filter_by(
            Email=Email).update(dict(Password=newpassword))
        print(admin)
        db.session.commit()
        # User.query.filter_by(Email).update(dict(Password='newpassword')))

        return render_template('ResetPassword.html', form=form)
    else:
        error = "danish"
        return render_template('ResetPassword.html', form=form, Error=error)


@app.route('/editprofile/', methods=['GET', 'POST'])  # user
def Editprofile():  # new starting
    print(request.method)
    if request.method == "POST":
        user_email = session["email"]
        # form se value lene ka tarika... extract data from form
        First_Name = request.form.get('First_Name', '')
        Last_Name = request.form.get('Last_Name', '')
        dob = request.form.get('dob', '')
        amin = Registation.query.filter_by(Email=user_email).update(
            dict(First_Name=First_Name, Last_Name=Last_Name, Dob=dob))
        print(amin)
        db.session.commit()
        return redirect(url_for('home'))
        pass
    if request.method == "GET":
        # by default get method - browser
        user_email = session["email"]
        user = Registation.query.filter_by(Email=user_email).first()
        # form with inital values
        Form = EditProfile(
            First_Name=user. First_Name, Last_Name=user.Last_Name,
            dob=user.Dob, Email=user.Email
            )
        return render_template('editprofile.html', form=Form)
        pass


@app.route('/Epassword', methods=['GET', 'POST'])  # user
def Epassword():
    form = epassword()
    if(request.method == "POST"):
        email = request.form.get('Email', '')
        Otp = request.form.get('Otp', '')
        newpassword = request.form.get('newpassword', '')
        newpassword1 = request.form.get('newpassword1', '')
        record = Registation.query.filter_by(Email=email).first()
        print(type(record.otp))
        print(type(Otp))
        if int(Otp) == (record.otp):
            # false aa raha  #database it is int ,
            #  form se string atta so u need to convert in int
            hash = generate_password_hash(newpassword)
            amin = Registation.query.filter_by(
                Email=email).update(dict(Password=hash))
            print(amin)
            db.session.commit()

        else:
            print('nothello')

    else:
        return render_template('Epassword.html', form=form)

