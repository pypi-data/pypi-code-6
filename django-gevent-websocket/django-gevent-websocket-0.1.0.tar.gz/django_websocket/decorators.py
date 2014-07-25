
from functools import wraps
from select import select

def websocket(func):
    """
    Injects the websocket object into the argument list.
    
    This is just a shorthand for having:
    
        websocket = request.META['wsgi.websocket']
    
    as the first line of the view function (and removing websocket)
    from the arguments list.
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        return func(request, request.META['wsgi.websocket'], *args, **kwargs)
    return wrapper


def websocket_loop(func):
    """
    While the websocket is not closed, listen for incoming data
    on the websocket, and call func each time an event occurs.
    
    Note: this is only useful for situations where the handler only
    needs to listen for events coming from the WebSocket, but does show
    how you can encapsulate functionality into a decorator.
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        websocket = request.META['wsgi.websocket']
        fd = websocket.handler.socket.fileno()
        while not websocket.closed:
            select([fd], [], [])
            func(request, websocket, *args, **kwargs)
    
    return wrapper