from flask import Flask, render_template, redirect, url_for, session
from datetime import datetime
from flask import request
from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from form import forgetpasswordform, RPassword, EditProfile,epassword
# import for mails
from flask_mail import Mail, Message
from passlib.hash import pbkdf2_sha256
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os



database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ["Dbuser"],      #"postgres",
    dbpass=os.environ["Dbpass"],      #"irshad9473",
    dbhost="127.0.0.1",
    dbname=os.environ["Dbname"]       #"irshad"

)

app = Flask(__name__)
app.secret_key = '123456'
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
# mail  - Hard code  and it is security problem -  clicnt ko selll ..
app.config['MAIL_SERVER'] = os.environ["MAIL_SERVER"]
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ["MAIL_USERNAME"]                      #'irshad9473@gmail.com'  # enter your email here
# enter your email here
app.config['MAIL_DEFAULT_SENDER'] = os.environ["MAIL_DEFAULT_SENDER"         #'irshad9473@gmail.com'
app.config['MAIL_PASSWORD'] =  os.environ["MAIL_PASSWORD"]                 #'7668459042'  # enter your password here
mail = Mail(app)
# initialize the database connection
db = SQLAlchemy(app)


class Contacts(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),      nullable=False)
    phone_num = db.Column(db.String(100),  nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(100),  nullable=True)
    email = db.Column(db.String(100), nullable=False)


class Posts(db.Model):
# sno,tittle,content,date
    sno = db.Column(db.Integer, primary_key=True)
    tittle = db.Column(db.String(100),      nullable=False)
    Description = db.Column(db.String(500),  nullable=False)
    date = db.Column(db.String(100),  nullable=True)


class Registation(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    First_Name = db.Column(db.String(80), nullable=False)
    Last_Name = db.Column(db.String(80), nullable=False)
    Dob = db.Column(db.DateTime, nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Password = db.Column(db.String(300), nullable=False)
    otp = db.Column(db.Integer, nullable=False)


# initialize database migration management
migrate = Migrate(app, db)

db.create_all()
db.session.commit()


@app.route('/home')
def home():
        if session.get("authenticated", '') == True:
            post = Posts.query.all()
            print(post)
            return render_template('index.html', record=post)
        else:
            return redirect(url_for('Login'))
# @app.route('/', methods=['GET'], defaults={"page": 1})
# # @app.route('/<int:page>', methods=['GET'])
# def home(page=1):
#     per_page =10
#     posts = Posts.query.paginate(page,per_page,error_out=False)
#     return render_template('index.html',posts=posts)


@app.route('/about')
def about():
    if session.get("authenticated", '') == True:
       return render_template('about.html')
    else:
         return redirect(url_for('Login'))


@app.route('/post')
def post():
    if session.get("authenticated", '') == True:
      return render_template('post.html')
    else:
        return redirect(url_for('Login'))


@app.route('/contact', methods={'GET', 'POST'})
def contact():
    if session.get("authenticated", '') == True:

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


@app.route('/createpost', methods={'GET', 'POST'})
def createpost():
    if session.get("authenticated", '') == True:
      if(request.method == 'POST'):
        # add entry to the database...
        title = request.form.get('title')
        description = request.form.get('description')

        # insert
        record = Posts(tittle=title, Description=description, date="234")
        db.session.add(record)
        db.session.commit()

      return render_template('createpost.html')
    else:
        return redirect(url_for('Login'))


@app.route('/allcontact')
def allcontact():
    if session.get("authenticated", '') == True:
        data = Contacts.query.all()  # 2 record
        print(data)
        print(data[0])
        print(data[0].email)
        return render_template('allcontact.html', record=data)
    else:
        return redirect(url_for('Login'))


@app.route('/Register', methods={'GET', 'POST'})
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
            Otp = random.randint(1000,9999)

            try:
                  register = Registation(
                      First_Name=first_name, Last_Name=last_name, Dob=dob, Email=email, Password=hash, otp=Otp)
                  db.session.add(register)
                  db.session.commit()
                  message = "<div class='text-success'>Your Account has been Created</div>"
                  subject = "Registation Deatil"
                  recipients = [email, ]
                  mailbody = "your registation is done. "
                  send_mail(subject, recipients, mailbody)
            except Exception as E:
                print(E.args)
                message = "<div class='text-danger'>" + str(E)+"</div>"

        return render_template('Register.html', Error=message)


@app.route('/')
def Login():
        return render_template('Login.html')


@app.route('/Login1', methods={'POST', 'GET'})
def Login1():

        email = request.form.get('email', '')
        print(email)
        password = request.form.get('password', '')
        print(password)

        # query in database and get password for this email address
        record = Registation.query.filter_by(Email=email).first()
        print(record)
        # print(record.Email)

        # if condition mai cherck karo if record exist else error messe and return to login page
        # print(record.Password)
        if record != None:
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


@app.route('/Logout')
def Logout():
            session["authenticated"] = False
            session["email"] = ""
            return redirect(url_for('Login'))


@app.route('/fpassword', methods={'GET', 'POST'})
def fpassword():

           if request.method == "GET":
                print("Page Loaded")
                form = forgetpasswordform()
                return render_template('fpassword.html', form=form)
           else:
               # 1. User ne kya email dala
                email = request.form.get('email', '')
            # 2. Search in database
                Otp = random.randint(1000,9999)
                print(Otp)
                admin = Registation.query.filter_by(Email=email).update(dict(otp=Otp))
                db.session.commit()



                 #  email will be used to update in database

            # 4. Email password to user
                subject = "Otp"
                recipients = [email, ]
                # update OTP in data base for that email address
                mailbody =   "your otp is:" + str(Otp) +  '<a href="http://127.0.0.1:8000/Epassword">  Please click here</a> '             
                send_mail(subject, recipients, mailbody)
                form = forgetpasswordform()
                error = "<b>Pleace cheak the mailbox</b>"
                return render_template('fpassword.html',form=form ,Error=error)
                

@app.route('/ResetPassword', methods=['GET', 'POST'])
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


@app.route('/editprofile/', methods=['GET', 'POST'])
def Editprofile():  # new starting
        print(request.method)
        if request.method == "POST":
            user_email = session["email"]
            # form se value lene ka tarika... extract data from form
            First_Name = request.form.get('First_Name', '')
            Last_Name = request.form.get('Last_Name', '')
            dob=request.form.get('dob', '')
           
            amin = Registation.query.filter_by(Email=user_email).update(dict(First_Name=First_Name,Last_Name=Last_Name,Dob=dob))
            print(amin)
            db.session.commit()
            return redirect(url_for('home'))
            pass
        if request.method == "GET" :
            # by default get method - browser
            user_email = session["email"]
            user = Registation.query.filter_by(Email=user_email).first()
            # form with inital values
            Form=EditProfile(First_Name=user. First_Name ,Last_Name=user.Last_Name,dob=user.Dob,Email=user.Email)
            return render_template('editprofile.html', form=Form)
            pass

@app.route('/Epassword',methods=['GET', 'POST'])
def Epassword():
            form = epassword()
            if(request.method == "POST"):
                email=request.form.get('Email','')
                Otp=request.form.get('Otp','')
                newpassword=request.form.get('newpassword','')
                newpassword1=request.form.get('newpassword1','')
                record = Registation.query.filter_by(Email=email).first()
                print(type(record.otp))
                print(type(Otp))
                if int(Otp) == (record.otp):
                   hash=generate_password_hash(newpassword)                           # false aa raha  #database it is int , form se string atta so u need to convert in int
                   amin = Registation.query.filter_by(Email=email).update(dict(Password=hash))
                   print(amin)
                   db.session.commit()   

                else:
                    print('nothello')   
                
            else:
                return render_template('Epassword.html',form=form)
          
        # user ko jo OTP bhejoge ushko save karna hoga kyoki baad mai copmpare karoge ki user sahi OTP
        # pythoninport random call jald wo to ho jaye 

        # form 
        #   1 email2. OTP3. password4 again password
        #   submit 

        #   action : page 
        #   method post

        #   page :
        #   email from formopt
        #   database mai querylatest OTO
        #   if OTP match
        #   update databse password

        #   forgetpassword pe click ... ak page open hoga....email address  and send button
        #   send button pe email jaiga user ko with otp
        #   and url for new password

            

           



           



def send_mail(subject,recipients,mailbody):
    msg = Message(subject=subject,  recipients=recipients)
    msg.html=mailbody
 
    mail.send(msg)
             

# google pe syntax milta hai lekin concept tumhara clar hona chahie tabhi syntax ka use kar paoge
# google pe direct concept nahi milta
# jishka concept confusing ushka google help nhi kar pata

# get post 
# www.google.com  get bhi call post bhi call kar sakte





# @app.route('/addcontact',methods=['POST']) 
# def  addcontact():
#     email = request.form.get('email')
#     name = request.form.get('name')
#     phone_number=request.form.get('phone number')
#     # // name , email
#     #// Database Connection
#     # Insert In sdatabase 
#     #database close
#     return 'your contact has been added in main'    

# @app.route('/showcontact'  ) 
# def  showcontact():
    
#       #// Database Connection
#       # delete iod
#       # response 

#       return deleted

  

 
if __name__ =="__main__":
    app.run(host="localhost", port=8000, debug=True)
