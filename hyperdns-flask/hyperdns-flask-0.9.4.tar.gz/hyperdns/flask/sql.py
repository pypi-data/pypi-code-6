"""Expose Flask-SQLAlchemy models as HAL objects.
"""
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy import event
import sqlalchemy.orm

DATABASE=None


class db_commit(object):
    """
    for some reason we're getting automatic ROLLBACK - on top of that, pycharm
    is not allowing me to set breakpoints.  I don't know if we really need this
    wrapper or not - Flask handles this usually, but for some reason i no longer
    recall i added this wrapper to fix a bug.  Ideally it can be removed.
    """
    def __init__(self):
        pass
    
    def __call__(self,f):
        def _db_commit(*args, **kwargs):
            try:
                result=f(*args, **kwargs)
                DATABASE.session.commit()
            except:
                DATABASE.session.rollback()
                raise
            return result
        d=_db_commit
        d.__name__=f.__name__
        return d
    
class haldb(object):
    """This class should help isolate the haldb support from the normal
    SQLAlchemy support, clearly delineating what properties, objects, and
    collections are exposed via the API, and which are solely within the
    province of the ORM model.
    """        
    

    # record the implementation type and index key for child maps
    @staticmethod
    def Map(class_name,index_key,**kwargs):
        """Record the class_name and the index_key of the collection, otherwise
        pass all information to the regular ORM layer.
    
        :param class_name: the name of the class targetted by this 1:N relationsihp
        :param index_key: the name of the property by which the map is indexed
        """
        # grab the haldoc parameter from kwargs, save it, and then remove it so it
        # does not confuse the SQLAlchemy model
        haldoc=kwargs.get('haldoc')
        if 'haldoc' in kwargs:
            del kwargs['haldoc']
    
        # use an 'attribute_mapped_collection' unless overridden, attribute_mapped_collection
        # is the equivalent of a 'dict' like map
        if 'collection_class' in kwargs:
            result=DATABASE.relationship(class_name,**kwargs)
        else:
            result=DATABASE.relationship(class_name,
                collection_class=attribute_mapped_collection(index_key),**kwargs)

        # record the implementation type and the index and the docs
        result.hal_doc=haldoc
        result.impl_type=class_name
        result.impl_index=index_key

        return result

    @staticmethod
    def Resource(class_name,**kwargs):
        """This creates a 1:1 relationship between the parent class and the target
        class.  The helper records the implementation type of the target class
        for use in generating the API, and records the name of the backref for
        link generation.

        :param class_name: the name of the class targetted by this 1:1 relationship
        """
    
        # grab the haldoc parameter from kwargs, save it, and then remove it so it
        # does not confuse the SQLAlchemy model
        haldoc=kwargs.get('haldoc')
        if 'haldoc' in kwargs:
            del kwargs['haldoc']
    
        # uselist implies 1:1 and not 1:N relationship
        result=DATABASE.relationship(class_name,uselist=False,**kwargs)
    
        # store the local context on the result object
        result.hal_doc=haldoc
        result.impl_type=class_name
        result.impl_index=None
    
        return result

    @staticmethod
    def Property(coltype,*args,**kwargs):
        """This creates a Column on the database, and allows an additional property
        'haldoc' which is used for generating the API documentation.
    
        :param coltype: the type of this column
        """
    
        # grab the haldoc parameter from kwargs, save it, and then remove it so it
        # does not confuse the SQLAlchemy model
        haldoc=kwargs.get('haldoc')
        if 'haldoc' in kwargs:
            del kwargs['haldoc']
    
        # now generate the actual column, using the cleaned up kwargs
        result=DATABASE.Column(coltype,*args,**kwargs)
    
        # store the local context on the result object
        result.hal_doc=haldoc
        result.hal_property_type=coltype
    
        return result

def _setprops(self,props):
    """Set all the properties on a newly created object.  See test cases
    for example usage
    """
    for (key,value) in props.items():
        setattr(self,key,value)
    return self

def init_sqlalchemy_support(app):
    """
    Attaches support classes to SQLAlchemy that expose additional information
    to the api instrumentor so that we can auto navigate the model.
    
    This lets the SQLAlchemy model do
        app.db.
    """
    global DATABASE
    DATABASE=app.db
    
    DATABASE.hal=haldb
    # expose a simple way to set properties on a dict
    setattr(DATABASE.Model,'_setprops',_setprops)

    # when a request is completed, it is automatically committed
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    # when objects are created, they are automatically added to the database
    # session
    @event.listens_for(sqlalchemy.orm.mapper, 'init')
    def auto_add(target, args, kwargs):
        DATABASE.session.add(target)

    # i forget what this is about - something in flask w/ testing or maybe -it
    # was a year ago and I just don't recall why i put this in, probably didn't
    # understand at the time.
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        DATABASE.session.remove()


