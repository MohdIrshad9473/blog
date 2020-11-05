from models.registation import Registation
from View import db, app
from models.Contacts import Contacts
from flask import Flask, render_template, redirect, url_for, session
from flask import request


@app.route('/contact', methods={'GET', 'POST'})
def contact():
    if session.get("authenticated", '') is True:

        if(request.method == 'POST'):
            # add entry to the database...
            name = request.form.get('name')
            email = request.form.get('email')
            phone_number = request.form.get('phone_number')
            message = request.form.get('message')

            # insert
            entry = Contacts(name=name, phone_num=phone_number,
                             msg=message, email=email, date="123")
            db.session.add(entry)
            db.session.commit()
        return render_template('contact.html')

    else:
        return redirect(url_for('Login'))