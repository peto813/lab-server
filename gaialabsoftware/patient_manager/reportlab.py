# -*- coding: utf-8 -*-
import decimal
from io import BytesIO
#from django.conf import settings
from reportlab.lib.pagesizes import letter, A4, landscape, portrait
from django.http import HttpResponse
#from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch, cm, mm
from reportlab.platypus import Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, BaseDocTemplate, PageBreak,NextPageTemplate,FrameBreak, SimpleDocTemplate, Frame, Table, TableStyle, Spacer, PageTemplate
from reportlab.lib import colors
from functools import partial

def facturaGenerator(request, factura):
	D = decimal.Decimal
	cantida_cuentas = len(tableList)
	#BUILD RESPONSE
	#fecha_emision = timezone.now().date()
	#response = HttpResponse( content_type='application/pdf' )
	#filename = 'datosbancarios%s%s' %( request.user.condominio.nombre, fecha_emision )
	#response[ 'Content-Disposition' ] = 'attachment; filename="%s.pdf"' %( filename )
	#BUFFER
	buff = BytesIO()
	doc = BaseDocTemplate(buff, pagesize = letter, topMargin=0.5*inch, bottomMargin=0.5*inch, rightMargin=0.5*inch, leftMargin=0.5*inch )
	relacion_data_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height-(1*inch), id='relacion_data',showBoundary=1)
	doc.addPageTemplates(
		[
		PageTemplate(
			frames=[
			relacion_data_frame,
			],
			onPage = partial(static_elements, request = request, cantida_cuentas = cantida_cuentas)
			),
		]
		)
	#doc =  BaseDocTemplate(buff,pagesize=letter,pageTemplates=[],showBoundary=0,leftMargin=0.5*inch,rightMargin=0.5*inch,topMargin=0.5*inch,bottomMargin=0.5*inch,allowSplitting=0,title=None,author=None,_pageBreakQuick=1,encrypt=None)
	

	#STYLER
	#styles = getSampleStyleSheet()
	story = []

	#TABLE HEADER
	styles = getSampleStyleSheet()
	headerStyle = styles['h6']
	headerStyle.alignment = TA_CENTER
	#NEED DYNAMIC HEADERS
	#print tableList
	# relacion_list_header = []
	bank_list = []
	# all_keys = list(set().union(*(d.keys() for d in tableList)))
	# for column in all_keys:
	# 	relacion_list_header.append(Paragraph(str(column), headerStyle))
	# relacion_list.append(relacion_list_header)
	banco = Paragraph('''Banco''', headerStyle)
	nro_cuenta = Paragraph('''Numero de Cuenta''', headerStyle)
	info_adicional = Paragraph('''Informacion Adicional''', headerStyle)
	# pagos = Paragraph('''Abonos''', headerStyle)
	# porcentaje = Paragraph('''Alicuota''', headerStyle)
	# cuota = Paragraph('''Cuota''', headerStyle)
	# total = Paragraph('''Total''', headerStyle)
	header_list = [ banco, nro_cuenta, info_adicional ]
	# for key,value in tableList[0].iteritems():
	# 	if not key in ['inmueble', 'abonos', 'alicuota', 'porcentaje', 'total', 'deuda_previa', 'residente']:
	# 		print key
	# 		relacion_list.insert(4,value)

	#APPEND FIRST ROW
	bank_list.append(header_list)
	#print header_list

	#APPEND data
	styles = getSampleStyleSheet()
	dataStyle = styles['Normal']
	dataStyle.alignment = TA_CENTER
	dataStyle.fontSize = 6
	for row in tableList:
		banco = Paragraph( str(row['banco']), dataStyle)
		nro_cuenta = Paragraph( str(row['numero_de_cuenta']), dataStyle)
		info_adicional = Paragraph(str(row['informacion_adicional']), dataStyle)
		row_data = [ banco, nro_cuenta, info_adicional ]
		bank_list.append(row_data)

	table = Table(bank_list, colWidths = None, rowHeights=None, style=None, splitByRow=1,repeatRows=1, repeatCols=0, rowSplitRange=None, spaceBefore=None, spaceAfter=None)

	LIST_STYLE = TableStyle(
        [('LINEBELOW', ( 0,  1), ( -1, -1 ), 0.3, colors.black),
        #('BACKGROUND', ( 0, 1 ), ( -1,  1 ),colors.Color(red=(244.0/255),green=(243.0/255),blue=(242.0/255))),
        #('BACKGROUND', ( 0, -1 ), ( -1,  -1 ),colors.Color(red=(244.0/255),green=(243.0/255),blue=(242.0/255))),
        # ('LINEBELOW', ( 0,  0), ( -1, -20 ), 1, colors.black),
        #('LINEBELOW', ( 0,  0), ( -1, -20 ), 0.3, colors.black),
        ('BACKGROUND',(0, 0),( -1, 0 ),colors.gold),
        # ('ALIGN', (0,0), (-2,-1), 'LEFT'),
        # ('ALIGN', (1,0), (-1,-1), 'RIGHT')
        ]
        )
	table.setStyle(LIST_STYLE)
	story.append(table)
	#story.append(FrameBreak())


	#a= Table([[1, 2, 3],[4, 'foo', 6],[7, 8, 'bar'],])
	# logo_path = '/tucondominioaldia/usuario/pdfs/pdflogo.png'
	# logo = Image(logo_path, width= 3.5 *inch, height= 0.6 *inch)
	# story.append(logo)
	# #table = Table(total_a_pagar, colWidths=[1.875*inch,1.875*inch], rowHeights=None, style=None, splitByRow=1,repeatRows=0, repeatCols=0, rowSplitRange=None, spaceBefore=None,spaceAfter=None)
	#story.append(a)
	doc.build(story)
	#response.write(buff.getvalue())
	#buff.close()
	return buff

def static_elements(canvas, doc, request, cantida_cuentas):
	#page number

	if cantida_cuentas >1:
		text= 'Por favor hacer depositos en cualquiera de las siguientes cuentas'
	else:
		text = 'Por favor hacer los depositos en la siguiente cuenta'
	
	canvas.drawCentredString(doc.width/2, doc.height-(0.25*inch), text)

	canvas.saveState()
    #HEADER
	# canvas.setLineWidth(.6)
	# canvas.line(0*inch, 10.5*inch,8.5*inch,10.5*inch)
	styles = getSampleStyleSheet()
	styles1 = styles['Normal']
	styles1.leading = 12
	styles.fontSize = 35
	P = Paragraph('''
        <para alignment = "left"><font name="Times-Roman">
        %s<br/>
        RIF: %s
        </font></para>
        ''' %((request.user.condominio.nombre).upper(), request.user.condominio.rif ), styles1)
	aH = 1*inch
	aW = doc.width
	w,h = P.wrap(aW, aH)
	P.drawOn(canvas, doc.leftMargin, doc.height)


    #FOOTER
	#canvas.setLineWidth(.6)
	#canvas.line(0*inch, 1*inch,8.5*inch,1*inch)
	styles = getSampleStyleSheet()
	styles1 = styles['Normal']
	styles1.leading = 12
	styles.fontSize = 8
	P = Paragraph('''
        <para alignment = "center">
        <b>Condominioaldia.net</b> es una marca registrada de Fractal Software, C.A.
        todos los derechos reservados<br/>
		</para>
        ''', styles1)
	aH = 1*inch
	aW = doc.width
	w,h = P.wrap(aW, aH)
	P.drawOn(canvas, doc.leftMargin, doc.bottomMargin-(0.5*inch))


	canvas.restoreState()