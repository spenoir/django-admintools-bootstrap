import os
import logging

from django import forms
from django.template.loader import render_to_string
from django.conf import settings
from PIL import Image


logger = logging.getLogger(__name__)

try:
    from sorl.thumbnail.main import DjangoThumbnail

    def thumbnail(image_path):
        t = DjangoThumbnail(relative_source=image_path, requested_size=(200, 200))
        return u'<img src="%s" alt="%s" />' % (t.absolute_url, image_path)
except ImportError:
    def thumbnail(image_path):
        absolute_url = os.path.join(settings.MEDIA_ROOT, image_path)
        return u'<img src="%s" alt="%s" />' % (absolute_url, image_path)


class BootstrapAdminImageWidget(forms.ClearableFileInput):
    """
        A FileField Widget that displays an image instead of a file path
        if the current file is an image.
    """

    def render(self, name, value, attrs=None):

        file_name = str(value)
        if file_name:
            file_path = '%s%s' % (settings.MEDIA_URL, file_name)
            context = {
                'file_path': file_path,
                'file_name': file_name,
                'thumbnail': thumbnail(file_name),
            }
            try:
                Image.open(os.path.join(settings.MEDIA_ROOT, file_name))

            except IOError, e:
                logger.error(e)

            self.template_with_initial = render_to_string(
                'admin/widgets/_image_widget.html',
                dictionary=context
            )

        return self.template_with_initial
