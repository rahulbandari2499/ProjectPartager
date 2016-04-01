# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('PROJECT',SPAN('partager')),XML('&nbsp;'),
		_class="navbar-brand",_href="#",
		_id="web2py-logo")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################
response.menu = [
		(T('Home'), False, URL('default', 'home'),[]),
		(T('Add Project'),False,URL('default','upload_project'),[]),
		]

if auth.user:
	response.menu.append((T('My Projects'),False,URL('default','my_projects',args=(auth.user.id)),[]))


DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

rows=db(db.subcategory.id>0).select()	
print rows
def _():
	# shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu+=[
		    (T('Categories'),False,'#' , [
			    (T('Programming'),False,URL('default','view_projects_by_datetime',args=('programming')),[]),
			    (T('Games'),False,URL('default','view_projects_by_datetime',args=('games')),[]), 
			    (T('Development'),False,URL('default','view_projects_by_datetime',args=('development')),[]),
			    (T('Communications'),False,URL('default','view_projects_by_datetime',args=('communications')),[]), 
			    (T('Security'),False,URL('default','view_projects_by_datetime',args=('security')),[]), 

			    ])]
    response.menu+=[
		    (T('Sub Categories'),False,'#' , [
				    (T('C'),False,URL('default','view_projects_by_sub_categories',args=('c')),[]),
				    (T('Python'),False,URL('default','view_projects_by_sub_categories',args=('python')),[]),
				    (T('Java'),False,URL('default','view_projects_by_sub_categories',args=('java')),[]),
				    (T('Email'),False,URL('default','view_projects_by_sub_categories',args=('email')),[]),
				    (T('Fax'),False,URL('default','view_projects_by_sub_categories',args=('fax')),[]),
				    (T('Mobile'),False,URL('default','view_projects_by_sub_categories',args=('mobile')),[]),
				    (T('Data Base'),False,URL('default','view_projects_by_sub_categories',args=('database')),[]),
				    (T('Terminal'),False,URL('default','view_projects_by_sub_categories',args=('terminal')),[]),
				    (T('simulation'),False,URL('default','view_projects_by_sub_categories',args=('simulation')),[]),
				    (T('Card Games'),False,URL('default','view_projects_by_sub_categories',args=('card-games')),[]),
				    (T('Real Time Strategy'),False,URL('default','view_projects_by_sub_categories',args=('real-time-strategies')),[]),
				    (T('Cryptography'),False,URL('default','view_projects_by_sub_categories',args=('cryptography')),[]),
				    (T('Anti Virus'),False,URL('default','view_projects_by_sub_categories',args=('anti-virus')),[]),
				    (T('Password Manager'),False,URL('default','view_projects_by_sub_categories',args=('password-manager')),[]),
				    ])]




_()



response.menu+=[
		(T('Admin Manager'),False,URL('default','manage_projects'),
							    [(T('Create Category'),False,URL('default','new_category')),
								    (T('Create Sub-Category'),False,URL('default','new_subcategory')),
								    (T('Manage Projects'),False,URL('default','manage_projects')),])
							    ,]

response.menu+=[
		(T('Top Contributors'),False,URL('default','rank'),),
		(T('Contact Us'),False,URL('default','contact'),)
		]
if "auth" in locals(): auth.wikimenu()
