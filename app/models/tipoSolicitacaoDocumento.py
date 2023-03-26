from ..database import db
from ..models.tipoSolicitacao import TipoSolicitacao
from ..models.documento import Documento


class TipoSolicitacaoDocumento(db.Model):
    __tablename__ = 'tb_tipo_solicitacao_documento_tsd'
    __table_args__ = {"schema":"credencial"}

    id = db.Column('id_tipo_solicitacao_documento_tsd', db.Integer, autoincrement=True, primary_key=True)
    idTipoSolicitacao = db.Column('id_tipo_solicitacao_tsd',db.Integer, db.ForeignKey(TipoSolicitacao.id), nullable=False)
    idDocumento = db.Column('id_documento_tsd',db.Integer, db.ForeignKey(Documento.id), nullable=False)
    dataInicio = db.Column('dat_inicio_tsd', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_tsd', db.DateTime, nullable=True)

    tipoSolicitacao = db.relationship(TipoSolicitacao)
    documento = db.relationship(Documento)