from __future__ import unicode_literals
import os
from django.utils import timezone
from django.utils.encoding import smart_unicode
from django.db import models
from django.contrib.auth.models import User
from patient_manager.utils import countries, month_range_dt
from patient_manager.managers import PacienteManager, ReportsManager, EstudioManager
from admin_tools_stats.models import DashboardStatsCriteria,  DashboardStats
from validators import *
# Create your models here.

class Pacientes(models.Model):
	NAC_CHOICES = (
	    ( 'V', 'V' ),
	    ( 'E', 'E' ),
	)
	SEXO_CHOICES = (
	    ( 'M', 'M' ),
	    ( 'F', 'F' ),
	)
	user = models.OneToOneField(User, null = True)
	cedula = models.CharField(null = False, unique = True,blank = False, validators=[validate_positive_num], max_length = 50)
	nombres = models.CharField( null = False, blank = False, max_length = 50)
	apellidos = models.CharField( null = False,  blank = False, max_length = 50)
	direccion = models.CharField( null = True,  blank = True, max_length = 250)
	sexo = models.CharField(choices = SEXO_CHOICES, max_length = 10)
	nacionalidad = models.CharField(choices = NAC_CHOICES, max_length = 10)
	fecha_nacimiento = models.DateField(null = False)
	sub_tipos_estudios = models.ManyToManyField('Sub_Tipos_Estudios', help_text = 'Estudios relacionados', related_name ="pacientes", through="Estudios")
	# medicoReferido = models.CharField(null = True, blank = True, max_length = 50)
	# clinicaRef = models.CharField(null = True, blank = True, max_length = 50)
	celular = models.CharField(null = True, blank = True, max_length = 15, validators=[validate_positive_num])
	observaciones = models.TextField(null = True, blank = True, max_length = 500)
	patron = models.ForeignKey('ClientePostPago', null = True)
	detalle = models.CharField(null = True, blank = True, max_length=50)
	post_pago = models.BooleanField(default = False, verbose_name = 'Post Pago')
	objects = PacienteManager()
	class Meta:
		verbose_name = 'Paciente'
		verbose_name_plural = 'Pacientes'
	def __unicode__( self ): #__str__ for python 3.3
		#user_instance = self.maintenance_products.get(maintenance = self.id).user
		return smart_unicode( self.nombres + ' ' + self.apellidos ).title()

	def save(self, *args, **kwargs):
		try:
			patron = self.patron
			if not patron:
				self.post_pago = False
			else:
				self.post_pago = True
		except:
			self.post_pago  = False
		super(Pacientes, self).save(*args, **kwargs)

class Codigos(models.Model):
	titulo = models.BooleanField(default = False)
	numero = models.IntegerField(null = False, blank  = False,  unique = True, primary_key = True)
	descripcion = models.TextField(null = False, blank  = False)
	created = models.DateTimeField(auto_now_add=True, auto_now = False, verbose_name = 'Creado')
	class Meta:
		verbose_name = 'Codigo'
		verbose_name_plural = 'Codigos'
	def __unicode__( self ): #__str__ for python 3.3
		#user_instance = self.maintenance_products.get(maintenance = self.id).user
		return smart_unicode( self.numero )

class Laboratorio(models.Model):
	rif = models.CharField( null = False,  blank = True, max_length = 50 )
	razon_social= models.CharField( null = False,  blank = True, max_length = 50 )
	nombre = models.CharField( null = True,  blank = True, max_length = 50 )
	pais = models.CharField( null = False,  blank = False, max_length = 30 )
	estado = models.CharField( null = False,  blank = False, max_length = 30 )
	ciudad = models.CharField( null = False,  blank = False, max_length = 30 )
	direccion = models.CharField( null = False,  blank = False, max_length = 250 )
	codigo_postal = models.CharField( null = True,  blank = False, max_length = 250 )
	class Meta:
		verbose_name = 'Laboratorio'
		verbose_name_plural = 'Laboratorios'
	def __unicode__( self ): #__str__ for python 3.3
		#user_instance = self.maintenance_products.get(maintenance = self.id).user
		return smart_unicode( self.nombre )

class Nomina(models.Model):
	user = models.OneToOneField(User, null = True)
	cedula = models.CharField(null = False, blank = False, max_length = 50)
	nombres = models.CharField( null = False, blank = False, max_length = 50)
	laboratorio = models.ForeignKey(Laboratorio)
	acceso_a_sistema = models.BooleanField(default = False)
	#numero = models.IntegerField(null = False, blank  = False,  unique = True, primary_key = True)
	#descripcion = models.TextField(null = False, blank  = False)
	#created = models.DateTimeField(auto_now_add=True, auto_now = False, verbose_name = 'Creado')
	class Meta:
		verbose_name = 'Nomina'
		verbose_name_plural = 'Nomina'



class Tipos_Estudios(models.Model):
	TIPO_OPTIONS =  (
	    ( 'citologia', 'citologia' ),
	    ( 'biopsia', 'biopsia' ),
	)
	nombre = models.CharField(null = False, blank  = False, max_length = 100, unique = True, choices = TIPO_OPTIONS)
	created = models.DateTimeField(auto_now_add=True, auto_now = False)
	class Meta:
		verbose_name = 'Tipo de Estudio'
		verbose_name_plural = 'Tipos de Estudios'
	def __unicode__( self ): #__str__ for python 3.3
		#user_instance = self.maintenance_products.get(maintenance = self.id).user
		return smart_unicode( self.nombre )

class Sub_Tipos_Estudios(models.Model):
	nombre = models.CharField(null = False, blank  = False, max_length = 100)
	tipo_estudio = models.ForeignKey( Tipos_Estudios, null = False, on_delete = models.CASCADE, related_name = 'sub_tipos_estudios' )
	precio = models.DecimalField(null = False, blank = False, max_digits = 50, decimal_places = 2)
	created = models.DateTimeField(auto_now_add=True, auto_now = False, verbose_name='creado')
	last_modified_ts = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name = 'Ultima modificacion')
	#medico = models.ForeignKey('Medicos', null = True, blank = True)
	class Meta:
		verbose_name = 'Sub. Tipo de Estudio'
		verbose_name_plural = 'Sub. Tipos de Estudios'
	def __unicode__( self ): #__str__ for python 3.3
		#user_instance = self.maintenance_products.get(maintenance = self.id).user
		return smart_unicode( self.nombre )



class Clinicas(models.Model):
	user = models.OneToOneField( User, null = True )
	rif = models.CharField( null = True, blank  = True, max_length = 100, unique = True )
	nombre = models.CharField( null = False, blank  = False, max_length = 100 )
	medicos = models.ManyToManyField( 'Medicos', help_text = 'Medicos relacionados', related_name ="clinicas" )
	direccion = models.CharField( null = True,  blank = True, max_length = 250 )
	telefono = models.CharField( null = True, blank = True, max_length = 15, validators=[validate_positive_num] )
	def __unicode__( self ): #__str__ for python 3.3
		#user_instance = self.maintenance_products.get(maintenance = self.id).user
		return smart_unicode( self.nombre ).title()
	class Meta:
		verbose_name = 'Clinica(cliente)'
		verbose_name_plural = 'Clinicas(cliente)'



class Medicos(models.Model):
	user = models.OneToOneField( User, null = True )
	nombre = models.CharField( null = False, blank  = False, max_length = 100 )
	numero_licencia = models.CharField( null = True, blank  = True, max_length = 100, unique = True )
	celular = models.CharField( null = True, blank = True, max_length = 15, validators=[validate_positive_num] )
	direccion = models.CharField( null = True,  blank = True, max_length = 250 )
	def __unicode__( self ): #__str__ for python 3.3
		#user_instance = self.maintenance_products.get(maintenance = self.id).user
		return smart_unicode( self.nombre ).title()

	class Meta:
		verbose_name = 'Medico'
		verbose_name_plural = 'Medicos'



class ClientePostPago(models.Model):
	NAC_CHOICES = (
	    ( 'V', 'V' ),
	    ( 'E', 'E' ),
	    ( 'G', 'G' ),
	    ( 'J', 'J' ),
	)
	user = models.OneToOneField( User, null = True )
	rif = models.CharField( null = True, blank  = True, max_length = 100, unique = True )
	nombre = models.CharField( null = False, blank  = False, max_length = 100, verbose_name = 'Patron' )
	direccion = models.CharField( null = True,  blank = True, max_length = 250 )
	telefono = models.CharField(null = True, blank = True, max_length = 15, validators=[validate_positive_num])
	nacionalidad = models.CharField(choices = NAC_CHOICES, max_length = 10)
	email = models.EmailField(null = True)
	
	def __unicode__( self ): #__str__ for python 3.3
		return smart_unicode( self.nombre )


class Facturas(models.Model):
	NAC_CHOICES = (
	    ( 'V', 'V' ),
	    ( 'E', 'E' ),
	    ( 'G', 'G' ),
	    ( 'J', 'J' ),
	)
	SEXO_CHOICES = (
	    ( 'M', 'M' ),
	    ( 'F', 'F' ),
	)
	creador = models.ForeignKey(User, null = False)
	nacionalidad = models.CharField(choices = NAC_CHOICES, max_length = 10)
	nombre = models.CharField( null = False, blank  = False, max_length = 50)
	created = models.DateTimeField(auto_now_add=True, auto_now = False ,verbose_name = 'Creado')
	direccion = models.CharField( null = True,  blank = True, max_length = 250)
	last_modified_ts = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name = 'Ultima modificacion')
	monto = models.DecimalField(null = False, blank = False, max_digits = 50, decimal_places = 2)
	descuento =  models.DecimalField(null = False, blank = False, max_digits = 50, decimal_places = 2, default = 0)
	rif  = models.CharField( null = False,  blank = False, max_length = 250 )
	telefono = models.CharField(null = True, blank = True, max_length = 15, validators=[validate_positive_num])
	objects = ReportsManager()
	class Meta:
		verbose_name = 'Factura'
		verbose_name_plural = 'Facturas'
	def __unicode__( self ): #__str__ for python 3.3
		return smart_unicode( self.id )

class Detalles_Facturas(models.Model):
	factura = models.ForeignKey(Facturas)
	estudio_realizado = models.CharField( null = False,  blank = False, max_length = 250 )
	precio = models.DecimalField(null = False, blank = False, max_digits = 50, decimal_places = 2)


class Estudios(models.Model):#ESTUDIOS REALIZADOS
	# tipo_choices = (
	#     ( 'V', 'V' ),
	#     ( 'E', 'E' ),
	#     ( 'G', 'G' ),
	#     ( 'J', 'J' ),
	# )
	factura = models.ForeignKey(Facturas, null = True, on_delete= models.PROTECT)
	estudio_realizado = models.ForeignKey( Sub_Tipos_Estudios )
	paciente = models.ForeignKey( Pacientes )
	medico = models.ForeignKey( Medicos, null = False, blank = False )
	clinica = models.ForeignKey( Clinicas, null = True, blank = True )
	created = models.DateTimeField(auto_now_add=True, auto_now = False ,verbose_name = 'Creado')
	last_modified_ts = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name = 'Ultima modificacion')
	impreso = models.BooleanField(default = False, null = False, blank = False)
	#nro_sec_mes = models.IntegerField(null=True, blank = True)
	patron = models.ForeignKey('ClientePostPago', null = True)
	registrado_por = models.ForeignKey(Nomina, null = False)
	@property
	def nro_sec_mes(self):
		#ALL STUDIES FOR THIS LAB
		nro_sec_mes= 1
		estudios = Estudios.objects.all().filter(registrado_por__laboratorio=self.registrado_por.laboratorio)
		if estudios.exists():
			estudios = estudios.order_by('-created')
			estudio_mas_reciente = estudios[0]
			for estudio in estudios:
		 		if estudio_mas_reciente:
		 			if timezone.now().month == estudio_mas_reciente.created.month and timezone.now().year == estudio_mas_reciente.created.year:
		 				month_range = month_range_dt(timezone.now())
		 				month_data =estudios.filter( created__range=(month_range[0], month_range[1]) )
		 				month_data_pk = [item.pk for item in month_data.order_by('created')]
		 				nro_sec_mes =0
		 				for item in month_data_pk:
		 					if item == self.pk:
		 						break
		 					else:
		 						nro_sec_mes+=1
		 			
		 			elif timezone.now()> estudio_mas_reciente.created and timezone.now().month!=estudio_mas_reciente.created.month:
		 				nro_sec_mes = 1
		# else:
		# 	self.nro_sec_mes = 1
		# print self.nro_sec_mes
		return nro_sec_mes+1
	#tipo = models.CharField(default= 'Normal', blank = False, null = False, choices = tipo_choices)
	#objects =EstudioManager()

	class Meta:
		verbose_name = 'Estudios'
		verbose_name_plural = 'Estudios'
	def __unicode__( self ): #__str__ for python 3.3
		return smart_unicode( self.estudio_realizado.nombre )

	# def save(self, *args, **kwargs):
	# 	print 1
	# 	estudios = Estudios.objects.all().filter(registrado_por__laboratorio=self.registrado_por.laboratorio)
	# 	print 2
	# 	if estudios.exists():
	# 		print 3
	# 		for estudio in estudios:
	# 			print 4
	# 			estudio_mas_reciente = estudios.order_by('-nro_sec_mes')[0]
	# 			print 5
	# 			self.nro_sec_mes =0
	# 			if estudio_mas_reciente:
	# 				if timezone.now().month == estudio_mas_reciente.created.month and timezone.now().year == estudio_mas_reciente.created.year:
	# 					#get for this month range
	# 					month_range = month_range_dt(timezone.now())
	# 					self.nro_sec_mes= estudios.filter( created__range=(month_range[0], month_range[1]) ).count()+1

	# 					#count +1
	# 					#self.nro_sec_mes = int(estudio_mas_reciente.nro_sec_mes) +1
	# 				elif timezone.now()> estudio_mas_reciente.created and timezone.now().month!=estudio_mas_reciente.created.month:
	# 					self.nro_sec_mes = 0
	# 	else:
	# 		self.nro_sec_mes = 1
	# 	print self.nro_sec_mes
		#super(Estudios, self).save(*args, **kwargs)


def resultado_adjunto(resultado, filename):
	return os.path.join( 'resultados/%s/biopsias/%s' % (   str(resultado.estudio.paciente.nacionalidad ) + str(resultado.estudio.paciente.cedula), filename ) )

class Resultados_Codigos(models.Model):
	resultado = models.ForeignKey('Resultados', on_delete = models.CASCADE )
	codigo = models.ForeignKey('Codigos')
	created = models.DateTimeField(auto_now_add=True, auto_now = False, verbose_name = 'Creado')


class Resultados(models.Model):
	codigos = models.ManyToManyField(Codigos, through	= Resultados_Codigos)
	#estudio = models.ForeignKey( Estudios , related_name = 'resultados')
	estudio = models.OneToOneField( Estudios )
	created = models.DateTimeField(auto_now_add=True, auto_now = False ,verbose_name = 'Creado')
	last_modified_ts = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name = 'Ultima modificacion')
	adjunto = models.FileField( upload_to = resultado_adjunto, null = True, blank = True  )
	impreso = models.BooleanField(default = False, blank = True)
	class Meta:
		verbose_name = 'Resultado'
		verbose_name_plural = 'Resultados'
	def __unicode__( self ): #__str__ for python 3.3
		return smart_unicode( self.estudio.paciente.user.email )


#PROXY MODELS
class MyDashboardStatsCriteria(DashboardStatsCriteria):
    class Meta:
    	proxy = True
    	verbose_name = 'Criterio  de estadistica'
    	verbose_name = 'Criterios  de estadisticas'
        # help_texts = {
        #     'criteria_name': 'Debe ser una palabra unica. Ej. estado, si, no',
        # }

class MyDashboardStats(DashboardStats):
    class Meta:
    	proxy = True
    	verbose_name = 'Estadistica'
    	verbose_name_plural = 'Estadisticas'
        # help_texts = {
        #     'group': 'Group to which this message belongs to',
        # }