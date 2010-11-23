import time

from django.db import models
from django.utils import simplejson as json


def to_json(python_object):
    if isinstance(python_object, time.struct_time):          
        return {'__class__': 'time.asctime',
                '__value__': time.asctime(python_object)}    
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': list(python_object)}
    raise TypeError(repr(python_object) + ' is not JSON serializable')

def from_json(json_object):                                  
    if '__class__' in json_object:                            
        if json_object['__class__'] == 'time.asctime':
            return time.strptime(json_object['__value__'])    
        if json_object['__class__'] == 'bytes':
            return bytes(json_object['__value__'])            
    return json_object
    
class DictField(models.TextField):
    """DictField is a textfield that contains JSON-serialized dictionaries."""

    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        """Convert our string value to python after we load it from the DB"""
        if isinstance(value, dict):
            return value
        try:
            value = json.loads(value, object_hook=from_json)
        except: #this is required to load fixtures
            value = eval(value)
        assert isinstance(value, dict)
        return value

    def get_db_prep_save(self, value):
        """Convert our JSON object to a string before we save"""
        assert isinstance(value, dict)
        value = json.dumps(value, default=to_json)
        return super(DictField, self).get_db_prep_save(value)

class TupleField(models.TextField):
    """TupleField is a textfield that contains JSON-serialized tuples."""

    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""
        if isinstance(value, tuple):
            return value

        try:
            value = json.loads(value, object_hook=from_json)
        except: #this is required to load fixtures
            value = eval(value)
        assert isinstance(value, list)
        return tuple(value)

    def get_db_prep_save(self, value):
        """Convert our JSON object to a string before we save"""
        assert isinstance(value, tuple)
        value = json.dumps(value, default=to_json)
        return super(TupleField, self).get_db_prep_save(value)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^oxdjango\.fields\.DictField"])
    add_introspection_rules([], ["^oxdjango\.fields\.TupleField"])
except:
    pass
