from ..database import db
from ..rotas.solicitacaoRout import solicitacao_bp
from ..models.solicitacao import Solicitacao
from flask import flash, redirect, render_template, request, url_for


class solicitacaoController:
    pass

        # @solicitacao_bp.route('/listar')
        # def listar():
                
        #         try:
        #                 listSolicitacao = Solicitacao.query.order_by(Solicitacao.txtTipoSolicitacao.desc()).all()

        #         except Exception as e:
        #                 flash('Erro: {}'.format(e), 'error')
                        
        #         return render_template('cidadao.html', listTipoSolicitacao=listTipoSolicitacao)