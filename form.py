from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField,DateField,IntegerField
from wtforms import validators

# forget password design
class forgetpasswordform(FlaskForm):
    email = EmailField('Email', [validators.DataRequired()])
    submit = SubmitField('Submit')

class RPassword(FlaskForm):
    password = PasswordField('Enter old Password:', [validators.DataRequired()])
    newpassword = PasswordField('Enter  New Password:', [validators.DataRequired()])
    newpassword1 = PasswordField('confirm Password:', [validators.DataRequired()])
    submit = SubmitField('Submit')

class EditProfile(FlaskForm):
      First_Name = StringField('Enter first name:',  [validators.DataRequired()])
      Last_Name = StringField('Enter last name:',  [validators.DataRequired()])
      dob=DateField('Enter date of birth:', [validators.DataRequired()])
      Email =  EmailField('Email', [validators.DataRequired()])
      submit = SubmitField('Submit')

class epassword(FlaskForm):
    Email =  EmailField('Email', [validators.DataRequired()])
    Otp =   IntegerField('Otp', [validators.DataRequired()])
    newpassword = PasswordField('Enter  New Password:', [validators.DataRequired()])
    newpassword1 = PasswordField('confirm Password:', [validators.DataRequired()])
    submit = SubmitField('Submit')


    
# create form for rest password
# passform to Template

# User.query.filter_by(email='admin@gmail').update(dict(passord='new value@example.com')))

#request.user
#session["email"]

      


   