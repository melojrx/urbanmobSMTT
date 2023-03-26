from email.policy import default
from wtforms.widgets import TextArea
from wtforms import Form, StringField, SelectField, FileField
from wtforms.validators import DataRequired, InputRequired, Length
 
class SolicitacaoForm(Form):

    file = FileField(
        'Insira uma foto:',
        validators = [
            InputRequired(message=('*Campo Requerido'))
    ])