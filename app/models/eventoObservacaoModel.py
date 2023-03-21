from ..database import db


class EventoObservacao(db.Model):
    __tablename__ = 'tb_evento_observacao_eob'
    __table_args__ = {"schema":"cidade"}
    
    id = db.Column('id_evento_observacao_eob', db.Integer, autoincrement=True, primary_key=True)
    idEventoHistorico = db.Column('id_evento_historico_eob',db.Integer, db.ForeignKey('cidade.tb_evento_historico_ehi.id_evento_historico_ehi'), nullable=False)
    idUsuario = db.Column('id_usuario_eob', db.Integer, db.ForeignKey('cidade.tb_usuario_usu.id_usuario_usu'), nullable=False)
    txtObservacao = db.Column('txt_evento_observacao_eob', db.String, nullable=False)
    dataInicio = db.Column('dat_inicio_eob', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_eob', db.DateTime, nullable=True)

    eventoHistorico = db.relationship("EventoHistorico", back_populates="listObservacao") 
    usuario = db.relationship("User")
    
    def __init__(self, idEventoHistorico, idUsuario, txtObservacao, dataInicio):
        self.idEventoHistorico = idEventoHistorico
        self.idUsuario = idUsuario
        self.txtObservacao = txtObservacao
        self.dataInicio = dataInicio