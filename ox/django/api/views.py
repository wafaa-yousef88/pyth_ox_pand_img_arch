# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from __future__ import division, with_statement

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from ..shortcuts import render_to_json_response, json_response

from actions import actions

def api(request):
    if request.META['REQUEST_METHOD'] == "OPTIONS":
        response = render_to_json_response({'status': {'code': 200,
                                                       'text': 'use POST'}})
        response['Access-Control-Allow-Origin'] = '*'
        return response
    if not 'action' in request.POST:
        methods = actions.keys()
        api = []
        for f in sorted(methods):
            api.append({'name': f,
                        'doc': actions.doc(f).replace('\n', '<br>\n')})
        context = RequestContext(request, {
            'api': api,
            'settings': settings,
            'sitename': settings.SITENAME
        })
        return render_to_response('api.html', context)
    action = request.POST['action']
    version = getattr(request, 'version', None)
    if version:
        f = actions.versions.get(version, {}).get(action, actions.get(action))
    else:
        f = actions.get(action)
    if f:
        response = f(request)
    else:
        response = render_to_json_response(json_response(status=400,
                                text='Unknown action %s' % action))
    response['Access-Control-Allow-Origin'] = '*'
    return response

