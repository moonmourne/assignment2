import webapp2
from google.appengine.ext import ndb    

# import users api
from google.appengine.api import users
import os

# import module for templates
import jinja2
# for logging message to server log
import logging
import json
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# use the email as the key name
# Add the appropriate property based on the form in Assigment 1
class Form(ndb.Model):
    name = ndb.StringProperty()
    age = ndb.IntegerProperty()
    gender = ndb.IntegerProperty()
    years = ndb.IntegerProperty()
    talent_tree = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

# Learn how handle input and create error response
class SubmitForm(webapp2.RequestHandler):
    def post(self):
        # get the data
        age = int(self.request.get('age'))
        name = self.request.get('name')
        gender = int(self.request.get('gender'))
        years = int(self.request.get('years'))
        talent_tree = self.request.get('talent_tree')
        # get the current user
        user = users.get_current_user()
        
        if not user:
            # Error: user's login time out or logged out
            self.error(401)
            # you can send a error message as well
            self.response.out.write("Error: no login")
            return
        
        # get the email from user object
        if users.is_current_user_admin():
            email = self.request.get('email')
        else:
            email = user.email()
        
        # USE EMAIL AS KEY NAME
        form = Form(key=ndb.Key('Form', email), name=name,age=age,years=years,gender=gender,talent_tree=talent_tree)
        # update db
        form.put()
    
        self.response.write('Your form is saved')
        
        # HTTP STATUS CODE 200 is always sent automatically
   
# In the last demo, the previous form is only a static html, it is not useful in real applications
# Now the form is rendered as a template
class EditForm(webapp2.RequestHandler):
    def get(self):        
        
        user = users.get_current_user()
        if user:
            # redirect "/" after user has logged out
            logout_url = users.create_logout_url('/')
        else:
            # direct to login and redirect back to this page after login
            self.redirect(users.create_login_url(self.request.uri))
            # return will stop loading code below
            return
        
        # these are logging functions
        # useful when debugging your app
        logging.info(user.email())
        logging.info(user.user_id())
        
        ###################
        # Assignment Hint:
        # look up the datastore for the "Form" data of the current users
        # add the form data to the template_values and displayed in the html file 
        ###################
        
        # check if the current user is admin
        # When app is uploaded to GAE server, admins are Google Accounts with access to the application code
        isAdmin = users.is_current_user_admin()
        ancestor_key=ndb.Key(Form,user.email()) 
        qry=Form.query(ancestor=ancestor_key)
        formdata=qry.fetch()
        
        if len(formdata)>0:
            formdata = formdata[0]
        else:
            #formdata = Form(key=ndb.Key('Form', user.email()))
            formdata = False
        # these values are for the template
        template_values = {
            # pass an object
            'user': user,
            # pass an entity
            # 'form': form,
            # pass a string
            'formdata':formdata,
            'logout_url': logout_url,
            'isAdmin' : isAdmin
        }
        
        # finally render the template, the template is the form2.html in the templates folder
        template = JINJA_ENVIRONMENT.get_template('templates/form.html')
        self.response.write(template.render(template_values))
class Search(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.response.out.write(json.dumps({'status':'False','msg':"Error: no login"}))
            return
        if not users.is_current_user_admin():
            self.response.out.write(json.dumps({'status':'False','msg':"Error: you are not admin"}))
            return
        email = self.request.get('email')
        if not email:
            self.response.out.write(json.dumps({'status':'False','msg':"Error: please input email"}))
            return
        ancestor_key=ndb.Key(Form,email) 
        qry=Form.query(ancestor=ancestor_key)
        formdata=qry.fetch()
        if len(formdata)==0:
            self.response.out.write(json.dumps({'status':'False','msg':"Error: nothing found"}))
            return
        formdata=formdata[0]
        data={'status':'succ','data':{
        'name':formdata.name,
        'age':formdata.age,
        'email':formdata.key.id(),
        'gender':formdata.gender,
        'years':formdata.years,
        'talent_tree':formdata.talent_tree}
        }
        self.response.out.write(json.dumps(data))
# this is the "/" page, do not modify. This page is not part of the assignment
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello!<br>')
        self.response.write('Start your <a href="/edit/form">form</a>')        
        
app = webapp2.WSGIApplication([    
    ('/', MainHandler),  
    ('/edit/form', EditForm),  # show the form in a template
    ('/submit/form', SubmitForm), # submit and save form data
    ('/search', Search),
    ('*.', MainHandler)
    ], debug=True)
