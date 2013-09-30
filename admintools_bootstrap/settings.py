from appconf import AppConf


BUNDLES = (

)


class AdminToolsBootstrapConf(AppConf):
    SITE_LINK = '/'

    class Meta:
        prefix = 'ADMINTOOLS_BOOTSTRAP'
        proxy = True


admin_settings = AdminToolsBootstrapConf()

if getattr(admin_settings, 'MEDIA_BUNDLES'):
    admin_settings.MEDIA_BUNDLES += BUNDLES
else:
    setattr(admin_settings, 'MEDIA_BUNDLES', BUNDLES)