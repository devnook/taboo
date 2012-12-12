import simplejson

from google.appengine.ext import db

import datetime
import time

SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

def to_dict(model):
  output = {}

  for key, prop in model.properties().iteritems():
    value = getattr(model, key)

    if value is None or isinstance(value, SIMPLE_TYPES):
      output[key] = value
    elif isinstance(value, datetime.date):
      # Convert date/datetime to ms-since-epoch ("new Date()").
      ms = time.mktime(value.utctimetuple())
      ms += getattr(value, 'microseconds', 0) / 1000
      output[key] = int(ms)
    elif isinstance(value, db.GeoPt):
      output[key] = {'lat': value.lat, 'lon': value.lon}
    elif isinstance(value, db.Model):
      output[key] = to_dict(value)
    else:
      raise ValueError('cannot encode ' + repr(prop))

  return output


class Word(db.Model):
  word = db.StringProperty(required=True)
  forbidden_words = db.StringListProperty()
  created = db.DateTimeProperty(auto_now_add=True)

  def dict(self):
    obj = {
      'word': self.word,
      'forbidden_words': self.forbidden_words
    }
    return obj

class Task(db.Model):
  word = db.StringProperty(required=True)
  description = db.StringProperty(required=True)
  owner = db.UserProperty(required=True)
  assignee = db.UserProperty()

  def dict(self):
    obj = {
      'word': self.word,
      'description': self.description,
      'key': self.key().__str__(),
      'owner': self.owner.__str__()
    }
    return obj



class Solution(db.Model):
  task = db.ReferenceProperty(Task)
  owner = db.UserProperty()
