from wtforms import Form, RadioField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import (DataRequired, Email, EqualTo, InputRequired, Length)
class AnaliseDocumentacaoForm(Form):

    analise = RadioField('Deferir Documento?', 
                         validators=[DataRequired()], 
                         choices=[(True,'Sim'),(False,'Não')])
    
    observacao = TextAreaField('Observação', validators=[DataRequired()])
    
    documento = HiddenField("documento")

    idSolicitacaoDocumento = HiddenField("idSolicitacaoDocumento")

    idSolicitacaoHistorico = HiddenField("idSolicitacaoHistorico")

    idSolicitacao = HiddenField("idSolicitacao")

    submit = SubmitField('Cadastrar')