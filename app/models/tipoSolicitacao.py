from ..database import db
from flask_login import UserMixin


class TipoSolicitacao(db.Model, UserMixin):
    __tablename__ = 'tb_tipo_solicitacao_tis'
    __table_args__ = {"schema":"credencial"}

    id = db.Column('id_tipo_solicitacao_tis', db.Integer, autoincrement=True, primary_key=True)
    txtTipoSolicitacao = db.Column('txt_tipo_solicitacao_tis', db.String(200), nullable=False)
    txtIcone = db.Column('txt_icone_tis', db.String(50), nullable=False, unique=True)
    dataInicio = db.Column('dat_inicio_tis', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_tis', db.DateTime, nullable=True)

