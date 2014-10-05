class RedirectException(Exception):
    """
    Base class for redirecting user to a view when this exception
    is raise
    """
    view_name = None
    template_name = None
