# -*- coding: utf-8 -*-
#auth table for developer and others
#search bar(using keywords)
#public,private projects
#group accesses for many groups


#this for the main categories..
db.define_table('category',
		Field('name',requires=(IS_SLUG(),IS_LOWER(),IS_NOT_IN_DB(db,'category.name'))))


##this is for sub_category
db.define_table('subcategory',
		Field('category','reference category',requires=(IS_IN_DB(db,'category.id','%(name)s'))),
		Field('title',requires=(IS_SLUG(),IS_LOWER(),IS_NOT_IN_DB(db,'subcategory.title'),IS_NOT_EMPTY()),label="Sub Category"),
		)


## this for app upload form
db.define_table('project',
		Field('title','string',unique=True),
		Field('category','reference category',requires=(IS_IN_DB(db,'category.id','%(name)s (%(id)s)'))),
		Field('subcategory','reference subcategory', requires=(IS_IN_DB(db,'subcategory.id','%(title)s' '(%(category)s)')),comment="Select the sub-category corresponding to the id above"),
		Field('logo','upload',requires=IS_NOT_EMPTY()),
		Field('image','upload',label='ScreenShot',requires=(IS_NOT_EMPTY(),IS_IMAGE()),autodelete=True),
		Field('files','upload',comment="upload as a single zip file",requires=IS_NOT_EMPTY()),
		Field('features',"text",requires=IS_NOT_EMPTY()),
		Field('body',"text",requires=IS_NOT_EMPTY(),label='Description'),
		Field('rating','double',writable=False,readable=False,default=0),
		Field('permissions',requires=IS_IN_SET(['public','private'],error_message="It should be either public or private")),
		#Field('no_of_reviews','integer',writable=False,readable=False,default=0),
		Field('commenters','integer',writable=False,readable=False,default=0),
		Field('downloads','integer',writable=False,readable=False,default=0),
		auth.signature)

##comments database
db.define_table('comments',
		Field('project','reference project',readable=False,writable=False),
		#Field('parent_comment','reference comment',readable=False,writable=False),
		Field('rating','integer'),
		Field('body','text',requires=IS_NOT_EMPTY(),label="Comment"),
		auth.signature)


###collooraters
db.define_table('allowed_users',
		Field('projectadmin_email',type='string'),
		Field('other_email',type='string'),
		Field('project_name',type='string')
		)

##this a function returns the name of the project's author
def author(id):
	user=db.auth_user(id)
	return ("%(first_name)s %(last_name)s" %user)

#db.comments.rating.requires=IS_IN_SET(range(1,6))

##rating database
#db.define_table('rating',
#		Field('post','reference post',readable=False,writable=False),
#		Field('score','integer',default=0),
#		auth.signature)

#db.define_table('rater',
#		Field('project','reference project',readable=False,writable=False),
 #       	Field('rating','integer'),
#		auth.signature)

#db.comments.rating.requires=IS_IN_SET(range(1,6))


##password change
db.auth_user.password.requires=IS_STRONG(min=8,special=1,upper=1)
