import cgi
import webapp2

from handlers import home

app = webapp2.WSGIApplication([
  ('/', home.MainPage),
  ('/add_word', home.AddWordHandler),
  ('/get_words', home.GetWordsHandler),
  ('/publish', home.PublishHandler),
  ('/tasks', home.TasksHandler),
  ('/get_task', home.GetTaskHandler),
  ('/guess', home.GuessHandler),
], debug=True)
