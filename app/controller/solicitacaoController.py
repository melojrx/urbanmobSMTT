import os
import datetime
import tempfile
from ..database import db
from operator import and_, or_
from ..enum.statusEnum import StatusEnum
from ..enum.tipoSolicitacaoEnum import TipoSolicitacaoEnum
from pyreportjasper import PyReportJasper
from .roleRequired import  roles_required
from app.models.solicitacao import Solicitacao
from ..rotas.solicitacaoRout import solicitacao_bp
from flask_login import current_user, login_required
from ..models.status import Status
from ..models.tipoSolicitacao import TipoSolicitacao
from ..models.solicitacaoHistorico import SolicitacaoHistorico
from ..models.solicitacaoDocumento import SolicitacaoDocumento
from ..forms.analiseDocumentacaoForm import AnaliseDocumentacaoForm
from flask import flash, make_response, redirect, render_template, request, url_for, Response


class solicitacaoController:

        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/prepareSearch', methods=['GET'])
        def prepareSearch():
                
                global ROWS_PER_PAGE 
                ROWS_PER_PAGE = 10

                global listTipoSolicitacao 
                global listStatus
    
                try:
                        page = request.args.get('page', 1, type=int)

                        listStatus = db.session.query(Status).filter(Status.dataFim.is_(None)).all()
                        listTipoSolicitacao = db.session.query(TipoSolicitacao).filter(TipoSolicitacao.dataFim.is_(None)).all() 

                        listSolicitacaoHistorico = db.session.query(SolicitacaoHistorico).join(Status).filter(and_(SolicitacaoHistorico.dataFim.is_(None), or_(Status.id == StatusEnum.AGUARDANDO_ATENDIMENTO.value, Status.id == StatusEnum.REENVIADO.value))).paginate(page=page, per_page=ROWS_PER_PAGE)

                except Exception as e:
                        flash('Erro: {}'.format(e), 'error')                        

                return render_template('listarSolicitacao.html', listSolicitacaoHistorico=listSolicitacaoHistorico, listStatus=listStatus, listTipoSolicitacao=listTipoSolicitacao)
        

        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/search', methods=['GET'])
        def search():
                
                global ROWS_PER_PAGE 
                ROWS_PER_PAGE = 10

                try:
                        page = request.args.get('page', 1, type=int)

                        numProtocoloSearch = request.args.get('numProtocoloSearch')
                        tipoSolicitacaoSearch = request.args.get('tipoSolicitacaoSearch') 
                        statusSearch = request.args.get('statusSearch') 
                        dataInicioSearch = request.args.get('dataInicioSearch') 
                        dataFimSearch = request.args.get('dataFimSearch')


                        # if numProtocoloSearch == "" and statusSearch == "" and tipoSolicitacaoSearch == "" and dataInicioSearch == "" and dataFimSearch == "":
                        #         listSolicitacaoHistorico = None
                        #         flash('Informe pelo menos um critério de pesquisa', 'error')
                        #         return render_template('listarSolicitacao.html', listStatus=listStatus, listTipoSolicitacao=listTipoSolicitacao, listSolicitacaoHistorico=listSolicitacaoHistorico)
                
                        querySearch = SolicitacaoHistorico.query.filter(SolicitacaoHistorico.dataFim.is_(None))

                        if numProtocoloSearch != "":
                                querySearch= querySearch.join(SolicitacaoHistorico.solicitacao).filter(Solicitacao.txtProtocolo == numProtocoloSearch)

                        if tipoSolicitacaoSearch != "":
                                querySearch= querySearch.join(SolicitacaoHistorico.solicitacao).join(TipoSolicitacao).filter(TipoSolicitacao.id == tipoSolicitacaoSearch)

                        if statusSearch != "":
                                querySearch= querySearch.join(SolicitacaoHistorico.status).filter(Status.id == statusSearch)

                        if dataInicioSearch != "" and dataFimSearch != "":
                                querySearch = querySearch.filter(SolicitacaoHistorico.dataInicio >= dataInicioSearch).filter(SolicitacaoHistorico.dataInicio <= dataFimSearch)
                        elif dataInicioSearch != "" and dataFimSearch == "":
                                querySearch = querySearch.filter(SolicitacaoHistorico.dataInicio >= dataInicioSearch)
                        elif dataInicioSearch == "" and dataFimSearch != "":
                                querySearch = querySearch.filter(SolicitacaoHistorico.dataInicio <= dataFimSearch)

                        listSolicitacaoHistorico = querySearch.order_by(SolicitacaoHistorico.dataInicio.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)

                        if listSolicitacaoHistorico.items == []:
                                listSolicitacaoHistorico = None
                                flash('A pesquisa não encontrou nenhum resultado', 'error')
                                return render_template('listarSolicitacao.html', listSolicitacaoHistorico=listSolicitacaoHistorico, listStatus=listStatus,listTipoSolicitacao=listTipoSolicitacao)
                        
                except Exception as e:
                        flash('Erro: {}'.format(e), 'error')

                return render_template('listarSolicitacao.html', listSolicitacaoHistorico=listSolicitacaoHistorico, listStatus=listStatus, listTipoSolicitacao=listTipoSolicitacao)
        

        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/visualizar/<idSolicitacao>', methods=['GET'])
        def visualizar(idSolicitacao):
                
                try:
                        form = AnaliseDocumentacaoForm(request.form)
                        solicitacaoHistorico = db.session.query(SolicitacaoHistorico).join(Solicitacao).filter(and_(Solicitacao.id==idSolicitacao , SolicitacaoHistorico.dataFim.is_(None))).order_by(SolicitacaoHistorico.dataInicio.desc()).first() 
                        listSolicitacaoDocumento = db.session.query(SolicitacaoDocumento).join(Solicitacao).filter(and_(Solicitacao.id==idSolicitacao , SolicitacaoDocumento.dataFim.is_(None))).order_by(SolicitacaoDocumento.id.asc()).all() 
                        # solicitacao = Solicitacao.query.filter(Solicitacao.id == idSolicitacao).first()

                except Exception as e:
                        flash('Erro: {}'.format(e), 'error')
                        
                return render_template('visualizarDocumentos.html', form=form, solicitacaoHistorico=solicitacaoHistorico, listSolicitacaoDocumento=listSolicitacaoDocumento)        
        

        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/open/<idSolicitacaoDocumento>', methods=['GET'])
        def open(idSolicitacaoDocumento):
                
                solicitacaoDocumento = db.session.query(SolicitacaoDocumento).filter(SolicitacaoDocumento.id==idSolicitacaoDocumento).first() 
                response = make_response(solicitacaoDocumento.file)
                response.headers['Content-Type'] = solicitacaoDocumento.txtContenttype
                response.headers['Content-Disposition'] = \
                '_blank; filename=%s.pdf' % solicitacaoDocumento.documento.txtDocumento
                return response  

        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/atender/<idSolicitacaoHistorico>', methods=['GET'])
        def atender(idSolicitacaoHistorico):

                try:
                        # form = AnaliseDocumentacaoForm(request.form)
                        data = datetime.datetime.now()
                        solicitacaoHistorico = db.session.query(SolicitacaoHistorico).filter(SolicitacaoHistorico.id==idSolicitacaoHistorico).first() 
                        solicitacaoHistorico.dataFim = data
                        
                        newSolicitacaoHistorico = SolicitacaoHistorico(solicitacaoHistorico.solicitacao, StatusEnum.EM_ANDAMENTO.value, current_user.id, None, data)
                        db.session.add(newSolicitacaoHistorico)
                        db.session.commit()
                        flash('Solicitação alterada para: {status}'.format(status = StatusEnum.EM_ANDAMENTO.name), 'sucess')
                except Exception as e:
                        db.session.rollback
                        flash('Erro: {}'.format(e), 'error') 

                return redirect(url_for('solicitacao.visualizar', idSolicitacao=solicitacaoHistorico.solicitacao.id)) 
        
        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/analisar', methods=['POST'])
        def analisar():

                try:

                        form = AnaliseDocumentacaoForm(request.form)
                        idSolicitacaoHistorico = form.idSolicitacaoHistorico.data
                        idSolicitacao = form.idSolicitacao.data
                        #print('idSolicitacaoHistorico', idSolicitacaoHistorico)
                        observacao = form.observacao.data
                        #print('observacao', observacao)
                        listDocumentos = request.form.getlist('documento')
                        # print('listDocumentos', listDocumentos)
                        listRadio = [request.form[arg] for arg in listDocumentos]
                        # print('listRadio', listRadio)
                        listSolicitacaoDocumento = request.form.getlist('idSolicitacaoDocumento')
                        #print('listSolicitacaoDocumento', listSolicitacaoDocumento)



                        resultadoAnalise = True

                        for sd, r in zip(listSolicitacaoDocumento, listRadio):
                                solicitacaoDocumento = db.session.query(SolicitacaoDocumento).filter(SolicitacaoDocumento.id==sd).first() 
                                solicitacaoDocumento.flgDeferido = r=='true'
                                db.session.add(solicitacaoDocumento)

                                if r == 'false':
                                        resultadoAnalise = False

                        data = datetime.datetime.now()
                        solicitacaoHistorico = db.session.query(SolicitacaoHistorico).filter(SolicitacaoHistorico.id==idSolicitacaoHistorico).first() 
                        solicitacaoHistorico.dataFim = data
                        
                        newSolicitacaoHistorico = SolicitacaoHistorico(solicitacaoHistorico.solicitacao, StatusEnum.DEFERIDO.value if resultadoAnalise else StatusEnum.INDEFERIDO.value, current_user.id, observacao, data)
                        db.session.add(newSolicitacaoHistorico)
                        db.session.commit()                        

                except Exception as e:
                        db.session.rollback
                        flash('Erro: {}'.format(e), 'error') 
                        return redirect(url_for('solicitacao.visualizar', idSolicitacao=idSolicitacao)) 

                return redirect(url_for('solicitacao.visualizar', idSolicitacao=solicitacaoHistorico.solicitacao.id)) 
        

        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/imprimirCredencial/<idSolicitacao>', methods=['GET'])
        def imprimirCredencial(idSolicitacao):

                try:
                        solicitacao = db.session.query(Solicitacao).filter(Solicitacao.id==idSolicitacao).first()
                        emissao = datetime.datetime.now()
                        validade =  emissao + datetime.timedelta(days=365*5)
                        brasao = os.path.join(os.path.dirname(__file__), '..', 'static', 'img','pdf', 'republicaFederativaBrasil.jpg')
           
                        qr = solicitacao.txtCpf

                        if solicitacao.tipoSolicitacao.id == TipoSolicitacaoEnum.IDOSO.value:

                                parametros = {'emissao': emissao.strftime('%d/%m/%Y'), 'unidadeUF': 'CE', 'municipio': 'Fortaleza', 'orgao': 'SMTT',
                                        'resolucao' : solicitacao.tipoSolicitacao.txtResolucao,
                                        'tipoSolicitacao' : solicitacao.tipoSolicitacao.txtTipoSolicitacao,
                                        'validade': validade.strftime('%d/%m/%Y'), 'brasao': brasao, 'registro': solicitacao.txtProtocolo, 'qr': qr}

                                input_file = os.path.join(os.path.dirname(__file__), '..', 'static', 'report','credencialIdoso.jrxml')
                        
                        elif solicitacao.tipoSolicitacao.id == TipoSolicitacaoEnum.DEFICIENTE.value:
                                deficienteIcon = os.path.join(os.path.dirname(__file__), '..', 'static', 'img','pdf', 'deficiente.jpg')

                                parametros = {'emissao': emissao.strftime('%d/%m/%Y'), 'unidadeUF': 'CE', 'municipio': 'Fortaleza', 'orgao': 'SMTT', 
                                        'deficienteIcon': deficienteIcon, 'resolucao' : solicitacao.tipoSolicitacao.txtResolucao,
                                        'validade': validade.strftime('%d/%m/%Y'), 'brasao': brasao, 'registro': solicitacao.txtProtocolo, 'qr': qr}

                                input_file = os.path.join(os.path.dirname(__file__), '..', 'static', 'report','credencialDeficiente.jrxml')
                        else:
                                return render_template('erro.html', erro='Em desenvolvimento')

                        output_file = tempfile.NamedTemporaryFile(suffix='.pdf').name
                        pyreportjasper = PyReportJasper()
                        pyreportjasper.config(input_file, output_file, output_formats=["pdf"], parameters=parametros)
                        pyreportjasper.process_report()

                        with open(output_file, 'rb') as f:
                                 pdf_content = f.read()

                        return Response(pdf_content, mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=' + solicitacao.txtProtocolo + '.pdf'})

                except Exception as e:
                        flash('Erro: {}'.format(e), 'error') 

        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/finalizar/<idSolicitacaoHistorico>', methods=['GET'])
        def finalizar(idSolicitacaoHistorico):

                try:
                        form = AnaliseDocumentacaoForm(request.form)
                        data = datetime.datetime.now()
                        solicitacaoHistorico = db.session.query(SolicitacaoHistorico).filter(SolicitacaoHistorico.id==idSolicitacaoHistorico).first() 
                        solicitacaoHistorico.dataFim = data
                        
                        newSolicitacaoHistorico = SolicitacaoHistorico(solicitacaoHistorico.solicitacao, StatusEnum.FINALIZADO.value, current_user.id, None, data)
                        db.session.add(newSolicitacaoHistorico)
                        db.session.commit()
                        flash('Solicitação alterada para: {status}'.format(status = StatusEnum.FINALIZADO.name), 'sucess')
                except Exception as e:
                        db.session.rollback
                        flash('Erro: {}'.format(e), 'error') 

                return redirect(url_for('solicitacao.prepareSearch'))   
                            
        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/estatisticas', methods=['GET'])
        def estatisticas():
                flash('Funcionalidade em Desenvolvimento', 'sucess')
                return redirect(url_for('solicitacao.prepareSearch'))
        
        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/relatorios', methods=['GET'])
        def relatorios():
                flash('Funcionalidade em Desenvolvimento', 'sucess')
                return redirect(url_for('solicitacao.prepareSearch'))
        
        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/avisos', methods=['GET'])
        def avisos():
                flash('Funcionalidade em Desenvolvimento', 'sucess')
                return redirect(url_for('solicitacao.prepareSearch'))