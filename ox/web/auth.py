# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2009
import os

from ox.utils import json


def get(key):
    user_auth = os.environ.get('oxAUTH', os.path.expanduser('~/.ox/auth.json'))
    auth = {}
    if os.path.exists(user_auth):
        f = open(user_auth, "r")
        data = f.read()
        f.close()
        auth = json.loads(data)
    if key in auth:
        return auth[key]
    print "please add key %s to json file '%s'" % (key, user_auth)
    return ""

