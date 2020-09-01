from flask import Flask, render_template
from flask import request
app = Flask(__name__)
@app.route('/')
def index():
  user_agent = request.headers.get('User-Agent')
  return '<p>Your browser is {}</p>'.format(user_agent)