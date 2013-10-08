from appconf import AppConf
from django.conf import settings


ADMIN_MEDIA_BUNDLES = (

    ('admin.css',
        'admintools_bootstrap/chosen/chosen.css',
        'admintools_bootstrap/lib/datepicker.scss',
        'admintools_bootstrap/lib/bootstrap-fileupload.scss',
        'admintools_bootstrap/sass/admin.scss',
    ),

    #('admin_dashboard.css',
    #    'admintools_bootstrap/sass/dashboard.scss',
    #),

    ('admin.js',
        'admintools_bootstrap/js/lazyload.js',
        'admintools_bootstrap/js/jquery-1.9.1.js',
        'admintools_bootstrap/js/jquery-ui-1.10.3.custom.js',
        'admintools_bootstrap/js/json2.js',
        'admin_tools/js/jquery/jquery.cookie.min.js',
        'admin_tools/js/menu.js',
        'admintools_bootstrap/chosen/chosen.jquery.js',
        'admintools_bootstrap/js/bootstrap/dropdown.js',
        'admintools_bootstrap/js/bootstrap/alert.js',
        'admintools_bootstrap/js/bootstrap-datepicker.js',
        'admintools_bootstrap/js/bootstrap-fileupload.js',
        'admintools_bootstrap/js/dismissAddAnotherPopup.js',
        'admintools_bootstrap/js/admin.js',
    ),

    #('admin_dashboard.js',
    #    'admin_tools/js/jquery/jquery.dashboard.js',
    #    'admin_tools/js/dashboard.js',
    #),
)


class AdminToolsBootstrapConf(AppConf):
    SITE_LINK = '/'

    class Meta:
        prefix = 'ADMINTOOLS_BOOTSTRAP'


if getattr(settings, 'MEDIA_BUNDLES'):
    settings.MEDIA_BUNDLES += ADMIN_MEDIA_BUNDLES
else:
    setattr(settings, 'MEDIA_BUNDLES', ADMIN_MEDIA_BUNDLES)