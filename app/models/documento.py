from ..database import db
from flask_login import UserMixin

class Documento(db.Model, UserMixin):
    __tablename__ = 'tb_documento_doc'
    __table_args__ = {"schema":"credencial"}

    id = db.Column('id_documento_doc', db.Integer, autoincrement=True, primary_key=True)
    txtdocumento= db.Column('txt_documento_doc', db.String(200), nullable=False)
    dataInicio = db.Column('dat_inicio_doc', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_doc', db.DateTime, nullable=True)
