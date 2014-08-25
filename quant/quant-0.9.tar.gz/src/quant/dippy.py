# DIPPY: Dependency injection for Python
#----------------------------------------------------------------------
# Copyright 2007 David Heath (david@davidheath.org).
# All rights reserved.
#
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of the
# License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# Full license available from: http://www.gnu.org/copyleft/lesser.html
#----------------------------------------------------------------------
#
# The DIPPY container supports both constructor and 'setter' (actually
# direct attribute access) injection.
#
# Furthermore I make a distinction between the following service types:
#
#   1) Factory services - which exist to create multiple instances of
#      objects. A factory service will fulfil dependencies of created
#      objects, but allow other constructor arguments to be specified
#      at creation time. The container quants an appropriately
#      configured factory, and container clients actually instantiate
#      the object themselves.
# 
#   2) Singleton services - which are managed by the container. Only a
#      single instance will ever be created. Additional constructor
#      arguments may be passed at registration time.
# 
#   3) Instance services - useful for things such as configuration
#      settings, flags, strings etc. The container is quantd with
#      the object instance, rather than the class.
# 
#   Example:
#
#   class Article:
#     constructor_dependencies = dict(db='database')
#   
#     def __init__(db, id=None):
#       self.db = db
# 
#       if id:
#         self.load(id)
#   
#   container.register_instance('db_password', 'very_s3cret')
#   container.register_instance('db_host', '127.0.0.1')
#   container.register_instance('db_user', 'mydbuser')
#   container.register_singleton('database', MysqlDatabase)
#   container.register_service_factory('article', Article)
#   a = container.article(234) # instantiate article id 234
#
# Acknowledgements:
#   Marcus Baker (http://lastcraft.com), for telling me about DI in the first place
#   Martin Fowler, for his fantastic article on DI:
#     http://www.martinfowler.com/articles/injection.html
#   Pico Container, for detailing the Patterns and Anti-patterns relating to DI
#   Jim Weirich, for demonstrating an alternate approach to DI in dynamic languages:
#     http://onestepback.org/index.cgi/Tech/Ruby/DependencyInjectionInRuby.rdoc
#   Christian Neukirchen, Dissident, for a thought provoking approach to DI in ruby:
#     http://chneukirchen.org/blog/archive/2005/08/design-and-evolution-of-a-dependency-injection-framework.html
#  
class Error(Exception):
  def __init__(self, message):
    self.message = message

  def __str__(self):
      return "%s: %s" % (self.__class__, self.message)
  
class MissingServiceError(Error):
  pass

class DuplicateServiceError(Error):
  pass

class ClassServiceInitialiser(object):
    def __init__(self, container, the_class):
      self.container = container
      self.the_class = the_class

    # given a map of dependencies (name => service_name) produce a map
    # of concrete service instances (name => service)
    def satisfy(self, dependencies):
      satisfied_dependencies = {}
      for name, servicename in dependencies.iteritems():
        satisfied_dependencies[name] = getattr(self.container, servicename)

      return satisfied_dependencies

    def merge_dicts_from_class_heirarchy(self, the_class, dict_name):
      if the_class == object:
        return {}
      else:
        try:
          the_dict = getattr(the_class, dict_name)
        except AttributeError:
          the_dict = {}
        
        for base in the_class.__bases__:
          the_dict.update(self.merge_dicts_from_class_heirarchy(base, dict_name))
        return the_dict
      
    def initialise(self):
      constructor_dependencies = self.satisfy(
        self.merge_dicts_from_class_heirarchy(self.the_class, 'constructor_dependencies')
        )

      instance_dependencies = self.satisfy(
        self.merge_dicts_from_class_heirarchy(self.the_class, 'instance_dependencies')
        )

      # define the factory method for this service
      def factory(*args, **kwds):
          kwds.update(constructor_dependencies)
          instance = self.the_class(*args, **kwds)
          for name, value in instance_dependencies.iteritems():
            setattr(instance, name, value)
          return instance
        
      return factory

class SingletonInitialiser(object):
  def __init__(self, service_initialiser, *args, **kwds):
    self.service_initialiser = service_initialiser
    self.args = args
    self.kwds = kwds

  def initialise(self):
    return self.service_initialiser.initialise()(*self.args, **self.kwds)

class InstanceInitialiser(object):
  def __init__(self, instance):
    self.instance = instance

  def initialise(self):
    return self.instance

class Container(object):
    
    # Create a dependency injection container.  Specify a parent
    # container to use as a fallback for service lookup.
    def __init__(self, parent = None):
      self.services = {}
      self.cache = {}
      self.parent = parent

    # Register a service using an arbitrary service initialiser class
    def register(self, name, service_initialiser):
        if self.services.has_key(name):
            raise DuplicateServiceError("Duplicate Service Name '%s'" % name)
            
        self.services[name] = service_initialiser
        
    # Register a service which has no special creation or management
    # behaviour, just the single specified instance
    def register_instance(self, name, service_instance):
      self.register(name, InstanceInitialiser(service_instance))

    # Register a service created using a class. Any further positional
    # and keyword arguments will be passed to the class constructor
    # when creating the single instance (in addition to any
    # dependencies required by the class). 
    def register_singleton(self, name, the_class, *args, **kwds):
        self.register(name, SingletonInitialiser(ClassServiceInitialiser(self, the_class), *args, **kwds))
      
    # Register a factory for creating objects of a given class with
    # injected dependencies. This is used for objects which are not
    # singletons, ie. which expect to exist in multiple
    # instances. They may have constructor arguments which vary their
    # creation, in addition to any automatically injected
    # dependencies.
    def register_service_factory(self, name, the_class):
        self.register(name, ClassServiceInitialiser(self, the_class))

    # Look up a service by name
    def get_service(self, name):
        if not self.cache.has_key(name):
            self.cache[name] = self.find_initialiser(name).initialise()
            
        return self.cache[name]

    # Another way to look up a service by name. The requested
    # attribute name is used as the service name.
    def __getattr__(self, service_name):
      return self.get_service(service_name)

    # Return the initialiser that creates the named service.  Throw an
    # exception if no service creation initialiser of the given name can be
    # found in the container or its parents.
    def find_initialiser(self, name):
        if not self.services.has_key(name):
            if self.parent:
                return self.parent.find_initialiser(name)
            else:
                raise MissingServiceError("Unknown Service '%s'" % name)

        return self.services[name]
