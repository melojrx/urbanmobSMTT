from wtforms import Form, FileField, HiddenField, StringField
from wtforms.validators import InputRequired
 
class SolicitacaoDocumentoForm(Form):
    
    file = FileField(
        '',
        validators = [
            InputRequired(message=('*Campo Requerido'))
    ])

    tipoSolicitacao = HiddenField("Field 1")