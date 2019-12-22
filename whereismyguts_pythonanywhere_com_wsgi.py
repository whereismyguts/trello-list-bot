# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below has been auto-generated for your Flask project

import sys

# add your project directory to the sys.path
project_home = u'/home/whereismyguts/mysite'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
# from trello_flask_app import app as application 

import tornado.web
import tornado.wsgi


'''
this file must be copied to '/var/www/whereismyguts_pythonanywhere_com_wsgi.py'
there need to be an value called 'application' in this file
'''

# from trello_parser import get_status  
# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#         text = get_status(web=True)
#         self.write(text)


# from linkman.run import HANDLERS  
# application = tornado.wsgi.WSGIApplication(HANDLERS, debug=True)


# import flask app but need to call it "application" for WSGI to work                                    │+                        self.finish()
from trello_flask_app import app as application 
