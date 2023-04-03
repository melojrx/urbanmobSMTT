from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import HiddenField, StringField
from wtforms.validators import InputRequired, Email, Length
 
class SolicitacaoDocumentoForm(FlaskForm):
    
    file = FileField(
        '',
        validators = [
        InputRequired(message=('*Campo Requerido')),
        FileAllowed(['png', 'pdf', 'jpg', 'jpeg'], "Formatos válidos: .png, .pdf e .jpg!")
        ],
        id=None)

    documento = HiddenField("documento")

    solicitacaoDocumento = HiddenField("solicitacaoDocumento")

    solicitacaoHistorico = HiddenField("solicitacaoHistorico")

    tipoSolicitacao = HiddenField("tipoSolicitacao")

    nome = StringField(
        'Nome:',
        render_kw={"placeholder": "Nome"},
        validators = [
            InputRequired(message=('*Campo Requerido')),
            Length(max=200, message='O campo Nome deve ter no máximo %(max)d caracteres')
    ])    

    cpf = StringField(
        'CPF:',
        render_kw={"placeholder": "CPF"},
        validators = [
            InputRequired(message=('*Campo Requerido')),
            Length(min=11, max=11, message='O campo CPF deve ter %(max)d caracteres')
    ])    

    email = StringField(
    'E-mail',
    render_kw={"placeholder": "E-mail"},
    validators= [
        InputRequired(message=('*Campo Requerido')),
        Email(message=('Ops. Não nos parece um e-mail válido.')),
        Length(max=50, message='O campo E-mail deve ter no máximo %(max)d caracteres')
    ])

    endereco = StringField(
        'Endereço:',
        render_kw={"placeholder": "Endereço"},
        validators = [
            InputRequired(message=('*Campo Requerido')),
            Length(max=200, message='O campo Endereço deve ter no máximo %(max)d caracteres')
    ])

    whatsapp = StringField(
        'Whatsapp:',
        render_kw={"placeholder": "Whatsapp"},
        validators = [
            InputRequired(message=('*Campo Requerido')),
            Length(max=15, message='O campo Whatsapp deve ter no máximo %(max)d caracteres')
    ])     