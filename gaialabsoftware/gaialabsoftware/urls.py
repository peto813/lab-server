# -*- coding: utf-8 -*-

# encoding=utf8  
"""gaialabsoftware URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
#DJANGO IMPORTS
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import *
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# REST FRAMEWORK IMPORTS
from rest_framework import routers

#VIEWS IMPORTS
from patient_manager.views import (
	Index_View,
	ResultadosViewSet,
	ImprimirEstudiosView,
	CodigosViewSet,
	EstudioNoImpresoView,
	FirstPatientView,
    VerifyPatientView,
    PacientesViewSet,
    EstudiosView,
    EstudiosRealizadosViewSet,
    CargarCSV,
    ResultadosCodigosViewSet,
    EstudiosViewSet,
    ContribuyenteView,
    FacturasViewSet,
    #FacturaView,
    CustomLoginView,
    ClientesPostPagoViewSet,
    PacientePostPagoView,
    PacientesPostPagoViewSet,
    VerifyPatientPostPagoView,
    generarNotaPostPagoView,
    CustomLoginView,
    CustomUserDetailsView,
    ChartsView,
    pacienteEmailView,
    ResultadosCitologiaView,
    SexoPacienteEstadisticaView,
    NacionalidadPacienteEstadisticaView,
    TipoPacienteEstadisticaView,
    PreciosView,
    EstudiosEstadisticaView,
    reportesViewSet,
    InitialView,
	)


#REST FRAMEWORK VIEWSET ROUTER
router = routers.DefaultRouter()
router.register(r'pacientes', PacientesViewSet)
router.register(r'pacientes_post_pago', PacientesPostPagoViewSet)
router.register(r'estudios_realizados', EstudiosRealizadosViewSet)
router.register(r'codigos', CodigosViewSet)
router.register(r'resultados', ResultadosViewSet)
router.register(r'resultados_codigos', ResultadosCodigosViewSet)
router.register(r'estudios_model', EstudiosViewSet)
router.register(r'facturas', FacturasViewSet)
router.register(r'clientes_postpago', ClientesPostPagoViewSet)
router.register(r'estudios_estadisticas', EstudiosEstadisticaView)

#URLS
urlpatterns = [
    url(r'^admin_tools/', include('admin_tools.urls')),
    #REST FRAMEWORK ROUTER URL
    url(r'^api/', include(router.urls)),

    #DJANGO URLS
    url(r'^rest-auth/login/$', CustomLoginView.as_view(), name='rest_login'),
     url(r'^rest-auth/user/$', CustomUserDetailsView.as_view(), name='rest_user_details'),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/csv/(.*?)/', CargarCSV.as_view(), name='csv_codigos' ),
    #url(r'^admin/csv_estudios/', CargarCSVEstudios.as_view(), name='csv_estudios' ),
    url(r'^$', Index_View.as_view(), name = 'index'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^api/verify_patient', VerifyPatientView.as_view(), name = 'verify_patient'),
    url(r'^api/verify_post_pago_patient', VerifyPatientPostPagoView.as_view(), name = 'verify_post_pago_patient'),
    url(r'^api/estudios/', EstudiosView.as_view(), name = 'estudios'),
    url(r'^api/first_patient/', FirstPatientView.as_view(), name = 'first_patient'),
    url(r'^api/deleteunprinted/', EstudioNoImpresoView.as_view(), name = 'deleteunprinted'),
    url(r'^api/imprimir_estudios/(?P<cedula>[0-9]+)/(?P<nacionalidad>[A-Za-z]{1})$', ImprimirEstudiosView.as_view(), name = 'imprimir_estudios'),
    url(r'^api/generar_nota_postpago/(?P<cedula>[0-9]+)/(?P<nacionalidad>[A-Za-z]{1})$', generarNotaPostPagoView.as_view(), name = 'generar_nota_postpago'),    
    url(r'^api/contribuyente/', ContribuyenteView.as_view(), name = 'api/contribuyente/'),
    url(r'^api/paciente_post_pago/', PacientePostPagoView.as_view(), name='paciente_post_pago'),
    url(r'^api/reportes/$', reportesViewSet.as_view(), name='reportes'),
    url(r'^api/reportes/(?P<mes>.*?)/$', reportesViewSet.as_view(), name='reportes'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^charts/', ChartsView.as_view(), name='charts'),
    url(r'^api/precios/', PreciosView.as_view(), name='precios'),
    url(r'^api/initial/', InitialView.as_view(), name='precios'),
    #ADMIN EMAIL URLS
    url(r'^paciente_email/', pacienteEmailView.as_view(), name='paciente_email'),
    url(r'^resultados_citologia/(?P<pk>[0-9]+)/$', ResultadosCitologiaView.as_view(), name='resultados_citologia'),
    #url(r'^factura/', FacturaView.as_view(), name = 'factura')

    #STATISTICS URLS
    url(r'^api/sexo_paciente/', SexoPacienteEstadisticaView.as_view(), name = 'sexo_paciente'),
    url(r'^api/nacionalidad_paciente/', NacionalidadPacienteEstadisticaView.as_view(), name = 'nacionalidad_paciente'),
    url(r'^api/tipo_paciente/', TipoPacienteEstadisticaView.as_view(), name = 'tipo_paciente'),
    #url(r'^api/estudios_estadisticas/', EstudiosEstadisticaView.as_view(), name = 'estudios_estadisticas'),
]

# urlpatterns += i18n_patterns(
#     url(r'^admin/', include(admin.site.urls)),
# )

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)