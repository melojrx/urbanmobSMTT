from ..database import db
from flask_login import UserMixin


class TipoSolicitacao(db.Model, UserMixin):
    __tablename__ = 'tb_tipo_solicitacao_tis'
    __table_args__ = {"schema":"credencial"}

    tipo_solicitacao_documento_tsd = db.Table('tb_tipo_solicitacao_documento_tsd', db.Model.metadata,
        db.Column('id_tipo_solicitacao_tsd', db.Integer, db.ForeignKey('id_tipo_solicitacao_tis')),
        db.Column('id_documento_tsd', db.Integer, db.ForeignKey('id_documento_doc'))
    )

    id = db.Column('id_tipo_solicitacao_tis', db.Integer, autoincrement=True, primary_key=True)
    txtTipoSolicitacao = db.Column('txt_tipo_solicitacao_tis', db.String(200), nullable=False)
    txtIcone = db.Column('txt_icone_tis', db.String(50), nullable=False, unique=True)
    dataInicio = db.Column('dat_inicio_tis', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_tis', db.DateTime, nullable=True)

    documento = db.relationship("tb_documento_doc",secondary=tipo_solicitacao_documento_tsd)

