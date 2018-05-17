# -*- coding: utf-8 -*-
from django.db import models
from django.db import connection
from datetime import date, datetime

class EstudioManager(models.Manager):
	def query_for_lab(self, lab):
		return self.filter(registrado_por__laboratorio = lab)

class PacienteManager(models.Manager):
	def calculate_age(self,born):
	    today = date.today()
	    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class ReportsManager(models.Manager):
	def get_report(self, date_obj):
		if type(date_obj) is not datetime:
		    raise TypeError('arg must be a datetime.datetime, not a %s' % type(date_obj))
		report= {}
		minDate = date_obj.replace(year = 2016)
		maxDate = date_obj
		facturas_dia = self.filter(created__range=(minDate, maxDate))
		print facturas_dia
		print minDate, maxDate
        # self.filter(id__in = del_list).delete()
        # condominio_activator(self, condominio)
		return report

def time():
	from django.utils import timezone
	print 'culo'
	return timezone.now()