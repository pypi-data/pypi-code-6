from werkzeug.exceptions import HTTPException

class BaseHttpException(HTTPException):
  pass

class HttpNotFound(BaseHttpException):
  code = 404
