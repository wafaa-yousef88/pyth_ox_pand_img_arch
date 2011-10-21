# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import os
import mimetypes
from datetime import datetime, timedelta

from django.http import HttpResponse, Http404
from django.conf import settings


def HttpFileResponse(path, content_type=None, filename=None):
    if not os.path.exists(path):
        raise Http404
    if not content_type:
        content_type = mimetypes.guess_type(path)[0]
    if not content_type:
        content_type = 'application/octet-stream'
    
    if getattr(settings, 'XACCELREDIRECT', False):
        response = HttpResponse()
        response['Content-Length'] = os.stat(path).st_size
        
        for PREFIX in ('STATIC', 'MEDIA'):
            root = getattr(settings, PREFIX+'_ROOT', '')
            url = getattr(settings, PREFIX+'_URL', '')
            if root and path.startswith(root):
                path = url + path[len(root)+1:]
        response['X-Accel-Redirect'] = path
        if content_type:
            response['Content-Type'] = content_type
    elif getattr(settings, 'XSENDFILE', False):
        response = HttpResponse()
        response['X-Sendfile'] = path
        if content_type:
            response['Content-Type'] = content_type
        response['Content-Length'] = os.stat(path).st_size
    else:
        response = HttpResponse(open(path), content_type=content_type)
    if filename:
       response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    response['Expires'] = datetime.strftime(datetime.utcnow() + timedelta(days=1), "%a, %d-%b-%Y %H:%M:%S GMT")
    return response

