# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from celery.utils import get_full_cls_name
from celery.backends import default_backend

from shortcuts import json_response


def task_status(request, task_id):
    response = json_response(status=200, text='ok')
    status = default_backend.get_status(task_id)
    res = default_backend.get_result(task_id)
    response['data'] = {
        'id':     task_id,
        'status': status,
        'result': res
    }
    if status in default_backend.EXCEPTION_STATES:
        traceback = default_backend.get_traceback(task_id)
        response['data'].update({'result':    str(res.args[0]),
                                 'exc':       get_full_cls_name(res.__class__),
                                 'traceback': traceback})
    return response

