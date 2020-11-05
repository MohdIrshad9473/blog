
import os
from flask import Flask, render_template, redirect, url_for, session
from datetime import datetime
from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# import for mails
# python linting now enable
# admin mai

from View.configuration import config


app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret_key  # one by o
app.config.update(   # bulk mai init karne ka
    SQLALCHEMY_DATABASE_URI=config.database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    MAIL_SERVER=config.Mail_SERVER
)
# mail  - Hard code  and it is security problem -  clicnt ko selll ..

app.config['MAIL_PORT'] = config.MAIL_PORT  # config
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ["MAIL_USERNAME"]
# enter your email her
app.config['MAIL_DEFAULT_SENDER'] = os.environ["MAIL_USERNAME"]
app.config['MAIL_PASSWORD'] = os.environ["MAIL_PASSWORD"]

# initialize the database connection
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.create_all()
db.session.commit()

import router
from router import common
from router import contact
