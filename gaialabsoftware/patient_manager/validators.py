# -*- coding: utf-8 -*-
def validate_positive_num(value):
	try:
	    if int(value) < 0:
	        raise ValidationError(
	            _('%(value)s value is not positive'),
	            params={'value': value},
	        )
	except:
		raise ValidationError(
			_('%(value)s not number'),
			params={'value': value},
		)	
