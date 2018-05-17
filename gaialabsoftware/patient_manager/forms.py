# -*- coding: utf-8 -*-
from django import  forms
from patient_manager.models import *

# from django.contrib import messages
# from django.core.validators import RegexValidator
# from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
# from usuario.validators import user_validator
# import re, datetime
# from django.contrib.admin import widgets
# from django.db.models import Count, Min, Sum, Avg
# from tucondominioaldia.mypythonmethods import estados, municipios, parroquias, listado_de_bancos, is_luhn_valid, monthName, get_currency
# from django.utils import timezone
# from django.forms import ModelChoiceField
# from django.conf import settings



class Cargar_Codigos_CSV(forms.Form):
    file = forms.FileField(required = True)
    def clean_file(self):
        if str(self.cleaned_data.get( 'file' ).content_type) == 'text/csv':
            return self.cleaned_data.get( 'file' )
        raise forms.ValidationError("Formato de archivo equivocado" )


class SendEmailPacientesForm(forms.Form):
    pacientes = forms.ModelMultipleChoiceField(label="Para:",
                                           queryset=Pacientes.objects.all(),
                                           widget=forms.SelectMultiple())
    asunto = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Subject')}))
    mensaje = forms.CharField(widget=forms.Textarea)
    adjunto = forms.FileField(required= False)

class sendResultadosForm(SendEmailPacientesForm):
    pacientes = forms.ModelMultipleChoiceField(label="Para:",
                                           queryset=Resultados.objects.all(),
                                           widget=forms.SelectMultiple())


class MyDashboardStatsCriteriaAdminForm(forms.ModelForm):

    class Meta:
        model = MyDashboardStatsCriteria
        fields = '__all__'
        help_texts = {
            'criteria_name': ('Debe ser una palabra unica. Ej. estado, si, no'),
            'criteria_fix_mapping': ('Debe ser una palabra unica. Ej. estado, si, no'),
            'dynamic_criteria_field_name': ('Debe ser una palabra unica. Ej. estado, si, no'),
            'criteria_dynamic_mapping': ('Debe ser una palabra unica. Ej. estado, si, no')
        }
        labels = {
            'criteria_name': _('Nombre de Criterio'),
            'criteria_fix_mapping': _('Nombre de Criterio'),
            'dynamic_criteria_field_name': _('Nombre de Criterio'),
            'criteria_dynamic_mappingcriteria_dynamic_mapping': _('Nombre de Criterio')
        }