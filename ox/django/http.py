# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import os
import mimetypes

from django.http import HttpResponse, Http404
from django.conf import settings


def HttpFileResponse(path, content_type=None, filename=None):
    if not os.path.exists(path):
        raise Http404
    if not content_type:
        content_type = mimetypes.guess_type(path)[0]
    if settings.XACCELREDIRECT:
        response = HttpResponse()
        response['Content-Length'] = os.stat(path).st_size
        if path.startswith(settings.STATIC_ROOT):
            path = settings.STATIC_URL + path[len(settings.STATIC_ROOT)+1:]
        if path.startswith(settings.MEDIA_ROOT):
            path = settings.MEDIA_URL + path[len(settings.MEDIA_ROOT)+1:]
        response['X-Accel-Redirect'] = path
        response['Content-Type'] = content_type
    elif settings.XSENDFILE:
        response = HttpResponse()
        response['X-Sendfile'] = path
        response['Content-Type'] = content_type
        response['Content-Length'] = os.stat(path).st_size
    else:
        response = HttpResponse(open(path), content_type=content_type)
    if filename:
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response

