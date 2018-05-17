# -*- coding: utf-8 -*-

# encoding=utf8  
import django_filters
from models import *
from django.db.models import Q
from django.db import models as django_models
from patient_manager.utils import calculate_age
#import models
#http://hecms.com/api/auctionproducts?category=clothing&max_price=10.00
#http://hecms.com/api/auctionproducts?lot_number=123465

class ClientePostPagoSFilter(django_filters.FilterSet):
    class Meta:
        model = ClientePostPago
        fields = '__all__'

class Codigos_Filter(django_filters.FilterSet):
    class Meta:
        model = Codigos
        fields = '__all__'


class EstudiosStatsFilter(django_filters.FilterSet):
    paciente_edad_lte = django_filters.NumberFilter( method = 'paciente_edad_lte_filter')
    paciente_edad_gte = django_filters.NumberFilter( method = 'paciente_edad_gte_filter')
    paciente_edad = django_filters.NumberFilter( method = 'paciente_edad_filter')
    paciente_edad_lt = django_filters.NumberFilter( method = 'paciente_edad_lt_filter')
    paciente_edad_gt = django_filters.NumberFilter( method = 'paciente_edad_gt_filter')
    class Meta:
        model = Estudios
        fields = '__all__'

    def paciente_edad_lt_filter(self, queryset, name, value):
        print 'peo'
        return_queryset =[]
        for estudio in queryset:
            fecha_nacimiento = estudio.paciente.fecha_nacimiento
            age = calculate_age(fecha_nacimiento)
            if age < value:
                return_queryset.append(estudio)
        return return_queryset

    def paciente_edad_gt_filter(self, queryset, name, value):
        print 'peo'
        return_queryset =[]
        for estudio in queryset:
            fecha_nacimiento = estudio.paciente.fecha_nacimiento
            age = calculate_age(fecha_nacimiento)
            if age > value:
                return_queryset.append(estudio)
        return return_queryset


    def paciente_edad_gte_filter(self, queryset, name, value):
        print 'peo'
        return_queryset =[]
        for estudio in queryset:
            fecha_nacimiento = estudio.paciente.fecha_nacimiento
            age = calculate_age(fecha_nacimiento)
            if age >= value:
                return_queryset.append(estudio)
        return return_queryset

    def paciente_edad_lte_filter(self, queryset, name, value):
        print 'peo'
        return_queryset =[]
        for estudio in queryset:
            fecha_nacimiento = estudio.paciente.fecha_nacimiento
            age = calculate_age(fecha_nacimiento)
            if age <= value:
                return_queryset.append(estudio)
        return return_queryset

    def paciente_edad_filter(self, queryset, name, value):
        print 'peo'
        return_queryset =[]
        for estudio in queryset:
            fecha_nacimiento = estudio.paciente.fecha_nacimiento
            age = calculate_age(fecha_nacimiento)
            if age == value:
                return_queryset.append(estudio)
        return return_queryset







class Estudios_Filter(django_filters.FilterSet):

    cedula = django_filters.NumberFilter(name = "paciente__cedula", lookup_expr = 'iexact')
    result_present = django_filters.BooleanFilter( method = 'result_present_filter' )
    results_printed = django_filters.BooleanFilter( method = 'results_printed_filter' )
    timestamp_lte = django_filters.IsoDateTimeFilter( name = "created", lookup_expr = 'lte')
    timestamp_gte = django_filters.IsoDateTimeFilter( name = "created", lookup_expr = 'gte')
    patron = django_filters.NumberFilter( lookup_expr = 'exact')
    #resultadosnoimpresos  = django_filters.BooleanFilter(name='resultados__impreso')
    class Meta:
        model = Estudios
        fields = ['cedula', 'impreso', 'timestamp_lte', 'timestamp_gte']



    def filter_patron(self, queryset, name, value):
        return queryset.filter(patron = value)

    def result_present_filter( self, queryset, name, value ):
        return queryset.filter(estudios__isnull = True ).exists()

    def results_printed_filter( self, estudios, name, value ):
        #print estudios.filter(resultados__isnull=True)
        return estudios.filter(Q(resultados__isnull=True) | Q(resultados__impreso=False))
        #return estudios.filter(resultados__impreso=value)


class Facturas_Filter( django_filters.FilterSet ):
    timestamp_lte = django_filters.IsoDateTimeFilter( name = "created", lookup_expr = 'lte')
    timestamp_gte = django_filters.IsoDateTimeFilter( name = "created", lookup_expr = 'gte')
    class Meta:
        model = Facturas
        fields = ['id', 'creador', 'created', 'monto', 'descuento']



class Pacientes_Filter(django_filters.FilterSet):
    timestamp_gte = django_filters.IsoDateTimeFilter(name = "user__date_joined", lookup_expr = 'gte')
    timestamp_lte = django_filters.IsoDateTimeFilter(name = "user__date_joined", lookup_expr = 'lte')
    patron = django_filters.NumberFilter( lookup_expr = 'exact')
    post_pago = django_filters.BooleanFilter()

    def filter_post_pago(self, queryset, name, value):
        return queryset.filter(published_on__isnull=False)


    def filter_patron(self, queryset, name, value):
        # construct the full lookup expression.
        #lookup = '__'.join([name, 'isnull'])
        return queryset.filter(patron = value)

    class Meta:
        model = Pacientes
        fields = [  'cedula', 'nombres', 'apellidos', 'fecha_nacimiento', 'sexo', 'celular', 'user__date_joined' ]
        #fields = {"search_param": ['iexact', 'icontains', 'in', 'startswith']}


class Resultados_Filter( django_filters.FilterSet ):
    class Meta:
        model = Resultados
        fields = ['impreso', 'estudio']
