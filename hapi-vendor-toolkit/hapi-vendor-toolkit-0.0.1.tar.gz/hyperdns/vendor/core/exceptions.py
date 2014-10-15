

class LoginFailureException(Exception):
    """When a driver is created with the expectation of being able to log
    in, and it can not log in, then it throws a LoginFailureException from
    the constructor.
    """
    pass

class MissingRequiredConfigurationException(Exception):
    """When a driver is created but the settings argument is missing
    a property, this exception is raised.
    """
    def __init__(self,parameter):
        Exception.__init__(self,"Can not find parameter '%s' in config" % parameter)
        self.parameter=parameter
    
class NotLoggedInException(Exception):
    """Indicates that an action was attempted without login, but when
    login is required.
    """
    pass
    
class TransactionInProgressException(Exception):
    """Indicates that a transaction is already in progress, when one
    should not be.
    """
    pass
    
class TransactionNotInProgressException(Exception):
    """Indicates that a transaction is not in progress when one should
    be
    """
    pass
    
class ZoneNotFoundException(Exception):
    """Indicates that a zone was expected to exist, but could not be
    located.
    """
    def __init__(self,fqdn):
        super(ZoneNotFoundException,self).__init__("Zone not found: %s" % fqdn)
        self.fqdn=fqdn

class ResourceNotFoundException(Exception):
    """Resource was not found when expected
    """
    def __init__(self,rname):
        Exception.__init__(self)
        self.rname=rname

class ZoneAlreadyExistsException(Exception):
    """Indicates an attempt to create a zone that already exists, but
    may have different SOA information.
    """
    def __init__(self,fqdn):
        Exception.__init__(self)
        self.fqdn=fqdn
        
class RecordAlreadyExistsException(Exception):
    """Indicates that a record already exists when it should not.
    For example, when creating a record, the record should not already
    exist.
    """
    def __init__(self,spec):
        Exception.__init__(self)
        self.spec=spec

class ImplementationMissingException(Exception):
    """This exception indicates that an implementation should be provided,
    but has not yet provided
    """
    pass

class OperationNotSupportedException(Exception):
    """Indicates that an operation is not supported in the current driver.
    For example, creation and deletion on some vendors is synonymous with
    registration and requires the payment of money or other activities which
    are properly done within that vendor's primary environment.  When such
    an operation is encountered, an OperationNotSupportedException is generated.
    """
    pass

class MalformedZoneFQDN(Exception):
    """Indicates that an attempt was made to use a zone fqdn without the
    trailing dot.  This exception ensures that there is consistency in the
    calling conventions, rather than adding the dot on the assumption that
    the caller meant to have it but did not.
    """
    def __init__(self,fqdn):
        Exception.__init__(self)
        self.fqdn=fqdn
    
class CommunicationsFailureException(Exception):
    """This is a base class which we use when there is an unexpected
    result from the endpoint.
    
    :param status: The HTTP status code
    :param content: The response body, if any
    :param msg: The exception message
    """
    def __init__(self,status,content,msg=None):
        if msg==None:
            msg=self.__class__.__name__
        super(CommunicationsFailureException,self).__init__(msg)
        self.message=msg
        self.status=status
        self.content=content
        
    def __str__(self):
        return "%s - HTTP result was %s:%s" % (self.message,self.status,self.content)
        
class CreateRecordException(CommunicationsFailureException):
    """Indicates that an attempt to create a record failed.
    """
    pass
    
class DeleteRecordException(CommunicationsFailureException):
    """Indicates that an attempt to delete a record failed.
    """
    pass

class ZoneCreationException(CommunicationsFailureException):
    """Indicates that an attempt to create a zone failed
    """
    pass
    
class ZoneDeletionException(CommunicationsFailureException):
    """Indicates the failure to delete a zone.
    """
    pass

class RESTResourceeDisappearanceException(Exception):
    """Indicates that the REST resource returned by the Dyn layer
    has disappeared between the time the Dyn api returned the result
    and the time we requested it.
    """
    pass
class ResourceDeletionFailure(CommunicationsFailureException):
    """Indicates that we failed to delete a resource.
    """
    pass
    
class CanNotUpdateSOARecordsException(Exception):
    """Soa records can not be manipulated using createRecord or
    deleteRecord.
    """
    pass
    
class UnsupportedRecordTypeException(Exception):
    """The record type is currently not suppored
    """
    def __init__(self,rdtype,msg=""):
        self.rdtype=rdtype
        super(UnsupportedRecordTypeException,self).__init__("Unsupported record type for this operation, type=%s (%s) : %s" % (rdtype.name,rdtype.value,msg))