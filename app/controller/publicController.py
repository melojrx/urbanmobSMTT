from ..rotas.publicRout import public_bp
from flask import flash, render_template
from ..models.tipoSolicitacao import TipoSolicitacao
from app.models.tipoSolicitacaoDocumento import TipoSolicitacaoDocumento

class publicController:

    @public_bp.route('/')
    def home():
            return render_template('index.html')
    
    @public_bp.route('/cidadao')
    def cidadao():
            
        ##global listTipoSolicitacao

        try:
                listTipoSolicitacao = TipoSolicitacao.query.filter( TipoSolicitacao.dataFim.is_(None)).order_by(TipoSolicitacao.txtTipoSolicitacao.desc()).all()

        except Exception as e:
                flash('Erro: {}'.format(e), 'error')
                
        return render_template('cidadao.html', listTipoSolicitacao=listTipoSolicitacao)
    
    @public_bp.route('/tipoSolicitacao/<tipo_solicitacao>')
    def selecionarTipoSolicitacao(tipo_solicitacao):

        listTipoSolicitacaoDocumento = TipoSolicitacaoDocumento.query.filter(TipoSolicitacaoDocumento.idTipoSolicitacao == tipo_solicitacao)
        tipoSolicitacao = listTipoSolicitacaoDocumento.first().tipoSolicitacao
 
        return render_template('cadastrarSolicitacao.html', tipoSolicitacao=tipoSolicitacao, listTipoSolicitacaoDocumento=listTipoSolicitacaoDocumento)
