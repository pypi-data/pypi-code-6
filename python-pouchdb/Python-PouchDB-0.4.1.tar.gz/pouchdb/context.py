#	Copyright 2013-2014, Marten de Vries
#
#	Licensed under the Apache License, Version 2.0 (the "License");
#	you may not use this file except in compliance with the License.
#	You may obtain a copy of the License at
#
#	http://www.apache.org/licenses/LICENSE-2.0
#
#	Unless required by applicable law or agreed to in writing, software
#	distributed under the License is distributed on an "AS IS" BASIS,
#	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#	See the License for the specific language governing permissions and
#	limitations under the License.

import sys
import os
import json
import base64
import logging

from pouchdb import utils

logger = logging.getLogger(__name__)

#A lot of 'pragma: no cover/branch' statements here. Every path is
#covered when running python setup.py extensive_test, but that
#script uses multiple different Python versions and Qt bindings.That is
#impractical for coverage generation.

def importBestSuitedQtBinding():
	#first try to import a binding imported by another module already
	bindings = ["PySide", "PyQt5", "PyQt4"]
	importedBindings = [b for b in bindings if b in sys.modules]
	with utils.suppress(IndexError):
		importBinding(importedBindings[0])
		#imported a binding earlier imported by another module
		#succesfully, stop trying to import a binding.
		return #pragma: no cover
	#no other module imported a binding yet, import one ourselves.
	for binding in bindings: #pragma: no branch
		with utils.suppress(ImportError):
			importBinding(binding)
			#succes: stop trying
			return

def importBinding(binding):
	{
		"PySide": importPySide,
		"PyQt5": importPyQt5,
		"PyQt4": importPyQt4,
	}[binding]()

def importPySide():
	global QtCore, QtGui, QtNetwork, QtWebKit, QtWebKitWidgets
	from PySide import QtCore, QtGui, QtNetwork, QtWebKit
	QtWebKitWidgets = QtWebKit
	logger.info("Imported PySide")

def importPyQt5(): #pragma: no cover
	global QtCore, QtGui, QtWebKit, QtNetwork, QtWebKitWidgets
	from PyQt5 import QtCore, QtNetwork, QtWebKitWidgets, QtWebKit, QtWidgets as QtGui
	logger.info("Imported PyQt5")

def importPyQt4(): #pragma: no cover
	global QtCore, QtGui, QtWebKit, QtNetwork, QtWebKitWidgets
	from PyQt4 import QtCore, QtGui, QtNetwork, QtWebKit
	QtWebKitWidgets = QtWebKit
	logger.info("Imported PyQt4")

#Import a Qt binding
importBestSuitedQtBinding()

class Page(QtWebKitWidgets.QWebPage):
	def __init__(self, gate, *args, **kwargs):
		super(Page, self).__init__(*args, **kwargs)

		self._gate = gate
		self._messages = []

		self.mainFrame().javaScriptWindowObjectCleared.connect(self._setGate)

	def _setGate(self):
		self.mainFrame().addToJavaScriptWindowObject("gate", self._gate)

	def javaScriptConsoleMessage(self, message, lineNumber, sourceId):
		self._messages.append("line %s: %s" % (lineNumber, message))

	def getMessagesAndReset(self):
		r = self._messages
		self._messages = []
		return r

class Gate(QtCore.QObject):
	try:
		Signal = QtCore.Signal
	except AttributeError: #pragma: no cover
		Signal = QtCore.pyqtSignal
	callbackCalled = Signal([str, str])

class JSError(Exception):
	def __init__(self, messages, *args, **kwargs):
		message = "\n".join(messages)

		super(JSError, self).__init__(message, *args, **kwargs)

class JSON(object):
	def __init__(self, data):
		self.data = data

class Blob(object):
	def __init__(self, data):
		self.data = data

	def toJS(self):
		return "b64toBlob('%s')" % unicode(base64.b64encode(self.data), encoding="ascii")

class JSContext(object):
	JSError = JSError

	_functions = {}

	def __init__(self, js, className, ignoredErrors, storageDir, baseUrl, *args, **kwargs):
		super(JSContext, self).__init__(*args, **kwargs)

		self._html = "<script>" + js + "</script>"
		self._className = className
		self._ignoredErrors = ignoredErrors
		self._baseUrl = baseUrl

		#this is used to prevent another callback than the return-of-a-
		#statement callback being called first after a Python command.
		#Otherwise you risk having a promise that has already fired
		#before said promise is accessable to a Python user.
		self._evalJsWaiting = False

		#this is used to track functions that are being waited on via
		#waitUntilCalled.
		self._waitedOn = set()

		self._app = QtGui.QApplication.instance()
		if not self._app: #pragma: no branch
			self._app = QtGui.QApplication(sys.argv)

		self._gate = Gate()
		self._gate.callbackCalled.connect(self._callbackCalled)
		self._page = Page(self._gate)

		#200 databases (1GB max) should be enough. Maybe -1 would work,
		#but since there's no documentation for that this is probably
		#the best solution.
		#
		#Uses globalSettings() because the offlineStoragePath() property
		#is static anyway. This way, the console given by inspect() also
		#gets these settings.
		QtWebKit.QWebSettings.globalSettings().setOfflineStorageDefaultQuota(1024 * 1024 * 5 * 200)
		#Stop the same-origin policy for file URLs (which we use).
		QtWebKit.QWebSettings.globalSettings().setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)
		QtWebKit.QWebSettings.globalSettings().setAttribute(QtWebKit.QWebSettings.OfflineStorageDatabaseEnabled, True)

		path = os.path.expandvars(os.path.abspath(os.path.expanduser(storageDir)))
		currentPath = QtWebKit.QWebSettings.globalSettings().offlineStoragePath()

		if currentPath != path:
			if not currentPath:
				QtWebKit.QWebSettings.globalSettings().setOfflineStoragePath(path)
			else:
				logger.debug("offlineStoragePath - old: %s, new: %s", currentPath, path)
				raise ValueError("QWebSettings' offlineStoragePath() property is already set to another value. Impossible to change it since it's a static property.")

		#Qt guarantees the html is loaded immeadiately, and since there
		#aren't any resources, we don't need to block until loaded.
		self._page.mainFrame().setHtml(self._html, QtCore.QUrl(self._baseUrl))
		logger.debug("(re)loaded page")

	def getDbSize(self, name):
		for db in self._page.mainFrame().securityOrigin().databases():
			if db.name() == name:
				return db.size()
		raise KeyError("No such database")

	def inspect(self, block=True):
		"""Useful for debugging. You just import pouchdb, call
		   pouchdb.getContext().inspect(), and a web inspector will pop
		   up that you can use to manually inspect the pouchdb webkit
		   environment.

		"""
		QtWebKit.QWebSettings.globalSettings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
		if not hasattr(self, "_i"): #pragma: no branch
			self._i = QtWebKitWidgets.QWebInspector()
			self._i.setPage(self._page)
		self._i.show()
		while block and self._i.isVisible():#pragma: no cover
			self._app.processEvents()
		self._i.close()
		QtWebKit.QWebSettings.globalSettings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, False)

	def clearCookies(self):
		self._page.networkAccessManager().setCookieJar(QtNetwork.QNetworkCookieJar())

	def _callbackCalled(self, id, args):
		if self._evalJsWaiting and id != "evalJs":
			#schedule to run this function later again - when this
			#condition is hopefully solved.
			QtCore.QTimer.singleShot(0, lambda: self._callbackCalled(id, args))
			return

		def callFunc():
			logger.debug("callback '%s' called with args %s", id, args)
			self._waitedOn.discard(func)
			func(*self._toPyArgs(args))

		func = self._functions[unicode(id)]
		#calling a function from a slot called by the JS engine blocks
		#the JS engine itself, which we don't want, so execute somewhere
		#else in the event loop.
		QtCore.QTimer.singleShot(0, callFunc)

	def _toPyArgs(self, args):
		args = json.loads(unicode(args))
		return [self._toPyArg(a) for a in args]

	def _toPyArg(self, arg):
		#function conversion
		with utils.suppress(TypeError, KeyError):
			if arg["type"] == "_js_returned_function":
				return lambda *args: self.evalJs("return functions[%s](%s);" % (
					arg["functionId"],
					self._toJSArgs(args),
				))
		#'blob' conversion
		with utils.suppress(TypeError, KeyError):
			if arg["type"] == "_js_returned_blob":
				return utils.AttrAccessDict({
					"type": arg["blobType"],
					"data": base64.b64decode(arg["data"].encode("ascii")),
				})
		#object: recursion
		with utils.suppress(AttributeError):
			newArg = utils.AttrAccessDict()
			for key, value in arg.iteritems():
				newArg[key] = self._toPyArg(value)
			return newArg

		#array: recursion
		if isinstance(arg, list):
			return map(self._toPyArg, arg)

		#everything else
		return arg

	def newObject(self, id, *args):
		self.evalJs("""
			objects[{id}] = new {className}({args});
		""".format(
			className=self._className,
			id=id,
			args=self._toJSArgs(args),
		))

	def _toJSArgs(self, args):
		return ", ".join(self._toJSArg(a) for a in args)

	def _toJSArg(self, arg):
		#callables
		if callable(arg):
			self._functions[str(id(arg))] = arg
			return "createCallback('%s')" % id(arg)

		#'blobs'
		if isinstance(arg, Blob):
			return arg.toJS()

		#json values can pass through - they are already valid JS.
		if isinstance(arg, JSON):
			return arg.data

		#mappings - handle recursively
		with utils.suppress(AttributeError):
			obj = "{"
			for k, v in arg.iteritems():
				obj += '"' + k +'":' + self._toJSArg(v) + ","
			return obj.strip(",") + "}"

		#the default
		return json.dumps(arg)

	def staticProperty(self, propertyName):
		js = "return %s['%s']" % (self._className, propertyName)
		return self.evalJs(js)

	def callStatic(self, funcName, *args):
		js = "return {className}.{funcName}({args});".format(
			className=self._className,
			args=self._toJSArgs(args),
			funcName=funcName,
			id=id,
		)
		return self.evalJs(js)

	def call(self, id, funcName, *args):
		js = "return objects[{id}].{funcName}({args});".format(
			args=self._toJSArgs(args),
			funcName=funcName,
			id=id,
		)
		return self.evalJs(js)

	def waitUntilCalled(self, callbacks):
		"""Blocks until one of the `callbacks` is called. When passing
		   in only one callback ommitting the list is allowed.

		"""
		#when only one, put it in a list.
		if callable(callbacks):
			callbacks = [callbacks]

		self._waitedOn.update(callbacks)

		while all(callback in self._waitedOn for callback in callbacks):
			self._app.processEvents()

			errors = []
			for error in self._page.getMessagesAndReset():
				for ignoredPattern in self._ignoredErrors:
					if ignoredPattern in error:
						break
				else:
					errors.append(error)
			if errors:
				raise JSError(errors)

		for callback in callbacks:
			#to clean the set if called with multiple callbacks
			self._waitedOn.discard(callback)

	def evalJs(self, userJs):
		logger.debug("evalling JS: %s", userJs.strip())
		returned = {}
		def callback(result=None):
			self._evalJsWaiting = False
			returned["result"] = result
		self._functions["evalJs"] = callback
		js = """
			var result = (function () {
				%s
			}());
			createCallback('evalJs')(result);
		""".replace("\n", "") % userJs
		self._evalJsWaiting = True
		self._page.mainFrame().evaluateJavaScript(js)

		self.waitUntilCalled(callback)

		return returned["result"]
