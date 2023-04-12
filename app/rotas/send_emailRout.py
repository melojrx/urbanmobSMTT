from flask import Blueprint

send_email_bp = Blueprint('send_email', __name__)

from ..controller.send_emailController import *