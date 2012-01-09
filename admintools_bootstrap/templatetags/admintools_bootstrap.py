from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.contrib.admin.views.main import PAGE_VAR, ALL_VAR


register = template.Library()

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
