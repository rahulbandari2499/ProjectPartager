#home/====#sort_by_mostdownloaded
#upload_project(auth_dev)
#view_projects_by_criteria
#view_project
#edit_project/delete_project
#my_project
#user_projects
#sort_by_rating
#sort_by_date
#(doubt)sort_by_mostcomments
#(doubt)sort_by_user's_no_of _uploads/

###<------strategy-------->
###home/page==default 
###upload_project/
###view_project/id
###edit_project/id
###my_projects/user_id/page
###@user_projects/user_id/page
###view_projects_by_downloads/category/page
###view_projects_by_rating/category/page
###view_projects_by_datetime/category/page
###view_projects_by_most_comments/category/page

#db.rater.rating.widget=plugin_widget

def search_func():
	form = db().select(db.project.ALL, orderby=db.project.title)
	form1=db().select(db.auth_user.ALL)
	form2=db().select(db.category.ALL)
	form3=db().select(db.subcategory.ALL)
	t= request.vars.s
	return locals()



###<-----CODE STARTS HERE-------->
PROJECTS_PER_PAGE=6

##create category
@auth.requires_membership('admins')
def new_category():
	form=SQLFORM(db.category).process()
	if form.accepted:
		session.flash='New Category Created Successfully'
		redirect(URL('home'))
	return locals()

##create new_subcategory
@auth.requires_membership('admins')
def new_subcategory():
	form=SQLFORM(db.subcategory).process()
	if form.accepted:
		session.flash='New Sub-Category Created Successfully'
		redirect(URL('home'))
	return locals()

##to get category from the arguments
def get_category():
	category_name=request.args(0)
	category=db.category(name=category_name)
	if not category:
		session.flash='This category is not Present'
		redirect(URL('home'))
	return category


#page=request.args(0,cast=int,default=0)
#	start=page*PROJECTS_PER_PAGE
#	stop=start+PROJECTS_PER_PAGE
#	projects=db((db.project.id>0) & (db.project.permissions=="public")).select(orderby=~db.project.rating,limitby=(start,stop))
#	give=db(db.project.id>0).select(orderby=~db.project.downloads)
#	if auth.user:
#		rem=db((db.project.id>0) & (db.project.permissions=="private") & (db.project.created_by==auth.user.id)).select(orderby=~db.project.rating,limitby=(start,stop))
#	
#	projects= projects | rem
#	projects.limitby(start,stop)
#	return locals()




#show all projects (default=most downloaded)
def home():
	page=request.args(0,cast=int,default=0)
	projects=db((db.project.id>0) & (db.project.permissions=="public")).select()
	give=db((db.project.id>0) & (db.project.permissions=="public")).select()
	if auth.user:
		rem=db((db.project.id>0) & (db.project.permissions=="private") & (db.project.created_by==auth.user.id)).select()
		rem1=db((db.project.id>0) & (db.project.permissions=="private") & (db.project.created_by==auth.user.id)).select()
		projects= projects | rem
		give=give | rem1
	projects=projects.sort(lambda row: row.rating,reverse=True)
#	projects=db().select(limitby=(start,stop))
	total=len(projects)
	num_pages=total/PROJECTS_PER_PAGE
	cur_page=page
	start=page*PROJECTS_PER_PAGE
	stop=start+PROJECTS_PER_PAGE
	if stop>total:
		stop=total
	projects=projects[start:stop]
	prev=page-1 if page>0 else None
	next=page+1 if (len(projects)>=6 and len(give)!=stop)  else None
	return locals()
#{{if len(projects)>=6 and len(give)!=stop:}}

###upload_project/
###view_project/id
###edit_project/id
###my_projects/user_id/page
@auth.requires_membership('developer')
def upload_project():
	form=SQLFORM(db.project).process(next='view_project/[id]')
	#form=SQLFORM(db.project).process()
	#if(db.subcategory.category==db.category.id):
	if (form.accepted):
		#redirect(URL('view_project',args=form.id))
		session.flash='Thanks For Your Contribution'
	#else:
	#	response.flash="please select category and sub-category correspondingly"
	return locals()

#reviews orderby
def view_project():
	id=request.args(0,cast=int)
	db.comments.project.default=id
	#db.comments.readable=False
	#db.comments.writable=False
	form=SQLFORM(db.comments).process()
	reviews=db(db.comments.project==id).select(limitby=(0,5))
	
	#print reviews
	#form1=SQLFORM(db.rater).process()
	project=db.project(id)
	row=db(db.allowed_users.project_name==project.title).select()
	#print row
	return locals()



@auth.requires_login()
def write_a_review():
	id=request.args(0,cast=int)
	project=db.project(id)
	db.comments.project.default=id
	form=SQLFORM(db.comments).process()

	if form.accepted:
		session.flash="Thanks For Your Review"
		redirect(URL('view_reviews',args=id))
	return locals()

@auth.requires_login()
def edit_review():
	id=request.args(0,cast=int)
	id1=request.args(1,cast=int)
	#project=db.project(id)
	form=SQLFORM(db.comments,id,showid=False,deletable=True).process()
	if form.accepted:
		session.flash="Review Is Edited Successfully"
		redirect(URL('view_reviews',args=id1))
	return locals()



##@this is to be done
def view_reviews():
	id=request.args(0,cast=int)
	page=request.args(1,cast=int,default=0)
	start=page*PROJECTS_PER_PAGE
	stop=start+PROJECTS_PER_PAGE
	project=db.project(id)
	reviews=db(db.comments.project==id).select(orderby=~db.comments.created_on,limitby=(start,stop))
	give=db(db.comments.project==id).select(orderby=~db.comments.created_on)
	return locals()

@auth.requires_membership('developer')
def edit_project():
	id=request.args(0,cast=int)
	project=db.project(id)
	form=SQLFORM(db.project,id,showid=False,deletable=True).process()
	if form.accepted:
		session.flash="Project Is Edited Successfully"
		redirect(URL('view_project',args=id))
	return locals()

@auth.requires_login()
def my_projects():   ##to list all recipes of logined user
	id=auth.user_id
	owner=author(id)
	page=request.args(1,cast=int,default=0)
	start=page*PROJECTS_PER_PAGE
	stop=start+PROJECTS_PER_PAGE
	projects=db(db.project.created_by==id).select(orderby=~db.project.created_on,limitby=(start,stop))
	give=db(db.project.created_by==id).select(orderby=~db.project.created_on)
	return locals()
###view_projects_by_author/user_id/page

def view_projects_by_author():
	user_id=request.args(0,cast=int)
	page=request.args(1,cast=int,default=0)
	projects=db((db.project.created_by==user_id) & (db.project.permissions=="public")).select()
	give=db((db.project.created_by==user_id) & (db.project.permissions=="public")).select()

	#WATCH THIS
	if auth.user:
		rem=db((db.project.id>0) & (db.project.permissions=="private") & (db.project.created_by==auth.user.id)).select()
		rem1=db((db.project.id>0) & (db.project.permissions=="private") & (db.project.created_by==auth.user.id)).select()
		give=give | rem1
		projects= projects | rem
	projects=projects.sort(lambda row: row.rating,reverse=True)
	total=len(projects)
	num_pages=total/PROJECTS_PER_PAGE
	cur_page=page
	start=page*PROJECTS_PER_PAGE
	stop=start+PROJECTS_PER_PAGE
	if stop>total:
		stop=total
	projects=projects[start:stop]
	prev=page-1 if page>0 else None
	next=page+1 if (len(projects)>=6 and len(give)!=stop)  else None
	return locals()


###view_projects_by_downloads/category/page
###view_projects_by_rating/category/page
###view_projects_by_datetime/category/page
###view_projects_by_most_comments/category/page

def view_projects_by_downloads():
	category=get_category()
	page=request.args(1,cast=int,default=0)
	projects=db((db.project.category==category.id)  & (db.project.permissions=="public")).select()
	give=db((db.project.category==category.id)  & (db.project.permissions=="public")).select()
	if auth.user:
		rem=db((db.project.category==category.id) & (db.project.permissions=="private") & (db.project.created_by==auth.user.id)).select()
		rem1=db((db.project.category==category.id) & (db.project.permissions=="private") & (db.project.created_by==auth.user.id)).select()
		projects= projects | rem
		give= give | rem1
	projects=projects.sort(lambda row: row.downloads,reverse=True)
	total=len(projects)
	num_pages=total/PROJECTS_PER_PAGE
	cur_page=page
	start=page*PROJECTS_PER_PAGE
	stop=start+PROJECTS_PER_PAGE
	if stop>total:
		stop=total
	projects=projects[start:stop]
	prev=page-1 if page>0 else None
	next=page+1 if (len(projects)>=6 and len(give)!=stop)  else None
	return locals()



def view_projects_by_rating():
	category=get_category()
	page=request.args(1,cast=int,default=0)
	projects=db((db.project.category==category.id)  & (db.project.permissions=="public")).select()
	give=db((db.project.category==category.id)  & (db.project.permissions=="public")).select()
	if auth.user:
		rem=db((db.project.category==category.id) & (db.project.permissions=="private") & (db.project.created_by==auth.user.id)).select()
		rem1=db((db.project.category==category.id) & (db.project.permissions=="private") & (db.project.created_by==auth.user.id)).select()
		projects= projects | rem
		give= give | rem1
	projects=projects.sort(lambda row: row.rating,reverse=True)
	total=len(projects)
	num_pages=total/PROJECTS_PER_PAGE
	cur_page=page
	start=page*PROJECTS_PER_PAGE
	stop=start+PROJECTS_PER_PAGE
	if stop>total:
		stop=total
	projects=projects[start:stop]
	prev=page-1 if page>0 else None
	next=page+1 if (len(projects)>=6 and len(give)!=stop)  else None
	return locals()


def view_projects_by_datetime():
	category=get_category()
	page=request.args(1,cast=int,default=0)
	projects=db((db.project.category==category.id)  & (db.project.permissions=="public")).select()
	give=db((db.project.category==category.id)  & (db.project.permissions=="public")).select()
	if auth.user:
		rem=db((db.project.category==category.id) & (db.project.permissions=="private") & (db.project.created_by==auth.user.id)).select()
		rem1=db((db.project.category==category.id) & (db.project.permissions=="private") & (db.project.created_by==auth.user.id)).select()
		projects= projects | rem
		give= give | rem1
	projects=projects.sort(lambda row: row.created_on,reverse=True)
	total=len(projects)
	num_pages=total/PROJECTS_PER_PAGE
	cur_page=page
	start=page*PROJECTS_PER_PAGE
	stop=start+PROJECTS_PER_PAGE
	if stop>total:
		stop=total
	projects=projects[start:stop]
	prev=page-1 if page>0 else None
	next=page+1 if (len(projects)>=6 and len(give)!=stop)  else None
	return locals()


def view_projects_by_most_comments():
	category=get_category()
	page=request.args(1,cast=int,default=0)
	projects=db((db.project.category==category.id)  & (db.project.permissions=="public")).select()
	give=db((db.project.category==category.id)  & (db.project.permissions=="public")).select()
	if auth.user:
		rem=db((db.project.category==category.id) & (db.project.permissions=="private") & (db.project.created_by==auth.user.id)).select()
		rem1=db((db.project.category==category.id) & (db.project.permissions=="private") & (db.project.created_by==auth.user.id)).select()
		projects= projects | rem
		give= give | rem1
	projects=projects.sort(lambda row: row.commenters,reverse=True)
	total=len(projects)
	num_pages=total/PROJECTS_PER_PAGE
	cur_page=page
	start=page*PROJECTS_PER_PAGE
	stop=start+PROJECTS_PER_PAGE
	if stop>total:
		stop=total
	projects=projects[start:stop]
	prev=page-1 if page>0 else None
	next=page+1 if (len(projects)>=6 and len(give)!=stop)  else None
	return locals()

#view_project_by_sub_categories/sub_category_name/page
def view_projects_by_sub_categories():
	sub_id=request.args(0)
	page=request.args(1,cast=int,default=0)
	scid = db.subcategory(db.subcategory.title==sub_id).id
	qr = (db.project.subcategory == scid) & (db.project.permissions=="public")
	projects = db(qr).select()
	give= db(qr).select()
	if auth.user:
		rem=db((db.project.subcategory==scid) & (db.project.permissions=="private") & (db.project.created_by==auth.user.id)).select()
		rem1=db((db.project.subcategory==scid) & (db.project.permissions=="private") & (db.project.created_by==auth.user.id)).select()
		projects= projects | rem 
		give=give | rem1
	projects=projects.sort(lambda row: row.rating,reverse=True)
	total=len(projects)
	num_pages=total/PROJECTS_PER_PAGE
	cur_page=page
	start=page*PROJECTS_PER_PAGE
	stop=start+PROJECTS_PER_PAGE
	if stop>total:
		stop=total
	projects=projects[start:stop]
	prev=page-1 if page>0 else None
	next=page+1 if (len(projects)>=6 and len(give)!=stop)  else None
	return locals()


@auth.requires_membership('admins')
def manage_projects():
	grid=SQLFORM.smartgrid(db.project)
	return locals()

#try doing Ajax
def make_public():
	id=request.args(0,cast=int)
	project=db.project(id)
	if project.permissions=="private":
		project.update_record(permissions="public")
		session.flash="Project Added As Public"
	elif project.permissions=="public":
		project.update_record(permissions="private")
		session.flash="Project Added As Private"
	redirect(URL('home'))
	return locals()
def user():
	if(auth.user!=None):
		if(auth.user.typist=='developer'):
			auth.add_membership(3,auth.user.id)
	return dict(form=auth())
##do ajax
def download1():
	project = db.project(request.args(0,cast=int)) or redirect(URL('index'))
	project.downloads=project.downloads + 1
	project.update_record()
	redirect(URL('download',args=project.files))
	return locals()


##rank
def rank():
	projects=db(db.project.id>0).select()
	users=db(db.auth_user.id>0).select()
	for user in users:
		user.score=0
		user.uploads=0
	for project in projects:
		for user in users:
			if project.created_by==user.id:
				user.uploads+=1
				user.score+=project.downloads+project.rating
				user.update_record()
	sort=db(db.auth_user.id>0).select(orderby=~db.auth_user.score | ~db.auth_user.uploads)
	return locals()

def confirm_delcollo():
	user = db.allowed_users(request.args(0,cast=int)) or redirect(URL('index'))
	project=db(db.allowed_users.project_name==user.project_name).select()
	db(request.args(0,cast=int)==db.allowed_users.id).delete()
	redirect(URL('home'))


def view_collo():
	project = db.project(request.args(0,cast=int))
	row=db(db.allowed_users.project_name==project.title).select()
	return locals()
	
def delcollo():
	project = db.project(request.args(0,cast=int))
	row=db(db.allowed_users.project_name==project.title).select()
	if auth.user:
		if auth.user.id==project.created_by:
			return dict(row=row,project=project)
	else:
		session.flash="You Don't have permissions"
		redirect(URL('view_project',args=project.id))


##add collo

@auth.requires_login()
def addcollo():
	project=db.project(request.args(0,cast=int)) or redirect(URL('index'))
	#db.allowed_users.project_name.default=project.title
	form1=SQLFORM.factory(
			#Field('add_collaborator',type='string',requires=(IS_IN_DB(db,'auth_user.id','%(first_name)s'))),
			Field('add_collaborator',type='string',requires=(IS_IN_DB(db,'auth_user.first_name'))			))
	row1=db(db.allowed_users.project_name==project.title).select()
	if form1.process().accepted:
		db.allowed_users.insert(other_email=request.vars.add_collaborator)
		row=db(db.allowed_users.other_email==request.vars.add_collaborator).select().last()
		row.project_name=project.title
		row.projectadmin_email=auth.user.first_name
		row.update_record()
		redirect(URL('view_project',args=project.id))
	if auth.user.id==project.created_by:
		return dict(form1=form1,project=project,row1=row1)
	else:
		session.flash="You Don't Have Permissions"
		redirect(URL('view_project',args=project.id))

def vote_callback():
	vars=request.post_vars
	print vars
	if vars and auth.user:
		id=vars.id
		if vars.direction=="up": 
			direction1=+1 	
		project=db.project(id)
		#print project
		if project:
			project.update_record(downloads=int(project.downloads)+direction1)
		else:
			pass
	return str(project.downloads)




@cache.action()
def download():
	return response.download(request, db)

def index():
	return locals()

def contact():
	return locals()

def call():
	return service()
