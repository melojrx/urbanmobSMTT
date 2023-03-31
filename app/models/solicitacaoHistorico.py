from ..database import db
from ..models.solicitacao import Solicitacao
from ..models.status import Status
from ..models.userModel import User

class SolicitacaoHistorico(db.Model):
    __tablename__ = 'tb_solicitacao_historico_shi'
    __table_args__ = {"schema":"credencial"}

    id = db.Column('id_solicitacao_historico_shi', db.Integer, autoincrement=True, primary_key=True)
    idSolicitacao = db.Column('id_solicitacao_shi',db.Integer, db.ForeignKey(Solicitacao.id), nullable=False)
    idStatus = db.Column('id_status_shi',db.Integer, db.ForeignKey(Status.id), nullable=False)
    idUsuario = db.Column('id_usuario_shi',db.Integer, db.ForeignKey(User.id))
    txtObservacao = db.Column('txt_observacao_shi', db.String(400))
    dataInicio = db.Column('dat_inicio_shi', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_shi', db.DateTime, nullable=True)


    solicitacao = db.relationship("Solicitacao") 
    status = db.relationship("Status")
    # usuario = db.relationship("User")


    def __init__(self, solicitacao, idStatus, idUsuario, txtObservacao, dataInicio):
        self.solicitacao = solicitacao
        self.idStatus = idStatus
        self.idUsuario = idUsuario
        self.txtObservacao = txtObservacao
        self.dataInicio = dataInicio