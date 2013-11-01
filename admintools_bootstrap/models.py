from appconf import AppConf
from django.contrib import admin
from django.db.models import DateTimeField, ImageField, DateField
from admintools_bootstrap.widgets import BootstrapAdminSplitDateTime, BootstrapAdminImageWidget, BootstrapAdminDateWidget


class BootstrapModelAdmin(admin.ModelAdmin):
    """
        Subclass this for bootstrap widget overrides or simply copy
        the formfield_overrides over into your admin classes
    """
    formfield_overrides = {
        DateTimeField: {'widget': BootstrapAdminSplitDateTime},
        DateField: {'widget': BootstrapAdminDateWidget},
        ImageField: {'widget': BootstrapAdminImageWidget},
        #ForeignKey: {'widget': BootstrapRelatedFieldWidgetWrapper}
    }



class AdminToolsBootstrapConf(AppConf):
    SITE_LINK = '/'

    class Meta:
        prefix = 'ADMINTOOLS_BOOTSTRAP'