# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import datetime
from django.utils import datetime_safe
from django.http import HttpResponse, Http404
try:
    import simplejson as json
except ImportError:
    from django.utils import simplejson as json
from django.conf import settings

class HttpErrorJson(Http404):
    def __init__(self, response):
        self.response = response

def json_response(data=None, status=200, text='ok'):
    if not data:
        data = {}
    return {'status': {'code': status, 'text': text}, 'data': data}

def _to_json(python_object):
    if isinstance(python_object, datetime.datetime):
        if python_object.year < 1900:
            tt = python_object.timetuple()
            return '%d-%02d-%02dT%02d:%02d%02dZ' % tuple(list(tt)[:6])
        return python_object.strftime('%Y-%m-%dT%H:%M:%SZ')
    if isinstance(python_object, datetime_safe.datetime):
        return python_object.strftime('%Y-%m-%dT%H:%M:%SZ')
    raise TypeError(u'%s %s is not JSON serializable' % (repr(python_object), type(python_object)))

def render_to_json_response(dictionary, content_type="text/json", status=200):
    indent=None
    if settings.DEBUG:
        content_type = "text/javascript"
        indent = 2
    if getattr(settings, 'JSON_DEBUG', False):
        print json.dumps(dictionary, indent=2, default=_to_json, ensure_ascii=False).encode('utf-8')

    return HttpResponse(json.dumps(dictionary, indent=indent, default=_to_json,
        ensure_ascii=False).encode('utf-8'), content_type=content_type, status=status)

def get_object_or_404_json(klass, *args, **kwargs):
    from django.shortcuts import _get_queryset
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        response = {'status': {'code': 404,
                               'text': '%s not found' % queryset.model._meta.object_name}}
        raise HttpErrorJson(response)

