import datetime
from ..database import db
from operator import and_
from flask_login import current_user, login_required
from ..enum.statusEnum import StatusEnum
from app.models.solicitacao import Solicitacao
from .roleRequired import  roles_required
from ..rotas.solicitacaoRout import solicitacao_bp
from ..models.solicitacaoHistorico import SolicitacaoHistorico
from ..models.solicitacaoDocumento import SolicitacaoDocumento
from flask import flash, make_response, redirect, render_template, request, url_for


class solicitacaoController:
    
        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/listar', methods=['GET'])
        def listar():
                
                try:
                        listSolicitacaoHistorico = SolicitacaoHistorico.query.filter(SolicitacaoHistorico.dataFim.is_(None)).order_by(SolicitacaoHistorico.dataInicio.desc()).limit(10).all()
                
                except Exception as e:
                        flash('Erro: {}'.format(e), 'error')
                        
                return render_template('listarSolicitacao.html', listSolicitacaoHistorico=listSolicitacaoHistorico)
        

        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/visualizar/<idSolicitacao>', methods=['GET'])
        def visualizar(idSolicitacao):
                
                try:
                        listSolicitacaoDocumento = db.session.query(SolicitacaoDocumento).join(Solicitacao).filter(and_(Solicitacao.id==idSolicitacao , SolicitacaoDocumento.dataFim.is_(None))).order_by(SolicitacaoDocumento.id.asc()).all() 

                except Exception as e:
                        flash('Erro: {}'.format(e), 'error')
                        
                return render_template('visualizarDocumentos.html', listSolicitacaoDocumento=listSolicitacaoDocumento)        
        

        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/open/<idSolicitacaoDocumento>', methods=['GET'])
        def open(idSolicitacaoDocumento):
                
                solicitacaoDocumento = db.session.query(SolicitacaoDocumento).filter(SolicitacaoDocumento.id==idSolicitacaoDocumento).first() 
                response = make_response(solicitacaoDocumento.file)
                response.headers['Content-Type'] = 'application/pdf'
                response.headers['Content-Disposition'] = \
                '_blank; filename=%s.pdf' % 'yourfilename'
                return response  

        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/atender/<idSolicitacaoHistorico>', methods=['GET'])
        def atender(idSolicitacaoHistorico):

                try:
                        data = datetime.datetime.now()
                        solicitacaoHistorico = db.session.query(SolicitacaoHistorico).filter(SolicitacaoHistorico.id==idSolicitacaoHistorico).first() 
                        solicitacaoHistorico.dataFim = data
                        
                        newSolicitacaoHistorico = SolicitacaoHistorico(solicitacaoHistorico.solicitacao, StatusEnum.EM_ANDAMENTO.value, current_user.id, data)
                        db.session.add(newSolicitacaoHistorico)
                        db.session.commit()
                        flash('Solicitação alterada para: {status}'.format(status = StatusEnum.EM_ANDAMENTO.name), 'sucess')
                except Exception as e:
                        db.session.rollback
                        flash('Erro: {}'.format(e), 'error') 

                return redirect(url_for('solicitacao.visualizar', idSolicitacao=solicitacaoHistorico.solicitacao.id)) 