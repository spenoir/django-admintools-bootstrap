import os
import logging

from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.conf import settings
from PIL import Image
from django.utils.html import format_html


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


class BootstrapFilteredSelectMultiple(forms.SelectMultiple):
    """
        removing 2 select fields widget
    """

    def __init__(self, verbose_name, is_stacked, attrs=None, choices=[]):
        super(BootstrapFilteredSelectMultiple, self).__init__(attrs, choices)


class BootstrapAdminDateWidget(forms.DateInput):

    def render(self, name, value, attrs=None):
        context = {
            'name': name,
            'value': value,
            'attrs': attrs
        }
        return render_to_string(
            'admin/widgets/_admin_date_widget.html',
            dictionary=context
        )


class BootstrapAdminTimeWidget(forms.TimeInput):

    def render(self, name, value, attrs=None):
        context = {
            'name': name,
            'value': value,
            'attrs': attrs
        }
        return render_to_string(
            'admin/widgets/_admin_date_widget_mirror.html',
            dictionary=context
        )


class BootstrapAdminSplitDateTime(forms.SplitDateTimeWidget):
    """
    A SplitDateTime Widget that has some admin-specific styling.
    """
    def __init__(self, attrs=None):
        widgets = [BootstrapAdminDateWidget, BootstrapAdminTimeWidget]
        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
        # we want to define widgets.
        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        return format_html('%s%s' % (rendered_widgets[0],rendered_widgets[1]))


class BootstrapRelatedFieldWidgetWrapper(forms.Widget):

    def __init__(self, widget, rel, admin_site, can_add_related=None):
        self.is_hidden = widget.is_hidden
        self.needs_multipart_form = widget.needs_multipart_form
        self.attrs = widget.attrs
        self.choices = widget.choices
        self.widget = widget
        self.rel = rel
        # Backwards compatible check for whether a user can add related
        # objects.
        if can_add_related is None:
            can_add_related = rel.to in admin_site._registry
        self.can_add_related = can_add_related
        # so we can check if the related object is registered with this AdminSite
        self.admin_site = admin_site

    @property
    def media(self):
        return self.widget.media

    def render(self, name, value, *args, **kwargs):
        rel_to = self.rel.to
        info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
        self.widget.choices = self.choices
        output = [self.widget.render(name, value, *args, **kwargs)]
        if self.can_add_related:

            context = {
                'output': output,
                'related_url': reverse('admin:%s_%s_add' % info, current_app=self.admin_site.name),
                'name': name
            }

            return render_to_string(
                'admin/widgets/_admin_related_widget.html',
                dictionary=context
            )

    def build_attrs(self, extra_attrs=None, **kwargs):
        "Helper function for building an attribute dictionary."
        self.attrs = self.widget.build_attrs(extra_attrs=None, **kwargs)
        return self.attrs

    def value_from_datadict(self, data, files, name):
        return self.widget.value_from_datadict(data, files, name)

    def _has_changed(self, initial, data):
        return self.widget._has_changed(initial, data)

    def id_for_label(self, id_):
        return self.widget.id_for_label(id_)