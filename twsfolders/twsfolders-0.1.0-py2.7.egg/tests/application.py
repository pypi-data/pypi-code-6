
from zope.interface import implementer, Interface

from twsfolders.folder import Folder


class ApplicationItemTypeError(Exception):
    pass


class ApplicationServiceItemTypeError(Exception):
    pass


class IApplication(Interface):
    pass


class Application(Folder):
    """ any item of Application must be of type Service"""

    def allow_add_item(self, item, overwrite=False, raise_err=False):
        allow = super(Application, self).allow_add_item(item, overwrite=overwrite, raise_err=raise_err)
        if allow:
            if not isinstance(item, ApplicationService):
                if raise_err:
                    raise ApplicationItemTypeError('adding a non service to application is prohibited')
                else:
                    allow = False

        return allow


class IApplicationService(Interface):
    pass


@implementer(IApplicationService)
class ApplicationService(Folder):

    def allow_add_item(self, item, overwrite=False, raise_err=False):
        allow = super(ApplicationService, self).allow_add_item(item, overwrite=overwrite, raise_err=raise_err)
        if allow:
            if isinstance(item, ApplicationService) and isinstance(self.parent, ApplicationService):
                if raise_err:
                    raise ApplicationServiceItemTypeError('adding a service to a service that is under a service')
                else:
                    allow = False

        return allow

    def start(self):
        return True

    def stop(self):
        return True


def application_folders_validator(item):
    """ To think that all rootfolders items are of type Application"""
    if isinstance(item, Application):
        return True

    return False
