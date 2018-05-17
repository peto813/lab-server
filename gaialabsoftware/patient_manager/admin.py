# -*- coding: utf-8 -*-
import csv
from django.contrib import admin
from django.conf import settings
from .models import *
from django.utils.encoding import smart_unicode
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render
#USED TO GET URL
#from django.contrib.sites.models import Site
from django.http import HttpResponse
from patient_manager.utils import calculate_age
from admin_tools_stats.models import DashboardStatsCriteria,  DashboardStats
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, EmailMessage
from django.db.models import Q
from django.contrib.sites.models import Site
from patient_manager.forms import (
    SendEmailPacientesForm,
    MyDashboardStatsCriteriaAdminForm,
    sendResultadosForm,
    )

admin.site.site_title = 'Administrador'
admin.site.site_header = 'Administrador'
admin.site.index_title = 'Panel de Control'
admin.site.site_url = '/'


class MyDashboardStatsCriteriaAdmin( admin.ModelAdmin ):
    """
    Allows the administrator to view and modify certain attributes
    of a DashboardStats.
    """
    #form = MyDashboardStatsCriteriaAdminForm
    list_display = ('id', 'criteria_name', 'created_date')
    list_filter = ['created_date']
    ordering = ('id', )
    save_as = True
admin.site.unregister(DashboardStatsCriteria)
admin.site.register(MyDashboardStatsCriteria, MyDashboardStatsCriteriaAdmin)


class MyDashboardStatsAdmin( admin.ModelAdmin ):

    #form = MyDashboardStatsCriteriaAdminForm()
    """
    Allows the administrator to view and modify certain attributes
    of a DashboardStats.
    """
    list_display = ('id', 'graph_key', 'graph_title', 'model_name',
                    'is_visible', 'created_date')
    list_filter = ['created_date']
    ordering = ('id', )
    save_as = True
admin.site.unregister(DashboardStats)
admin.site.register(MyDashboardStats, MyDashboardStatsAdmin)

class CustomUserAdmin(UserAdmin):
    #inlines = (ProfileInline, )
    list_display = ['username', 'first_name', 'last_name','email', 'is_superuser', 'is_active', 'tipo_usuario']
    #list_editable = ('is_active', )
    #search_fields = [ 'email', 'first_name', 'last_name' ]
    list_filter = ('is_active', 'is_superuser', 'is_staff')  
    readonly_fields = ('tipo_usuario',)
    def tipo_usuario(self, obj):
        if hasattr(obj, 'nomina'):
            return 'Nomina'
        elif hasattr(obj, 'pacientes'):
            return 'Paciente'
        elif hasattr(obj, 'medicos'):
            return 'Medico'
        elif hasattr(obj, 'clinicas'):
            return 'Clinica'            
        elif obj.is_staff:
            return 'Staff'
        else:
            return 'No establecido'
        return obj.userprofile.mobile_number
    tipo_usuario.short_description = "Tipo"
    # def office_number(self, obj):
    #     return obj.userprofile.office_number 
    # def company_name(self, obj):
    #     return obj.userprofile.company_name
    # def profile_picture(self, obj):
    #     return mark_safe(obj.userprofile.image_tag())
        # html = u' <img src="%s" />' %(obj.userprofile.profile_picture)admin_thumbnail
        # print obj.userprofile.profile_picture
        # return mark_safe(html)
    #profile_picture.allow_tags = True
    # def image_tag(self):
    #     return u'<img src="%s" />' % <URL to the image>          
    #mobile_number.allow_tags = True
    #mobile_number.short_description = "Mobile"
    #office_number.short_description = "Office #"
    # def get_inline_instances(self, request, obj=None):
    #     if not obj:
    #         return list()
    #     return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class ClientePostPagoAdmin( admin.ModelAdmin ):
    list_display = ['user', 'rif','nombre', 'nacionalidad', 'telefono', 'direccion', 'email']
admin.site.register( ClientePostPago, ClientePostPagoAdmin )


class LaboratoriosAdmin( admin.ModelAdmin ):
    list_display = ['rif', 'razon_social','pais', 'estado', 'ciudad', 'direccion', 'codigo_postal']
admin.site.register( Laboratorio, LaboratoriosAdmin )


class NominaAdmin( admin.ModelAdmin ):
    list_display = ['user', 'cedula','nombres', 'laboratorio', 'acceso_a_sistema']

    actions = [ 'download_csv']


    def download_csv(self, request, queryset):
        f = open('nomina.csv', 'wb')
        writer = csv.writer(f)
        writer.writerow([ "usuario","cedula", "nombres", "laboratorio", 'acceso_sistema'])
        for s in queryset:
            writer.writerow([s.user, s.cedula, s.nombres, s.laboratorio, 'acceso_a_sistema' ])
        f.close()

        f = open('nomina.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=stat-info.csv'
        return response
    download_csv.short_description = "Descargar CSV"

admin.site.register( Nomina, NominaAdmin )

class PacientesAdmin( admin.ModelAdmin ):
    # def user_instance(self, obj):
    #     return 'Id: '+ str(obj.user.pk)  + ' - ' + str(obj.user.first_name) + ' ' + str(obj.user.last_name)
    # def first_name(self, obj):
    #     return smart_unicode(obj.user.first_name)
    # def last_name(self, obj):
    #     return smart_unicode(obj.user.last_name)
    # #user_instance.short_description = 'user_instance'
    search_fields = ['cedula', 'nombres', 'apellidos', 'user__email', 'celular' ]
    list_filter = ('sexo', 'nacionalidad','post_pago','patron__nombre', 'user__email') 
    actions = ['send_email', 'download_csv']


    def download_csv(self, request, queryset):
        f = open('pacientes.csv', 'wb')
        writer = csv.writer(f)
        writer.writerow([ "nacionalidad","cedula", "nombres", "apellidos", "sexo", "fecha_nacimiento", "post_pago", "edad", "patron"])
        for s in queryset:
            writer.writerow([s.nacionalidad, s.cedula, s.nombres, s.apellidos, s.sexo, s.fecha_nacimiento, s.post_pago, calculate_age(s.fecha_nacimiento), s.patron or 'no aplica'])
        f.close()

        f = open('pacientes.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=stat-info.csv'
        return response
    download_csv.short_description = "Descargar CSV"


    def send_email(self, request, pacientes):
        form = SendEmailPacientesForm(initial={'pacientes': pacientes})
        falta_correo = False
        for paciente in pacientes:
            if not paciente.user.email:
                falta_correo = True
        if falta_correo:
            message= "Algunos de los pacientes seleccionados no tienen registrado un correo electronico."
            messages.warning(request, message)
        else:
            return render(request, 'mass_email.html', {'form': form, 'url': '/paciente_email/'})
    send_email.short_description = "Enviar E-mail a pacientes seleccionados"

    def nombre(self, obj):
        return obj

    def email(self, obj):
        return obj.user.email
    email.short_description = 'Correo Electronico' 

    def nacionalidad_ext(self, obj):
        a = 'Venezolano' if obj.nacionalidad=='V' else 'Extranjero'
        return a
    
    fields = [ 'cedula', 'nombre', 'sexo',  'post_pago','nacionalidad_ext','celular', 'email', 'fecha_nacimiento']
    list_display = ['cedula', 'nombre', 'sexo', 'fecha_nacimiento' ]
    readonly_fields = ('user', 'nombre','email','nacionalidad_ext','post_pago',)
admin.site.register( Pacientes, PacientesAdmin )

class CodigosAdmin( admin.ModelAdmin ):

    list_display = ['numero', 'titulo','descripcion']
    search_fields = ['titulo', 'numero', 'descripcion' ]
    list_filter = ['titulo']

    actions = ['download_csv']
    def download_csv(self, request, queryset):
        f = open('codigos.csv', 'wb')
        writer = csv.writer(f)
        writer.writerow([ "titulo","numero", "descripcion", "fecha"])
        for s in queryset:
            writer.writerow([s.titulo, s.numero, s.descripcion, s.created])
        f.close()

        f = open('codigos.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=stat-info.csv'
        return response
    download_csv.short_description = "Descargar CSV"

    def csv_button(self, obj):
        url = '/admin/csv/Codigos'
        html ='<a style="margin-left:10px;" href="%s"><b>%s</b></a>' % ( url, 'Cargar con archivo CSV')
        return html
    csv_button.allow_tags = True
    csv_button.short_description = "Cargar con CSV"

    fields = ['numero','titulo','descripcion', 'created', 'csv_button']
    readonly_fields = ('csv_button', 'created',)
admin.site.register( Codigos, CodigosAdmin )

class ResultadosAdmin( admin.ModelAdmin ):
    raw_id_fields = ['codigos', 'estudio']

    actions = ['send_email_paciente' ]
    fields =['estudio', 'paciente','impreso', 'adjunto', 'tipo_estudio']
    readonly_fields = ('impreso','paciente','tipo_estudio','resultado_link')
    list_display = ['estudio', 'paciente', 'resultado_link' ]

    def send_email_paciente(self, request, resultados):
        #form = sendResultadosForm(initial={'resultados': resultados})
        resultados_no_impresos = resultados.filter(impreso= False)
        if resultados_no_impresos:
            message= "Algunos de los resultados no han sido impresos, por ende no han sido enviados."
            messages.warning(request, message)
        resultados =  resultados.filter(impreso= True)
        falta_correo = False
        for resultado in resultados:
            tipo_estudio= resultado.estudio.estudio_realizado.tipo_estudio.nombre
            if not resultado.estudio.paciente.user.email:
                falta_correo = True
                #check citologia or biopsia
            
            else:
                if tipo_estudio == 'citologia':
                    print 'culo'
                    codigos= resultado.codigos.all()
                    html_content = render_to_string('citologia.html', {'resultado':resultado, 'codigos': codigos})
                    # create the email, and attach the HTML version as well.
                    text_content = 'Estimado(a) %s %s, Le presentamos los resultados de su citologia: ' %(str(resultado.estudio.paciente.nombres).title(), str(resultado.estudio.paciente.apellidos).title())
                    msg = EmailMultiAlternatives('Resultados de su citologia', text_content, settings.DEFAULT_FROM_EMAIL, [resultado.estudio.paciente.user.email])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                elif tipo_estudio == 'biopsia':
                    email = EmailMessage(
                        'Sus Resultados',
                        'Estimado %s, a continuacion los resultados de la biopsia- %s.' %(str(resultado.estudio.paciente).title(), str(resultado.estudio.estudio_realizado.nombre)),
                        settings.DEFAULT_FROM_EMAIL,
                        #['to1@example.com', 'to2@example.com'],
                        [resultado.estudio.paciente.user.email]
                        #reply_to=['another@example.com'],
                        #headers={'Message-ID': 'foo'},
                    )

                    file =resultado.adjunto
                    content_type = str(file.content_type)
                    file_name = str(file.name)
                    email.attach(file_name, file.read(), content_type)
                    email.send()
        if falta_correo:
            message= "Algunos de los pacientes relacionados a estos resultados no tienen registrado un correo electronico."
            messages.warning(request, message)
        
    send_email_paciente.short_description = "Enviar resultado a paciente"

    def tipo_estudio(self, resultado):
        return str(resultado.estudio.estudio_realizado.tipo_estudio).title()

    def resultado_link(self, resultado):
        tipo_estudio =  resultado.estudio.estudio_realizado.tipo_estudio
        if tipo_estudio == 'biopsia':
            current_site = Site.objects.get_current()
            base_domain = current_site.domain
            url = 'resultados_citologia/%s' %(resultado.id)
            html_link = '<a href="%s"><button type="button" style="cursor:pointer">%s</button></a>' % (resultado.adjunto, str(tipo_estudio).title())
            return html_link
        else:
            current_site = Site.objects.get_current()
            base_domain = current_site.domain
            url = str(current_site)+'resultados_citologia/%s/' %(resultado.id)
            disabled = '' if resultado.impreso == True else 'disabled'
            html_link = '<a href="%s"><button type="button" style="cursor:pointer" %s>%s</button></a>' % (url, disabled,str(tipo_estudio).title())
            return html_link
            #services_txt += html_link if len(services_txt) == 0 else '<br>'+ html_link
    resultado_link.allow_tags = True
    resultado_link.short_description = "Ver Resultado"
    # def last_name(self, obj):
    #     return smart_unicode(obj.user.last_name)
    # #user_instance.short_description = 'user_instance'
    # # search_fields = ['=id', 'condominio__rif', ]
    # # list_filter = ('timestamp', 'fechafacturacion',)  
    # # save_on_top = True
    # # form = Egresos_Condominio_Form
    # fields = [ 'user_instance', 'first_name', 'last_name','company_name',  'profile_picture', 'mobile_number', 'office_number' ]
    def paciente(self, obj):
        return obj.estudio.paciente

    

admin.site.register( Resultados, ResultadosAdmin )


class EstudiosAdmin( admin.ModelAdmin ):
    
    # def user_instance(self, obj):
    #     return 'Id: '+ str(obj.user.pk)  + ' - ' + str(obj.user.first_name) + ' ' + str(obj.user.last_name)
    # def first_name(self, obj):
    #     return smart_unicode(obj.user.first_name)
    # def last_name(self, obj):
    #     return smart_unicode(obj.user.last_name)
    # #user_instance.short_description = 'user_instance'
    actions = ['download_csv']
    def download_csv(self, request, queryset):
        f = open('estudios.csv', 'wb')
        writer = csv.writer(f)
        writer.writerow([ "estudio_realizado","paciente", "medico", "clinica", "fecha", "patron"])
        for s in queryset:
            writer.writerow([s.estudio_realizado, s.paciente, s.medico, s.clinica, s.created, s.patron or 'no aplica'])
        f.close()

        f = open('estudios.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=stat-info.csv'
        return response
    download_csv.short_description = "Descargar CSV"

    search_fields = ['id','paciente__cedula', 'paciente__nombres','paciente__apellidos', 'clinica__nombre', 'medico__nombre', 'estudio__nombre' ]
    list_filter = ('paciente__nacionalidad', 'paciente__sexo',)  
    # # save_on_top = True
    # # form = Egresos_Condominio_Form
    def estudio_title(self, obj):
        return str(obj.estudio_realizado.nombre).title()
    readonly_fields = ('impreso','created', 'last_modified_ts','estudio_title',)
    fields = [ 'paciente', 'medico','clinica',  'created', 'last_modified_ts', 'impreso' ]
    list_display = ['id','estudio_title', 'paciente', 'medico', 'clinica', 'created', 'nro_sec_mes']
admin.site.register( Estudios, EstudiosAdmin )


class Tipos_EstudiosAdmin( admin.ModelAdmin ):
	pass
    # def user_instance(self, obj):
    #     return 'Id: '+ str(obj.user.pk)  + ' - ' + str(obj.user.first_name) + ' ' + str(obj.user.last_name)
    # def first_name(self, obj):
    #     return smart_unicode(obj.user.first_name)
    # def last_name(self, obj):
    #     return smart_unicode(obj.user.last_name)
    # #user_instance.short_description = 'user_instance'
    # # search_fields = ['=id', 'condominio__rif', ]
    # # list_filter = ('timestamp', 'fechafacturacion',)  
    # # save_on_top = True
    # # form = Egresos_Condominio_Form
    # readonly_fields = ('user_instance', 'first_name', 'last_name', 'mobile_number', 'office_number', 'profile_picture', 'company_name',)
    # fields = [ 'user_instance', 'first_name', 'last_name','company_name',  'profile_picture', 'mobile_number', 'office_number' ]
    # list_display = ['id', 'first_name', 'last_name', 'company_name', 'profile_picture' ]
admin.site.register( Tipos_Estudios, Tipos_EstudiosAdmin )

class FacturasAdmin( admin.ModelAdmin ):
    list_display = ['creador', 'created', 'monto', 'paciente', 'patron' ]
    #actions = ['send_email_patron','send_email_paciente' ]
    # # save_on_top = True
    # # form = Egresos_Condominio_Form
    readonly_fields = ( 'paciente', 'patron',)

    def patron(self, factura):
        try:
            patron = factura.estudios_set.all().first().patron
            if patron:
                return patron
        except:
            return ''

    def paciente(self, factura):
        print dir(factura)
        return factura.estudios_set.all().first().paciente

    def send_email_patron(self, request, facturas):
        form = SendEmailPacientesForm(initial={'facturas': facturas})
        falta_correo = False
        for factura in facturas:
            if not paciente.user.email:
                falta_correo = True
        if falta_correo:
            message= "Algunos de los pacientes seleccionados no tienen registrado un correo electronico."
            messages.warning(request, message)
        else:
            return render(request, 'mass_email.html', {'form': form, 'url': '/factura_email/'})
    send_email_patron.short_description = "Enviar factura a patron"

    def send_email_paciente(self, request, facturas):
        form = SendEmailPacientesForm(initial={'facturas': facturas})
        falta_correo = False
        for factura in facturas:
            if not paciente.user.email:
                falta_correo = True
        if falta_correo:
            message= "Algunos de los pacientes seleccionados no tienen registrado un correo electronico."
            messages.warning(request, message)
        else:
            return render(request, 'mass_email.html', {'form': form, 'url': '/factura_email/'})
    send_email_paciente.short_description = "Enviar factura a paciente"

admin.site.register( Facturas, FacturasAdmin )

class Sub_Tipos_EstudiosAdmin( admin.ModelAdmin ):
    actions = [ 'download_csv']


    def download_csv(self, request, queryset):
        f = open('estudios_dat.csv', 'wb')
        writer = csv.writer(f)
        writer.writerow([ "nombre","tipo_estudio", "precio", "fecha"])
        for s in queryset:
            writer.writerow([s.nombre, s.tipo_estudio, s.precio, s.created ])
        f.close()

        f = open('estudios_dat.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=stat-info.csv'
        return response
    download_csv.short_description = "Descargar CSV"

    def nombre_tit(self, obj):
        return obj.nombre.title()

    def tipo_estudiox(self, obj):
        return str(obj.tipo_estudio.nombre).title()
    tipo_estudiox.short_description = 'Clasificacion'

    def csv_button(self, obj):
        current_site = Site.objects.get_current().domain
        url  = current_site + 'admin/csv/Sub_Tipos_Estudios'
        #if obj.origin_lon  and obj.origin_lat:
        url = '/admin/csv/Sub_Tipos_Estudios'
        html ='<a style="margin-left:10px;" href="%s"><b>%s</b></a>' % ( url, 'Cargar con archivo CSV')
        return html
    csv_button.allow_tags = True
    csv_button.short_description = "Cargar con CSV"


    search_fields = ['nombre', 'precio', 'tipo_estudio']
    list_filter = ('tipo_estudio',)  
    # # save_on_top = True
    # # form = Egresos_Condominio_Form
    fields = [ 'nombre','tipo_estudio','precio', 'created','last_modified_ts','csv_button' ]
    list_display = ['nombre_tit', 'tipo_estudiox', 'precio' ]
    readonly_fields = ( 'nombre_tit', 'tipo_estudiox', 'csv_button', 'created','last_modified_ts' )
    def save_model(self, request, obj, form, change):

        obj.nombre = obj.nombre.lower()
        super(Sub_Tipos_EstudiosAdmin, self).save_model(request, obj, form, change)

admin.site.register( Sub_Tipos_Estudios, Sub_Tipos_EstudiosAdmin )


class MedicosAdmin( admin.ModelAdmin ):
    list_display = ['user', 'nombre','numero_licencia', 'celular', 'direccion']

    actions = [ 'download_csv']


    def download_csv(self, request, queryset):
        f = open('medicos.csv', 'wb')
        writer = csv.writer(f)
        writer.writerow(['user', 'nombre','numero_licencia', 'celular', 'direccion'])
        for s in queryset:
            writer.writerow([s.user, s.nombre, s.numero_licencia, s.celular, s.direccion])
        f.close()

        f = open('medicos.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=stat-info.csv'
        return response
    download_csv.short_description = "Descargar CSV"

admin.site.register( Medicos, MedicosAdmin )

class ClinicasAdmin( admin.ModelAdmin ):
    list_display = ['user', 'nombre','rif', 'telefono', 'direccion']

    actions = [ 'download_csv']


    def download_csv(self, request, queryset):
        f = open('medicos.csv', 'wb')
        writer = csv.writer(f)
        writer.writerow(['user', 'nombre','rif', 'telefono', 'direccion'])
        for s in queryset:
            writer.writerow([s.user, s.nombre, s.rif, s.telefono, s.direccion])
        f.close()

        f = open('medicos.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=stat-info.csv'
        return response
    download_csv.short_description = "Descargar CSV"

admin.site.register( Clinicas, ClinicasAdmin )