import random
from models.registation import Registation
from View import db, app
from helper import utility
from View.configuration import config
from flask import Flask, render_template, redirect, url_for, session
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash



