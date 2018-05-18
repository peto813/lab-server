"""
WSGI config for gaialabsoftware project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os, sys
#sys.path.append('/var/www/gaialabsoftware/gaialabsoftware')
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gaialabsoftware.settings")

application = get_wsgi_application()
