from app import app
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1q2w3eadmin@201.49.23.87:5432/postgres'

app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

@app.errorhandler(Exception)
def internal_error(e):
    db.session.rollback()
    return render_template('erro.html', e=e)