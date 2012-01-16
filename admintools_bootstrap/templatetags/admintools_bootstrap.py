from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.utils.translation import ugettext as _
from django.contrib.admin.views.main import PAGE_VAR, ALL_VAR
from django.conf import settings
from django.contrib.sites.models import Site

from BeautifulSoup import BeautifulSoup


register = template.Library()


@register.simple_tag
def atb_site_link():
    if settings.ADMINTOOLS_BOOTSTRAP_SITE_LINK:
        return '''
            <li><a href="%s"  class="top-icon" title="%s" rel="popover" data-placement="below"><span class="ui-icon ui-icon-home ui-state-default"></span></a></li>
            ''' % (settings.ADMINTOOLS_BOOTSTRAP_SITE_LINK, _('Open site'))
    else:
        return ''

@register.simple_tag
def atb_site_name():
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        return Site.objects.get_current().name
    else:
        return _('Django site')


@register.simple_tag
def bootstrap_page_url(cl, page_num):
    """
        generates page URL for given page_num, uses for prev and next links
        django numerates pages from 0
    """
    return escape(cl.get_query_string({PAGE_VAR: page_num-1}))

DOT = '.'

def bootstrap_paginator_number(cl,i, li_class=None):
    """
    Generates an individual page index link in a paginated list.
    """
    if i == DOT:
        return u'<li><a href="#">...</a></li>'
    elif i == cl.page_num:
        return mark_safe(u'<li class="active"><a href="#">%d</a></li> ' % (i+1))
    else:
        return mark_safe(u'<li><a href="%s">%d</a></li>' % (escape(cl.get_query_string({PAGE_VAR: i})), i+1))
paginator_number = register.simple_tag(bootstrap_paginator_number)


def bootstrap_pagination(cl):
    """
    Generates the series of links to the pages in a paginated list.
    """
    paginator, page_num = cl.paginator, cl.page_num

    pagination_required = (not cl.show_all or not cl.can_show_all) and cl.multi_page
    if not pagination_required:
        page_range = []
    else:
        ON_EACH_SIDE = 3
        ON_ENDS = 2

        # If there are 10 or fewer pages, display links to every page.
        # Otherwise, do some fancy
        if paginator.num_pages <= 10:
            page_range = range(paginator.num_pages)
        else:
            # Insert "smart" pagination links, so that there are always ON_ENDS
            # links at either end of the list of pages, and there are always
            # ON_EACH_SIDE links at either end of the "current page" link.
            page_range = []
            if page_num > (ON_EACH_SIDE + ON_ENDS):
                page_range.extend(range(0, ON_EACH_SIDE - 1))
                page_range.append(DOT)
                page_range.extend(range(page_num - ON_EACH_SIDE, page_num + 1))
            else:
                page_range.extend(range(0, page_num + 1))
            if page_num < (paginator.num_pages - ON_EACH_SIDE - ON_ENDS - 1):
                page_range.extend(range(page_num + 1, page_num + ON_EACH_SIDE + 1))
                page_range.append(DOT)
                page_range.extend(range(paginator.num_pages - ON_ENDS, paginator.num_pages))
            else:
                page_range.extend(range(page_num + 1, paginator.num_pages))

    need_show_all_link = cl.can_show_all and not cl.show_all and cl.multi_page
    return {
        'cl': cl,
        'pagination_required': pagination_required,
        'show_all_url': need_show_all_link and cl.get_query_string({ALL_VAR: ''}),
        'page_range': page_range,
        'ALL_VAR': ALL_VAR,
        '1': 1,
        'curr_page': cl.paginator.page(cl.page_num+1),
    }
bootstrap_pagination = register.inclusion_tag('admin/pagination.html')(bootstrap_pagination)

# breadcrumbs tag

class BreadcrumbsNode(template.Node):
    """
        renders bootstrap breadcrumbs list.
        usage::
            {% breadcrumbs %}
            url1|text1
            url2|text2
            text3
            {% endbreadcrumbs %}
        | is delimiter by default, you can use {% breadcrumbs delimiter_char %} to change it.
        lines without delimiters are interpreted as active breadcrumbs

    """
    def __init__(self, nodelist, delimiter):
        self.nodelist = nodelist
        self.delimiter = delimiter

    def render(self, context):
        data = self.nodelist.render(context).strip()

        if not data:
            return ''

        try:
            data.index('<div class="breadcrumbs">')
        except ValueError:
            lines = [ l.strip().split(self.delimiter) for l in data.split("\n") if l.strip() ]
        else:
            # data is django-style breadcrumbs, parsing
            try:
                soup = BeautifulSoup(data)
                lines = [ (a.get('href'), a.text) for a in soup.findAll('a')]
                lines.append([soup.find('div').text.split('&rsaquo;')[-1].strip()])
            except Exception, e:
                lines = [["Cannot parse breadcrumbs: %s" % unicode(e)]]

        print lines


        out = '<ul class="breadcrumb">'
        curr = 0
        for d in lines:
            if d[0][0] == '*':
                active = ' class="active"'
                d[0] = d[0][1:]
            else:
                active = ''

            curr += 1
            if (len(lines) == curr):
                # last
                divider = ''
            else:
                divider = '<span class="divider">/</span>'

            if len(d) == 2:
                out += '<li%s><a href="%s">%s</a>%s</li>' % (active, d[0], d[1], divider)
            elif len(d) == 1:
                out += '<li%s>%s%s</li>' % (active, d[0], divider)
            else:
                raise ValueError('Invalid breadcrumb line: %s' % self.delimiter.join(d))
        out += '</ul>'
        return out

@register.tag(name='breadcrumbs')
def do_breadcrumbs(parser, token):
    try:
        tag_name, delimiter = token.contents.split(None, 1)
    except ValueError:
        delimiter = '|'

    nodelist = parser.parse(('endbreadcrumbs',))
    parser.delete_first_token()

    return BreadcrumbsNode(nodelist, delimiter)
