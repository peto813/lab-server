# -*- coding: utf-8 -*-
"""
This file was generated with the custommenu management command, it contains
the classes for the admin menu, you can customize this class as you want.

To activate your custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'gaialabsoftware.menu.CustomMenu'
"""

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu


class CustomMenu(Menu):
    """
    Custom Menu for gaialabsoftware admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Inicio'), reverse('admin:index')),
            #items.Bookmarks(),
            items.AppList(
                _('Applications'),
                exclude=('django.contrib.*','rest_framework.authtoken.*',)
            ),
            items.AppList(
                _('Administration'),
                models=('django.contrib.*',),
            ),
            items.MenuItem('Herramientas',
                children=[
                    items.MenuItem('Estadisticas', '/charts'),
                    #items.MenuItem('Estadisticas', '/bar/'),
                ]
            )
        ]




    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomMenu, self).init_with_context(context)
