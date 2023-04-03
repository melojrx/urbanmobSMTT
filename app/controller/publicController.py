import datetime
from ..database import db
from ..rotas.publicRout import public_bp
from flask import flash, render_template, request
from ..enum.statusEnum import StatusEnum
from ..models.solicitacao import Solicitacao
from ..models.tipoSolicitacao import TipoSolicitacao
from ..models.solicitacaoHistorico import SolicitacaoHistorico
from ..models.solicitacaoDocumento import SolicitacaoDocumento
from ..models.tipoSolicitacaoDocumento import TipoSolicitacaoDocumento
from ..forms.solicitacaoDocumentoForm import SolicitacaoDocumentoForm
from ..forms.consultarProtocoloForm import ConsultarProtocoloForm

class publicController:

        @public_bp.route('/')
        def home():
                return render_template('index.html')
        
        @public_bp.route('/cidadao')
        def cidadao():
                
                try:
                        listTipoSolicitacao = TipoSolicitacao.query.filter( TipoSolicitacao.dataFim.is_(None)).order_by(TipoSolicitacao.txtTipoSolicitacao.desc()).all()

                except Exception as e:
                        flash('Erro: {}'.format(e), 'error')
                        
                return render_template('cidadao.html', listTipoSolicitacao=listTipoSolicitacao)
        
        @public_bp.route('/tipoSolicitacao/<tipo_solicitacao>')
        def selecionarTipoSolicitacao(tipo_solicitacao):

                listTipoSolicitacaoDocumento = TipoSolicitacaoDocumento.query.filter(TipoSolicitacaoDocumento.idTipoSolicitacao == tipo_solicitacao)
                tipoSolicitacao = listTipoSolicitacaoDocumento.first().tipoSolicitacao
                documento = listTipoSolicitacaoDocumento.first().documento
                form = SolicitacaoDocumentoForm(request.form)
                form.tipoSolicitacao.data = tipo_solicitacao
                return render_template('cadastrarSolicitacao.html', tipoSolicitacao=tipoSolicitacao, listTipoSolicitacaoDocumento=listTipoSolicitacaoDocumento, form=form)
        

        @public_bp.route('/cadastrar', methods=['POST'])
        def cadastrar():

                try:

                        form = SolicitacaoDocumentoForm(request.form)

                        idTipoSolicitacao = form.tipoSolicitacao.data

                        dataInicio = datetime.datetime.now()
                        txtProtocolo = str(dataInicio.year) + str(dataInicio.day) + str(dataInicio.month) + str(dataInicio.hour) + str(dataInicio.minute) + str(dataInicio.second)

                        solicitacao = Solicitacao()
                        solicitacao.set_idTipoSolicitacao(idTipoSolicitacao)

                        listSolicitacaoDocumento = []
                        
                        listDocumentos = request.form.getlist('documento')
                        listFiles = request.files.getlist('file')

                        for documento, file in zip(listDocumentos, listFiles):
                                solicitacaoDocumento = SolicitacaoDocumento()
                                solicitacaoDocumento.set_solicitacao(solicitacao)
                                solicitacaoDocumento.set_idDocumento(documento)
                                solicitacaoDocumento.set_file(file.read())
                                solicitacaoDocumento.set_filename(file.filename)
                                solicitacaoDocumento.set_contenttype(file.content_type)
                                solicitacaoDocumento.set_dataInicio(dataInicio)
                                listSolicitacaoDocumento.append(solicitacaoDocumento)

                        solicitacao.set_txtProtocolo(txtProtocolo)
                        solicitacao.set_txtCpf(form.cpf.data)
                        solicitacao.set_txtNome(form.nome.data)
                        solicitacao.set_txtEmail(form.email.data)
                        solicitacao.set_txtEndereco(form.endereco.data)
                        solicitacao.set_txtWhatsapp(form.whatsapp.data)
                        solicitacao.set_listSolicitacaoDocumento(listSolicitacaoDocumento)

                        solicitacaoHistorico = SolicitacaoHistorico(solicitacao, StatusEnum.AGUARDANDO_ATENDIMENTO.value, None, None, dataInicio)

                        db.session.add(solicitacao)
                        db.session.add(solicitacaoHistorico)
                        db.session.commit()
                        flash('Solicitação cadastrada com sucesso', 'sucess')
                except Exception as e:
                       db.session.rollback
                       flash('Erro: {}'.format(e), 'error')
                 
                return render_template('protocolo.html', protocolo=solicitacao.get_txtProtocolo(), data=dataInicio)
        
        @public_bp.route('/consultarProtocolo' , methods=['GET', 'POST'])
        def consultarProtocolo():

                form = ConsultarProtocoloForm(request.form)
                if request.method == 'POST': 
                        try:
                                numeroProtocolo = form.numeroProtocolo.data
                                solicitacao= db.session.query(Solicitacao).join(SolicitacaoHistorico).filter(Solicitacao.txtProtocolo==numeroProtocolo).order_by(SolicitacaoHistorico.dataInicio.asc()).first() 
                                return render_template('consultarProtocolo.html', form=form, solicitacao=solicitacao)
                        except Exception as e:
                                flash('Erro: {}'.format(e), 'error')     
                else:
                        return render_template('consultarProtocolo.html', form=form, solicitacao=None)
        
