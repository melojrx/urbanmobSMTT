from ..database import db
from operator import and_
from base64 import b64encode
from flask_login import login_required

from app.models.solicitacao import Solicitacao
from .roleRequired import  roles_required
from ..rotas.solicitacaoRout import solicitacao_bp
from ..models.solicitacaoHistorico import SolicitacaoHistorico
from ..models.solicitacaoDocumento import SolicitacaoDocumento
from flask import flash, redirect, render_template, request, url_for


class solicitacaoController:
    
        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/listar', methods=['GET', 'POST'])
        def listar():
                
                try:
                        listSolicitacaoHistorico = SolicitacaoHistorico.query.filter(SolicitacaoHistorico.dataFim.is_(None)).order_by(SolicitacaoHistorico.dataInicio.desc()).limit(10).all()
                
                except Exception as e:
                        flash('Erro: {}'.format(e), 'error')
                        
                return render_template('listarSolicitacao.html', listSolicitacaoHistorico=listSolicitacaoHistorico)
        

        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/visualizar/<idSolicitacao>', methods=['POST'])
        def visualizar(idSolicitacao):
                
                try:
                        print(request.method)

                        listSolicitacaoDocumento = db.session.query(SolicitacaoDocumento).join(Solicitacao).filter(and_(Solicitacao.id==idSolicitacao , SolicitacaoDocumento.dataFim.is_(None))).order_by(SolicitacaoDocumento.id.asc()).all() 

                        for t in listSolicitacaoDocumento:
                                t.fileBase64 = b64encode(t.file).decode()

                except Exception as e:
                        flash('Erro: {}'.format(e), 'error')
                        
                return render_template('visualizarDocumentos.html', listSolicitacaoDocumento=listSolicitacaoDocumento)        