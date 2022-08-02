from flask import Blueprint
from flask_login import login_required

views = Blueprint('views', __name__)

@views.route('/')
def home():
      return ' HELLO'