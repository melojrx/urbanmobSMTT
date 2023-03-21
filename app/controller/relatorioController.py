from flask import render_template, flash, request, Response
from flask_login import login_required
from app.relatorios.relatorio import PDF
from ..rotas.relatorioRout import relatorio_bp
from app.models.categoriaModel import Categoria
from app.models.subcategoriaModel import Subcategoria
from app.models.eventoHistoricoModel import EventoHistorico
from app.models.eventoModel import Evento

class eventoSearchController:

    @relatorio_bp.route('/prepareRelatorio', methods=['GET'])
    @login_required
    def prepareRelatorio():

        global listCategoria
        global categoriaSearch
        global dataInicioSearch
        global dataFimSearch

        listCategoria = Categoria.query.filter(Categoria.dataFim.is_(None)).all()
        listEventoHistoricoSearch = None
        categoriaSearch = None
        dataInicioSearch = None
        dataFimSearch = None
        return render_template('relatorio.html', listCategoria=listCategoria, listEventoHistoricoSearch=listEventoHistoricoSearch, categoriaSearch=categoriaSearch, dataInicioSearch=dataInicioSearch, dataFimSearch=dataFimSearch)

    # @relatorio_bp.route('/relatorioSearch', methods=['GET'])
    # @login_required
    # def relatorioSearch():

    #     try:

    #         categoriaSearch = request.args.get('categoriaSearch') 
    #         dataInicioSearch = request.args.get('dataInicioSearch') 
    #         dataFimSearch = request.args.get('dataFimSearch') 

    #         if categoriaSearch == "" and dataInicioSearch == "" and dataFimSearch == "":
    #             listEventoHistoricoSearch = None
    #             flash('Informe pelo menos um critério de pesquisa', 'error')
    #             return render_template('relatorio.html', listCategoria=listCategoria, listEventoHistoricoSearch=listEventoHistoricoSearch)

    #         querySearch = EventoHistorico.query.filter(EventoHistorico.dataFim.is_(None))

    #         if categoriaSearch != "":
    #             querySearch = querySearch.join(EventoHistorico.evento).join(Evento.subcategoria).join(Subcategoria.categoria).filter(Categoria.id == categoriaSearch)

    #         if dataInicioSearch != "" and dataFimSearch != "":
    #             querySearch = querySearch.join(EventoHistorico.evento).filter(Evento.dataInicio >= dataInicioSearch).filter(Evento.dataInicio <= dataFimSearch)
    #         elif dataInicioSearch != "" and dataFimSearch == "":
    #             querySearch = querySearch.join(EventoHistorico.evento).filter(Evento.dataInicio >= dataInicioSearch)
    #         elif dataInicioSearch == "" and dataFimSearch != "":
    #             querySearch = querySearch.join(EventoHistorico.evento).filter(Evento.dataInicio <= dataFimSearch)

    #         listEventoHistoricoSearch = querySearch.order_by(EventoHistorico.dataInicio.desc()).all()

    #         if listEventoHistoricoSearch == []:
    #             listEventoHistoricoSearch = None
    #             flash('A pesquisa não encontrou nenhum resultado', 'error')
    #             return render_template('relatorio.html', listCategoria=listCategoria, listEventoHistoricoSearch=listEventoHistoricoSearch)

    #     except Exception as e:
    #         flash('Erro: {}'.format(e), 'error')

    #     return render_template('relatorio.html', listEventoHistoricoSearch=listEventoHistoricoSearch, listCategoria=listCategoria, categoriaSearch=categoriaSearch, dataInicioSearch=dataInicioSearch, dataFimSearch=dataFimSearch)


    # @relatorio_bp.route('/printPDF/<listEventoHistoricoSearch>', methods=['GET'])
    # @login_required
    # def pritPDF(listEventoHistoricoSearch):
    #     flash('Funcionalidade em Desenvolcimento', 'error')
    #     return ''

    @relatorio_bp.route('/export', methods=['GET'])
    @login_required
    def export():

            categoriaSearch = request.args.get('categoriaSearch') 
            dataInicioSearch = request.args.get('dataInicioSearch') 
            dataFimSearch = request.args.get('dataFimSearch') 
            exportType = request.args.get('exportType') 

            if exportType == None:
                listEventoHistoricoSearch = None
                flash('Informe o tipo de lelatporio PDF ou CSV', 'error')
                return render_template('relatorio.html', listCategoria=listCategoria, listEventoHistoricoSearch=listEventoHistoricoSearch)

            if categoriaSearch == "" and dataInicioSearch == "" and dataFimSearch == "":
                listEventoHistoricoSearch = None
                flash('Informe pelo menos um critério de pesquisa', 'error')
                return render_template('relatorio.html', listCategoria=listCategoria, listEventoHistoricoSearch=listEventoHistoricoSearch)

            querySearch = EventoHistorico.query.filter(EventoHistorico.dataFim.is_(None))

            if categoriaSearch != "":
                querySearch = querySearch.join(EventoHistorico.evento).join(Evento.subcategoria).join(Subcategoria.categoria).filter(Categoria.id == categoriaSearch)

            if dataInicioSearch != "" and dataFimSearch != "":
                querySearch = querySearch.join(EventoHistorico.evento).filter(Evento.dataInicio >= dataInicioSearch).filter(Evento.dataInicio <= dataFimSearch)
            elif dataInicioSearch != "" and dataFimSearch == "":
                querySearch = querySearch.join(EventoHistorico.evento).filter(Evento.dataInicio >= dataInicioSearch)
            elif dataInicioSearch == "" and dataFimSearch != "":
                querySearch = querySearch.join(EventoHistorico.evento).filter(Evento.dataInicio <= dataFimSearch)

            listEventoHistoricoSearch = querySearch.order_by(EventoHistorico.dataInicio.desc()).all()

            if listEventoHistoricoSearch == []:
                listEventoHistoricoSearch = None
                flash('A pesquisa não encontrou nenhum resultado', 'error')

            if exportType == 'CSV':

                csv = 'Usuário,Status,Categoria,Data\n'

                for row in listEventoHistoricoSearch:
                    csv = csv + row.evento.usuario.name + ',' + row.statusEvento.txtStatusEvento + ',' + row.evento.subcategoria.categoria.txtCategoria + ',' + row.evento.dataInicio.strftime('%d/%m/%Y %H:%M') + '\n'

                return Response(
                    csv,
                    mimetype="text/csv",
                    headers={"Content-disposition":
                            "attachment; filename=relatório.csv"})

            elif exportType == 'PDF':
                pdf = PDF()
                pdf.alias_nb_pages()
                pdf.add_page('L')
                page_width = pdf.w - 2 * pdf.l_margin
		
                pdf.set_font('Courier', '', 12)
                
                col_width = page_width/4
                
                pdf.ln(1)
                
                th = pdf.font_size

                pdf.set_fill_color(64,64,64)
                pdf.set_text_color(255,255,255)
                pdf.cell(col_width, th, 'Usuário', border=1, fill=True)
                pdf.cell(col_width, th, 'Status', border=1, fill=True)
                pdf.cell(col_width, th, 'Categoria', border=1, fill=True)
                pdf.cell(col_width, th, 'Data', border=1, fill=True)
                pdf.ln(th)
                pdf.set_text_color(0,0,0)
                pdf.set_fill_color(224,224,224)
                for num, row in enumerate(listEventoHistoricoSearch, start=1):
                    pdf.cell(col_width, th, row.evento.usuario.name, border=1, fill=(num % 2 == 0))
                    pdf.cell(col_width, th, row.statusEvento.txtStatusEvento, border=1, fill=(num % 2 == 0))
                    pdf.cell(col_width, th, row.evento.subcategoria.categoria.txtCategoria, border=1, fill=(num % 2 == 0))
                    pdf.cell(col_width, th, row.evento.dataInicio.strftime('%d/%m/%Y %H:%M'), border=1, fill=(num % 2 == 0))
                    pdf.ln(th)
               
                return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=relatorio.pdf'})





        