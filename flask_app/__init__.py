from flask import Flask
from .filters import format_date
import secrets
from flask_bcrypt import Bcrypt
from os import environ

app = Flask(__name__)
# secret_key_urlsafe = secrets.token_urlsafe(16)
# app.secret_key = secret_key_urlsafe
app.secret_key = environ.get('SECRET_KEY_URLSAFE')

bcrypt = Bcrypt(app)
app.add_template_filter(format_date)