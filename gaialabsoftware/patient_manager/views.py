# -*- coding: utf-8 -*-

# encoding=utf8  
import json, datetime, pytz
import dateutil.parser
#DJANGO IMPORTS
from django.apps import apps
from django.db.models.functions import TruncDay, TruncDate
from django.db.models import Count
from django.db.models import Sum, Value as V
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.shortcuts import render
from .forms import Cargar_Codigos_CSV
import csv
from django.contrib import messages
from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from patient_manager.utils import last_day_of_month
from django.core.mail import send_mail, send_mass_mail, EmailMessage
from patient_manager.forms import SendEmailPacientesForm
from django.contrib.admin.views.decorators import staff_member_required

from patient_manager.managers import *

# from django.db.models.functions import TruncMonth
# Sales.objects
#     .annotate(month=TruncMonth('timestamp'))  # Truncate to month and add to select list
#     .values('month')                          # Group By month
#     .annotate(c=Count('id'))                  # Select the count of the grouping
#     .values('month', 'c')                     # (might be redundant, haven't tested) select month and count


#TEST CODE
# import dropbox
# dbx = dropbox.Dropbox('LnMjDYxN3XAAAAAAAAAACtCZAAOQoNMkcrOoWBDlKtDb-KFhbhVSsLsBuZBfQ4qs')
# for entry in dbx.files_list_folder('').entries:
#     print(entry.name)
#     print dbx.files_get_metadata(str(entry.name)).server_modified
#     #print(entry._field_names_.files_get_metadata)
from rest_framework.generics import (
    RetrieveAPIView,
    UpdateAPIView,
    ListCreateAPIView,
    GenericAPIView,
    ListAPIView,
    )

#REST FRAMEWORK IMPORTS
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_auth.views import LoginView, UserDetailsView

#DJANGO FILTERS IMPORTS
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from patient_manager.permissions import *
#fractal software functions
from fractal_software_methods import cne_object, seniat_object
from models import *

from serializers import (
    CNE_Serializer,
    Paciente_Serializer,
    Tipos_Estudios_Serializer,
    Clinicas_Serializer,
    Estudio_add_serializer,
    Estudios_Serializer,#SERIALIZER FOR APIVIEW
    Medicos_Serializer,
    EraseUnprintedTestSerializer,
    Codigos_Serializer,
    Resultados_Serializer,
    ResultadosCodigos_Serializer,
    EstudiosViewSet_Serializer,#SERIALIZER FOR VIEWSET
    FacturaSerializer,
    CustomLoginSerializer,
    ClientePostPagoSerializer,
    PacientePostPago_Serializer,
    EstudioPostPago_add_serializer,
    CustomUserDetailsSerializer,
    SexoPacienteEstadisticaViewSerializer,
    NacionalidadPacienteEstadisticaViewSerializer,
    tipoPacienteEstadisticaViewSerializer,
    Sub_Tipos_Estudios_Serializer,
    EstudiosStatsSerializer,
    reportSerializer,
    Context_Serializer,
    dateTimeSerializer,
	)

from pagination import (
	StandardResultsSetPagination,
	)
 
from restful_filters import (
    Codigos_Filter, 
    Pacientes_Filter,
    Estudios_Filter,
    Resultados_Filter,
    Facturas_Filter,
    ClientePostPagoSFilter,
    EstudiosStatsFilter,
    )
# Create your views here.


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer

class CustomUserDetailsView(UserDetailsView):
    serializer_class = CustomUserDetailsSerializer

#charts
#@method_decorator(staff_member_required, name='dispatch')
class ChartsView(TemplateView):
	template_name = "charts.html"

#admin mass email
@method_decorator(staff_member_required, name='dispatch')
class pacienteEmailView(TemplateView):
	template_name = "mass_email.html"
	def post(self, request):
		form = SendEmailPacientesForm(request.POST or None, request.FILES)
		if form.is_valid():
			pacientes = form.cleaned_data.get('pacientes')
			message_list = []
			asunto= form.cleaned_data.get('asunto')
			email_list = [str(paciente.user.email) for paciente in pacientes]
			mensaje= form.cleaned_data.get('mensaje')
			for paciente in pacientes:
				#message = (asunto, 'mensaje', settings.DEFAULT_FROM_EMAIL, [str(paciente.user.email)])
				email = EmailMessage(
				    asunto,
				    mensaje,
				    settings.DEFAULT_FROM_EMAIL,
				    #['to1@example.com', 'to2@example.com'],
				    [str(paciente.user.email)]
				    #reply_to=['another@example.com'],
				    #headers={'Message-ID': 'foo'},
				)
				file = request.FILES.get('adjunto')
				content_type = str(file.content_type)
				file_name = str(file.name)
				email.attach(file_name, file.read(), content_type)
				#message_list.append(message)
				email.send()
			#send_mass_mail(tuple(message_list))
			messages.success(request, 'Correo electronico enviado a pacientes.')
			return HttpResponseRedirect('/admin/patient_manager/pacientes/')
		context ={
			'form': form
		}
		return render(request,  self.template_name, context)

#admin mass email

class ResultadosCitologiaView(TemplateView):
	template_name = 'citologia.html'
	def get(self, request, pk = None):
		resultado = Resultados.objects.get(pk = pk)
		codigos= resultado.codigos.all()
		context ={
			'title' : 'Resultados de Citologia',
			'resultado' : resultado,
			'codigos' :codigos
		}
		return render(request,  self.template_name, context)


class Index_View(TemplateView):
	template_name = "index.html"
	def get(self, request):
		context ={
		}
		return render(request,  self.template_name, context)


class InitialView(APIView):
	def get(self, request):
		codigos=Codigos.objects.all().exists()
		laboratorios = Laboratorio.objects.all().exists()
		tipos_estudios = Tipos_Estudios.objects.all().exists()
		sub_tipos_estudios = Sub_Tipos_Estudios.objects.all().exists()
		nomina = Nomina.objects.all().exists()
		messages =  []
		sub_tipos_estudios_message = 'El administrador no ha resistrado sub tipos de estudios.'
		tipos_estudios_message = 'El administrador no ha resistrado tipos de estudios.'
		laboratorios_message = 'El administrador no ha resistrado laboratorios.'
		codigos_message = 'El administrador no ha resistrado codigos.'
		nomina_message = 'El administrador no ha resistrado nomina.'

		if not codigos:
			messages.append({'message': codigos_message})

		if not laboratorios:
			messages.append({'message': laboratorios_message})

		if not tipos_estudios:
			messages.append({'message': tipos_estudios_message})

		if not sub_tipos_estudios:
			messages.append({'message': sub_tipos_estudios_message})

		if not nomina:
			messages.append({'message': nomina_message})
		print messages
		return Response(messages, status=status.HTTP_200_OK)


@method_decorator(staff_member_required, name='dispatch')
class CargarCSV(TemplateView):
    template_name = "cargarcsv.html"
    url = '/static/archivos/'
    context = {}
    def get(self, request, model_name=None ):
    	print model_name, 'culo'
    	model = apps.get_model('patient_manager', model_name)
    	if model:
    		self.context['title'] = 'GaiaSoft | Cargar CSV ' + model_name.lower()
    		self.context['header'] = model_name.lower().replace('_', ' ').title()
    		self.context['ejemploCSV'] = self.url + 'MOCK_DATA_%s.csv' %(model_name)
    		self.context['instructions'] = " El archivo debe contener en la primera fila las columnas ej: 'numero','nombre', y 'descripcion' separadas por coma (en cualquier orden). Luego la data correspondiente separada igualmente por coma."
    	return render(request,  self.template_name, self.context)

    def post(self, request, model_name = None):
    	form = Cargar_Codigos_CSV(request.POST or None, request.FILES or None)
    	if form.is_valid():
			file= form.cleaned_data.get('file')
			#with open(‘some.csv’, ‘rb’) as f:
			reader = csv.reader(file)
			row_number = 0
			headers = {}
			for row in reader:
				if row_number == 0:
					index = 0
					for column in row:
						headers[str(column)] = str(index)
						index += 1
				else:
					try:
						model = apps.get_model('patient_manager', model_name)

						params = {}
						for key, value in headers.iteritems():
							field= model._meta.get_field(key)
							params[key] = row[int(headers[key])]
							if field.is_relation:
								related_model= field.related_model.objects.get(nombre = 'citologia')
								params[key] = related_model
							else:
								params[key] = row[int(headers[key])]
						#print params
						model.objects.create(**params)
						message_type= 'success'
					except:
						message_type= 'error'
						pass

				row_number+=1

			if not message_type =='error':
				messages.success(request, 'Codigos Cargados exitosamente')
			else:
				messages.warning(request, 'Error en la carga de archivo CSV asegurese de usar coma como separador y de que la primera fila contenga los nombres de las columnas "nombre, descripcion, numero sin mayusculas"')

    	self.context['form'] = form
    	self.context['title'] = 'GaiaSoft | Cargar CSV ' + model_name.lower()
    	self.context['header'] = model_name.lower().replace('_', ' ').title()
    	self.context['ejemploCSV'] = self.url + 'MOCK_DATA_%s.csv' %(model_name)
    	self.context['instructions'] = " El archivo debe contener en la primera fila las columnas ej: 'numero','nombre', y 'descripcion' separadas por coma (en cualquier orden). Luego la data correspondiente separada igualmente por coma."
    	return render(request,  self.template_name, self.context)




class VerifyPatientView(APIView):
	permission_class = (IsAuthenticated,)
	serializer_class = Paciente_Serializer
	def post(self, request):
		serializer = CNE_Serializer(data= request.data)
		if serializer.is_valid():
			try:
				paciente = Pacientes.objects.get( cedula = serializer.validated_data.get('cedula') )#, patron__isnull = not serializer.validated_data.get('post_pago') 
				serializer = self.serializer_class( paciente )
				return Response(serializer.data, status=status.HTTP_200_OK)
			except:

				ciudadano = cne_object(nacionalidad=serializer.validated_data.get('nacionalidad'), cedula=str(serializer.validated_data.get('cedula')))
				if not ciudadano:
					return Response('ciudadano no encontrado', status=status.HTTP_204_NO_CONTENT)
				return Response(ciudadano, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
		else:
			print serializer.errors
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPatientPostPagoView(VerifyPatientView):
	serializer_class = PacientePostPago_Serializer

class FirstPatientView(APIView):
	def get(self, request, format=None):
		queryset = Pacientes.objects.all().order_by('-user__date_joined')
		if queryset.exists():
			response = queryset.last().user.date_joined
		else:
			response = None
		return Response(response, status=status.HTTP_200_OK)



class ImprimirEstudiosView(APIView):
	permission_class = (IsAuthenticated,)
	queryset = Pacientes.objects.all()
	lookup_field = 'cedula'
	serializer = FacturaSerializer
	def post(self, request, cedula = None, nacionalidad = None):
		#try:
		data = request.data.copy()
		data['creador'] = request.user.id
		serializer = FacturaSerializer(data = data)
		if serializer.is_valid():
			Pacientes.objects.get(cedula = cedula).estudios_set.filter(impreso = False).update(impreso = True)
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
			
		else:
			print serializer.errors
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST )
		# except:
		# 	return Response('ERROR', status = status.HTTP_500_INTERNAL_SERVER_ERROR )
		return Response('OK', status=status.HTTP_200_OK)

class generarNotaPostPagoView(ImprimirEstudiosView):
	def post(self, request, cedula = None, nacionalidad = None):
		paciente = Pacientes.objects.get(cedula = cedula)
		all_estudios = Estudios.objects.all()
		estudios= paciente.estudios_set.filter(impreso = False)#.update(impreso = True)
		estudio_mas_reciente = all_estudios.order_by('-nro_sec_mes')[0]
		#estudio_mas_reciente = estudios.order_by('-nro_sec_mes')[0]
		nro_sec_mes= estudio_mas_reciente.nro_sec_mes or 1
		for estudio in estudios:
			if not timezone.now().month == estudio_mas_reciente.created.month and ( timezone.now()>estudio_mas_reciente.created  ):
				nro_sec_mes = 1
			else:
				nro_sec_mes +=1
			estudio.nro_sec_mes = nro_sec_mes
			estudio.impreso = True
			estudio.save()

		serializer = Estudios_Serializer(estudios, many = True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class EstudioNoImpresoView(APIView):
	permission_class = (IsAuthenticated,)
	queryset = Estudios.objects.all()
	serializer_class = Estudios_Serializer
	filter_backends = ( DjangoFilterBackend, )
	filter_class = Estudios_Filter
	def post(self, request, format=None):
		serializer = EraseUnprintedTestSerializer( data = request.data )
		if serializer.is_valid():
			serializer.erase()
			paciente = Pacientes.objects.get(cedula = request.GET.get('cedula') )
			serializer = Paciente_Serializer( paciente )
			return Response(serializer.data, status=status.HTTP_200_OK)
			# paciente = Pacientes.objects.get( cedula = serializer.validated_data.get('cedula') )
			# serializer = Paciente_Serializer( paciente )

			# serializer = self.serializer_class(queryset, many= True)
			# return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			print serializer.errors
		return Response('response', status=status.HTTP_200_OK)


class reportesViewSet(APIView):
	queryset= Facturas.objects.all()
	permission_class= (IsAuthenticated,)

	def get_range(self):
		queryset= self.queryset
		#closed_queryset= queryset.filter(cerrado=True)
		if queryset.exists():
			minDate=queryset.earliest('created').created.replace(day= 1, hour= 0, minute = 0, second=0,microsecond=0)
			maxDate=queryset.latest('created').created
			maxDate=maxDate.replace(day= last_day_of_month(maxDate), hour= 23, minute = 59, second=59, microsecond=999999 )
			#active_month = maxDate+relativedelta(months=1)
		else:
			minDate= self.request.user.date_joined.replace(day= 1, hour= 0, minute = 0, second=0,microsecond=0)
			maxDate=minDate.replace(day= last_day_of_month(minDate), hour= 23, minute = 59, second=59, microsecond=999999 )
			#active_month=minDate
		date_range={
			'maxDate':maxDate,
			'minDate':minDate
		}
		return date_range

	def get_queryset(self):
		return self.queryset.filter(creador__nomina__laboratorio = self.request.user.nomina.laboratorio)

	def get(self, request, mes = None):
		reportes= self.get_queryset()
		if mes:
			data = {
				'mes': mes
			}
			now = timezone.now()
			serializer= dateTimeSerializer(data=data)
			if serializer.is_valid():
				mes= serializer.validated_data.get('mes')
		else:
			mes = timezone.now()

		minDate= mes.replace(day= 1, hour= 0, minute = 0, second=0,microsecond=0)
		maxDate=mes.replace(day= last_day_of_month(minDate), hour= 23, minute = 59, second=59, microsecond=999999 )
		reportes= self.queryset.filter(created__range=(minDate, maxDate))
			#query form month else get current month
		'''
		service mysqld restart
		default-time-zone = 'UTC'
		to your /etc/mysql/my.cnf in [mysqld] section.
		'''
		reportes = reportes.annotate(day=TruncDay('created')).values('day').annotate(c=Count('id')).values('day', 'c').annotate(monto =Sum('monto')).values('day', 'c', 'monto')
		date_range = self.get_range()
		context= {
			'maxDate':date_range['maxDate'],
			'minDate': date_range['minDate'],
			'reportes':reportes
		}
		serializer = Context_Serializer(context)
		return Response(serializer.data, status=status.HTTP_200_OK)
	# permission_class = (IsAuthenticated,)
	# queryset = Facturas.objects.all()
	# serializer_class = FacturaSerializer
	# filter_backends = ( DjangoFilterBackend, SearchFilter)
	# filter_class = Facturas_Filter
	# search_fields = ['=id', '=rif', 'nombre', '=creador__username', '=monto']

class FacturasViewSet(viewsets.ModelViewSet):
	permission_class = (IsAuthenticated,)
	queryset = Facturas.objects.all()
	serializer_class = FacturaSerializer
	filter_backends = ( DjangoFilterBackend, SearchFilter)
	filter_class = Facturas_Filter
	search_fields = ['=id', '=rif', 'nombre', '=creador__username', '=monto']


class ResultadosCodigosViewSet(viewsets.ModelViewSet):
	permission_class = (IsAuthenticated,)
	queryset = Resultados_Codigos.objects.all()
	serializer_class = ResultadosCodigos_Serializer

	def get_object(self, pk):
		try:
			return Resultados_Codigos.objects.get(pk=pk)
		except Resultados_Codigos.DoesNotExist:
			raise Http404

	def destroy(self, request, pk=None):
		instance = self.get_object(pk)
		self.get_object(pk).delete()
		queryset = self.queryset.filter(resultado = instance.resultado)
		serializer = self.serializer_class(queryset, many = True)
		return Response(serializer.data, status=status.HTTP_202_ACCEPTED) 

	#pagination_class = StandardResultsSetPagination

class ResultadosViewSet(viewsets.ModelViewSet):
	permission_class = (IsAuthenticated,)
	queryset = Resultados.objects.all()
	serializer_class = Resultados_Serializer
	#pagination_class = StandardResultsSetPagination
	filter_backends = ( DjangoFilterBackend, SearchFilter,)
	filter_class = Resultados_Filter
	search_fields = ['=estudio__paciente__cedula', '=estudio__id', 'estudio__paciente__nombres', 'estudio__paciente__apellidos', 'estudio__estudio_realizado__nombre']

	def get_object(self, pk= None):
		try:
			return Resultados.objects.get(pk= pk)
		except:
			raise Http404

	def partial_update(self, request, pk = None):
		instance = self.get_object(pk)
		serializer = self.get_serializer(instance, data = request.data, partial = True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK) 
		return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST) 

	def create(self, request):
		serializer = self.get_serializer( data = request.data )
		if serializer.is_valid():
			serializer.save()
			estudio=  serializer.validated_data['estudio'].id
			queryset = Resultados_Codigos.objects.filter(resultado__estudio = estudio)
			serializer = ResultadosCodigos_Serializer(queryset, many= True)

			return Response(serializer.data, status=status.HTTP_200_OK) 
		print serializer.errors
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class EstudiosRealizadosViewSet(viewsets.ModelViewSet):
	permission_class = (IsAuthenticated,)
	queryset = Estudios.objects.all()
	serializer_class = Estudios_Serializer
	pagination_class = StandardResultsSetPagination
	#lookup_field = 'cedula'
	filter_backends = ( DjangoFilterBackend, )
	filter_class = Estudios_Filter
	


class CodigosViewSet(viewsets.ModelViewSet):
	permission_class = (IsAuthenticated,)
	queryset = Codigos.objects.all()
	serializer_class = Codigos_Serializer
	#lookup_field = 'cedula'
	filter_backends = ( DjangoFilterBackend, )
	filter_class = Codigos_Filter

class ClientesPostPagoViewSet(viewsets.ModelViewSet):
	permission_class = (IsAuthenticated,)
	queryset = ClientePostPago.objects.all()
	serializer_class = ClientePostPagoSerializer
	#lookup_field = 'cedula'
	filter_backends = ( DjangoFilterBackend, )
	filter_class = ClientePostPagoSFilter
	# def create(self, request):
	# 	#print request.data
	# 	#data = request.data.copy
	# 	serializer = ClientePostPagoSerializer(data= request.data)
	# 	if serializer.is_valid():
	# 		user = User.objects.create(username = serializer.validated_data.get('nacionalidad')+serializer.validated_data.get('rif'), email = serializer.validated_data.get('email', None))
	# 		serializer.save(user = user)
	# 		serializer = ClientePostPagoSerializer(self.get_queryset(), many = True)
	# 		return Response(serializer.data, status = status.HTTP_200_OK)
	# 	else:
	# 		print serializer.errors
	# 		return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)


class PacientePostPagoView(APIView):#ESTUDIOS PARA CLIENTE POST PAGO, GET Y POST
	permission_class = (IsAuthenticated,)
	def get(self, request, format=None):
		response = {}
		response['estudios'] = Tipos_Estudios_Serializer( Tipos_Estudios.objects.all(),  many = True).data
		response['clinicas'] = [item['nombre'] for item in Clinicas_Serializer( Clinicas.objects.all(), many = True ).data]		
		response['medicos'] = [item['nombre'] for item in Medicos_Serializer( Medicos.objects.all(), many = True ).data]
		response['clientes_postpago'] = ClientePostPagoSerializer( ClientePostPago.objects.all(),  many = True).data
		return Response(response, status=status.HTTP_200_OK)

	def post(self, request, format=None):
		data = request.data
		serializer = EstudioPostPago_add_serializer(data  = data)
		print data
		if serializer.is_valid():
			serializer.save()
			paciente = serializer.validated_data.get('paciente')#this gets the patient
			serializer = PacientePostPago_Serializer(paciente)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			print serializer.errors

		return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST )

class PacientesViewSet(viewsets.ModelViewSet):
	permission_class = (IsAuthenticated,)
	queryset = Pacientes.objects.all()
	serializer_class = Paciente_Serializer
	lookup_field = 'cedula'
	filter_backends = ( DjangoFilterBackend, SearchFilter,)
	search_fields = ['=cedula', 'nombres', 'apellidos', '=celular']
	filter_class = Pacientes_Filter

	def get_object(self, cedula):
		try:
			return Pacientes.objects.get(cedula=cedula)
		except Pacientes.DoesNotExist:
			raise Http404


	def create( self, request ):
		data = request.data.copy()
		birthday =  dateutil.parser.parse(data.get('fecha_nacimiento'))
		data['fecha_nacimiento'] = birthday.date()
		data['nombres'] = str(data['nombres']).lower()
		data['apellidos'] = str(data['apellidos']).lower()
		serializer = self.get_serializer(data = data)
		if serializer.is_valid():
			serializer.save()
			return Response( serializer.data, status = status.HTTP_200_OK )
		else:
			print serializer.errors
		return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST )


	def partial_update(self, request, cedula = None):
		data = request.data.copy()
		birthdat_string =  data.get('fecha_nacimiento').split('T')[0].split('-')
		birthday = datetime.date(int(birthdat_string[0]), int(birthdat_string[1]), int(birthdat_string[2]))
		data['fecha_nacimiento'] = birthday
		instance = self.get_object(cedula)
		serializer = Paciente_Serializer( instance, data = data, partial=True )
		if serializer.is_valid():
			serializer.save()
			#print serializer.validated_data
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			print serializer.errors
		return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

	# def partial_update(self, request, cedula = None):
	# 	print 'pepita'
	# 	data = request.data.copy()
	# 	birthdat_string =  data.get('fecha_nacimiento').split('T')[0].split('-')
	# 	birthday = datetime.date(int(birthdat_string[0]), int(birthdat_string[1]), int(birthdat_string[2]))
	# 	data['fecha_nacimiento'] = birthday
	# 	queryset = Pacientes.objects.get(cedula = cedula)
	# 	serializer = self.get_serializer(queryset ,data = data)
	# 	if serializer.is_valid():
	# 		serializer.save()
	# 		return Response( serializer.data, status = status.HTTP_200_OK )
	# 	else:
	# 		print serializer.errors
		return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST )

class PacientesPostPagoViewSet(PacientesViewSet):
	serializer_class = PacientePostPago_Serializer

class ContribuyenteView( APIView ):
	def post(self, request):
		try:
			response =  seniat_object(request.data['id_fiscal'])
		except:
			return Response('ERROR', status=status.HTTP_400_BAD_REQUEST)
		return Response(response, status=status.HTTP_200_OK)
		



class EstudiosView(APIView):#view that gets clinicas, medicos, estudios
	permission_class = (IsAuthenticated,)
	def get(self, request, format=None):
		response = {}
		response['estudios'] = Tipos_Estudios_Serializer( Tipos_Estudios.objects.all(),  many = True).data
		response['clinicas'] = [item['nombre'] for item in Clinicas_Serializer( Clinicas.objects.all(), many = True ).data]		
		response['medicos'] = [item['nombre'] for item in Medicos_Serializer( Medicos.objects.all(), many = True ).data]
		return Response(response, status=status.HTTP_200_OK)

	def post(self, request, format=None):#adds estudio
		data = {}
		data['estudio_realizado'] = request.data.get('subprueba')
		#data['prueba'] = request.data.get('subprueba')['tipo_estudio']
		data['medico'] = request.data.get('medico')
		data['clinica'] = request.data.get('clinica', None)
		data['paciente'] = request.data.get('paciente')
		serializer = Estudio_add_serializer(data  = data)
		if serializer.is_valid():
			serializer.save(registrado_por = self.request.user.nomina)
			paciente = serializer.validated_data.get('paciente')#this gets the patient
			serializer = Paciente_Serializer(paciente)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			print serializer.errors

		return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST )


class EstudiosViewSet(viewsets.ModelViewSet):
	permission_class = (IsAuthenticated,)
	queryset = Estudios.objects.all()
	serializer_class = EstudiosViewSet_Serializer
	filter_backends = ( DjangoFilterBackend, SearchFilter,)
	search_fields = ['=id', '=nro_sec_mes','estudio_realizado__nombre', '=estudio_realizado__precio', 'paciente__nombres',  'paciente__apellidos']
	filter_class = Estudios_Filter

	def get_queryset(self):
		return self.queryset.filter(registrado_por__laboratorio = self.request.user.nomina.laboratorio)


class PreciosView(APIView):
	def get(self, request, format=None):
		estudios = Sub_Tipos_Estudios.objects.all()
		serializer = Sub_Tipos_Estudios_Serializer(estudios, many = True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	
#ESTADISTICAS
class SexoPacienteEstadisticaView(APIView):
	permission_class = (IsAdminUser,)
	def get(self, request, format=None):
		femenino = len(Pacientes.objects.filter(sexo ='F'))
		masculino = len(Pacientes.objects.filter(sexo ='M'))
		data = {
			'femenino' : femenino,
			'masculino': masculino
		}
		serializer = SexoPacienteEstadisticaViewSerializer(data)
		return Response(serializer.data, status=status.HTTP_200_OK)

class NacionalidadPacienteEstadisticaView(APIView):
	permission_class = (IsAdminUser,)
	def get(self, request, format=None):
		extranjero = len(Pacientes.objects.filter(nacionalidad ='E'))
		venezolano = len(Pacientes.objects.filter(nacionalidad ='V'))
		data = {
			'venezolano' : venezolano,
			'extranjero': extranjero
		}
		serializer = NacionalidadPacienteEstadisticaViewSerializer(data)
		#response = Pacientes.objects.all().order_by('-user__date_joined').last().user.date_joined
		return Response(serializer.data, status=status.HTTP_200_OK)

class TipoPacienteEstadisticaView(APIView):
	permission_class = (IsAdminUser,)
	def get(self, request, format=None):
		normal = len(Pacientes.objects.filter(post_pago =False))
		post_pago = len(Pacientes.objects.filter(post_pago =True))
		data = {
			'post_pago' : post_pago,
			'normal': normal
		}

		serializer = tipoPacienteEstadisticaViewSerializer(data)
		#response = Pacientes.objects.all().order_by('-user__date_joined').last().user.date_joined
		return Response(serializer.data, status=status.HTTP_200_OK)


class EstudiosEstadisticaView(EstudiosViewSet):
	#permission_class = (IsAuthenticated,)#IsAdminUser,
	# queryset = Estudios.objects.all()
	#search_fields = []
	serializer_class = EstudiosStatsSerializer
	#filter_backends = ( DjangoFilterBackend,)
	#filter_class = EstudiosStatsFilter
