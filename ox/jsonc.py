#!/usr/bin/python
# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from __future__ import with_statement

from js import minify
from utils import json


def load(filename):
    with open(filename) as f:
        data = loads(f.read())
    return data

def loads(source):
    return json.loads(minify(source))

