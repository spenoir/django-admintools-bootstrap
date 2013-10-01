from appconf import AppConf


ADMIN_MEDIA_BUNDLES = (

    ('admin.css',
        'admintools_bootstrap/chosen/chosen.css',
        'admintools_bootstrap/sass/admin.scss',
    ),

    ('admin_dashboard.css',
        'admintools_bootstrap/sass/dashboard.scss',
    ),

    ('admin.js',
        'js/lazyload.js',
        'admintools_bootstrap/js/jquery-1.9.1.min.js',
        'admintools_bootstrap/js/json2.js',
        'admin_tools/js/jquery/jquery.cookie.min.js',
        'admin_tools/js/menu.js',
        'admintools_bootstrap/chosen/chosen.jquery.min.js',
        'admintools_bootstrap/js/bootstrap/dropdown.js',
        'admintools_bootstrap/js/bootstrap/alert.js',
        'admintools_bootstrap/js/dismissAddAnotherPopup.js',
        'admintools_bootstrap/js/admin.js',
    ),

    ('admin_dashboard.js',
        'admin_tools/js/jquery/jquery.dashboard.js',
        'admin_tools/js/dashboard.js',
    ),
)


class AdminToolsBootstrapConf(AppConf):
    SITE_LINK = '/'

    class Meta:
        prefix = 'ADMINTOOLS_BOOTSTRAP'
        proxy = True


admin_settings = AdminToolsBootstrapConf()

if getattr(admin_settings, 'MEDIA_BUNDLES'):
    admin_settings.MEDIA_BUNDLES += ADMIN_MEDIA_BUNDLES
else:
    setattr(admin_settings, 'MEDIA_BUNDLES', ADMIN_MEDIA_BUNDLES)