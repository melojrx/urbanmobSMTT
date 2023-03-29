from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import HiddenField
from wtforms.validators import InputRequired
 
class SolicitacaoDocumentoForm(FlaskForm):
    
    file = FileField(
        '',
        validators = [
        InputRequired(message=('*Campo Requerido')),
        FileAllowed(['png', 'pdf', 'jpg', 'jpeg'], "Formatos válidos: .png, .pdf e .jpg!")
        ],
        id=None)

    documento = HiddenField("documento")

    tipoSolicitacao = HiddenField("tipoSolicitacao")