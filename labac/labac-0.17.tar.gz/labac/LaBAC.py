import sys
class Label(object):
	
	def __init__(self,name):
		self.name = name
		# for object label we need all labels that are junior to a given label
		self.junior_labels = []
		self.senior_labels = []
	
	@property
        def is_senior_to(self):
                return self.junior_labels

	# return set of direct junior roles
	@is_senior_to.setter	
	def is_senior_to(self,label):
		self.junior_labels.append(label)
	

	@property
	def is_junior_to(self):
		return self.senior_labels

	@is_junior_to.setter
	def is_junior_to(self,label):
		self.senior_labels.append(label)

	# find all junior labels to this label
	def all_junior_labels(self):
		juniors =  self._all_junior_labels()
		if self in juniors:
			juniors.remove(self)
		return juniors
	
	def _all_junior_labels(self):
		res = []
		for l in iter(self.is_senior_to):
			res += l._all_junior_labels()
		# assuming a node is junior to itself
		return res + [self]

	def all_senior_labels(self):
		seniors = self._all_senior_labels()
		if self in seniors:
			seniors.remove(self)
		return seniors
		
	def _all_senior_labels(self):
		res = []
		for s in iter(self.is_junior_to):
			res += s._all_senior_labels()
		return res + [self]


'''
        Object label class. All the junior label of a label is maintained with 
	a label.
'''
class ObjectLabel(Label, object):
	
	def __init__(self, name):
		Label.__init__(self,name)
		#self.name = name
		# cleared_label  means the user label that have access this object label  as specified in the policy.
		self._cleared_u_label = []
		# inferred_label means inferred user labels that have access to this object label by user label hierarchy
		self._inferred_u_label = []

	@property
	def acl(self):
		return  self._cleared_u_label + self._inferred_u_label
		

	@property
	def cleared_user_label(self):
		return self._cleared_u_label
	
	'''
		param user_label : <Userlabel instance>
	'''
	@cleared_user_label.setter
	def cleared_user_label(self, user_label):		
		#self._cleared_u_label.append(user_label)
		self._cleared_u_label += [user_label] if user_label not in self._cleared_u_label else []
	
	'''  	we need to set inferred user label, inferred_user_label of a object, 
		contains all such labels ul st ul is senior to given user_label		
		Here I assume that user_label has already been set up for hierarchy.
	'''

	@property
	def inferred_user_label(self):
		return self._inferred_u_label

	'''
		param labels : [<UserLabel instance>, ... ]	
	'''

	@inferred_user_label.setter
	def inferred_user_label(self,labels):
		self._inferred_u_label += [l for l in labels if l not in self._inferred_u_label]
	
	def propagate(self):
		self.propagate_inferred_label(self.acl)
	
	'''
		if o1 dominates (>) o2, and o2 > o3 and so on, it method takes o1's acl 
		(both cleared & inferred label) and tie it with o2's inferred_u_label, 
		similarly, this happens for o2 and o3.

		This method can be improved for performance. Instread of iterating over 
		all juniors, propagate until deffered_user_label of a node change.

		param acl = [<UserLabel instance>, ...]
	'''
	def propagate_inferred_label(self, acl):
		immediate_juniors = self.is_senior_to
		for jnr_lbl in iter(immediate_juniors):
			jnr_lbl.inferred_user_label = acl
			acl = jnr_lbl.acl
			jnr_lbl.propagate_inferred_label(acl)

		

		
	
'''
	Class UserLabel correspond to a user label in the A/C model.
	for a user_label, our model is interested on all its senior_labels. 
	Note that user ObjectLabel class we were interested on junior_labels.
	This change in the requirement makes this code bit complicated.

'''

class UserLabel(Label,object):
	def __init__(self, name):
		Label.__init__(self,name)
		# senior labels are all the labels that are senior from this label




		


'''
	access label hierarchy. This is essentially a partial order.

'''

class LabelHierarchy:
	def __init__(self, user=False):
		# all the root of the partial order set is stored in root_list
		self.root_list = []
		# all labels of the Label Hierarchy
		self.labels=[]
		# if object_type = True , it means it is Object_label hieararchy. otherwise userlabel hierarchy
		self.object_type = True
		if user == True:
			self.object_type = False

	def _default_hierarchy_setup(self):

		self.add_x_dominates_y(x="private",y="public")
		self.add_x_dominates_y(x="protected",y="private")

	def add_x_dominates_y(self, x=None, y=None): # insert a hierarchy of two labels such that x dominates y. x_v, y_v are values of x & y
		if self.find_node(x) == None:
			self._add_2_nodes(x)
		if self.find_node(y) == None:
			self._add_2_nodes(y)

		xx = self.find_node(x)
		yy = self.find_node(y)
		#self._add_x_dominates_y(x=xx, y=yy)
		xx.is_senior_to = yy
		yy.is_junior_to = xx
		
	def _add_x_dominates_y(x=None, y=None):
		#if self.object_type == True:
		x.is_senior_to = y


	def _add_2_nodes(self,x_v):
		if self.object_type == True:
			tn = ObjectLabel(x_v)
		else:
			tn = UserLabel(x_v)
		self.labels.append(tn)
		
	
	def find_node(self,x_v):
		
		for n in self.labels:
			if n.name == x_v:
				return n
		return None
	
	def get_junior_labels(self):
		res = {}
		for label in iter(self.labels):
			#t =  (label, label.all_junior_labels())
			res[label] = label.all_junior_labels()
			#res.append(t)
		return res
	def get_senior_labels(self):
		res = {}
		for label in iter(self.labels):
			res[label] = label.all_senior_labels()
		return res

	def print_hierarchy(self,res):
		for k in res.keys():
			sys.stdout.write(format(k.name)+":")
			for v in res[k]:
				sys.stdout.write( v.name + " ")
			sys.stdout.write("\n")

	def get_hierarchy(self):
		#print "Junior Lists"
		self.print_hierarchy( self.get_junior_labels())
		#print "senior lists"
		self.print_hierarchy(self.get_senior_labels())

class Configuration(object):
	def __init__(self):
		self.policy_dict={}
		self._policy = None
		self._user_label_hierarchy = None
		self._object_label_hierarchy = None
		pass

	@staticmethod
	def _dummy_policy():
		return  [ ("o1","u1"), ("o2","u2") ]
	@staticmethod
	def _dummy_user_label():
		return [	("u1",["u2"]), \
				("u2",["u3"]) \
		       ]
	@staticmethod
	def _dummy_object_label():		
		return [	("o1",["o2"]), \
				("o2",["o3"]) \
		       ]
	
	@property
	def policy(self):
		return self.policy_dict
	

	#@policy.setter
	#def policy(self,policy):
	#	self._policy = policy

	@property
	def user_label_hierarchy(self):
		return self._user_label_hierarchy
	
	'''
		sets user labels & hierarchy
		param user_label_hiearchy: [ \
						(<string user_label1>, [ <string user_label2>, ...]) , \
						..., \
						(<string user_label>, [ <string user_label>, ...]) \
					   ]
		here user_label1 is dominating user_label2 and other in the list.
	'''	
	@user_label_hierarchy.setter
	def user_label_hierarchy(self, user_label_hierarchy):
		self._user_label_hierarchy = user_label_hierarchy


	@property
	def object_label_hierarchy(self):
		return self._object_label_hierarchy
	
	'''
		sets object labels & hierarchy
		param object_label_hiearchy: [ \
						(<string object_label1>, [ <string ob_label2>, ...]) , \
						..., \
						(<string ob_label>, [ <string ob_label>, ...]) \
					   ]
		here user_label1 is dominating user_label2 and other in the list.
	'''	
	@object_label_hierarchy.setter
	def object_label_hierarchy(self, ob_label_hierarchy):
		self._object_label_hierarchy = ob_label_hierarchy

	'''
		sets policy with action.
		param action: <string>
		param policy: [ \
				(<string object_label>,<string user_label>), ... \
			      ]
	'''
	def add_policy(self,action=None,policy=None):
		if action and policy:
			self.policy_dict[action] = policy
		pass


class Setup(object):
	'''
		param: conf is a object of class Configuration
	'''
	def __init__(self,conf):
		self.__object_hierarchy__ = None
		self.__user_hierarchy__ = None
		self.__policy__ = None

		self.object_hierarchy = conf.object_label_hierarchy
		self.user_hierarchy = conf.user_label_hierarchy
		self.policy_dict = conf.policy_dict
		#self.policy = policy
		pass
	@property	
	def object_hierarchy(self):
		return self.__object_hierarchy__

	@object_hierarchy.setter
	def object_hierarchy(self, hrchy):
		self.__object_hierarchy__ = LabelHierarchy(user=False) 
		try:
			for l_tuple in hrchy:
				(label,domination_list) = l_tuple
				for dl in domination_list:
					self.__object_hierarchy__.add_x_dominates_y(x=label,y=dl)
					pass

		except Exception as e:
			print e

	@property
	def user_hierarchy(self):
		return self.__user_hierarchy__

	@user_hierarchy.setter
	def user_hierarchy(self, hrchy):
		self.__user_hierarchy__ = LabelHierarchy(user=True)
		try:
			for l_tuple in hrchy:
				(label,domination_list) = l_tuple
				for dl in domination_list:
					self.__user_hierarchy__.add_x_dominates_y(x=label,y=dl)
					pass
		except Exception as e:
			print e

	def bind_objectLabel_with_userLabel(self):
		#print self.__policy__
		for plcy in iter(self.__policy__):
			(ol,ul) = plcy
			#now setup acl with each object.
			ol_instance = self.__object_hierarchy__.find_node(ol)
			ul_instance = self.__user_hierarchy__.find_node(ul)

			ol_instance.cleared_user_label = ul_instance
			ol_instance.inferred_user_label = ul_instance.all_senior_labels()
			# propagating acl of a object_label to all its junior object labels.
			ol_instance.propagate()
	
	'''
		get acl of all object_labels
		return a dictionary {'o_label':[u_label,...], ... } 
	'''
	@property
	def _acl(self):		
		all_o_labels = self.__object_hierarchy__.labels
		acl_dict= {}
		for o_label in iter(all_o_labels):
			acl_dict[o_label.name] =  [ l.name for l in o_label.acl ]
		return acl_dict
	
		
	@property
	def policy(self):
		return self.__policy__
	'''	
		param  plcy : [ ("o1","u1"), ... ]
	'''
	@policy.setter
	def policy(self,plcy):
		self.__policy__ = plcy
		self.bind_objectLabel_with_userLabel()

	'''
		get a dictionary like {action1:action1_acl, action2:action2_acl}
		where actionx_acl is also a dictionary.
	'''
	@property
	def acl(self):
		all_acl = {}
		for action in self.policy_dict.keys():
			plcy = self.policy_dict[action]
			self.policy = plcy
			all_acl[action] = self._acl
		return all_acl

class LaBAC(object):
	def __init__(self,conf=None):
		self.__conf__ = None
		if conf:
			self.__conf__ = conf
		self.__acl__ = None
	
	@property
	def conf(self):
		return self.__conf__ 

	@conf.setter
	def conf(self,conf):
		self.__conf__ = conf
	
	def setup(self):
		if self.__conf__:
			setup = Setup(self.__conf__)
			self.__acl__ = setup.acl
		else:
			#print error msg
			pass
	@property
	def acl(self):
		return self.__acl__

	def request(self,user=None, object=None, action=None):
		self.setup()
		#print self.__acl__
		#do some validation
		objects = []
		users = []
		object_acl = []
		if user and object and action:
			# from all acl get the acl for the action
			action_acl = self.__acl__[action]
			#print action_acl
			# if object is a single object, conver it to one element list.

			if isinstance(user, basestring):
				user = [user]
			if isinstance(object, basestring):
				object = [object]

			objects += object
			users += user
			
			for ob in objects:
				# get the acl for the requested object
				#print action_acl[ob]
				object_acl += action_acl[ob]
			

			# check the requested user_label is in object's acl
			#if user in object_acl:
			''' checking whether for the given objects, whether its combined acl contains
				any of the given user_labels.
				e.g. request(user=[ul1,ul2], object=[ol1,ol2], action=x), 
				object_acl contains all the user Labels  who can access ol1 or ol2.
				object_acl can be [ul1,ul3,ul4]. now, I am checking whether whether the
				set of object_acl and user has some label in common.

			'''
			if set(users) & set(object_acl): 
				return True
			else:
				return False



def complex_test():
	
	conf = Configuration()
	conf.object_label_hierarchy = [\
						("o1",["o2","o3","o4"]),\
						("o2",["o6","o5"]), \
						("o7",["o8","o9"])\
		
				      ]
	
	conf.user_label_hierarchy = [\
						("u1",["u2","u3"]),\
						("u2",["u4"])\
				    ]

	#conf.policy = [ ("o5","u1") ]
	#conf.add_policy("read",[ ("o1","u3"), ("o5","u3")] )
	conf.add_policy("read",[("o1","u2"),("o7","u1")])
	lbac = LaBAC(conf)
	#print lbac.acl
	print lbac.request(user=["u3","u1"],object=["o4","o7","o8","o9"],action="read")

if __name__ == "__main__":
	complex_test()
