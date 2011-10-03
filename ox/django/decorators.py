# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

try:
    from django.contrib.auth.decorators import wraps
except:
    from django.utils.functional import wraps
from shortcuts import render_to_json_response

def login_required_json(function=None):
    """
    Decorator for views that checks that the user is logged in
    return json error if not logged in.
    """

	def _wrapped_view(request, *args, **kwargs):
		if request.user.is_authenticated():
			return function(request, *args, **kwargs)
		return render_to_json_response({'status': {'code': 401, 'text': 'login required'}})
	return wraps(function)(_wrapped_view)

def admin_required_json(function=None):
    """
    Decorator for views that checks that the user is logged in
    return json error if not logged in.
    """

	def _wrapped_view(request, *args, **kwargs):
		if request.user.is_authenticated() and request.user.get_profile().get_level() == 'admin':
			return function(request, *args, **kwargs)
		return render_to_json_response({'status': {'code': 403, 'text': 'permission denied'}})
	return wraps(function)(_wrapped_view)
