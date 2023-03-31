import datetime
from ..database import db
from operator import and_
from flask_login import current_user, login_required
from ..enum.statusEnum import StatusEnum
from app.models.solicitacao import Solicitacao
from ..forms.analiseDocumentacaoForm import AnaliseDocumentacaoForm
from .roleRequired import  roles_required
from ..rotas.solicitacaoRout import solicitacao_bp
from ..models.solicitacaoHistorico import SolicitacaoHistorico
from ..models.solicitacaoDocumento import SolicitacaoDocumento
from app.relatorios.relatorio import PDF
from flask import flash, make_response, redirect, render_template, request, url_for, Response


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
                        form = AnaliseDocumentacaoForm(request.form)
                        solicitacaoHistorico = db.session.query(SolicitacaoHistorico).join(Solicitacao).filter(and_(Solicitacao.id==idSolicitacao , SolicitacaoHistorico.dataFim.is_(None))).order_by(SolicitacaoHistorico.id.asc()).first() 
                        listSolicitacaoDocumento = db.session.query(SolicitacaoDocumento).join(Solicitacao).filter(and_(Solicitacao.id==idSolicitacao , SolicitacaoDocumento.dataFim.is_(None))).order_by(SolicitacaoDocumento.id.asc()).all() 
                        #solicitacao = Solicitacao.query.filter(Solicitacao.id == idSolicitacao).first()

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
                        form = AnaliseDocumentacaoForm(request.form)
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

                return redirect(url_for('solicitacao.visualizar', form=form, idSolicitacao=solicitacaoHistorico.solicitacao.id)) 
        
        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/analisar', methods=['POST'])
        def analisar():
                listDocumentos = request.form.getlist('documento')
                #print('listDocumentos', listDocumentos)
                listRadio = [request.form[arg] for arg in listDocumentos]
                #print('listRadio', listRadio)
                listSolicitacaoDocumento = request.form.getlist('idSolicitacaoDocumento')
                #print('listSolicitacaoDocumento', listSolicitacaoDocumento)

                form = AnaliseDocumentacaoForm(request.form)
                idSolicitacaoHistorico = form.idSolicitacaoHistorico.data
                #print('idSolicitacaoHistorico', idSolicitacaoHistorico)
                observacao = form.observacao.data
                #print('observacao', observacao)

                try:

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

                return redirect(url_for('solicitacao.visualizar', form=form, idSolicitacao=solicitacaoHistorico.solicitacao.id)) 
        

        @login_required
        @roles_required('URBANMOB_ADMIN, URBANMOB_GOVERNO')
        @solicitacao_bp.route('/imprimirCredencial/<idSolicitacao>', methods=['GET'])
        def imprimirCredencial(idSolicitacao):

                try:
                        solicitacao = db.session.query(Solicitacao).filter(Solicitacao.id==idSolicitacao).first()

                        pdf = PDF()
                        pdf.alias_nb_pages()
                        pdf.add_page('L')
                                
                        
                        
                        
                        

                        # pdf.set_font('Courier', '', 12)
                        # page_width = pdf.w - 2 * pdf.l_margin
                        # col_width = page_width/4
                        # th = pdf.font_size
                        # pdf.ln(1)
                        # pdf.set_fill_color(64,64,64)
                        # pdf.set_text_color(255,255,255)
                        # pdf.cell(col_width, th, 'Usuário', border=1, fill=True)
                        # pdf.cell(col_width, th, 'Status', border=1, fill=True)
                        # pdf.cell(col_width, th, 'Categoria', border=1, fill=True)
                        # pdf.cell(col_width, th, 'Data', border=1, fill=True)
                        # pdf.ln(th)
                        # pdf.set_text_color(0,0,0)
                        # pdf.set_fill_color(224,224,224)

                
                        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=relatorio.pdf'})

                except Exception as e:
                        flash('Erro: {}'.format(e), 'error')       