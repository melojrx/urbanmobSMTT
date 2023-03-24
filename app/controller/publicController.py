from ..rotas.publicRout import public_bp
from ..models.tipoSolicitacao import TipoSolicitacao
from flask import flash, render_template

class publicController:

    @public_bp.route('/')
    def home():
            return render_template('index.html')
    
    @public_bp.route('/cidadao')
    def cidadao():
            
        ##global listTipoSolicitacao

        try:
                listTipoSolicitacao = TipoSolicitacao.query.filter( TipoSolicitacao.dataFim.is_(None)).order_by(TipoSolicitacao.txtTipoSolicitacao.desc()).all()
                print(listTipoSolicitacao)
        except Exception as e:
                flash('Erro: {}'.format(e), 'error')
                
        return render_template('cidadao.html', listTipoSolicitacao=listTipoSolicitacao)
    
    @public_bp.route('/tipoSolicitacao/<tipo_solicitacao>')
    def selecionarTipoSolicitacao(tipo_solicitacao):
        print(tipo_solicitacao)

        tipoSolicitacao= TipoSolicitacao.query.filter(TipoSolicitacao.id == tipo_solicitacao)
        listDocumento = TipoSolicitacao.query.filter( TipoSolicitacao.dataFim.is_(None)).order_by(TipoSolicitacao.txtTipoSolicitacao.desc()).all()

        return render_template('cadastrarSolicitacao.html',tipoSolicitacao=tipoSolicitacao) ##, listTipoSolicitacao=listTipoSolicitacao)
