from app.models.tipoSolicitacao import TipoSolicitacao
from ..database import db

class Solicitacao(db.Model):
    __tablename__ = 'tb_solicitacao_sol'
    __table_args__ = {"schema":"credencial"}

    id = db.Column('id_solicitacao_sol', db.Integer, autoincrement=True, primary_key=True)
    idTipoSolicitacao = db.Column('id_tipo_solicitacao_sol',db.Integer, db.ForeignKey(TipoSolicitacao.id), nullable=False)
    txtProtocolo = db.Column('txt_protocolo_sol', db.String(50), nullable=False)
    txtCpf = db.Column('txt_cpf_sol', db.String(11), nullable=False)
    txtNome = db.Column('txt_nome_sol', db.String(200), nullable=False)
    txtEmail = db.Column('txt_email_sol', db.String(50), nullable=False)
    txtEndereco = db.Column('txt_endereco_sol', db.String(200), nullable=False)
    txtWhatsapp = db.Column('txt_whatsapp_sol', db.String(15), nullable=False)



    tipoSolicitacao = db.relationship("TipoSolicitacao")
    listSolicitacaoHistorico = db.relationship("SolicitacaoHistorico", back_populates="solicitacao")
    listSolicitacaoDocumento = db.relationship("SolicitacaoDocumento", back_populates="solicitacao")


    def get_id(self):
        return self.id
       
    def set_id(self, id):
        self.id = id

    def get_idTipoSolicitacao(self):
        return self.idTipoSolicitacao
       
    def set_idTipoSolicitacao(self, idTipoSolicitacao):
        self.idTipoSolicitacao = idTipoSolicitacao 

    def get_txtProtocolo(self):
        return self.txtProtocolo
       
    def set_txtProtocolo(self, txtProtocolo):
        self.txtProtocolo = txtProtocolo 

    def get_txtCpf(self):
        return self.txtCpf
       
    def set_txtCpf(self, txtCpf):
        self.txtCpf = txtCpf 

    def get_txtNome(self):
        return self.txtNome
       
    def set_txtNome(self, txtNome):
        self.txtNome = txtNome 

    def get_txtEmail(self):
        return self.txtEmail
       
    def set_txtEmail(self, txtEmail):
        self.txtEmail = txtEmail 

    def get_txtEndereco(self):
        return self.txtEndereco
       
    def set_txtEndereco(self, txtEndereco):
        self.txtEndereco = txtEndereco 

    def get_txtWhatsapp(self):
        return self.txtWhatsapp
       
    def set_txtWhatsapp(self, txtWhatsapp):
        self.txtWhatsapp = txtWhatsapp                         

    def get_listSolicitacaoDocumento(self):
        return self.listSolicitacaoDocumento
       
    def set_listSolicitacaoDocumento(self, listSolicitacaoDocumento):
        self.listSolicitacaoDocumento = listSolicitacaoDocumento 