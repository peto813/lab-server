# -*- coding: utf-8 -*-

# encoding=utf8  
import json
from rest_framework import serializers
from rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from django.contrib.auth import get_user_model, authenticate
from patient_manager.models  import *
from django.utils import timezone
#from django.contrib.auth.models import User
#from rest_auth.serializers import UserDetailsSerializer
#from django.core.mail import send_mail, send_mass_mail
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework.exceptions import ValidationError
#from django.utils.crypto import get_random_string
#from allauth.account.utils import send_email_confirmation
#from allauth.account.models import EmailConfirmation, EmailAddress
# Get the UserModel
from patient_manager.utils import calculate_age
UserModel = get_user_model()


class LaboratorioSerializer(serializers.ModelSerializer):
	class Meta:
		model = Laboratorio
		#fields = ( 'title', 'created' )
		fields = '__all__'

class NominaSerializer(serializers.ModelSerializer):
	laboratorio = LaboratorioSerializer(read_only = True)
	class Meta:
		model = Nomina
		#fields = ( 'title', 'created' )
		fields = '__all__'


class CustomUserDetailsSerializer(UserDetailsSerializer):
	nomina = NominaSerializer()
	class Meta:
		model = UserModel
		fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'nomina',)
		read_only_fields = ('email', 'nomina',)


class CustomLoginSerializer(LoginSerializer):
	def validate(self, attrs):
		username = attrs.get('username')
		email = attrs.get('email')
		password = attrs.get('password')
		user = None

		if 'allauth' in settings.INSTALLED_APPS:
			from allauth.account import app_settings

			# Authentication through email
			if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
				user = self._validate_email(email, password)

			# Authentication through username
			if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
				user = self._validate_username(username, password)

			# Authentication through either username or email
			else:
				user = self._validate_username_email(username, email, password)

		else:
			# Authentication without using allauth
			if email:
				try:
					username = UserModel.objects.get(email__iexact=email).get_username()
				except UserModel.DoesNotExist:
					pass

			if username:
				user = self._validate_username_email(username, '', password)

		# Did we get back an active user?
		if user:
			if not hasattr(user, 'nomina') and not user.is_staff:
				raise ValidationError('Accesso Denegado')
			elif hasattr(user, 'nomina'):
				if not user.nomina.acceso_a_sistema:
					raise ValidationError('Accesso Denegado')
			if not user.is_active:
				msg = _('User account is disabled.')
				raise ValidationError(msg)
		else:
			msg = _('Unable to log in with provided credentials.')
			raise ValidationError(msg)

		# If required, is the email verified?
		if 'rest_auth.registration' in settings.INSTALLED_APPS:
			from allauth.account import app_settings
			if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
				email_address = user.emailaddress_set.get(email=user.email)
				if not email_address.verified:
					raise serializers.ValidationError(_('E-mail is not verified.'))

		attrs['user'] = user
		return attrs



class Medicos_Serializer( serializers.ModelSerializer ):
	# cedula = serializers.CharField(min_length = 4)
	# direccion = serializers.CharField(min_length = 3)
	# celular = serializers.CharField(min_length = 11, required= False)
	# email = serializers.EmailField(source='user.email', required= False, allow_blank=True)
	# estudios = Estudios_Serializer(required= False, many = True, read_only = True)
	#medicos = Medicos_Serializer()
	class Meta:
		model = Medicos
		#fields = ( 'title', 'created' )
		fields = '__all__'
		#lookup_field = 'cedula'



class Clinicas_Serializer( serializers.ModelSerializer ):
	# cedula = serializers.CharField(min_length = 4)
	# direccion = serializers.CharField(min_length = 3)
	# celular = serializers.CharField(min_length = 11, required= False)
	# email = serializers.EmailField(source='user.email', required= False, allow_blank=True)
	# estudios = Estudios_Serializer(required= False, many = True, read_only = True)
	#medicos = Medicos_Serializer()
	class Meta:
		model = Clinicas
		#fields = ( 'title', 'created' )
		fields = '__all__'
		#lookup_field = 'cedula'





class Sub_Tipos_Estudios_Serializer( serializers.ModelSerializer ):
	#detalles = Estudios_Detalles_Serializer( source = 'estudios_detalles_set', many = True )
	#clinica = serializers.ReadOnlyField(source = 'estudios_detalles_set.clinica')
	tipo = serializers.ReadOnlyField(source = 'tipo_estudio.nombre')
	class Meta:
		model = Sub_Tipos_Estudios
		#fields = ( 'title', 'created' )
		fields = '__all__'

	# def __init__(self, *args, **kwargs):
	# 	context = kwargs.pop( 'context', None )
	# 	if context and context['detalles']:
	# 		self.fields['detalles'] = Estudios_Detalles_Serializer( source = 'estudios_detalles_set', many = True )
	# 	super(Sub_Tipos_Estudios_Serializer, self).__init__(*args, **kwargs)
class CodigosResultadosSerializer(serializers.ModelSerializer):
	class Meta:
		model = Resultados_Codigos
		#fields = ( 'title', 'created' )
		fields = '__all__'
		depth = 1

class Codigos_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Codigos
		#fields = ( 'title', 'created' )
		fields = '__all__'


class CodigosField(serializers.Field):
    """
    Color objects are serialized into 'rgb(#, #, #)' notation.
    """
    def to_representation(self, obj):
		codigo_results = obj.through.objects.filter(resultado = obj.instance)
		serializer = CodigosResultadosSerializer(codigo_results, many = True)
		return serializer.data


    def to_internal_value(self, data):
    	#codigos = serializers.PrimaryKeyRelatedField( queryset=Codigos.objects.all(), required = False, allow_null = True )
        return Codigos.objects.get( numero = data )



class Resultados_Serializer( serializers.ModelSerializer ):
	estudio =  serializers.PrimaryKeyRelatedField( queryset = Estudios.objects.filter( impreso  = True ) )
	#codigos = serializers.PrimaryKeyRelatedField( queryset=Codigos.objects.all(), required = False, allow_null = True )
	tipo_cliente =  serializers.SerializerMethodField(read_only = True)
	tipo =serializers.SerializerMethodField(read_only = True)
	codigos = CodigosField(required = False,  allow_null = True)
	estudio_realizado = serializers.ReadOnlyField(source = 'estudio.estudio_realizado.nombre', read_only = True)
	paciente = serializers.SerializerMethodField(read_only = True)
	adjunto = serializers.FileField( allow_empty_file = False, required = False )
	medico = serializers.ReadOnlyField(source = 'estudio.medico.nombre', read_only = True)
	class Meta:
		model = Resultados
		#fields = ( 'title', 'created' )
		fields = '__all__'

	def get_tipo(self, resultado):
		tipo_estudio = resultado.estudio.estudio_realizado.tipo_estudio.nombre
		return tipo_estudio

	def get_tipo_cliente(self, resultado):
		tipo = 'normal' if not resultado.estudio.patron else 'postpago'
		return tipo


	def get_paciente(self, resultado):
		response = {
			'cedula' :resultado.estudio.paciente.cedula,
			'nacionalidad' :resultado.estudio.paciente.nacionalidad,
			'nombres' :resultado.estudio.paciente.nombres + ' ' + resultado.estudio.paciente.apellidos,
			'sexo':resultado.estudio.paciente.sexo,
			'fecha_nacimiento':str(resultado.estudio.paciente.fecha_nacimiento),
			'direccion':str(resultado.estudio.paciente.direccion),
			'email':str(resultado.estudio.paciente.user.email),
			'celular':str(resultado.estudio.paciente.celular),
			'observaciones':str(resultado.estudio.paciente.observaciones)
		}
		return response
	# def validate_codigos(self, data):
	# 	return data

	# def validate_adjunto(self, data):
	# 	return data

	def create(self, validated_data):
		estudio =  validated_data.get( 'estudio' )
		#print estudio.sub_tipos_estudios.tipo_estudio.nombre
		#print dir(estudio.estudio.tipo_estudio)
		tipo_estudio= estudio.estudio_realizado.tipo_estudio.nombre
		if tipo_estudio == 'citologia':
			resultado, created = Resultados.objects.get_or_create(
				#codigos = validated_data.get( 'codigos' ),
				estudio = estudio
			)
			resultado_codigo = Resultados_Codigos.objects.create(resultado = resultado, codigo = validated_data.get( 'codigos' ) )
			#print type(validated_data.get( 'codigos' ) )
			#resultado.codigos.add(  )
		else:
			validated_data['impreso'] = True
			resultado = Resultados.objects.create(**validated_data)
		return resultado

class Tipos_Estudios_Serializer( serializers.ModelSerializer ):
	# cedula = serializers.CharField(min_length = 4)
	# ciudad = serializers.CharField(min_length = 3)
	# celular = serializers.CharField(min_length = 11, required= False)
	# email = serializers.EmailField(source='user.email', required= False, allow_blank=True)
	sub_tipos_estudios = Sub_Tipos_Estudios_Serializer( many= True)
	class Meta:
		model = Tipos_Estudios
		#fields = ( 'title', 'created' )
		fields = '__all__'


class ResultadosCodigos_Serializer( serializers.ModelSerializer ):
	class Meta:
		model = Resultados_Codigos
		#fields = ( 'title', 'created' )
		fields = '__all__'
		depth = 1
		# read_only_fields = (
		# 	'service',
		# )

class Estudios_Serializer( serializers.ModelSerializer ):
	clinica  = Clinicas_Serializer()
	medico = Medicos_Serializer()
	tipo = serializers.ReadOnlyField(source = 'estudio_realizado.tipo_estudio.nombre')
	estudio_realizado = serializers.ReadOnlyField(source = 'estudio_realizado.nombre')
	#nro_sec_mes = serializers.SerializerMethodField(read_only =True)
	class Meta:
		model = Estudios
		#fields = ( 'title', 'created' )
		fields = '__all__'
	# def get_nro_sec_mes(self, instance):
	# 	#ALL STUDIES FOR THIS LAB
	# 	print 'culo'
	# 	estudios = Estudios.objects.all().filter(registrado_por__laboratorio=instance.registrado_por.laboratorio)
	# 	if estudios.exists():
	# 		estudios = estudios.order_by('-created')
	# 		estudio_mas_reciente = estudios[0]
	# 		for estudio in estudios:
	# 			nro_sec_mes =0
	# 			if estudio_mas_reciente:
	# 				if timezone.now().month == estudio_mas_reciente.created.month and timezone.now().year == estudio_mas_reciente.created.year:
	# 					#get for this month range
	# 					month_range = month_range_dt(timezone.now())
	# 					nro_sec_mes= estudios.filter( created__range=(month_range[0], month_range[1]) ).count()+1

	# 					#count +1
	# 					#self.nro_sec_mes = int(estudio_mas_reciente.nro_sec_mes) +1
	# 				elif timezone.now()> estudio_mas_reciente.created and timezone.now().month!=estudio_mas_reciente.created.month:
	# 					self.nro_sec_mes = 0
	# 	else:
	# 		self.nro_sec_mes = 1
	# 	print self.nro_sec_mes
	# 	return 1
	# 	return instance



class EstudiosViewSet_Serializer( serializers.ModelSerializer ):
	tipo = serializers.ReadOnlyField(source = 'estudio_realizado.tipo_estudio.nombre')
	tipo_cliente  = serializers.SerializerMethodField(read_only = True)
	resultado= serializers.SerializerMethodField(read_only=True)
	nro_sec_mes = serializers.ReadOnlyField()
	class Meta:
		model = Estudios
		#fields = ( 'title', 'created' )
		fields = '__all__'
		depth = 1

	def get_tipo_cliente(self, estudio):
		tipo_cliente = 'normal' if not estudio.patron else 'postpago'
		return tipo_cliente

	def get_resultado(self, estudio):
		try:
			resultado = estudio.resultados
		except:
			return []
		serializer = Resultados_Serializer(resultado)
		return serializer.data



class CNE_Serializer( serializers.Serializer ):
	NACIONALIDAD_CHOICES = (
		( 'V', 'V' ),
		( 'E', 'E' ),
	)
	cedula = serializers.IntegerField(required = True)
	nacionalidad =  serializers.ChoiceField(required = True, choices= NACIONALIDAD_CHOICES)
	#post_pago = serializers.BooleanField(required= True)

class EstudiosField(serializers.Field):
    """
    Color objects are serialized into 'rgb(#, #, #)' notation.
    """
    def to_representation(self, obj):
    	response_list = []
    	#print dir(self)
    	estudios = obj.through.objects.filter(paciente = obj.instance.id).filter( patron__isnull = True)
    	for estudio in estudios:
    		if estudio.impreso == False:
	    		response_list.append({
	    			'id': estudio.id,
	    			'clinica' : estudio.clinica.nombre if estudio.clinica else None, 
	    			'medico' : estudio.medico.nombre,
	    			'precio' : estudio.estudio_realizado.precio,
	    			'estudio': estudio.estudio_realizado.nombre,
	    			'tipo': estudio.estudio_realizado.tipo_estudio.nombre
	    		})
	    		#print response_list
    	return response_list

    def to_internal_value(self, data):

        return Estudios.objects.filter( id__in = data )


class ClientePostPagoSerializer(serializers.ModelSerializer):
	class Meta:
		model = ClientePostPago
		fields ='__all__'


class DetallesFacturasSerializer(serializers.ModelSerializer):
	class Meta:
		model = Detalles_Facturas
		fields ='__all__'

class reportSerializer(serializers.Serializer):
	c=serializers.IntegerField()
	day=serializers.DateTimeField()
	monto=serializers.DecimalField(max_digits=50, decimal_places=2, required = True)

class Context_Serializer(serializers.Serializer):
	minDate= serializers.DateTimeField()
	maxDate=  serializers.DateTimeField()
	reportes = reportSerializer(many= True)


class dateTimeSerializer(serializers.Serializer):
	mes = serializers.DateTimeField()

class FacturaSerializer(serializers.ModelSerializer):
	detalles = serializers.SerializerMethodField()
	creador_nombre = serializers.CharField(source = 'creador.username',read_only = True)
	creador = serializers.PrimaryKeyRelatedField( queryset=User.objects.all() )
	descuento = serializers.DecimalField(max_digits=50, decimal_places=2, required = True)
	is_otro_contribuyente = serializers.BooleanField( required = False)
	otro_rif = serializers.CharField(allow_blank = True, allow_null = True, required = False)
	otra_razon_social = serializers.CharField(allow_blank = True, allow_null = True, required = False)
	otra_nacionalidad = serializers.CharField(allow_blank = True, allow_null = True, required = False)
	class Meta:
		model = Facturas
		fields = [
		'detalles', 
		'creador', 
		'descuento', 
		'nacionalidad', 
		'rif', 
		'nombre', 
		'created', 
		'monto',
		'direccion',
		'id', 
		'telefono',
		'is_otro_contribuyente',
		'otro_rif',
		'otra_razon_social',
		'otra_nacionalidad',
		'creador_nombre'
		]
	def get_detalles(self, factura):
		detalles = []
		detalles_factura =  factura.detalles_facturas_set.all()
		for detalle in detalles_factura:
			detalles.append({
				'id':detalle.id,
				'estudio_realizado': detalle.estudio_realizado,
				'precio': detalle.precio
			})
		return detalles

	def validate(self, validated_data):
		is_otro_contribuyente = validated_data.get('is_otro_contribuyente',  None)
		if is_otro_contribuyente:
			otro_rif = validated_data.get('otro_rif', None)
			otra_razon_social = validated_data.get('otra_razon_social', None)
			otra_nacionalidad = validated_data.get('otra_nacionalidad', None)
			if not otro_rif:
				raise serializers.ValidationError("Debe proveer otro_rif.")
			elif not otra_razon_social:
				raise serializers.ValidationError("Debe proveer otra razon social.")
			elif not otra_nacionalidad:
				raise serializers.ValidationError("Debe proveer otra nacionalidad")
		return validated_data

	def create( self, validated_data ):
		estudios = Estudios.objects.filter(paciente__cedula = validated_data.get('rif'), paciente__nacionalidad =validated_data.get('nacionalidad'),impreso = True)
		is_otro_contribuyente = validated_data.pop('is_otro_contribuyente', None)
		if is_otro_contribuyente:
			otra_nacionalidad = validated_data.pop('otra_nacionalidad', None)
			otra_razon_social = validated_data.pop('otra_razon_social', None)
			otro_rif = validated_data.pop('otro_rif', None)
			validated_data['rif'] = otro_rif
			validated_data['nombre'] = otra_razon_social
			validated_data['nacionalidad'] = otra_nacionalidad
		factura = Facturas.objects.create(**validated_data)
		#estudio_mas_reciente = all_estudios.latest('created')
		#nro_sec_mes= estudio_mas_reciente.nro_sec_mes or 1
		if estudios.exists():

			for estudio in estudios:
				#estudio_mas_reciente = all_estudios.order_by('-nro_sec_mes')[0]
				# print estudio_mas_reciente.nro_sec_mes
				# nro_sec_mes =0
				# if estudio_mas_reciente:
				# 	if timezone.now().month == estudio_mas_reciente.created.month and timezone.now().year == estudio_mas_reciente.created.year:
				# 		nro_sec_mes = int(estudio_mas_reciente.nro_sec_mes) +1
				# 	elif timezone.now()> estudio_mas_reciente.created and timezone.now().month!=estudio_mas_reciente.created.month:
				# 		nro_sec_mes = 0

				# else:
				# 	nro_sec_mes=0
				# print estudio_mas_reciente
				# ###############
				# if not timezone.now().month == estudio_mas_reciente.created.month and ( timezone.now()>estudio_mas_reciente.created  ):
				# 	print 2
				# 	nro_sec_mes = 1
				# 	print 3
				# else:
				# 	print 4.0
				# 	nro_sec_mes +=1
				# 	print 4
				################
				estudio.factura = factura
				#estudio.nro_sec_mes = nro_sec_mes
				estudio.save()
				Detalles_Facturas.objects.create(factura = factura, estudio_realizado = estudio.estudio_realizado.nombre, precio = estudio.estudio_realizado.precio)

		return factura

		# self.nro_sec_mes = 1
		# model_empty = not Estudios.objects.all().exists()
		# if not model_empty:
		# 	estudio_mas_reciente = Estudios.objects.latest('created')
		# 	if not timezone.now().month == estudio_mas_reciente.created.month and ( timezone.now()>estudio_mas_reciente.created  ):
		# 		self.nro_sec_mes = 1
		# 	else:
		# 		self.nro_sec_mes += estudio_mas_reciente.nro_sec_mes



class EraseUnprintedTestSerializer(serializers.Serializer):

	del_list  = serializers.ListField(
	   child=serializers.IntegerField(min_value=0)
	)

	def validate_del_list(self, data):
		try:
			data = [Estudios.objects.get(id = item_id, impreso= False) for item_id in data]
		except:
			raise serializers.ValidationError("Identificador de Estudio Invalido")
		return data
	# def save(self):
	# 	print self.validated_data, 'peo'
	def erase(self):
		print 'culo'
		for item in self.validated_data['del_list']:
			item.delete()





class UserSerializer(serializers.ModelSerializer):
	#laboratorio = LaboratorioSerializer(read_only = True)
	class Meta:
		model = User
		#fields = ( 'title', 'created' )
		fields = '__all__'


class Paciente_Serializer( serializers.ModelSerializer ):
	cedula = serializers.CharField(min_length = 4)
	direccion = serializers.CharField(min_length = 3, required = True, allow_blank=False)
	celular = serializers.CharField(min_length = 11, required= False,allow_blank=True)
	email = serializers.EmailField( source='user.email',allow_blank=True, required = False)
	sub_tipos_estudios = EstudiosField(read_only = True)
	user = UserSerializer( read_only = True )
	tipo = serializers.SerializerMethodField(read_only = True)
	#estudios = Sub_Tipos_Estudios_Serializer(required= False, many = True, read_only = True, context= {'detalles': True})
	class Meta:
		model = Pacientes
		#fields = ( 'title', 'created' )
		fields = '__all__'

	def get_tipo(self, paciente):
		tipo_paciente = 'normal' if paciente.patron ==None else 'postpago'
		return tipo_paciente

	def validate_email(self, email):
		return email

	def create(self, validated_data):
		try:
			email=  validated_data.get( 'user' or None ).get('email' or None)
		except:
			email  = ''
		cedula = validated_data['cedula']
		nacionalidad = validated_data['nacionalidad']
		user = User.objects.create(username = str(nacionalidad)+str(cedula), email = str(email))
		validated_data['user'] = user
		paciente = Pacientes.objects.create( **validated_data)
		return paciente

	def update(self, instance, validated_data):
		instance.user.email = validated_data.get('user').get('email',  instance.user.email)
		instance.direccion = validated_data.get('direccion', instance.direccion)
		instance.observaciones = validated_data.get('observaciones', instance.observaciones)
		instance.save()
		instance.user.save()
		return instance


class EstudiosPostPagoField(serializers.Field):
    """
    Color objects are serialized into 'rgb(#, #, #)' notation.
    """
    def to_representation(self, obj):
    	response_list = []
    	estudios = obj.through.objects.filter(paciente = obj.instance.id).filter( patron__isnull = False)
    	for estudio in estudios:
    		if estudio.impreso == False:
	    		response_list.append({
	    			'id': estudio.id,
	    			'clinica' : estudio.clinica.nombre if estudio.clinica else None, 
	    			'medico' : estudio.medico.nombre,
	    			'precio' : estudio.estudio_realizado.precio,
	    			'estudio': estudio.estudio_realizado.nombre,
	    			'tipo': estudio.estudio_realizado.tipo_estudio.nombre
	    		})
    	return response_list

    def to_internal_value(self, data):
        return Estudios.objects.filter( id__in = data )



class PacientePostPago_Serializer( Paciente_Serializer ):
	direccion = serializers.CharField(min_length = 3, required = False, allow_blank=True)
	sub_tipos_estudios = EstudiosPostPagoField(read_only = True)
	# def create(self, validated_data):
	# 	try:
	# 		email=  validated_data.get( 'user' or None ).get('email' or None)
	# 	except:
	# 		email  = None
	# 	cedula = validated_data['cedula']
	# 	nacionalidad = validated_data['nacionalidad']
	# 	user = User.objects.create(username = str(nacionalidad)+str(cedula), email = str(email))
	# 	validated_data['user'] = user
	# 	paciente = Pacientes.objects.create( **validated_data)
	# 	return paciente

class Medicos_Serializer( serializers.ModelSerializer ):
	class Meta:
		model = Medicos
		#fields = ( 'title', 'created' )
		fields = '__all__'
		#lookup_field = 


class Estudio_add_serializer( serializers.Serializer ):
	paciente = serializers.CharField(min_length = 4)
	clinica= serializers.CharField( required = False, allow_blank=True)
	medico = serializers.CharField(min_length = 4, required= True, allow_blank =False)
	#prueba = serializers.PrimaryKeyRelatedField(queryset = Tipos_Estudios.objects.all())
	estudio_realizado = serializers.PrimaryKeyRelatedField(queryset = Sub_Tipos_Estudios.objects.all())

	def validate_paciente( self, cedula ):
		try:
			paciente = Pacientes.objects.get( cedula = cedula )
		except:
			raise serializers.ValidationError("paciente invalido")
		return paciente

	def validate_clinica( self, clinica ):
		clinica_referida, created = Clinicas.objects.get_or_create( nombre = clinica.lower() )
		return clinica_referida

	def validate_medico( self, medico ):
		medico_referido, created = Medicos.objects.get_or_create( nombre = medico.lower() )
		return medico_referido

	def create(self, validated_data):
		estudio = Estudios.objects.create(impreso = False, **validated_data)
		return estudio		#paciente.estudios.add( self.validated_data['subprueba'] )





class EstudioPostPago_add_serializer( Estudio_add_serializer ):
	patron = serializers.PrimaryKeyRelatedField(queryset = ClientePostPago.objects.all(), required = True)
	#sub_tipos_estudios = EstudiosPostPagoField(read_only = True)
	# def create(self, validated_data):
	# 	estudio = Estudios.objects.create(patron = patron,impreso = False, **validated_data)
	# 	return estudio		#paci


#ESTADISTICAS
class SexoPacienteEstadisticaViewSerializer( serializers.Serializer ):
	masculino = serializers.IntegerField(min_value=0, read_only = True)
	femenino = serializers.IntegerField(min_value=0, read_only = True)
	
class NacionalidadPacienteEstadisticaViewSerializer( serializers.Serializer ):
	venezolano = serializers.IntegerField(min_value=0, read_only = True)
	extranjero = serializers.IntegerField(min_value=0, read_only = True)

class tipoPacienteEstadisticaViewSerializer( serializers.Serializer ):
	post_pago = serializers.IntegerField(min_value=0, read_only = True)
	normal = serializers.IntegerField(min_value=0, read_only = True)

class EstudiosStatsSerializer( serializers.ModelSerializer ):
	tipo = serializers.ReadOnlyField(source = 'estudio_realizado.tipo_estudio.nombre', read_only=True)
	examen = serializers.ReadOnlyField(source = 'estudio_realizado.nombre', read_only=True)
	sexo = serializers.ReadOnlyField(source = 'paciente.sexo', read_only=True)
	edad  =  serializers.SerializerMethodField(read_only = True)
	class Meta:
		model = Estudios
		#fields = ( 'title', 'created' )
		fields = ['tipo', 'sexo', 'edad', 'created', 'examen']
		#lookup_field = 
	def get_edad(self, estudio):
		return calculate_age(estudio.paciente.fecha_nacimiento)