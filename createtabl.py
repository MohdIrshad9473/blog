from flask import Flask, render_template
from datetime import datetime
app = Flask(__name__)   #web site app
@app.route(‘/hello’)
def hello_world():
   return ‘hello world’

)
