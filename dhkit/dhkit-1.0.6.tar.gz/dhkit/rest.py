# coding:utf8

"""
Created on 2014-10-14

@author: tufei
@description: 基于Tornado框架实现的RESTFul形式的API
         
Copyright (c) 2014 infohold inc. All rights reserved.
"""
import json
import tornado.web
import tornado.gen
import httplib
import dhkit.error


class RestError(dhkit.error.Error):

    httpcode = 500

    def __init__(self, msg=None):
        code = self.cls_code - self.httpcode
        super(RestError, self).__init__(msg, code)

    def to_dict(self):
        return dict(return_code=self.code, return_message=self.message)


class BadRequestError(RestError):

    httplib = httplib.BAD_REQUEST


class NotFoundError(RestError):

    httpcode = httplib.NOT_FOUND


class UnAuthorizedError(RestError):

    httpcode = httplib.UNAUTHORIZED


class ForbiddenError(RestError):

    httpcode = httplib.FORBIDDEN


class MethodNotAllowedError(RestError):

    httpcode = httplib.METHOD_NOT_ALLOWED


class RestRequestHandler(tornado.web.RequestHandler):
    """Rest handler

    default use tornado.gen.coroutine
    """

    ALLOW_CORS = True

    ACCESS_CONTROL_ALLOW_HEADERS = [
        'Origin',
        'No-Cache',
        'X-Requested-With',
        'If-Modified-Since',
        'Pragma',
        'Last-Modified',
        'Cache-Control',
        'Expires',
        'Content-Type',
        'X-E4M-With',
    ]

    def options(self, *args, **kwargs):
        self.set_header('Allow', ','.join(self.SUPPORTED_METHODS))

    def return_back(self, chunk):
        raise tornado.gen.Return(chunk)

    def set_cors_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', ','.join(self.SUPPORTED_METHODS))
        self.set_header('Access-Control-Allow-Headers', ','.join(self.ACCESS_CONTROL_ALLOW_HEADERS))

    def write(self, chunk):
        if isinstance(chunk, (dict, list)):
            chunk = self.dump_response(chunk)
            self.set_header("Content-Type", "application/json; charset=UTF-8")
        super(RestRequestHandler, self).write(chunk)

    def _handle_request_exception(self, e):
        if isinstance(e, RestError):
            self.write(e.to_dict())
            self.set_status(e.httpcode)
            if not self._finished:
                self.finish()
            return
        super(RestRequestHandler, self)._handle_request_exception(e)

    @tornado.gen.coroutine
    def _wrap_method(self):
        method = getattr(self, self.request.method.lower())
        method = tornado.gen.coroutine(method)
        chunk = yield method(*self.path_args, **self.path_kwargs)
        if chunk is not None:
            self.write(chunk)
        if self.ALLOW_CORS:
            self.set_cors_headers()

    def _execute_method(self):
        if not self._finished:
            self._when_complete(self._wrap_method(), self._execute_finish)

    def dump_response(self, chunk):
        """默认使用JSON序列化
        :param chunk:
        :return:
        """
        return json.dumps(chunk, ensure_ascii=False)

