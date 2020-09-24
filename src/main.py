from flask import Flask, render_template,redirect,url_for,session
from datetime import datetime
from flask import request
from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from form import forgetpasswordform 


database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser="postgres",
    dbpass="irshad9473",
    dbhost="127.0.0.1",
    dbname="irshad"
)

app = Flask(__name__)
app.secret_key='123456'
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

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
    Description= db.Column(db.String(500),  nullable=False)
    date = db.Column(db.String(100),  nullable=True)

class Registation(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    First_Name = db.Column(db.String(80), nullable=False)
    Last_Name = db.Column(db.String(80), nullable=False)
    Dob = db.Column(db.DateTime, nullable=False)
    Email = db.Column(db.String(100), nullable=False,unique=True)
    Password = db.Column(db.String(80), nullable=False)

      

# initialize database migration management
migrate = Migrate(app, db)

db.create_all()
db.session.commit()


@app.route('/home')
def home ():
        if session.get("authenticated",'') == True:
            post = Posts.query.all()
            print(post)            
            return render_template('index.html',record=post)
        else:
            return redirect(url_for('Login'))
# @app.route('/', methods=['GET'], defaults={"page": 1}) 
# # @app.route('/<int:page>', methods=['GET'])
# def home(page=1):
#     per_page =10
#     posts = Posts.query.paginate(page,per_page,error_out=False)
#     return render_template('index.html',posts=posts)





@app.route('/about') 
def  about():
    if session.get("authenticated",'') == True:
       return render_template('about.html')
    else:
         return redirect(url_for('Login'))
@app.route('/post') 
def  post():
    if session.get("authenticated",'') == True:
      return render_template('post.html')
    else:
        return redirect(url_for('Login'))
@app.route('/contact', methods={'GET','POST'}) 
def  contact():
    if session.get("authenticated",'') == True:

        if(request.method=='POST'):
            # add entry to the database...
            name=request.form.get('name')
            email=request.form.get('email')
            phone_number=request.form.get('phone_number')
            message=request.form.get('message')

            # insert
            entry = Contacts(name=name, phone_num=phone_number, msg=message, email=email, date="123")
            db.session.add(entry)
            db.session.commit()

        return render_template('contact.html') 


    else:
     return redirect(url_for('Login'))      
@app.route('/createpost', methods={'GET','POST'}) 
def  createpost():
    if session.get("authenticated",'') == True:
      if(request.method=='POST'):
        # add entry to the database...
        title=request.form.get('title')
        description=request.form.get('description')

        #insert
        record = Posts(tittle=title,Description=description,date="234")
        db.session.add(record)
        db.session.commit()  

      return render_template('createpost.html')
    else:
        return redirect(url_for('Login'))    

@app.route('/allcontact') 
def  allcontact():
    if session.get("authenticated",'') == True:
        data = Contacts.query.all() # 2 record
        print(data)  
        print(data[0])
        print(data[0].email)
        return  render_template('allcontact.html',record=data) 
    else:
        return redirect(url_for('Login'))    
@app.route('/Register', methods={'GET','POST'}) 
def  Register():
       
        message=""
        if(request.method=='POST'):
            # add entry to the database...
            first_name=request.form.get('fname')
            last_name=request.form.get('lname')
            dob=request.form.get('dob')
            email=request.form.get('email')
            password=request.form.get('password')
            
            try:
                  register = Registation(First_Name=first_name,Last_Name=last_name, Dob=dob,Email=email,Password=password)
                  db.session.add(register)
                  db.session.commit() 
                  message="<div class='text-success'>record created</div>"
            except Exception as E:
                print(E.args)
                message="<div class='text-danger'>" +str(E)+"</div>"
            
        return render_template('Register.html',Error=message)
        
@app.route('/') 
def  Login():
        return render_template('Login.html')

@app.route('/Login1',methods={'POST'}) 
def  Login1():

        email =request.form.get('email', '')
        print(email)
        password =request.form.get('password', '')
        print(password)

        #query in database and get password for this email address
        record = Registation.query.filter_by(Email=email).first()
        print(record.Password)
        if password==record.Password:
            session["authenticated"] = True
            return redirect(url_for('home'))
            pass
        else:
            session["authenticated"] = False
            Error="incorrect Login or password"
            return render_template('Login.html',error=Error)
@app.route('/Logout') 
def  Logout():
            session["authenticated"] = False
            Error="incorrect Login or password"
            return redirect(url_for('Login'))

@app.route('/fpassword') 
def  fpassword():    
            form = forgetpasswordform()
            return render_template('fpassword.html', form=form)
          
             


             



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
    app.run(debug=True)
