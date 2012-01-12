#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.sites.models import Site

def site(request):
    """
        adds `site` template variable
    """
    return {'site': Site.objects.get_current()}
