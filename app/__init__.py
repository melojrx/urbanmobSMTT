from flask_login import LoginManager
from flask import Blueprint, Flask, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.debug = True
# app.config['SQLALCHEMY_ECHO'] = True

login_manager = LoginManager(app)
login_manager.login_view = "login.login"
login_manager.login_message = u"Por favor, realize o login para acessar a página"

from .rotas.loginRout import login_bp
from .rotas.publicRout import public_bp


app.register_blueprint(public_bp)
app.register_blueprint(login_bp)
# print(list(app.url_map.iter_rules()))