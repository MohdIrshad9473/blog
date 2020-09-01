from flask import Flask, render_template
from datetime import datetime
app = Flask(__name__)   #web site app

@app.route('/')
def hello_world():
      return 'Hello World'
 
@app.route('/user/<name>')
def user(name):
    return'<h2>naddem {}</h2>'.format(name)





if __name__ =="__main__":
    app.run()