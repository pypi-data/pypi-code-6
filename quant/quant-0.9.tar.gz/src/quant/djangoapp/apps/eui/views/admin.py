from quant.djangoapp.apps.eui.views.base import QuantView
from dm.view.admin import AdminView
from dm.view.admin import AdminIndexView
from dm.view.admin import AdminModelView
from dm.view.admin import AdminListView
from dm.view.admin import AdminCreateView
from dm.view.admin import AdminReadView
from dm.view.admin import AdminUpdateView
from dm.view.admin import AdminDeleteView
from dm.view.admin import AdminListHasManyView
from dm.view.admin import AdminCreateHasManyView
from dm.view.admin import AdminReadHasManyView
from dm.view.admin import AdminUpdateHasManyView
from dm.view.admin import AdminDeleteHasManyView

class QuantAdminView(AdminView, QuantView):
    pass

class QuantAdminIndexView(AdminIndexView, QuantView):
    pass

class QuantAdminModelView(AdminModelView, QuantView):
    pass

class QuantAdminListView(AdminListView, QuantView):
    pass 

class QuantAdminCreateView(AdminCreateView, QuantView):
    pass

class QuantAdminReadView(AdminReadView, QuantView):
    pass

class QuantAdminUpdateView(AdminUpdateView, QuantView):
    pass

class QuantAdminDeleteView(AdminDeleteView, QuantView):
    pass

class QuantAdminListHasManyView(AdminListHasManyView, QuantView):
    pass

class QuantAdminCreateHasManyView(AdminCreateHasManyView, QuantView):
    pass

class QuantAdminReadHasManyView(AdminReadHasManyView, QuantView):
    pass

class QuantAdminUpdateHasManyView(AdminUpdateHasManyView, QuantView):
    pass

class QuantAdminDeleteHasManyView(AdminDeleteHasManyView, AdminView):
    pass


def index(request):
    view = QuantAdminIndexView(request=request)
    return view.getResponse()

def model(request):
    view = QuantAdminModelView(request=request)
    return view.getResponse()

def list(request, className):
    view = QuantAdminListView(
        request=request,
        domainClassName=className,
    )
    return view.getResponse()

def create(request, className):
    view = QuantAdminCreateView(
        request=request,
        domainClassName=className,
    )
    return view.getResponse()

def read(request, className, objectKey):
    view = QuantAdminReadView(
        request=request,
        domainClassName=className,
        domainObjectKey=objectKey,
    )
    return view.getResponse()

def update(request, className, objectKey):
    view = QuantAdminUpdateView(
        request=request,
        domainClassName=className,
        domainObjectKey=objectKey,
    )
    return view.getResponse()

def delete(request, className, objectKey):
    view = QuantAdminDeleteView(
        request=request,
        domainClassName=className,
        domainObjectKey=objectKey,
    )
    return view.getResponse()

def listHasMany(request, className, objectKey, hasMany):
    view = QuantAdminListHasManyView(
        request=request,
        domainClassName=className,
        domainObjectKey=objectKey,
        hasManyName=hasMany,
    )
    return view.getResponse()

def createHasMany(request, className, objectKey, hasMany):
    view = QuantAdminCreateHasManyView(
        request=request,
        domainClassName=className,
        domainObjectKey=objectKey,
        hasManyName=hasMany,
    )
    return view.getResponse()

def readHasMany(request, className, objectKey, hasMany, attrKey):
    view = QuantAdminReadHasManyView(
        request=request,
        domainClassName=className,
        domainObjectKey=objectKey,
        hasManyName=hasMany,
        hasManyKey=attrKey,
    )
    return view.getResponse()

def updateHasMany(request, className, objectKey, hasMany, attrKey):
    view = QuantAdminUpdateHasManyView(
        request=request,
        domainClassName=className,
        domainObjectKey=objectKey,
        hasManyName=hasMany,
        hasManyKey=attrKey,
    )
    return view.getResponse()

def deleteHasMany(request, className, objectKey, hasMany, attrKey):
    view = QuantAdminDeleteHasManyView(
        request=request,
        domainClassName=className,
        domainObjectKey=objectKey,
        hasManyName=hasMany,
        hasManyKey=attrKey,
    )
    return view.getResponse()


viewDict = {}
viewDict['ListView']   = QuantAdminListView
viewDict['CreateView'] = QuantAdminCreateView
viewDict['ReadView']   = QuantAdminReadView
viewDict['UpdateView'] = QuantAdminUpdateView
viewDict['DeleteView'] = QuantAdminDeleteView

def view(request, caseName, actionName, className, objectKey):
    if caseName == 'model':
        viewClassName = actionName.capitalize() + 'View'
        viewClass = viewDict[viewClassName]
        viewArgs = []
        if className:
            viewArgs.append(className)
            if objectKey:
                viewArgs.append(objectKey)
        view = viewClass(request=request)
        return view.getResponse(*viewArgs)
    raise Exception, "Case '%s' not supported." % caseName

