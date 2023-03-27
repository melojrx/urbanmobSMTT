from ..database import db
from flask_login import login_required
from roleRequired import  roles_required
from ..rotas.solicitacaoRout import solicitacao_bp
from ..models.solicitacaoHistorico import SolicitacaoHistorico
from flask import flash, redirect, render_template, request, url_for


class solicitacaoController:
    
        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/listar')
        def listar():
                
                try:
                        listSolicitacaoHistorico = SolicitacaoHistorico.query.filter(SolicitacaoHistorico.dataFim.is_(None)).order_by(SolicitacaoHistorico.dataInicio.desc()).limit(10).all()
                
                except Exception as e:
                        flash('Erro: {}'.format(e), 'error')
                        
                return render_template('listarSolicitacao.html', listSolicitacaoHistorico=listSolicitacaoHistorico)