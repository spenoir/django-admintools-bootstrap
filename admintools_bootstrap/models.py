from django.contrib.admin import widgets
from django import forms
from django.template.loader import render_to_string
from django.utils.html import format_html


from django.contrib import admin
from django.db.models import DateTimeField, ImageField, ForeignKey
from admintools_bootstrap.widgets import BootstrapAdminSplitDateTime, BootstrapAdminImageWidget, BootstrapRelatedFieldWidgetWrapper


class BootstrapModelAdmin(admin.ModelAdmin):
    """
        Subclass this for bootstrap widget overrides or simply copy
        the formfield_overrides over into your admin classes
    """
    formfield_overrides = {
        DateTimeField: {'widget': BootstrapAdminSplitDateTime},
        ImageField: {'widget': BootstrapAdminImageWidget},
        #ForeignKey: {'widget': BootstrapRelatedFieldWidgetWrapper}
    }


import admintools_bootstrap.settings
