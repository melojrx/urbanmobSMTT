from ..database import db

class Status(db.Model):
    __tablename__ = 'tb_status_sta'
    __table_args__ = {"schema":"credencial"}

    id = db.Column('id_status_sta', db.Integer, autoincrement=True, primary_key=True)
    txtStatus = db.Column('txt_status_sta', db.String(200), nullable=False)
    dataInicio = db.Column('dat_inicio_sta', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_sta', db.DateTime, nullable=True)