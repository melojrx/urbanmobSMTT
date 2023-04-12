from flask_login import LoginManager
from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.debug = True
# app.config['SQLALCHEMY_ECHO'] = True

# Configurações de Email # 
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'urbanpass2@gmail.com'
app.config['MAIL_PASSWORD'] = 'vrznaicxfqgfbgfv'
app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


login_manager = LoginManager(app)
login_manager.login_view = "login.login"
login_manager.login_message = u"Por favor, realize o login para acessar a página"

from .rotas.loginRout import login_bp
from .rotas.publicRout import public_bp
from .rotas.solicitacaoRout import solicitacao_bp
from .rotas.send_emailRout import send_email_bp

app.register_blueprint(public_bp)
app.register_blueprint(login_bp)
app.register_blueprint(solicitacao_bp)
app.register_blueprint(send_email_bp)
# print(list(app.url_map.iter_rules()))