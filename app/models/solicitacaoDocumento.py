from ..database import db
from app.models.solicitacao import Solicitacao

class SolicitacaoDocumento(db.Model):
    __tablename__ = 'tb_solicitacao_documento_sdo'
    __table_args__ = {"schema":"credencial"}

    id = db.Column('id_solicitacao_documento_sdo', db.Integer, autoincrement=True, primary_key=True)
    idSolicitacao = db.Column('id_solicitacao_sdo',db.Integer, db.ForeignKey(Solicitacao.id), nullable=False)
    file = db.Column('img_file_sdo', db.LargeBinary, nullable=False)
    dataInicio = db.Column('dat_inicio_sdo', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_sdo', db.DateTime, nullable=True)

    solicitacao = db.relationship("Solicitacao", back_populates="listSolicitacaoDocumento") 

    def get_solicitacao(self):
        return self.solicitacao
       
    def set_solicitacao(self, solicitacao):
        self.solicitacao = solicitacao

    def get_file(self):
        return self.file
       
    def set_file(self, file):
        self.file = file

    def get_dataInicio(self):
        return self.dataInicio
       
    def set_dataInicio(self, dataInicio):
        self.dataInicio = dataInicio
