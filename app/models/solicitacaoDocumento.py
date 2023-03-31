from app.models.documento import Documento
from ..database import db
from app.models.solicitacao import Solicitacao

class SolicitacaoDocumento(db.Model):
    __tablename__ = 'tb_solicitacao_documento_sdo'
    __table_args__ = {"schema":"credencial"}

    id = db.Column('id_solicitacao_documento_sdo', db.Integer, autoincrement=True, primary_key=True)
    idSolicitacao = db.Column('id_solicitacao_sdo',db.Integer, db.ForeignKey(Solicitacao.id), nullable=False)
    idDocumento = db.Column('id_documento_sdo',db.Integer, db.ForeignKey(Documento.id), nullable=False)
    file = db.Column('img_file_sdo', db.LargeBinary, nullable=False)
    filename = db.Column('txt_filename_sdo', db.String(50), nullable=False)
    txtContenttype = db.Column('txt_contenttype_sdo', db.String(50), nullable=False)
    flgDeferido = db.Column('flg_deferido_sdo', db.Boolean, nullable=True, default=None)
    dataInicio = db.Column('dat_inicio_sdo', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_sdo', db.DateTime, nullable=True)

    solicitacao = db.relationship("Solicitacao", back_populates="listSolicitacaoDocumento") 
    documento = db.relationship("Documento") 

    def get_solicitacao(self):
        return self.solicitacao
       
    def set_solicitacao(self, solicitacao):
        self.solicitacao = solicitacao

    def get_idDocumento(self):
        return self.idDocumento
       
    def set_idDocumento(self, idDocumento):
        self.idDocumento = idDocumento

    def get_file(self):
        return self.file
       
    def set_file(self, file):
        self.file = file

    def get_filename(self):
        return self.filename
       
    def set_filename(self, filename):
        self.filename = filename

    def get_contenttype(self):
        return self.txtContenttype
       
    def set_contenttype(self, txtContenttype):
        self.txtContenttype = txtContenttype

    def get_flgDeferido(self):
        return self.flgDeferido
       
    def set_flgDeferido(self, flgDeferido):
        self.flgDeferido = flgDeferido

    def get_dataInicio(self):
        return self.dataInicio
       
    def set_dataInicio(self, dataInicio):
        self.dataInicio = dataInicio
