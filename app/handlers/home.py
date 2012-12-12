import datetime
import logging
import simplejson

import abstract_handler
from google.appengine.api import users

from google.appengine.ext import db


from models import models




BLOG_KEY = 'ag1kZXZ-Z3Vlc3Rib29rcgoLEgRTaXRlGAEM'


class Error(Exception):
  """Base error class"""



class GetTaskHandler(abstract_handler.AbstractHandler):

  def findTask(self, retry):
    task = None
    tasks = models.Task.all()
    task = tasks.get()
    logging.info(task)
    # check if solved?
    solution = models.Solution.all().filter('task =', task)
    logging.info(task)
    if not solution or retry == 0:
      return task
    else:
      retry = retry - 1
      return self.findTask(retry)

  def get(self):
    # Latest unsolved.
    task = self.findTask(10)
    logging.info('final task')
    task = task.dict()
    logging.info(task)

    response = {'task': task}
    self.RenderJson(response)

class GuessHandler(abstract_handler.AbstractHandler):
  def post(self):
    request = simplejson.loads(self.request.body)
    task_key = request.get('task_key')
    word = request.get('word')
    task = models.Task.get(task_key)
    message = 'You are correct!' if task.word == word else 'Nope.'
    response = {'message': message}
    self.RenderJson(response)

class TasksHandler(abstract_handler.AbstractHandler):
  def get(self):
    tasks = models.Task.all()
    response = {'tasks': tasks}
    self.Render('tasks.html', response)


class PublishHandler(abstract_handler.AbstractJsonHandler):
  def post(self):
    request = self.json_request_
    task = models.Task(
        word=request['word'],
        description=request['description'],
        owner=users.get_current_user()
    )
    task.put();
    msg = 'You creates task: %s' % request['word'];
    self.RenderJson({'message': msg})

class GetWordsHandler(abstract_handler.AbstractHandler):
  def get(self):
    words = [word.dict() for word in models.Word.all()]
    logging.info(words)


    self.RenderJson(words)

class MainPage(abstract_handler.AbstractHandler):
  def get(self):
    words = [word.dict() for word in models.Word.all()]
    logging.info(words)

    template_values = {
        'words': words,
    }
    self.Render('index.html', template_values)


class AddWordHandler(abstract_handler.AbstractJsonHandler):
  def post(self):
    #request = self.json_request
    word = models.Word(word=self.json.get('word'))
    word.forbidden_words = self.json.get('forbidden_words').split('\n')
    word.put()
    msg = 'You submitted word: %s' % word.word;
    self.RenderJson({'message': msg})



