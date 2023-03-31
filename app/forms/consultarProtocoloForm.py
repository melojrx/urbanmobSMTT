from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
 
class ConsultarProtocoloForm(FlaskForm):
    
    numeroProtocolo = StringField(
        'Nº. do Protocolo',
        validators = [
        InputRequired(message=('*Campo Requerido'))
        ])
    
    submit = SubmitField('Consultar')