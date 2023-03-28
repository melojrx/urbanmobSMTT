from wtforms import Form, FileField, HiddenField, StringField
from wtforms.validators import InputRequired
 
class SolicitacaoDocumentoForm(Form):
    
    file = FileField(
        '',
        validators = [InputRequired(message=('*Campo Requerido'))],
        id=None)

    tipoSolicitacao = HiddenField("Field 1")