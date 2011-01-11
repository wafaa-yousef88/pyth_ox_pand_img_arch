# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
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

def render_to_json_response(dictionary, content_type="text/json", status=200):
    indent=None
    if settings.DEBUG:
        content_type = "text/javascript"
        indent = 2
    if settings.JSON_DEBUG:
        print json.dumps(dictionary, indent=2)
    if 'status' in dictionary and 'code' in dictionary['status']:
			status = dictionary['status']['code']
    return HttpResponse(json.dumps(dictionary, indent=indent),
                        content_type=content_type, status=status)

def get_object_or_404_json(klass, *args, **kwargs):
    from django.shortcuts import _get_queryset
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        response = {'status': {'code': 404,
                               'text': '%s not found' % queryset.model._meta.object_name}}
        raise HttpErrorJson(response)

