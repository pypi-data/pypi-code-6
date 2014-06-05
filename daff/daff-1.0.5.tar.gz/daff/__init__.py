#!/usr/bin/env python
import builtins as python_lib_Builtin
import math as python_lib_Math
import math as Math
from builtins import str as String
from builtins import dict as python_lib_Dict
import os as python_lib_Os
import math as python__Boot_Math
import inspect as python__Boot_Inspect
import builtins as python_internal_HxBuiltin
from builtins import bytes as python_lib_Bytes
import functools as python_lib_FuncTools
import inspect as python_lib_Inspect
import json as python_lib_Json
try:
	import msvcrt as python_lib_Msvcrt
except:
	pass

import random as python_lib_Random
from builtins import set as python_lib_Set
import shutil as python_lib_ShUtil
import subprocess as python_lib_Subprocess
import sys as python_lib_Sys
try:
	import termios as python_lib_Termios
except:
	pass

import time as python_lib_Time
try:
	import tty as python_lib_Tty
except:
	pass

from datetime import datetime as python_lib_datetime_DateTime
from datetime import timedelta as python_lib_datetime_TimeDelta
from datetime import tzinfo as python_lib_datetime_TzInfo
from datetime import timezone as python_lib_datetime_Timezone
from io import StringIO as python_lib_io_StringIO
import urllib.parse as python_lib_urllib_Parse


class _hx_ClassRegistry(python_lib_Dict):

	def __init__(self):
		super().__init__()

	def _register(self,cls,name):
		cls._hx_class = cls
		cls._hx_class_name = name
		self[name] = cls

	def registerAbstract(self,name):
		_g = self
		def _hx_local_0(cls):
			_g._register(cls,name)
			return cls
		wrapper = _hx_local_0
		return wrapper

	def registerEnum(self,name,constructs):
		_g = self
		def _hx_local_0(cls):
			_g._register(cls,name)
			cls._hx_constructs = constructs
			return cls
		wrapper = _hx_local_0
		return wrapper

	def registerClass(self,name,fields = None,props = None,methods = None,statics = None,interfaces = None,superClass = None):
		_g = self
		if (fields is None):
			fields = []
		if (props is None):
			props = []
		if (methods is None):
			methods = []
		if (statics is None):
			statics = []
		if (interfaces is None):
			interfaces = []
		def _hx_local_0(cls):
			_g._register(cls,name)
			cls._hx_fields = fields
			cls._hx_props = props
			cls._hx_methods = methods
			cls._hx_statics = statics
			cls._hx_interfaces = interfaces
			if (superClass is not None):
				cls._hx_super = superClass
			return cls
		wrapper = _hx_local_0
		return wrapper


class _hx_AnonObject:

	def __init__(self,fields):
		self.__dict__ = fields
_hx_classes = _hx_ClassRegistry()


@_hx_classes.registerClass("python.Boot", statics=["mathRound","mkSet","keywords","arrayJoin","isInstance","builtinStr","builtinHasAttr","builtinGetAttr","isPyBool","isPyInt","isPyFloat","builtinLen","builtinInt","builtinCallable","inspectGetMembers","inspectIsClass","inspectIsFunction","inspectIsMethod","isClass","isAnonObject","_add_dynamic","toString","toString1","isMetaType","fields","isString","isArray","field","getInstanceFields","getSuperClass","getClassFields","unsafeFastCodeAt","handleKeywords","prefixLength","unhandleKeywords"])
class python_Boot:

	@staticmethod
	def mathRound(v):
		return python__Boot_Math.floor((v + 0.5))

	@staticmethod
	def mkSet(a):
		return python_internal_HxBuiltin.set(a)

	@staticmethod
	def arrayJoin(x,sep):
		return sep.join([python_Boot.toString1(x1,'') for x1 in x])

	@staticmethod
	def isInstance(o,x):
		return python_internal_HxBuiltin.isinstance(o,x)

	@staticmethod
	def builtinStr(o):
		return python_internal_HxBuiltin.str(o)

	@staticmethod
	def builtinHasAttr(o,x):
		return python_internal_HxBuiltin.hasattr(o,x)

	@staticmethod
	def builtinGetAttr(o,x):
		return python_internal_HxBuiltin.getattr(o,x)

	@staticmethod
	def isPyBool(o):
		return python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.bool)

	@staticmethod
	def isPyInt(o):
		return python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.int)

	@staticmethod
	def isPyFloat(o):
		return python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.float)

	@staticmethod
	def builtinLen(o):
		return python_internal_HxBuiltin.len(o)

	@staticmethod
	def builtinInt(o):
		return python_internal_HxBuiltin.int(o)

	@staticmethod
	def builtinCallable(o):
		return python_internal_HxBuiltin.callable(o)

	@staticmethod
	def inspectGetMembers(o,f):
		python__Boot_Inspect.getmembers(o, f)

	@staticmethod
	def inspectIsClass(o):
		return python__Boot_Inspect.isclass(o)

	@staticmethod
	def inspectIsFunction(o):
		return python__Boot_Inspect.isfunction(o)

	@staticmethod
	def inspectIsMethod(o):
		return python__Boot_Inspect.ismethod(o)

	@staticmethod
	def isClass(o):
		return ((o is not None) and ((HxOverrides.eq(o,String) or python__Boot_Inspect.isclass(o))))

	@staticmethod
	def isAnonObject(o):
		return python_internal_HxBuiltin.isinstance(o,_hx_AnonObject)

	@staticmethod
	def _add_dynamic(a,b):
		if (python_internal_HxBuiltin.isinstance(a,String) or python_internal_HxBuiltin.isinstance(b,String)):
			return (python_Boot.toString1(a,"") + python_Boot.toString1(b,""))
		return (a + b)

	@staticmethod
	def toString(o):
		return python_Boot.toString1(o,"")

	@staticmethod
	def toString1(o,s):
		if (o is None):
			return "null"
		if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.str):
			return o
		if (s is None):
			s = ""
		if (python_lib_Builtin.len(s) >= 5):
			return "<...>"
		if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.bool):
			if o:
				return "true"
			else:
				return "false"
		if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.int):
			return python_internal_HxBuiltin.str(o)
		if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.float):
			try:
				if (o == python_internal_HxBuiltin.int(o)):
					o1 = None
					v = o
					o1 = python__Boot_Math.floor((v + 0.5))
					return python_internal_HxBuiltin.str(o1)
				else:
					return python_internal_HxBuiltin.str(o)
			except Exception as _hx_e:
				_hx_e1 = _hx_e.val if isinstance(_hx_e, _HxException) else _hx_e
				e = _hx_e1
				return python_internal_HxBuiltin.str(o)
		if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
			o11 = o
			l = python_lib_Builtin.len(o11)
			st = "["
			s = (HxOverrides.stringOrNull(s) + "\t")
			_g = 0
			while ((_g < l)):
				i = _g
				_g = (_g + 1)
				prefix = ""
				if (i > 0):
					prefix = ","
				st = (HxOverrides.stringOrNull(st) + HxOverrides.stringOrNull(((HxOverrides.stringOrNull(prefix) + HxOverrides.stringOrNull(python_Boot.toString1((o11[i] if i >= 0 and i < python_lib_Builtin.len(o11) else None),s))))))
			st = (HxOverrides.stringOrNull(st) + "]")
			return st
		try:
			if python_internal_HxBuiltin.hasattr(o,"toString"):
				return o.toString()
		except Exception as _hx_e:
			_hx_e1 = _hx_e.val if isinstance(_hx_e, _HxException) else _hx_e
			pass
		if (python__Boot_Inspect.isfunction(o) or python__Boot_Inspect.ismethod(o)):
			return "<function>"
		if python_internal_HxBuiltin.hasattr(o,"__class__"):
			if python_Boot.isAnonObject(o):
				toStr = None
				try:
					fields = python_Boot.fields(o)
					fieldsStr = None
					_g1 = []
					_g11 = 0
					while ((_g11 < python_lib_Builtin.len(fields))):
						f = (fields[_g11] if _g11 >= 0 and _g11 < python_lib_Builtin.len(fields) else None)
						_g11 = (_g11 + 1)
						x = ((("" + HxOverrides.stringOrNull(f)) + " : ") + HxOverrides.stringOrNull(python_Boot.toString1(python_Boot.field(o,f),(HxOverrides.stringOrNull(s) + "\t"))))
						_g1.append(x)
					fieldsStr = _g1
					toStr = (("{ " + HxOverrides.stringOrNull(python_Boot.arrayJoin(fieldsStr,", "))) + " }")
				except Exception as _hx_e:
					_hx_e1 = _hx_e.val if isinstance(_hx_e, _HxException) else _hx_e
					e2 = _hx_e1
					return "{ ... }"
				if (toStr is None):
					return "{ ... }"
				else:
					return toStr
			if python_internal_HxBuiltin.isinstance(o,Enum):
				o2 = o
				l1 = python_internal_HxBuiltin.len(o2.params)
				hasParams = (l1 > 0)
				if hasParams:
					paramsStr = ""
					_g2 = 0
					while ((_g2 < l1)):
						i1 = _g2
						_g2 = (_g2 + 1)
						prefix1 = ""
						if (i1 > 0):
							prefix1 = ","
						paramsStr = (HxOverrides.stringOrNull(paramsStr) + HxOverrides.stringOrNull(((HxOverrides.stringOrNull(prefix1) + HxOverrides.stringOrNull(python_Boot.toString1((o2.params[i1] if i1 >= 0 and i1 < python_lib_Builtin.len(o2.params) else None),s))))))
					return (((HxOverrides.stringOrNull(o2.tag) + "(") + HxOverrides.stringOrNull(paramsStr)) + ")")
				else:
					return o2.tag
			if python_internal_HxBuiltin.hasattr(o,"_hx_class_name"):
				if (o.__class__.__name__ != "type"):
					fields1 = python_Boot.getInstanceFields(o)
					fieldsStr1 = None
					_g3 = []
					_g12 = 0
					while ((_g12 < python_lib_Builtin.len(fields1))):
						f1 = (fields1[_g12] if _g12 >= 0 and _g12 < python_lib_Builtin.len(fields1) else None)
						_g12 = (_g12 + 1)
						x1 = ((("" + HxOverrides.stringOrNull(f1)) + " : ") + HxOverrides.stringOrNull(python_Boot.toString1(python_Boot.field(o,f1),(HxOverrides.stringOrNull(s) + "\t"))))
						_g3.append(x1)
					fieldsStr1 = _g3
					toStr1 = (((Std.string(o._hx_class_name) + "( ") + HxOverrides.stringOrNull(python_Boot.arrayJoin(fieldsStr1,", "))) + " )")
					return toStr1
				else:
					fields2 = python_Boot.getClassFields(o)
					fieldsStr2 = None
					_g4 = []
					_g13 = 0
					while ((_g13 < python_lib_Builtin.len(fields2))):
						f2 = (fields2[_g13] if _g13 >= 0 and _g13 < python_lib_Builtin.len(fields2) else None)
						_g13 = (_g13 + 1)
						x2 = ((("" + HxOverrides.stringOrNull(f2)) + " : ") + HxOverrides.stringOrNull(python_Boot.toString1(python_Boot.field(o,f2),(HxOverrides.stringOrNull(s) + "\t"))))
						_g4.append(x2)
					fieldsStr2 = _g4
					toStr2 = (((("#" + Std.string(o._hx_class_name)) + "( ") + HxOverrides.stringOrNull(python_Boot.arrayJoin(fieldsStr2,", "))) + " )")
					return toStr2
			if (o == String):
				return "#String"
			if (o == list):
				return "#Array"
			if python_internal_HxBuiltin.callable(o):
				return "function"
			try:
				if python_internal_HxBuiltin.hasattr(o,"__repr__"):
					return o.__repr__()
			except Exception as _hx_e:
				_hx_e1 = _hx_e.val if isinstance(_hx_e, _HxException) else _hx_e
				pass
			if python_internal_HxBuiltin.hasattr(o,"__str__"):
				return o.__str__([])
			if python_internal_HxBuiltin.hasattr(o,"__name__"):
				return o.__name__
			return "???"
		else:
			try:
				def _hx_local_7(_):
					return True
				python__Boot_Inspect.getmembers(o, _hx_local_7)
				return python_internal_HxBuiltin.str(o)
			except Exception as _hx_e:
				_hx_e1 = _hx_e.val if isinstance(_hx_e, _HxException) else _hx_e
				e4 = _hx_e1
				return "???"

	@staticmethod
	def isMetaType(v,t):
		return (v == t)

	@staticmethod
	def fields(o):
		a = []
		if (o is not None):
			if python_internal_HxBuiltin.hasattr(o,"_hx_fields"):
				fields = o._hx_fields
				return python_internal_HxBuiltin.list(fields)
			if python_internal_HxBuiltin.isinstance(o,_hx_AnonObject):
				d = o.__dict__
				keys = d.keys()
				handler = python_Boot.unhandleKeywords
				for k in keys:
					a.append(handler(k))
			elif python_internal_HxBuiltin.hasattr(o,"__dict__"):
				a1 = []
				d1 = o.__dict__
				keys1 = d1.keys()
				for k in keys1:
					a.append(k)
		return a

	@staticmethod
	def isString(o):
		return python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.str)

	@staticmethod
	def isArray(o):
		return python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list)

	@staticmethod
	def field(o,field):
		if (field is None):
			return None
		_hx_local_0 = python_lib_Builtin.len((field))
		if (_hx_local_0 == 6):
			if ((field) == "length"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.str):
					s = o
					return python_internal_HxBuiltin.len(s)
				elif python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					x = o
					return python_internal_HxBuiltin.len(x)
			elif ((field) == "charAt"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.str):
					s3 = o
					def _hx_local_1(a1):
						return HxString.charAt(s3,a1)
					return _hx_local_1
			elif ((field) == "substr"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.str):
					s8 = o
					def _hx_local_2(a14):
						return HxString.substr(s8,a14)
					return _hx_local_2
			elif ((field) == "filter"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					x5 = o
					def _hx_local_3(f1):
						return python_internal_ArrayImpl.filter(x5,f1)
					return _hx_local_3
			elif ((field) == "concat"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					a16 = o
					def _hx_local_4(a21):
						return python_internal_ArrayImpl.concat(a16,a21)
					return _hx_local_4
			elif ((field) == "insert"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					a3 = o
					def _hx_local_5(a17,x8):
						python_internal_ArrayImpl.insert(a3,a17,x8)
					return _hx_local_5
			elif ((field) == "remove"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					x12 = o
					def _hx_local_6(e2):
						return python_internal_ArrayImpl.remove(x12,e2)
					return _hx_local_6
			elif ((field) == "splice"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					x16 = o
					def _hx_local_7(a19,a22):
						return python_internal_ArrayImpl.splice(x16,a19,a22)
					return _hx_local_7
		elif (_hx_local_0 == 5):
			if ((field) == "split"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.str):
					s7 = o
					def _hx_local_8(d):
						return HxString.split(s7,d)
					return _hx_local_8
			elif ((field) == "shift"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					x13 = o
					def _hx_local_9():
						return python_internal_ArrayImpl.shift(x13)
					return _hx_local_9
			elif ((field) == "slice"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					x14 = o
					def _hx_local_10(a18):
						return python_internal_ArrayImpl.slice(x14,a18)
					return _hx_local_10
		elif (_hx_local_0 == 11):
			if ((field) == "toLowerCase"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.str):
					s1 = o
					def _hx_local_11():
						return HxString.toLowerCase(s1)
					return _hx_local_11
			elif ((field) == "toUpperCase"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.str):
					s2 = o
					def _hx_local_12():
						return HxString.toUpperCase(s2)
					return _hx_local_12
			elif ((field) == "lastIndexOf"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.str):
					s6 = o
					def _hx_local_13(a13):
						return HxString.lastIndexOf(s6,a13)
					return _hx_local_13
				elif python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					a2 = o
					def _hx_local_14(x2):
						return python_internal_ArrayImpl.lastIndexOf(a2,x2)
					return _hx_local_14
		elif (_hx_local_0 == 4):
			if ((field) == "copy"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					def _hx_local_15():
						x6 = o
						return python_internal_HxBuiltin.list(x6)
					return _hx_local_15
			elif ((field) == "join"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					def _hx_local_16(sep):
						return python_internal_ArrayImpl.join(o,sep)
					return _hx_local_16
			elif ((field) == "push"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					x10 = o
					def _hx_local_17(e):
						return python_internal_ArrayImpl.push(x10,e)
					return _hx_local_17
			elif ((field) == "sort"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					x15 = o
					def _hx_local_18(f2):
						python_internal_ArrayImpl.sort(x15,f2)
					return _hx_local_18
		elif (_hx_local_0 == 10):
			if ((field) == "charCodeAt"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.str):
					s4 = o
					def _hx_local_19(a11):
						return HxString.charCodeAt(s4,a11)
					return _hx_local_19
		elif (_hx_local_0 == 3):
			if ((field) == "map"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					x4 = o
					def _hx_local_20(f):
						return python_internal_ArrayImpl.map(x4,f)
					return _hx_local_20
			elif ((field) == "pop"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					x9 = o
					def _hx_local_21():
						return python_internal_ArrayImpl.pop(x9)
					return _hx_local_21
		elif (_hx_local_0 == 9):
			if ((field) == "substring"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.str):
					s9 = o
					def _hx_local_22(a15):
						return HxString.substring(s9,a15)
					return _hx_local_22
		elif (_hx_local_0 == 8):
			if ((field) == "toString"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.str):
					s10 = o
					def _hx_local_23():
						return HxString.toString(s10)
					return _hx_local_23
				elif python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					x3 = o
					def _hx_local_24():
						return python_internal_ArrayImpl.toString(x3)
					return _hx_local_24
			elif ((field) == "iterator"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					x7 = o
					def _hx_local_25():
						return python_internal_ArrayImpl.iterator(x7)
					return _hx_local_25
		elif (_hx_local_0 == 7):
			if ((field) == "indexOf"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.str):
					s5 = o
					def _hx_local_26(a12):
						return HxString.indexOf(s5,a12)
					return _hx_local_26
				elif python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					a = o
					def _hx_local_27(x1):
						return python_internal_ArrayImpl.indexOf(a,x1)
					return _hx_local_27
			elif ((field) == "unshift"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					x11 = o
					def _hx_local_28(e1):
						python_internal_ArrayImpl.unshift(x11,e1)
					return _hx_local_28
			elif ((field) == "reverse"):
				if python_internal_HxBuiltin.isinstance(o,python_internal_HxBuiltin.list):
					a4 = o
					def _hx_local_29():
						python_internal_ArrayImpl.reverse(a4)
					return _hx_local_29
		else:
			pass
		field1 = None
		if field in python_Boot.keywords:
			field1 = ("_hx_" + field)
		elif ((((python_lib_Builtin.len(field) > 2) and ((python_internal_HxBuiltin.ord(field[0]) == 95))) and ((python_internal_HxBuiltin.ord(field[1]) == 95))) and ((python_internal_HxBuiltin.ord(field[(python_lib_Builtin.len(field) - 1)]) != 95))):
			field1 = ("_hx_" + field)
		else:
			field1 = field
		if python_internal_HxBuiltin.hasattr(o,field1):
			return python_internal_HxBuiltin.getattr(o,field1)
		else:
			return None

	@staticmethod
	def getInstanceFields(c):
		f = None
		if python_internal_HxBuiltin.hasattr(c,"_hx_fields"):
			x = c._hx_fields
			x2 = c._hx_methods
			f = (x + x2)
		else:
			f = []
		sc = python_Boot.getSuperClass(c)
		if (sc is None):
			return f
		else:
			scArr = python_Boot.getInstanceFields(sc)
			scMap = None
			_g = haxe_ds_StringMap()
			_g1 = 0
			while ((_g1 < python_lib_Builtin.len(scArr))):
				f1 = (scArr[_g1] if _g1 >= 0 and _g1 < python_lib_Builtin.len(scArr) else None)
				_g1 = (_g1 + 1)
				_g.h[f1] = f1
			scMap = _g
			res = []
			_g11 = 0
			while ((_g11 < python_lib_Builtin.len(f))):
				f11 = (f[_g11] if _g11 >= 0 and _g11 < python_lib_Builtin.len(f) else None)
				_g11 = (_g11 + 1)
				if (not f11 in scMap.h):
					scArr.append(f11)
			return scArr

	@staticmethod
	def getSuperClass(c):
		if (c is None):
			return None
		try:
			if python_internal_HxBuiltin.hasattr(c,"_hx_super"):
				return c._hx_super
			return None
		except Exception as _hx_e:
			_hx_e1 = _hx_e.val if isinstance(_hx_e, _HxException) else _hx_e
			pass
		return None

	@staticmethod
	def getClassFields(c):
		if python_internal_HxBuiltin.hasattr(c,"_hx_statics"):
			x = c._hx_statics
			return python_internal_HxBuiltin.list(x)
		else:
			return []

	@staticmethod
	def unsafeFastCodeAt(s,index):
		return python_internal_HxBuiltin.ord(s[index])

	@staticmethod
	def handleKeywords(name):
		if name in python_Boot.keywords:
			return ("_hx_" + name)
		elif ((((python_lib_Builtin.len(name) > 2) and ((python_internal_HxBuiltin.ord(name[0]) == 95))) and ((python_internal_HxBuiltin.ord(name[1]) == 95))) and ((python_internal_HxBuiltin.ord(name[(python_lib_Builtin.len(name) - 1)]) != 95))):
			return ("_hx_" + name)
		else:
			return name

	@staticmethod
	def unhandleKeywords(name):
		if (HxString.substr(name,0,python_Boot.prefixLength) == "_hx_"):
			real = HxString.substr(name,python_Boot.prefixLength,None)
			if real in python_Boot.keywords:
				return real
		return name


@_hx_classes.registerClass("Enum", fields=["tag","index","params"], methods=["__str__"])
class Enum:

	def __init__(self,tag,index,params):
		self.tag = None
		self.index = None
		self.params = None
		self.tag = tag
		self.index = index
		self.params = params

	def __str__(self):
		if (self.params is None):
			return self.tag
		else:
			return (((HxOverrides.stringOrNull(self.tag) + "(") + HxOverrides.stringOrNull(",".join([python_Boot.toString1(x1,'') for x1 in self.params]))) + ")")

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.tag = None
		_hx_o.index = None
		_hx_o.params = None


@_hx_classes.registerClass("HxOverrides", statics=["iterator","eq","stringOrNull","shift","toUpperCase","toLowerCase","rshift","modf","arrayGet","arraySet"])
class HxOverrides:

	@staticmethod
	def iterator(x):
		if python_internal_HxBuiltin.isinstance(x,python_internal_HxBuiltin.list):
			return python_HaxeIterator(x.__iter__())
		return x.iterator()

	@staticmethod
	def eq(a,b):
		if (python_internal_HxBuiltin.isinstance(a,python_internal_HxBuiltin.list) or python_internal_HxBuiltin.isinstance(b,python_internal_HxBuiltin.list)):
			return a is b
		return (a == b)

	@staticmethod
	def stringOrNull(s):
		if (s is None):
			return "null"
		else:
			return s

	@staticmethod
	def shift(x):
		return Reflect.callMethod(None,Reflect.field(x,"shift"),[])

	@staticmethod
	def toUpperCase(x):
		return Reflect.callMethod(None,Reflect.field(x,"toUpperCase"),[])

	@staticmethod
	def toLowerCase(x):
		return Reflect.callMethod(None,Reflect.field(x,"toLowerCase"),[])

	@staticmethod
	def rshift(val,n):
		return ((val % 0x100000000) >> n)

	@staticmethod
	def modf(a,b):
		return float('nan') if (b == 0.0) else a % b if a > 0 else -(-a % b)

	@staticmethod
	def arrayGet(a,i):
		if python_internal_HxBuiltin.isinstance(a,python_internal_HxBuiltin.list):
			x = a
			if ((i > -1) and ((i < python_lib_Builtin.len(x)))):
				return x[i]
			else:
				return None
		else:
			return a[i]

	@staticmethod
	def arraySet(a,i,v):
		if python_internal_HxBuiltin.isinstance(a,python_internal_HxBuiltin.list):
			x = a
			v1 = v
			l = python_lib_Builtin.len(x)
			while ((l < i)):
				x.append(None)
				l = (l + 1)
			if (l == i):
				x.append(v1)
			else:
				x[i] = v1
			return v1
		else:
			a[i] = v
			return v


@_hx_classes.registerClass("Alignment", fields=["map_a2b","map_b2a","ha","hb","ta","tb","ia","ib","map_count","order_cache","order_cache_has_reference","index_columns","reference","meta"], methods=["range","tables","headers","setRowlike","link","addIndexColumns","getIndexColumns","a2b","b2a","count","toString","toOrderPruned","toOrder","getSource","getTarget","getSourceHeader","getTargetHeader","toOrderCached","pruneOrder","toOrder3"])
class Alignment:

	def __init__(self):
		self.map_a2b = None
		self.map_b2a = None
		self.ha = None
		self.hb = None
		self.ta = None
		self.tb = None
		self.ia = None
		self.ib = None
		self.map_count = None
		self.order_cache = None
		self.order_cache_has_reference = None
		self.index_columns = None
		self.reference = None
		self.meta = None
		self.map_a2b = haxe_ds_IntMap()
		self.map_b2a = haxe_ds_IntMap()
		def _hx_local_0():
			self.hb = 0
			return self.hb
		self.ha = _hx_local_0()
		self.map_count = 0
		self.reference = None
		self.meta = None
		self.order_cache_has_reference = False
		self.ia = 0
		self.ib = 0

	def range(self,ha,hb):
		self.ha = ha
		self.hb = hb

	def tables(self,ta,tb):
		self.ta = ta
		self.tb = tb

	def headers(self,ia,ib):
		self.ia = ia
		self.ib = ib

	def setRowlike(self,flag):
		pass

	def link(self,a,b):
		self.map_a2b.set(a,b)
		self.map_b2a.set(b,a)
		_hx_local_0 = self
		_hx_local_1 = _hx_local_0.map_count
		_hx_local_0.map_count = (_hx_local_1 + 1)
		_hx_local_1

	def addIndexColumns(self,unit):
		if (self.index_columns is None):
			self.index_columns = list()
		_this = self.index_columns
		_this.append(unit)

	def getIndexColumns(self):
		return self.index_columns

	def a2b(self,a):
		return self.map_a2b.h.get(a,None)

	def b2a(self,b):
		return self.map_b2a.h.get(b,None)

	def count(self):
		return self.map_count

	def toString(self):
		return ("" + HxOverrides.stringOrNull(self.map_a2b.toString()))

	def toOrderPruned(self,rowlike):
		return self.toOrderCached(True,rowlike)

	def toOrder(self):
		return self.toOrderCached(False,False)

	def getSource(self):
		return self.ta

	def getTarget(self):
		return self.tb

	def getSourceHeader(self):
		return self.ia

	def getTargetHeader(self):
		return self.ib

	def toOrderCached(self,prune,rowlike):
		if (self.order_cache is not None):
			if (self.reference is not None):
				if (not self.order_cache_has_reference):
					self.order_cache = None
		if (self.order_cache is None):
			self.order_cache = self.toOrder3(prune,rowlike)
		if (self.reference is not None):
			self.order_cache_has_reference = True
		return self.order_cache

	def pruneOrder(self,o,ref,rowlike):
		tl = ref.tb
		tr = self.tb
		if rowlike:
			if (Reflect.field(tl,"get_width")() != Reflect.field(tr,"get_width")()):
				return
		elif (Reflect.field(tl,"get_height")() != Reflect.field(tr,"get_height")()):
			return
		units = o.getList()
		left_units = list()
		left_locs = list()
		right_units = list()
		right_locs = list()
		eliminate = list()
		ct = 0
		_g1 = 0
		_g = python_lib_Builtin.len(units)
		while ((_g1 < _g)):
			i = _g1
			_g1 = (_g1 + 1)
			unit = (units[i] if i >= 0 and i < python_lib_Builtin.len(units) else None)
			if ((unit.l < 0) and ((unit.r >= 0))):
				right_units.append(unit)
				right_locs.append(i)
				ct = (ct + 1)
			elif ((unit.r < 0) and ((unit.l >= 0))):
				left_units.append(unit)
				left_locs.append(i)
				ct = (ct + 1)
			elif (ct > 0):
				len = python_lib_Builtin.len(left_units)
				pos = 0
				if (pos < 0):
					pos = (python_lib_Builtin.len(left_units) + pos)
				if (pos < 0):
					pos = 0
				res = left_units[pos:(pos + len)]
				del left_units[pos:(pos + len)]
				res
				len1 = python_lib_Builtin.len(right_units)
				pos1 = 0
				if (pos1 < 0):
					pos1 = (python_lib_Builtin.len(right_units) + pos1)
				if (pos1 < 0):
					pos1 = 0
				res1 = right_units[pos1:(pos1 + len1)]
				del right_units[pos1:(pos1 + len1)]
				res1
				len2 = python_lib_Builtin.len(left_locs)
				pos2 = 0
				if (pos2 < 0):
					pos2 = (python_lib_Builtin.len(left_locs) + pos2)
				if (pos2 < 0):
					pos2 = 0
				res2 = left_locs[pos2:(pos2 + len2)]
				del left_locs[pos2:(pos2 + len2)]
				res2
				len3 = python_lib_Builtin.len(right_locs)
				pos3 = 0
				if (pos3 < 0):
					pos3 = (python_lib_Builtin.len(right_locs) + pos3)
				if (pos3 < 0):
					pos3 = 0
				res3 = right_locs[pos3:(pos3 + len3)]
				del right_locs[pos3:(pos3 + len3)]
				res3
				ct = 0
			while (((python_lib_Builtin.len(left_locs) > 0) and ((python_lib_Builtin.len(right_locs) > 0)))):
				l = (left_units[0] if 0 < python_lib_Builtin.len(left_units) else None).l
				r = (right_units[0] if 0 < python_lib_Builtin.len(right_units) else None).r
				view = tl.getCellView()
				match = True
				if rowlike:
					w = Reflect.field(tl,"get_width")()
					_g2 = 0
					while ((_g2 < w)):
						j = _g2
						_g2 = (_g2 + 1)
						if (not view.equals(tl.getCell(j,l),tr.getCell(j,r))):
							match = False
							break
				else:
					h = Reflect.field(tl,"get_height")()
					_g21 = 0
					while ((_g21 < h)):
						j1 = _g21
						_g21 = (_g21 + 1)
						if (not view.equals(tl.getCell(l,j1),tr.getCell(r,j1))):
							match = False
							break
				if match:
					eliminate.append((left_locs[0] if 0 < python_lib_Builtin.len(left_locs) else None))
					eliminate.append((right_locs[0] if 0 < python_lib_Builtin.len(right_locs) else None))
				if (python_lib_Builtin.len(left_units) == 0):
					None
				else:
					left_units.pop(0)
				if (python_lib_Builtin.len(right_units) == 0):
					None
				else:
					right_units.pop(0)
				if (python_lib_Builtin.len(left_locs) == 0):
					None
				else:
					left_locs.pop(0)
				if (python_lib_Builtin.len(right_locs) == 0):
					None
				else:
					right_locs.pop(0)
				ct = (ct - 2)
		if (python_lib_Builtin.len(eliminate) > 0):
			def _hx_local_3(a,b):
				return (a - b)
			eliminate.sort(key= python_lib_FuncTools.cmp_to_key(_hx_local_3))
			_hx_del = 0
			_g3 = 0
			while ((_g3 < python_lib_Builtin.len(eliminate))):
				e = (eliminate[_g3] if _g3 >= 0 and _g3 < python_lib_Builtin.len(eliminate) else None)
				_g3 = (_g3 + 1)
				_this = o.getList()
				pos4 = (e - _hx_del)
				if (pos4 < 0):
					pos4 = (python_lib_Builtin.len(_this) + pos4)
				if (pos4 < 0):
					pos4 = 0
				res4 = _this[pos4:(pos4 + 1)]
				del _this[pos4:(pos4 + 1)]
				res4
				_hx_del = (_hx_del + 1)

	def toOrder3(self,prune,rowlike):
		ref = self.reference
		if (ref is None):
			ref = Alignment()
			ref.range(self.ha,self.ha)
			ref.tables(self.ta,self.ta)
			_g1 = 0
			_g = self.ha
			while ((_g1 < _g)):
				i = _g1
				_g1 = (_g1 + 1)
				ref.link(i,i)
		order = Ordering()
		if (self.reference is None):
			order.ignoreParent()
		xp = 0
		xl = 0
		xr = 0
		hp = self.ha
		hl = ref.hb
		hr = self.hb
		vp = haxe_ds_IntMap()
		vl = haxe_ds_IntMap()
		vr = haxe_ds_IntMap()
		_g2 = 0
		while ((_g2 < hp)):
			i1 = _g2
			_g2 = (_g2 + 1)
			vp.set(i1,i1)
		_g3 = 0
		while ((_g3 < hl)):
			i2 = _g3
			_g3 = (_g3 + 1)
			vl.set(i2,i2)
		_g4 = 0
		while ((_g4 < hr)):
			i3 = _g4
			_g4 = (_g4 + 1)
			vr.set(i3,i3)
		ct_vp = hp
		ct_vl = hl
		ct_vr = hr
		prev = -1
		ct = 0
		max_ct = ((((hp + hl) + hr)) * 10)
		while ((((ct_vp > 0) or ((ct_vl > 0))) or ((ct_vr > 0)))):
			ct = (ct + 1)
			if (ct > max_ct):
				haxe_Log.trace("Ordering took too long, something went wrong",_hx_AnonObject({'fileName': "Alignment.hx", 'lineNumber': 241, 'className': "Alignment", 'methodName': "toOrder3"}))
				break
			if (xp >= hp):
				xp = 0
			if (xl >= hl):
				xl = 0
			if (xr >= hr):
				xr = 0
			if ((xp < hp) and ((ct_vp > 0))):
				if ((self.a2b(xp) is None) and ((ref.a2b(xp) is None))):
					if xp in vp.h:
						order.add(-1,-1,xp)
						prev = xp
						vp.remove(xp)
						ct_vp = (ct_vp - 1)
					xp = (xp + 1)
					continue
			zl = None
			zr = None
			if ((xl < hl) and ((ct_vl > 0))):
				zl = ref.b2a(xl)
				if (zl is None):
					if xl in vl.h:
						order.add(xl,-1,-1)
						vl.remove(xl)
						ct_vl = (ct_vl - 1)
					xl = (xl + 1)
					continue
			if ((xr < hr) and ((ct_vr > 0))):
				zr = self.b2a(xr)
				if (zr is None):
					if xr in vr.h:
						order.add(-1,xr,-1)
						vr.remove(xr)
						ct_vr = (ct_vr - 1)
					xr = (xr + 1)
					continue
			if (zl is not None):
				if (self.a2b(zl) is None):
					if xl in vl.h:
						order.add(xl,-1,zl)
						prev = zl
						vp.remove(zl)
						ct_vp = (ct_vp - 1)
						vl.remove(xl)
						ct_vl = (ct_vl - 1)
						xp = (zl + 1)
					xl = (xl + 1)
					continue
			if (zr is not None):
				if (ref.a2b(zr) is None):
					if xr in vr.h:
						order.add(-1,xr,zr)
						prev = zr
						vp.remove(zr)
						ct_vp = (ct_vp - 1)
						vr.remove(xr)
						ct_vr = (ct_vr - 1)
						xp = (zr + 1)
					xr = (xr + 1)
					continue
			if ((((zl is not None) and ((zr is not None))) and ((self.a2b(zl) is not None))) and ((ref.a2b(zr) is not None))):
				if ((zl == ((prev + 1))) or ((zr != ((prev + 1))))):
					if xr in vr.h:
						order.add(ref.a2b(zr),xr,zr)
						prev = zr
						vp.remove(zr)
						ct_vp = (ct_vp - 1)
						key = ref.a2b(zr)
						vl.remove(key)
						ct_vl = (ct_vl - 1)
						vr.remove(xr)
						ct_vr = (ct_vr - 1)
						xp = (zr + 1)
						xl = (ref.a2b(zr) + 1)
					xr = (xr + 1)
					continue
				else:
					if xl in vl.h:
						order.add(xl,self.a2b(zl),zl)
						prev = zl
						vp.remove(zl)
						ct_vp = (ct_vp - 1)
						vl.remove(xl)
						ct_vl = (ct_vl - 1)
						key1 = self.a2b(zl)
						vr.remove(key1)
						ct_vr = (ct_vr - 1)
						xp = (zl + 1)
						xr = (self.a2b(zl) + 1)
					xl = (xl + 1)
					continue
			xp = (xp + 1)
			xl = (xl + 1)
			xr = (xr + 1)
		if prune:
			self.pruneOrder(order,ref,rowlike)
		return order

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.map_a2b = None
		_hx_o.map_b2a = None
		_hx_o.ha = None
		_hx_o.hb = None
		_hx_o.ta = None
		_hx_o.tb = None
		_hx_o.ia = None
		_hx_o.ib = None
		_hx_o.map_count = None
		_hx_o.order_cache = None
		_hx_o.order_cache_has_reference = None
		_hx_o.index_columns = None
		_hx_o.reference = None
		_hx_o.meta = None


@_hx_classes.registerClass("python.internal.ArrayImpl", statics=["get_length","concat","copy","iterator","indexOf","lastIndexOf","join","toString","pop","push","unshift","remove","shift","slice","sort","splice","map","filter","insert","reverse","_get","_set","unsafeGet","unsafeSet"])
class python_internal_ArrayImpl:

	@staticmethod
	def get_length(x):
		return python_internal_HxBuiltin.len(x)

	@staticmethod
	def concat(a1,a2):
		return (a1 + a2)

	@staticmethod
	def copy(x):
		return python_internal_HxBuiltin.list(x)

	@staticmethod
	def iterator(x):
		return python_HaxeIterator(x.__iter__())

	@staticmethod
	def indexOf(a,x,fromIndex = None):
		len = python_lib_Builtin.len(a)
		l = None
		if (fromIndex is None):
			l = 0
		elif (fromIndex < 0):
			l = (len + fromIndex)
		else:
			l = fromIndex
		if (l < 0):
			l = 0
		_g = l
		while ((_g < len)):
			i = _g
			_g = (_g + 1)
			if (a[i] == x):
				return i
		return -1

	@staticmethod
	def lastIndexOf(a,x,fromIndex = None):
		len = python_lib_Builtin.len(a)
		l = None
		if (fromIndex is None):
			l = len
		elif (fromIndex < 0):
			l = ((len + fromIndex) + 1)
		else:
			l = (fromIndex + 1)
		if (l > len):
			l = len
		def _hx_local_1():
			nonlocal l
			l = (l - 1)
			return l
		while ((_hx_local_1() > -1)):
			if (a[l] == x):
				return l
		return -1

	@staticmethod
	def join(x,sep):
		return sep.join([python_Boot.toString1(x1,'') for x1 in x])

	@staticmethod
	def toString(x):
		return (("[" + HxOverrides.stringOrNull(python_internal_ArrayImpl.join(x,","))) + "]")

	@staticmethod
	def pop(x):
		if (python_lib_Builtin.len(x) == 0):
			return None
		else:
			return x.pop()

	@staticmethod
	def push(x,e):
		x.append(e)
		return python_internal_HxBuiltin.len(x)

	@staticmethod
	def unshift(x,e):
		return x.insert(0, e)

	@staticmethod
	def remove(x,e):
		try:
			x.remove(e)
			return True
		except Exception as _hx_e:
			_hx_e1 = _hx_e.val if isinstance(_hx_e, _HxException) else _hx_e
			e1 = _hx_e1
			return False

	@staticmethod
	def shift(x):
		if (python_lib_Builtin.len(x) == 0):
			return None
		return x.pop(0)

	@staticmethod
	def slice(x,pos,end = None):
		return x[pos:end]

	@staticmethod
	def sort(x,f):
		x.sort(key= python_lib_FuncTools.cmp_to_key(f))

	@staticmethod
	def splice(x,pos,len):
		if (pos < 0):
			pos = (python_lib_Builtin.len(x) + pos)
		if (pos < 0):
			pos = 0
		res = x[pos:(pos + len)]
		del x[pos:(pos + len)]
		return res

	@staticmethod
	def map(x,f):
		return python_internal_HxBuiltin.list(python_internal_HxBuiltin.map(f,x))

	@staticmethod
	def filter(x,f):
		return python_internal_HxBuiltin.list(python_internal_HxBuiltin.filter(f,x))

	@staticmethod
	def insert(a,pos,x):
		a.insert(pos, x)

	@staticmethod
	def reverse(a):
		a.reverse()

	@staticmethod
	def _get(x,idx):
		if ((idx > -1) and ((idx < python_lib_Builtin.len(x)))):
			return x[idx]
		else:
			return None

	@staticmethod
	def _set(x,idx,v):
		l = python_lib_Builtin.len(x)
		while ((l < idx)):
			x.append(None)
			l = (l + 1)
		if (l == idx):
			x.append(v)
		else:
			x[idx] = v
		return v

	@staticmethod
	def unsafeGet(x,idx):
		return x[idx]

	@staticmethod
	def unsafeSet(x,idx,val):
		x[idx] = val
		return val


@_hx_classes.registerClass("Bag", fields=["size"], methods=["getItem","getItemView"])
class Bag:	pass


@_hx_classes.registerClass("CellInfo", fields=["value","pretty_value","category","category_given_tr","separator","updated","conflicted","pvalue","lvalue","rvalue"], methods=["toString"])
class CellInfo:

	def __init__(self):
		self.value = None
		self.pretty_value = None
		self.category = None
		self.category_given_tr = None
		self.separator = None
		self.updated = None
		self.conflicted = None
		self.pvalue = None
		self.lvalue = None
		self.rvalue = None
		pass

	def toString(self):
		if (not self.updated):
			return self.value
		if (not self.conflicted):
			return ((HxOverrides.stringOrNull(self.lvalue) + "::") + HxOverrides.stringOrNull(self.rvalue))
		return ((((HxOverrides.stringOrNull(self.pvalue) + "||") + HxOverrides.stringOrNull(self.lvalue)) + "::") + HxOverrides.stringOrNull(self.rvalue))

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.value = None
		_hx_o.pretty_value = None
		_hx_o.category = None
		_hx_o.category_given_tr = None
		_hx_o.separator = None
		_hx_o.updated = None
		_hx_o.conflicted = None
		_hx_o.pvalue = None
		_hx_o.lvalue = None
		_hx_o.rvalue = None


@_hx_classes.registerClass("Change", fields=["change","parent","local","remote","mode"], methods=["getMode","toString"])
class Change:

	def __init__(self,txt = None):
		self.change = None
		self.parent = None
		self.local = None
		self.remote = None
		self.mode = None
		if (txt is not None):
			self.mode = ChangeType.NOTE_CHANGE
			self.change = txt
		else:
			self.mode = ChangeType.NO_CHANGE

	def getMode(self):
		return ("" + Std.string(self.mode))

	def toString(self):
		_g = self.mode
		if ((_g.index) == 0):
			return "no change"
		elif ((_g.index) == 2):
			return ((("local change: " + Std.string(self.remote)) + " -> ") + Std.string(self.local))
		elif ((_g.index) == 1):
			return ((("remote change: " + Std.string(self.local)) + " -> ") + Std.string(self.remote))
		elif ((_g.index) == 3):
			return ((((("conflicting change: " + Std.string(self.parent)) + " -> ") + Std.string(self.local)) + " / ") + Std.string(self.remote))
		elif ((_g.index) == 4):
			return ((((("same change: " + Std.string(self.parent)) + " -> ") + Std.string(self.local)) + " / ") + Std.string(self.remote))
		elif ((_g.index) == 5):
			return self.change
		else:
			pass

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.change = None
		_hx_o.parent = None
		_hx_o.local = None
		_hx_o.remote = None
		_hx_o.mode = None

@_hx_classes.registerEnum("ChangeType", ["NO_CHANGE","REMOTE_CHANGE","LOCAL_CHANGE","BOTH_CHANGE","SAME_CHANGE","NOTE_CHANGE"])
class ChangeType(Enum):
	def __init__(self, t, i, p):
		super(ChangeType,self).__init__(t, i, p)
ChangeType.NO_CHANGE = ChangeType("NO_CHANGE", 0, list())
ChangeType.REMOTE_CHANGE = ChangeType("REMOTE_CHANGE", 1, list())
ChangeType.LOCAL_CHANGE = ChangeType("LOCAL_CHANGE", 2, list())
ChangeType.BOTH_CHANGE = ChangeType("BOTH_CHANGE", 3, list())
ChangeType.SAME_CHANGE = ChangeType("SAME_CHANGE", 4, list())
ChangeType.NOTE_CHANGE = ChangeType("NOTE_CHANGE", 5, list())


@_hx_classes.registerAbstract("Class")
class Class:
	pass


@_hx_classes.registerClass("Compare", methods=["compare","compareStructured","compareTable","comparePrimitive"])
class Compare:

	def __init__(self):
		pass

	def compare(self,parent,local,remote,report):
		ws = Workspace()
		ws.parent = parent
		ws.local = local
		ws.remote = remote
		ws.report = report
		report.clear()
		if (((parent is None) or ((local is None))) or ((remote is None))):
			_this = report.changes
			x = Change("only 3-way comparison allowed right now")
			_this.append(x)
			return False
		if ((parent.hasStructure() or local.hasStructure()) or remote.hasStructure()):
			return self.compareStructured(ws)
		return self.comparePrimitive(ws)

	def compareStructured(self,ws):
		ws.tparent = ws.parent.getTable()
		ws.tlocal = ws.local.getTable()
		ws.tremote = ws.remote.getTable()
		if (((ws.tparent is None) or ((ws.tlocal is None))) or ((ws.tremote is None))):
			_this = ws.report.changes
			x = Change("structured comparisons that include non-tables are not available yet")
			_this.append(x)
			return False
		return self.compareTable(ws)

	def compareTable(self,ws):
		ws.p2l = TableComparisonState()
		ws.p2r = TableComparisonState()
		ws.p2l.a = ws.tparent
		ws.p2l.b = ws.tlocal
		ws.p2r.a = ws.tparent
		ws.p2r.b = ws.tremote
		cmp = CompareTable()
		cmp.attach(ws.p2l)
		cmp.attach(ws.p2r)
		c = Change()
		c.parent = ws.parent
		c.local = ws.local
		c.remote = ws.remote
		if (ws.p2l.is_equal and (not ws.p2r.is_equal)):
			c.mode = ChangeType.REMOTE_CHANGE
		elif ((not ws.p2l.is_equal) and ws.p2r.is_equal):
			c.mode = ChangeType.LOCAL_CHANGE
		elif ((not ws.p2l.is_equal) and (not ws.p2r.is_equal)):
			ws.l2r = TableComparisonState()
			ws.l2r.a = ws.tlocal
			ws.l2r.b = ws.tremote
			cmp.attach(ws.l2r)
			if ws.l2r.is_equal:
				c.mode = ChangeType.SAME_CHANGE
			else:
				c.mode = ChangeType.BOTH_CHANGE
		else:
			c.mode = ChangeType.NO_CHANGE
		if (c.mode != ChangeType.NO_CHANGE):
			_this = ws.report.changes
			_this.append(c)
		return True

	def comparePrimitive(self,ws):
		sparent = ws.parent.toString()
		slocal = ws.local.toString()
		sremote = ws.remote.toString()
		c = Change()
		c.parent = ws.parent
		c.local = ws.local
		c.remote = ws.remote
		if ((sparent == slocal) and ((sparent != sremote))):
			c.mode = ChangeType.REMOTE_CHANGE
		elif ((sparent == sremote) and ((sparent != slocal))):
			c.mode = ChangeType.LOCAL_CHANGE
		elif ((slocal == sremote) and ((sparent != slocal))):
			c.mode = ChangeType.SAME_CHANGE
		elif ((sparent != slocal) and ((sparent != sremote))):
			c.mode = ChangeType.BOTH_CHANGE
		else:
			c.mode = ChangeType.NO_CHANGE
		if (c.mode != ChangeType.NO_CHANGE):
			_this = ws.report.changes
			_this.append(c)
		return True

	@staticmethod
	def _hx_empty_init(_hx_o):		pass


@_hx_classes.registerClass("CompareFlags", fields=["ordered","show_unchanged","unchanged_context","always_show_order","never_show_order","show_unchanged_columns","unchanged_column_context","always_show_header","acts"], methods=["allowUpdate","allowInsert","allowDelete"])
class CompareFlags:

	def __init__(self):
		self.ordered = None
		self.show_unchanged = None
		self.unchanged_context = None
		self.always_show_order = None
		self.never_show_order = None
		self.show_unchanged_columns = None
		self.unchanged_column_context = None
		self.always_show_header = None
		self.acts = None
		self.ordered = True
		self.show_unchanged = False
		self.unchanged_context = 1
		self.always_show_order = False
		self.never_show_order = True
		self.show_unchanged_columns = False
		self.unchanged_column_context = 1
		self.always_show_header = True
		self.acts = None

	def allowUpdate(self):
		if (self.acts is None):
			return True
		return "update" in self.acts.h

	def allowInsert(self):
		if (self.acts is None):
			return True
		return "insert" in self.acts.h

	def allowDelete(self):
		if (self.acts is None):
			return True
		return "delete" in self.acts.h

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.ordered = None
		_hx_o.show_unchanged = None
		_hx_o.unchanged_context = None
		_hx_o.always_show_order = None
		_hx_o.never_show_order = None
		_hx_o.show_unchanged_columns = None
		_hx_o.unchanged_column_context = None
		_hx_o.always_show_header = None
		_hx_o.acts = None


@_hx_classes.registerClass("CompareTable", fields=["comp","indexes"], methods=["attach","align","getComparisonState","alignCore","alignCore2","alignColumns","testHasSameColumns","hasSameColumns2","testIsEqual","isEqual2","compareCore","storeIndexes","getIndexes"])
class CompareTable:

	def __init__(self):
		self.comp = None
		self.indexes = None
		pass

	def attach(self,comp):
		self.comp = comp
		more = self.compareCore()
		while ((more and comp.run_to_completion)):
			more = self.compareCore()
		return (not more)

	def align(self):
		alignment = Alignment()
		self.alignCore(alignment)
		return alignment

	def getComparisonState(self):
		return self.comp

	def alignCore(self,align):
		if (self.comp.p is None):
			self.alignCore2(align,self.comp.a,self.comp.b)
			return
		align.reference = Alignment()
		self.alignCore2(align,self.comp.p,self.comp.b)
		self.alignCore2(align.reference,self.comp.p,self.comp.a)
		align.meta.reference = align.reference.meta

	def alignCore2(self,align,a,b):
		if (align.meta is None):
			align.meta = Alignment()
		self.alignColumns(align.meta,a,b)
		column_order = align.meta.toOrderPruned(False)
		common_units = list()
		_g = 0
		_g1 = column_order.getList()
		while ((_g < python_lib_Builtin.len(_g1))):
			unit = (_g1[_g] if _g >= 0 and _g < python_lib_Builtin.len(_g1) else None)
			_g = (_g + 1)
			if (((unit.l >= 0) and ((unit.r >= 0))) and ((unit.p != -1))):
				common_units.append(unit)
		align.range(Reflect.field(a,"get_height")(),Reflect.field(b,"get_height")())
		align.tables(a,b)
		align.setRowlike(True)
		w = Reflect.field(a,"get_width")()
		ha = Reflect.field(a,"get_height")()
		hb = Reflect.field(b,"get_height")()
		av = a.getCellView()
		N = 5
		columns = list()
		if (python_lib_Builtin.len(common_units) > N):
			columns_eval = list()
			_g11 = 0
			_g2 = python_lib_Builtin.len(common_units)
			while ((_g11 < _g2)):
				i = _g11
				_g11 = (_g11 + 1)
				ct = 0
				mem = haxe_ds_StringMap()
				mem2 = haxe_ds_StringMap()
				ca = (common_units[i] if i >= 0 and i < python_lib_Builtin.len(common_units) else None).l
				cb = (common_units[i] if i >= 0 and i < python_lib_Builtin.len(common_units) else None).r
				_g21 = 0
				while ((_g21 < ha)):
					j = _g21
					_g21 = (_g21 + 1)
					key = av.toString(a.getCell(ca,j))
					if (not key in mem.h):
						mem.h[key] = 1
						ct = (ct + 1)
				_g22 = 0
				while ((_g22 < hb)):
					j1 = _g22
					_g22 = (_g22 + 1)
					key1 = av.toString(b.getCell(cb,j1))
					if (not key1 in mem2.h):
						mem2.h[key1] = 1
						ct = (ct + 1)
				columns_eval.append([i, ct])
			def _hx_local_3(a1,b1):
				if ((a1[1] if 1 < python_lib_Builtin.len(a1) else None) < (b1[1] if 1 < python_lib_Builtin.len(b1) else None)):
					return 1
				if ((a1[1] if 1 < python_lib_Builtin.len(a1) else None) > (b1[1] if 1 < python_lib_Builtin.len(b1) else None)):
					return -1
				return 0
			sorter = _hx_local_3
			columns_eval.sort(key= python_lib_FuncTools.cmp_to_key(sorter))
			def _hx_local_4(v):
				return (v[0] if 0 < python_lib_Builtin.len(v) else None)
			columns = Lambda.array(Lambda.map(columns_eval,_hx_local_4))
			columns = columns[0:N]
		else:
			_g12 = 0
			_g3 = python_lib_Builtin.len(common_units)
			while ((_g12 < _g3)):
				i1 = _g12
				_g12 = (_g12 + 1)
				columns.append(i1)
		top = None
		v1 = Math.pow(2,python_lib_Builtin.len(columns))
		top = Math.floor((v1 + 0.5))
		pending = haxe_ds_IntMap()
		_g4 = 0
		while ((_g4 < ha)):
			j2 = _g4
			_g4 = (_g4 + 1)
			pending.set(j2,j2)
		pending_ct = ha
		_g5 = 0
		while ((_g5 < top)):
			k = _g5
			_g5 = (_g5 + 1)
			if (k == 0):
				continue
			if (pending_ct == 0):
				break
			active_columns = list()
			kk = k
			at = 0
			while ((kk > 0)):
				if ((kk % 2) == 1):
					active_columns.append((columns[at] if at >= 0 and at < python_lib_Builtin.len(columns) else None))
				kk = (kk >> 1)
				at = (at + 1)
			index = IndexPair()
			_g23 = 0
			_g13 = python_lib_Builtin.len(active_columns)
			while ((_g23 < _g13)):
				k1 = _g23
				_g23 = (_g23 + 1)
				unit1 = python_internal_ArrayImpl._get(common_units, (active_columns[k1] if k1 >= 0 and k1 < python_lib_Builtin.len(active_columns) else None))
				index.addColumns(unit1.l,unit1.r)
				align.addIndexColumns(unit1)
			index.indexTables(a,b)
			h = Reflect.field(a,"get_height")()
			if (Reflect.field(b,"get_height")() > h):
				h = Reflect.field(b,"get_height")()
			if (h < 1):
				h = 1
			wide_top_freq = index.getTopFreq()
			ratio = wide_top_freq
			ratio = (ratio / ((h + 20)))
			if (ratio >= 0.1):
				continue
			if (self.indexes is not None):
				_this = self.indexes
				_this.append(index)
			fixed = list()
			_hx_local_8 = pending.keys()
			while (_hx_local_8.hasNext()):
				j3 = _hx_local_8.next()
				cross = index.queryLocal(j3)
				spot_a = cross.spot_a
				spot_b = cross.spot_b
				if ((spot_a != 1) or ((spot_b != 1))):
					continue
				fixed.append(j3)
				align.link(j3,python_internal_ArrayImpl._get(cross.item_b.lst, 0))
			_g24 = 0
			_g14 = python_lib_Builtin.len(fixed)
			while ((_g24 < _g14)):
				j4 = _g24
				_g24 = (_g24 + 1)
				pending.remove((fixed[j4] if j4 >= 0 and j4 < python_lib_Builtin.len(fixed) else None))
				pending_ct = (pending_ct - 1)
		align.link(0,0)

	def alignColumns(self,align,a,b):
		align.range(Reflect.field(a,"get_width")(),Reflect.field(b,"get_width")())
		align.tables(a,b)
		align.setRowlike(False)
		slop = 5
		va = a.getCellView()
		vb = b.getCellView()
		ra_best = 0
		rb_best = 0
		ct_best = -1
		ma_best = None
		mb_best = None
		ra_header = 0
		rb_header = 0
		ra_uniques = 0
		rb_uniques = 0
		_g = 0
		while ((_g < slop)):
			ra = _g
			_g = (_g + 1)
			if (ra >= Reflect.field(a,"get_height")()):
				break
			_g1 = 0
			while ((_g1 < slop)):
				rb = _g1
				_g1 = (_g1 + 1)
				if (rb >= Reflect.field(b,"get_height")()):
					break
				ma = haxe_ds_StringMap()
				mb = haxe_ds_StringMap()
				ct = 0
				uniques = 0
				_g3 = 0
				_g2 = Reflect.field(a,"get_width")()
				while ((_g3 < _g2)):
					ca = _g3
					_g3 = (_g3 + 1)
					key = va.toString(a.getCell(ca,ra))
					if key in ma.h:
						ma.h[key] = -1
						uniques = (uniques - 1)
					else:
						ma.h[key] = ca
						uniques = (uniques + 1)
				if (uniques > ra_uniques):
					ra_header = ra
					ra_uniques = uniques
				uniques = 0
				_g31 = 0
				_g21 = Reflect.field(b,"get_width")()
				while ((_g31 < _g21)):
					cb = _g31
					_g31 = (_g31 + 1)
					key1 = vb.toString(b.getCell(cb,rb))
					if key1 in mb.h:
						mb.h[key1] = -1
						uniques = (uniques - 1)
					else:
						mb.h[key1] = cb
						uniques = (uniques + 1)
				if (uniques > rb_uniques):
					rb_header = rb
					rb_uniques = uniques
				_hx_local_5 = ma.keys()
				while (_hx_local_5.hasNext()):
					key2 = _hx_local_5.next()
					i0 = ma.h.get(key2,None)
					i1 = mb.h.get(key2,None)
					if (i1 is not None):
						if ((i1 >= 0) and ((i0 >= 0))):
							ct = (ct + 1)
				if (ct > ct_best):
					ct_best = ct
					ma_best = ma
					mb_best = mb
					ra_best = ra
					rb_best = rb
		if (ma_best is None):
			return
		_hx_local_6 = ma_best.keys()
		while (_hx_local_6.hasNext()):
			key3 = _hx_local_6.next()
			i01 = ma_best.h.get(key3,None)
			i11 = mb_best.h.get(key3,None)
			if ((i11 is not None) and ((i01 is not None))):
				align.link(i01,i11)
		align.headers(ra_header,rb_header)

	def testHasSameColumns(self):
		p = self.comp.p
		a = self.comp.a
		b = self.comp.b
		eq = self.hasSameColumns2(a,b)
		if (eq and ((p is not None))):
			eq = self.hasSameColumns2(p,a)
		self.comp.has_same_columns = eq
		self.comp.has_same_columns_known = True
		return True

	def hasSameColumns2(self,a,b):
		if (Reflect.field(a,"get_width")() != Reflect.field(b,"get_width")()):
			return False
		if ((Reflect.field(a,"get_height")() == 0) or ((Reflect.field(b,"get_height")() == 0))):
			return True
		av = a.getCellView()
		_g1 = 0
		_g = Reflect.field(a,"get_width")()
		while ((_g1 < _g)):
			i = _g1
			_g1 = (_g1 + 1)
			_g3 = (i + 1)
			_g2 = Reflect.field(a,"get_width")()
			while ((_g3 < _g2)):
				j = _g3
				_g3 = (_g3 + 1)
				if av.equals(a.getCell(i,0),a.getCell(j,0)):
					return False
			if (not av.equals(a.getCell(i,0),b.getCell(i,0))):
				return False
		return True

	def testIsEqual(self):
		p = self.comp.p
		a = self.comp.a
		b = self.comp.b
		eq = self.isEqual2(a,b)
		if (eq and ((p is not None))):
			eq = self.isEqual2(p,a)
		self.comp.is_equal = eq
		self.comp.is_equal_known = True
		return True

	def isEqual2(self,a,b):
		if ((Reflect.field(a,"get_width")() != Reflect.field(b,"get_width")()) or ((Reflect.field(a,"get_height")() != Reflect.field(b,"get_height")()))):
			return False
		av = a.getCellView()
		_g1 = 0
		_g = Reflect.field(a,"get_height")()
		while ((_g1 < _g)):
			i = _g1
			_g1 = (_g1 + 1)
			_g3 = 0
			_g2 = Reflect.field(a,"get_width")()
			while ((_g3 < _g2)):
				j = _g3
				_g3 = (_g3 + 1)
				if (not av.equals(a.getCell(j,i),b.getCell(j,i))):
					return False
		return True

	def compareCore(self):
		if self.comp.completed:
			return False
		if (not self.comp.is_equal_known):
			return self.testIsEqual()
		if (not self.comp.has_same_columns_known):
			return self.testHasSameColumns()
		self.comp.completed = True
		return False

	def storeIndexes(self):
		self.indexes = list()

	def getIndexes(self):
		return self.indexes

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.comp = None
		_hx_o.indexes = None


@_hx_classes.registerClass("Coopy", fields=["format_preference","io","mv"], methods=["saveTable","saveText","loadTable"], statics=["compareTables","compareTables3","randomTests","cellFor","jsonToTable","coopyhx","main","show","jsonify"])
class Coopy:

	def __init__(self):
		self.format_preference = None
		self.io = None
		self.mv = None
		pass

	def saveTable(self,name,t):
		txt = ""
		if (self.format_preference != "json"):
			csv = Csv()
			txt = csv.renderTable(t)
		else:
			value = Coopy.jsonify(t)
			txt = haxe_format_JsonPrinter._hx_print(value,None,None)
		return self.saveText(name,txt)

	def saveText(self,name,txt):
		if (name != "-"):
			self.io.saveContent(name,txt)
		else:
			self.io.writeStdout(txt)
		return True

	def loadTable(self,name):
		txt = self.io.getContent(name)
		try:
			json = python_lib_Json.loads(txt,None,None,python_Lib.dictToAnon)
			self.format_preference = "json"
			t = Coopy.jsonToTable(json)
			if (t is None):
				raise _HxException("JSON failed")
			return t
		except Exception as _hx_e:
			_hx_e1 = _hx_e.val if isinstance(_hx_e, _HxException) else _hx_e
			e = _hx_e1
			csv = Csv()
			self.format_preference = "csv"
			data = csv.parseTable(txt)
			h = python_lib_Builtin.len(data)
			w = 0
			if (h > 0):
				w = python_lib_Builtin.len((data[0] if 0 < python_lib_Builtin.len(data) else None))
			output = SimpleTable(w, h)
			_g = 0
			while ((_g < h)):
				i = _g
				_g = (_g + 1)
				_g1 = 0
				while ((_g1 < w)):
					j = _g1
					_g1 = (_g1 + 1)
					val = python_internal_ArrayImpl._get((data[i] if i >= 0 and i < python_lib_Builtin.len(data) else None), j)
					output.setCell(j,i,Coopy.cellFor(val))
			if (output is not None):
				output.trimBlank()
			return output

	@staticmethod
	def compareTables(local,remote):
		ct = CompareTable()
		comp = TableComparisonState()
		comp.a = local
		comp.b = remote
		ct.attach(comp)
		return ct

	@staticmethod
	def compareTables3(parent,local,remote):
		ct = CompareTable()
		comp = TableComparisonState()
		comp.p = parent
		comp.a = local
		comp.b = remote
		ct.attach(comp)
		return ct

	@staticmethod
	def randomTests():
		st = SimpleTable(15, 6)
		tab = st
		haxe_Log.trace(((("table size is " + Std.string(Reflect.field(tab,"get_width")())) + "x") + Std.string(Reflect.field(tab,"get_height")())),_hx_AnonObject({'fileName': "Coopy.hx", 'lineNumber': 42, 'className': "Coopy", 'methodName': "randomTests"}))
		tab.setCell(3,4,SimpleCell(33))
		haxe_Log.trace(("element is " + Std.string(tab.getCell(3,4))),_hx_AnonObject({'fileName': "Coopy.hx", 'lineNumber': 44, 'className': "Coopy", 'methodName': "randomTests"}))
		compare = Compare()
		d1 = ViewedDatum.getSimpleView(SimpleCell(10))
		d2 = ViewedDatum.getSimpleView(SimpleCell(10))
		d3 = ViewedDatum.getSimpleView(SimpleCell(20))
		report = Report()
		compare.compare(d1,d2,d3,report)
		haxe_Log.trace(("report is " + Std.string(report)),_hx_AnonObject({'fileName': "Coopy.hx", 'lineNumber': 52, 'className': "Coopy", 'methodName': "randomTests"}))
		d2 = ViewedDatum.getSimpleView(SimpleCell(50))
		report.clear()
		compare.compare(d1,d2,d3,report)
		haxe_Log.trace(("report is " + Std.string(report)),_hx_AnonObject({'fileName': "Coopy.hx", 'lineNumber': 56, 'className': "Coopy", 'methodName': "randomTests"}))
		d2 = ViewedDatum.getSimpleView(SimpleCell(20))
		report.clear()
		compare.compare(d1,d2,d3,report)
		haxe_Log.trace(("report is " + Std.string(report)),_hx_AnonObject({'fileName': "Coopy.hx", 'lineNumber': 60, 'className': "Coopy", 'methodName': "randomTests"}))
		d1 = ViewedDatum.getSimpleView(SimpleCell(20))
		report.clear()
		compare.compare(d1,d2,d3,report)
		haxe_Log.trace(("report is " + Std.string(report)),_hx_AnonObject({'fileName': "Coopy.hx", 'lineNumber': 64, 'className': "Coopy", 'methodName': "randomTests"}))
		tv = TableView()
		comp = TableComparisonState()
		ct = CompareTable()
		comp.a = st
		comp.b = st
		ct.attach(comp)
		haxe_Log.trace("comparing tables",_hx_AnonObject({'fileName': "Coopy.hx", 'lineNumber': 74, 'className': "Coopy", 'methodName': "randomTests"}))
		t1 = SimpleTable(3, 2)
		t2 = SimpleTable(3, 2)
		t3 = SimpleTable(3, 2)
		dt1 = ViewedDatum(t1, TableView())
		dt2 = ViewedDatum(t2, TableView())
		dt3 = ViewedDatum(t3, TableView())
		compare.compare(dt1,dt2,dt3,report)
		haxe_Log.trace(("report is " + Std.string(report)),_hx_AnonObject({'fileName': "Coopy.hx", 'lineNumber': 82, 'className': "Coopy", 'methodName': "randomTests"}))
		t3.setCell(1,1,SimpleCell("hello"))
		compare.compare(dt1,dt2,dt3,report)
		haxe_Log.trace(("report is " + Std.string(report)),_hx_AnonObject({'fileName': "Coopy.hx", 'lineNumber': 85, 'className': "Coopy", 'methodName': "randomTests"}))
		t1.setCell(1,1,SimpleCell("hello"))
		compare.compare(dt1,dt2,dt3,report)
		haxe_Log.trace(("report is " + Std.string(report)),_hx_AnonObject({'fileName': "Coopy.hx", 'lineNumber': 88, 'className': "Coopy", 'methodName': "randomTests"}))
		v = Viterbi()
		td = TableDiff(None, None)
		idx = Index()
		dr = DiffRender()
		cf = CompareFlags()
		hp = HighlightPatch(None, None)
		csv = Csv()
		tm = TableModifier(None)
		return 0

	@staticmethod
	def cellFor(x):
		if (x is None):
			return None
		return SimpleCell(x)

	@staticmethod
	def jsonToTable(json):
		output = None
		_g = 0
		_g1 = python_Boot.fields(json)
		while ((_g < python_lib_Builtin.len(_g1))):
			name = (_g1[_g] if _g >= 0 and _g < python_lib_Builtin.len(_g1) else None)
			_g = (_g + 1)
			t = Reflect.field(json,name)
			columns = Reflect.field(t,"columns")
			if (columns is None):
				continue
			rows = Reflect.field(t,"rows")
			if (rows is None):
				continue
			output = SimpleTable(python_lib_Builtin.len(columns), python_lib_Builtin.len(rows))
			has_hash = False
			has_hash_known = False
			_g3 = 0
			_g2 = python_lib_Builtin.len(rows)
			while ((_g3 < _g2)):
				i = _g3
				_g3 = (_g3 + 1)
				row = (rows[i] if i >= 0 and i < python_lib_Builtin.len(rows) else None)
				if (not has_hash_known):
					if (python_lib_Builtin.len(python_Boot.fields(row)) == python_lib_Builtin.len(columns)):
						has_hash = True
					has_hash_known = True
				if (not has_hash):
					lst = row
					_g5 = 0
					_g4 = python_lib_Builtin.len(columns)
					while ((_g5 < _g4)):
						j = _g5
						_g5 = (_g5 + 1)
						val = (lst[j] if j >= 0 and j < python_lib_Builtin.len(lst) else None)
						output.setCell(j,i,Coopy.cellFor(val))
				else:
					_g51 = 0
					_g41 = python_lib_Builtin.len(columns)
					while ((_g51 < _g41)):
						j1 = _g51
						_g51 = (_g51 + 1)
						val1 = Reflect.field(row,(columns[j1] if j1 >= 0 and j1 < python_lib_Builtin.len(columns) else None))
						output.setCell(j1,i,Coopy.cellFor(val1))
		if (output is not None):
			output.trimBlank()
		return output

	@staticmethod
	def coopyhx(io):
		args = io.args()
		if ((args[0] if 0 < python_lib_Builtin.len(args) else None) == "--test"):
			return Coopy.randomTests()
		more = True
		output = None
		css_output = None
		fragment = False
		pretty = True
		flags = CompareFlags()
		flags.always_show_header = True
		while (more):
			more = False
			_g1 = 0
			_g = python_lib_Builtin.len(args)
			while ((_g1 < _g)):
				i = _g1
				_g1 = (_g1 + 1)
				tag = (args[i] if i >= 0 and i < python_lib_Builtin.len(args) else None)
				if (tag == "--output"):
					more = True
					output = python_internal_ArrayImpl._get(args, (i + 1))
					pos = i
					if (pos < 0):
						pos = (python_lib_Builtin.len(args) + pos)
					if (pos < 0):
						pos = 0
					res = args[pos:(pos + 2)]
					del args[pos:(pos + 2)]
					res
					break
				elif (tag == "--css"):
					more = True
					fragment = True
					css_output = python_internal_ArrayImpl._get(args, (i + 1))
					pos1 = i
					if (pos1 < 0):
						pos1 = (python_lib_Builtin.len(args) + pos1)
					if (pos1 < 0):
						pos1 = 0
					res1 = args[pos1:(pos1 + 2)]
					del args[pos1:(pos1 + 2)]
					res1
					break
				elif (tag == "--fragment"):
					more = True
					fragment = True
					pos2 = i
					if (pos2 < 0):
						pos2 = (python_lib_Builtin.len(args) + pos2)
					if (pos2 < 0):
						pos2 = 0
					res2 = args[pos2:(pos2 + 1)]
					del args[pos2:(pos2 + 1)]
					res2
					break
				elif (tag == "--plain"):
					more = True
					pretty = False
					pos3 = i
					if (pos3 < 0):
						pos3 = (python_lib_Builtin.len(args) + pos3)
					if (pos3 < 0):
						pos3 = 0
					res3 = args[pos3:(pos3 + 1)]
					del args[pos3:(pos3 + 1)]
					res3
					break
				elif (tag == "--all"):
					more = True
					flags.show_unchanged = True
					pos4 = i
					if (pos4 < 0):
						pos4 = (python_lib_Builtin.len(args) + pos4)
					if (pos4 < 0):
						pos4 = 0
					res4 = args[pos4:(pos4 + 1)]
					del args[pos4:(pos4 + 1)]
					res4
					break
				elif (tag == "--act"):
					more = True
					if (flags.acts is None):
						flags.acts = haxe_ds_StringMap()
					flags.acts.h[python_internal_ArrayImpl._get(args, (i + 1))] = True
					True
					pos5 = i
					if (pos5 < 0):
						pos5 = (python_lib_Builtin.len(args) + pos5)
					if (pos5 < 0):
						pos5 = 0
					res5 = args[pos5:(pos5 + 2)]
					del args[pos5:(pos5 + 2)]
					res5
					break
				elif (tag == "--context"):
					more = True
					context = Std.parseInt(python_internal_ArrayImpl._get(args, (i + 1)))
					if (context >= 0):
						flags.unchanged_context = context
					pos6 = i
					if (pos6 < 0):
						pos6 = (python_lib_Builtin.len(args) + pos6)
					if (pos6 < 0):
						pos6 = 0
					res6 = args[pos6:(pos6 + 2)]
					del args[pos6:(pos6 + 2)]
					res6
					break
		cmd = (args[0] if 0 < python_lib_Builtin.len(args) else None)
		if (python_lib_Builtin.len(args) < 2):
			io.writeStderr("daff can produce and apply tabular diffs.\n")
			io.writeStderr("Call as:\n")
			io.writeStderr("  daff [--output OUTPUT.csv] a.csv b.csv\n")
			io.writeStderr("  daff [--output OUTPUT.csv] parent.csv a.csv b.csv\n")
			io.writeStderr("  daff [--output OUTPUT.jsonbook] a.jsonbook b.jsonbook\n")
			io.writeStderr("  daff patch [--output OUTPUT.csv] source.csv patch.csv\n")
			io.writeStderr("  daff trim [--output OUTPUT.csv] source.csv\n")
			io.writeStderr("  daff render [--output OUTPUT.html] diff.csv\n")
			io.writeStderr("\n")
			io.writeStderr("If you need more control, here is the full list of flags:\n")
			io.writeStderr("  daff diff [--output OUTPUT.csv] [--context NUM] [--all] [--act ACT] a.csv b.csv\n")
			io.writeStderr("     --context NUM: show NUM rows of context\n")
			io.writeStderr("     --all:         do not prune unchanged rows\n")
			io.writeStderr("     --act ACT:     show only a certain kind of change (update, insert, delete)\n")
			io.writeStderr("\n")
			io.writeStderr("  daff render [--output OUTPUT.html] [--css CSS.css] [--fragment] [--plain] diff.csv\n")
			io.writeStderr("     --css CSS.css: generate a suitable css file to go with the html\n")
			io.writeStderr("     --fragment:    generate just a html fragment rather than a page\n")
			io.writeStderr("     --plain:       do not use fancy utf8 characters to make arrows prettier\n")
			return 1
		if (output is None):
			output = "-"
		cmd1 = (args[0] if 0 < python_lib_Builtin.len(args) else None)
		offset = 1
		if (not Lambda.has(["diff", "patch", "trim", "render"],cmd1)):
			if ((cmd1.find(".") != -1) or ((cmd1.find("--") == 0))):
				cmd1 = "diff"
				offset = 0
		tool = Coopy()
		tool.io = io
		parent = None
		if ((python_lib_Builtin.len(args) - offset) >= 3):
			parent = tool.loadTable((args[offset] if offset >= 0 and offset < python_lib_Builtin.len(args) else None))
			offset = (offset + 1)
		a = tool.loadTable((args[offset] if offset >= 0 and offset < python_lib_Builtin.len(args) else None))
		b = None
		if ((python_lib_Builtin.len(args) - offset) >= 2):
			b = tool.loadTable(python_internal_ArrayImpl._get(args, (1 + offset)))
		if (cmd1 == "diff"):
			ct = Coopy.compareTables3(parent,a,b)
			align = ct.align()
			td = TableDiff(align, flags)
			o = SimpleTable(0, 0)
			td.hilite(o)
			tool.saveTable(output,o)
		elif (cmd1 == "patch"):
			patcher = HighlightPatch(a, b)
			patcher.apply()
			tool.saveTable(output,a)
		elif (cmd1 == "trim"):
			tool.saveTable(output,a)
		elif (cmd1 == "render"):
			renderer = DiffRender()
			renderer.usePrettyArrows(pretty)
			renderer.render(a)
			if (not fragment):
				renderer.completeHtml()
			tool.saveText(output,renderer.html())
			if (css_output is not None):
				tool.saveText(css_output,renderer.sampleCss())
		return 0

	@staticmethod
	def main():
		io = TableIO()
		return Coopy.coopyhx(io)

	@staticmethod
	def show(t):
		w = Reflect.field(t,"get_width")()
		h = Reflect.field(t,"get_height")()
		txt = ""
		_g = 0
		while ((_g < h)):
			y = _g
			_g = (_g + 1)
			_g1 = 0
			while ((_g1 < w)):
				x = _g1
				_g1 = (_g1 + 1)
				txt = (HxOverrides.stringOrNull(txt) + Std.string(t.getCell(x,y)))
				txt = (HxOverrides.stringOrNull(txt) + " ")
			txt = (HxOverrides.stringOrNull(txt) + "\n")
		haxe_Log.trace(txt,_hx_AnonObject({'fileName': "Coopy.hx", 'lineNumber': 355, 'className': "Coopy", 'methodName': "show"}))

	@staticmethod
	def jsonify(t):
		workbook = haxe_ds_StringMap()
		sheet = list()
		w = Reflect.field(t,"get_width")()
		h = Reflect.field(t,"get_height")()
		txt = ""
		_g = 0
		while ((_g < h)):
			y = _g
			_g = (_g + 1)
			row = list()
			_g1 = 0
			while ((_g1 < w)):
				x = _g1
				_g1 = (_g1 + 1)
				v = t.getCell(x,y)
				if (v is not None):
					x1 = v.toString()
					row.append(x1)
				else:
					row.append(None)
			sheet.append(row)
		workbook.h["sheet"] = sheet
		return workbook

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.format_preference = None
		_hx_o.io = None
		_hx_o.mv = None


@_hx_classes.registerClass("CrossMatch", fields=["spot_a","spot_b","item_a","item_b"])
class CrossMatch:

	def __init__(self):
		self.spot_a = None
		self.spot_b = None
		self.item_a = None
		self.item_b = None
		pass

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.spot_a = None
		_hx_o.spot_b = None
		_hx_o.item_a = None
		_hx_o.item_b = None


@_hx_classes.registerClass("Csv", fields=["cursor","row_ended","has_structure"], methods=["renderTable","renderCell","parseTable","parseCell","parseSingleCell"])
class Csv:

	def __init__(self):
		self.cursor = None
		self.row_ended = None
		self.has_structure = None
		self.cursor = 0
		self.row_ended = False

	def renderTable(self,t):
		result = ""
		w = Reflect.field(t,"get_width")()
		h = Reflect.field(t,"get_height")()
		txt = ""
		v = t.getCellView()
		_g = 0
		while ((_g < h)):
			y = _g
			_g = (_g + 1)
			_g1 = 0
			while ((_g1 < w)):
				x = _g1
				_g1 = (_g1 + 1)
				if (x > 0):
					txt = (HxOverrides.stringOrNull(txt) + ",")
				txt = (HxOverrides.stringOrNull(txt) + HxOverrides.stringOrNull(self.renderCell(v,t.getCell(x,y))))
			txt = (HxOverrides.stringOrNull(txt) + "\r\n")
		return txt

	def renderCell(self,v,d):
		if (d is None):
			return "NULL"
		if v.equals(d,None):
			return "NULL"
		str = v.toString(d)
		delim = ","
		need_quote = False
		_g1 = 0
		_g = python_lib_Builtin.len(str)
		while ((_g1 < _g)):
			i = _g1
			_g1 = (_g1 + 1)
			ch = None
			if ((i < 0) or ((i >= python_lib_Builtin.len(str)))):
				ch = ""
			else:
				ch = str[i]
			if (((((((ch == "\"") or ((ch == "'"))) or ((ch == delim))) or ((ch == "\r"))) or ((ch == "\n"))) or ((ch == "\t"))) or ((ch == " "))):
				need_quote = True
				break
		result = ""
		if need_quote:
			result = (HxOverrides.stringOrNull(result) + "\"")
		line_buf = ""
		_g11 = 0
		_g2 = python_lib_Builtin.len(str)
		while ((_g11 < _g2)):
			i1 = _g11
			_g11 = (_g11 + 1)
			ch1 = None
			if ((i1 < 0) or ((i1 >= python_lib_Builtin.len(str)))):
				ch1 = ""
			else:
				ch1 = str[i1]
			if (ch1 == "\""):
				result = (HxOverrides.stringOrNull(result) + "\"")
			if ((ch1 != "\r") and ((ch1 != "\n"))):
				if (python_lib_Builtin.len(line_buf) > 0):
					result = (HxOverrides.stringOrNull(result) + HxOverrides.stringOrNull(line_buf))
					line_buf = ""
				result = (HxOverrides.stringOrNull(result) + HxOverrides.stringOrNull(ch1))
			else:
				line_buf = (HxOverrides.stringOrNull(line_buf) + HxOverrides.stringOrNull(ch1))
		if need_quote:
			result = (HxOverrides.stringOrNull(result) + "\"")
		return result

	def parseTable(self,txt):
		self.cursor = 0
		self.row_ended = False
		self.has_structure = True
		result = list()
		row = list()
		while ((self.cursor < python_lib_Builtin.len(txt))):
			cell = self.parseCell(txt)
			row.append(cell)
			if self.row_ended:
				result.append(row)
				row = list()
			_hx_local_0 = self
			_hx_local_1 = _hx_local_0.cursor
			_hx_local_0.cursor = (_hx_local_1 + 1)
			_hx_local_1
		return result

	def parseCell(self,txt):
		if (txt is None):
			return None
		self.row_ended = False
		first_non_underscore = python_lib_Builtin.len(txt)
		last_processed = 0
		quoting = False
		quote = 0
		result = ""
		start = self.cursor
		_g1 = self.cursor
		_g = python_lib_Builtin.len(txt)
		while ((_g1 < _g)):
			i = _g1
			_g1 = (_g1 + 1)
			ch = HxString.charCodeAt(txt,i)
			last_processed = i
			if ((ch != 95) and ((i < first_non_underscore))):
				first_non_underscore = i
			if self.has_structure:
				if (not quoting):
					if (ch == 44):
						break
					if ((ch == 13) or ((ch == 10))):
						ch2 = HxString.charCodeAt(txt,(i + 1))
						if (ch2 is not None):
							if (ch2 != ch):
								if ((ch2 == 13) or ((ch2 == 10))):
									last_processed = (last_processed + 1)
						self.row_ended = True
						break
					if ((ch == 34) or ((ch == 39))):
						if (i == self.cursor):
							quoting = True
							quote = ch
							if (i != start):
								c = ch
								result = (HxOverrides.stringOrNull(result) + Std.string("".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c]))))
							continue
						elif (ch == quote):
							quoting = True
					c1 = ch
					result = (HxOverrides.stringOrNull(result) + Std.string("".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c1]))))
					continue
				if (ch == quote):
					quoting = False
					continue
			c2 = ch
			result = (HxOverrides.stringOrNull(result) + Std.string("".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c2]))))
		self.cursor = last_processed
		if (quote == 0):
			if (result == "NULL"):
				return None
			if (first_non_underscore > start):
				_hx_del = (first_non_underscore - start)
				if (HxString.substr(result,_hx_del,None) == "NULL"):
					return HxString.substr(result,1,None)
		return result

	def parseSingleCell(self,txt):
		self.cursor = 0
		self.row_ended = False
		self.has_structure = False
		return self.parseCell(txt)

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.cursor = None
		_hx_o.row_ended = None
		_hx_o.has_structure = None


@_hx_classes.registerClass("Date", fields=["date"], methods=["toString"])
class Date:

	def toString(self):
		m = ((self.date.month - 1) + 1)
		d = self.date.day
		h = self.date.hour
		mi = self.date.minute
		s = self.date.second
		return ((((((((((Std.string(self.date.year) + "-") + HxOverrides.stringOrNull(((("0" + Std.string(m)) if ((m < 10)) else ("" + Std.string(m)))))) + "-") + HxOverrides.stringOrNull(((("0" + Std.string(d)) if ((d < 10)) else ("" + Std.string(d)))))) + " ") + HxOverrides.stringOrNull(((("0" + Std.string(h)) if ((h < 10)) else ("" + Std.string(h)))))) + ":") + HxOverrides.stringOrNull(((("0" + Std.string(mi)) if ((mi < 10)) else ("" + Std.string(mi)))))) + ":") + HxOverrides.stringOrNull(((("0" + Std.string(s)) if ((s < 10)) else ("" + Std.string(s))))))

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.date = None


@_hx_classes.registerClass("DiffRender", fields=["text_to_insert","td_open","td_close","open","pretty_arrows"], methods=["usePrettyArrows","insert","beginTable","beginRow","insertCell","endRow","endTable","html","toString","render","sampleCss","completeHtml"], statics=["examineCell","markSpaces","renderCell"])
class DiffRender:

	def __init__(self):
		self.text_to_insert = None
		self.td_open = None
		self.td_close = None
		self.open = None
		self.pretty_arrows = None
		self.text_to_insert = list()
		self.open = False
		self.pretty_arrows = True

	def usePrettyArrows(self,flag):
		self.pretty_arrows = flag

	def insert(self,str):
		_this = self.text_to_insert
		_this.append(str)

	def beginTable(self):
		self.insert("<table>\n")

	def beginRow(self,mode):
		self.td_open = "<td"
		self.td_close = "</td>"
		row_class = ""
		if (mode == "header"):
			self.td_open = "<th"
			self.td_close = "</th>"
		else:
			row_class = mode
		tr = "<tr>"
		if (row_class != ""):
			tr = (("<tr class=\"" + HxOverrides.stringOrNull(row_class)) + "\">")
		self.insert(tr)

	def insertCell(self,txt,mode):
		cell_decorate = ""
		if (mode != ""):
			cell_decorate = ((" class=\"" + HxOverrides.stringOrNull(mode)) + "\"")
		self.insert(((HxOverrides.stringOrNull(self.td_open) + HxOverrides.stringOrNull(cell_decorate)) + ">"))
		self.insert(txt)
		self.insert(self.td_close)

	def endRow(self):
		self.insert("</tr>\n")

	def endTable(self):
		self.insert("</table>\n")

	def html(self):
		return "".join([python_Boot.toString1(x1,'') for x1 in self.text_to_insert])

	def toString(self):
		return self.html()

	def render(self,rows):
		if ((Reflect.field(rows,"get_width")() == 0) or ((Reflect.field(rows,"get_height")() == 0))):
			return
		render = self
		render.beginTable()
		change_row = -1
		tt = TableText(rows)
		cell = CellInfo()
		corner = tt.getCellText(0,0)
		off = None
		if (corner == "@:@"):
			off = 1
		else:
			off = 0
		if (off > 0):
			if ((Reflect.field(rows,"get_width")() <= 1) or ((Reflect.field(rows,"get_height")() <= 1))):
				return
		_g1 = 0
		_g = Reflect.field(rows,"get_height")()
		while ((_g1 < _g)):
			row = _g1
			_g1 = (_g1 + 1)
			open = False
			txt = tt.getCellText(off,row)
			if (txt is None):
				txt = ""
			DiffRender.examineCell(0,row,txt,"",txt,corner,cell)
			row_mode = cell.category
			if (row_mode == "spec"):
				change_row = row
			render.beginRow(row_mode)
			_g3 = 0
			_g2 = Reflect.field(rows,"get_width")()
			while ((_g3 < _g2)):
				c = _g3
				_g3 = (_g3 + 1)
				DiffRender.examineCell(c,row,tt.getCellText(c,row),(tt.getCellText(c,change_row) if ((change_row >= 0)) else ""),txt,corner,cell)
				render.insertCell((cell.pretty_value if (self.pretty_arrows) else cell.value),cell.category_given_tr)
			render.endRow()
		render.endTable()

	def sampleCss(self):
		return ".highlighter .add { \n  background-color: #7fff7f;\n}\n\n.highlighter .remove { \n  background-color: #ff7f7f;\n}\n\n.highlighter td.modify { \n  background-color: #7f7fff;\n}\n\n.highlighter td.conflict { \n  background-color: #f00;\n}\n\n.highlighter .spec { \n  background-color: #aaa;\n}\n\n.highlighter .move { \n  background-color: #ffa;\n}\n\n.highlighter .null { \n  color: #888;\n}\n\n.highlighter table { \n  border-collapse:collapse;\n}\n\n.highlighter td, .highlighter th {\n  border: 1px solid #2D4068;\n  padding: 3px 7px 2px;\n}\n\n.highlighter th, .highlighter .header { \n  background-color: #aaf;\n  font-weight: bold;\n  padding-bottom: 4px;\n  padding-top: 5px;\n  text-align:left;\n}\n\n.highlighter tr:first-child td {\n  border-top: 1px solid #2D4068;\n}\n\n.highlighter td:first-child { \n  border-left: 1px solid #2D4068;\n}\n\n.highlighter td {\n  empty-cells: show;\n}\n"

	def completeHtml(self):
		self.text_to_insert.insert(0, "<html>\n<meta charset='utf-8'>\n<head>\n<style TYPE='text/css'>\n")
		x = self.sampleCss()
		self.text_to_insert.insert(1, x)
		self.text_to_insert.insert(2, "</style>\n</head>\n<body>\n<div class='highlighter'>\n")
		_this = self.text_to_insert
		_this.append("</div>\n</body>\n</html>\n")

	@staticmethod
	def examineCell(x,y,value,vcol,vrow,vcorner,cell):
		cell.category = ""
		cell.category_given_tr = ""
		cell.separator = ""
		cell.conflicted = False
		cell.updated = False
		def _hx_local_1():
			def _hx_local_0():
				cell.rvalue = None
				return cell.rvalue
			cell.lvalue = _hx_local_0()
			return cell.lvalue
		cell.pvalue = _hx_local_1()
		cell.value = value
		if (cell.value is None):
			cell.value = ""
		cell.pretty_value = cell.value
		if (vrow is None):
			vrow = ""
		if (vcol is None):
			vcol = ""
		removed_column = False
		if (vrow == ":"):
			cell.category = "move"
		if (vcol.find("+++") >= 0):
			def _hx_local_2():
				cell.category = "add"
				return cell.category
			cell.category_given_tr = _hx_local_2()
		elif (vcol.find("---") >= 0):
			def _hx_local_3():
				cell.category = "remove"
				return cell.category
			cell.category_given_tr = _hx_local_3()
			removed_column = True
		if (vrow == "!"):
			cell.category = "spec"
		elif (vrow == "@@"):
			cell.category = "header"
		elif (vrow == "+++"):
			if (not removed_column):
				cell.category = "add"
		elif (vrow == "---"):
			cell.category = "remove"
		elif (vrow.find("->") >= 0):
			if (not removed_column):
				tokens = vrow.split("!")
				full = vrow
				part = (tokens[1] if 1 < python_lib_Builtin.len(tokens) else None)
				if (part is None):
					part = full
				def _hx_local_4():
					_this = cell.value
					return _this.find(part)
				if (_hx_local_4() >= 0):
					cat = "modify"
					div = part
					if (part != full):
						def _hx_local_5():
							_this1 = cell.value
							return _this1.find(full)
						if (_hx_local_5() >= 0):
							div = full
							cat = "conflict"
							cell.conflicted = True
					cell.updated = True
					cell.separator = div
					if (cell.pretty_value == div):
						tokens = ["", ""]
					else:
						_this2 = cell.pretty_value
						if (div == ""):
							tokens = python_internal_HxBuiltin.list(_this2)
						else:
							tokens = _this2.split(div)
					pretty_tokens = tokens
					if (python_lib_Builtin.len(tokens) >= 2):
						python_internal_ArrayImpl._set(pretty_tokens, 0, DiffRender.markSpaces((tokens[0] if 0 < python_lib_Builtin.len(tokens) else None),(tokens[1] if 1 < python_lib_Builtin.len(tokens) else None)))
						python_internal_ArrayImpl._set(pretty_tokens, 1, DiffRender.markSpaces((tokens[1] if 1 < python_lib_Builtin.len(tokens) else None),(tokens[0] if 0 < python_lib_Builtin.len(tokens) else None)))
					if (python_lib_Builtin.len(tokens) >= 3):
						ref = (pretty_tokens[0] if 0 < python_lib_Builtin.len(pretty_tokens) else None)
						python_internal_ArrayImpl._set(pretty_tokens, 0, DiffRender.markSpaces(ref,(tokens[2] if 2 < python_lib_Builtin.len(tokens) else None)))
						python_internal_ArrayImpl._set(pretty_tokens, 2, DiffRender.markSpaces((tokens[2] if 2 < python_lib_Builtin.len(tokens) else None),ref))
					sep = None
					c = 8594
					sep = "".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c]))
					cell.pretty_value = sep.join([python_Boot.toString1(x1,'') for x1 in pretty_tokens])
					def _hx_local_6():
						cell.category = cat
						return cell.category
					cell.category_given_tr = _hx_local_6()
					offset = None
					if cell.conflicted:
						offset = 1
					else:
						offset = 0
					cell.lvalue = (tokens[offset] if offset >= 0 and offset < python_lib_Builtin.len(tokens) else None)
					cell.rvalue = python_internal_ArrayImpl._get(tokens, (offset + 1))
					if cell.conflicted:
						cell.pvalue = (tokens[0] if 0 < python_lib_Builtin.len(tokens) else None)

	@staticmethod
	def markSpaces(sl,sr):
		if (sl == sr):
			return sl
		if ((sl is None) or ((sr is None))):
			return sl
		slc = StringTools.replace(sl," ","")
		src = StringTools.replace(sr," ","")
		if (slc != src):
			return sl
		slo = String("")
		il = 0
		ir = 0
		while ((il < python_lib_Builtin.len(sl))):
			cl = None
			if ((il < 0) or ((il >= python_lib_Builtin.len(sl)))):
				cl = ""
			else:
				cl = sl[il]
			cr = ""
			if (ir < python_lib_Builtin.len(sr)):
				if ((ir < 0) or ((ir >= python_lib_Builtin.len(sr)))):
					cr = ""
				else:
					cr = sr[ir]
			if (cl == cr):
				slo = (HxOverrides.stringOrNull(slo) + HxOverrides.stringOrNull(cl))
				il = (il + 1)
				ir = (ir + 1)
			elif (cr == " "):
				ir = (ir + 1)
			else:
				c = 9251
				slo = (HxOverrides.stringOrNull(slo) + Std.string("".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c]))))
				il = (il + 1)
		return slo

	@staticmethod
	def renderCell(tt,x,y):
		cell = CellInfo()
		corner = tt.getCellText(0,0)
		off = None
		if (corner == "@:@"):
			off = 1
		else:
			off = 0
		DiffRender.examineCell(x,y,tt.getCellText(x,y),tt.getCellText(x,off),tt.getCellText(off,y),corner,cell)
		return cell

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.text_to_insert = None
		_hx_o.td_open = None
		_hx_o.td_close = None
		_hx_o.open = None
		_hx_o.pretty_arrows = None


@_hx_classes.registerAbstract("EnumValue")
class EnumValue:
	pass


@_hx_classes.registerClass("Row", methods=["getRowString"])
class Row:	pass


@_hx_classes.registerClass("HighlightPatch", fields=["source","patch","view","csv","header","headerPre","headerPost","headerRename","headerMove","modifier","currentRow","payloadCol","payloadTop","mods","cmods","rowInfo","cellInfo","rcOffset","indexes","sourceInPatchCol","patchInSourceCol","patchInSourceRow","lastSourceRow","actions","rowPermutation","rowPermutationRev","colPermutation","colPermutationRev","haveDroppedColumns"], methods=["reset","apply","needSourceColumns","needSourceIndex","applyRow","getDatum","getString","applyMeta","applyHeader","lookUp","applyAction","checkAct","getPreString","getRowString","sortMods","processMods","computeOrdering","permuteRows","finishRows","permuteColumns","finishColumns"], interfaces=[Row])
class HighlightPatch:

	def __init__(self,source,patch):
		self.source = None
		self.patch = None
		self.view = None
		self.csv = None
		self.header = None
		self.headerPre = None
		self.headerPost = None
		self.headerRename = None
		self.headerMove = None
		self.modifier = None
		self.currentRow = None
		self.payloadCol = None
		self.payloadTop = None
		self.mods = None
		self.cmods = None
		self.rowInfo = None
		self.cellInfo = None
		self.rcOffset = None
		self.indexes = None
		self.sourceInPatchCol = None
		self.patchInSourceCol = None
		self.patchInSourceRow = None
		self.lastSourceRow = None
		self.actions = None
		self.rowPermutation = None
		self.rowPermutationRev = None
		self.colPermutation = None
		self.colPermutationRev = None
		self.haveDroppedColumns = None
		self.source = source
		self.patch = patch
		self.view = patch.getCellView()

	def reset(self):
		self.header = haxe_ds_IntMap()
		self.headerPre = haxe_ds_StringMap()
		self.headerPost = haxe_ds_StringMap()
		self.headerRename = haxe_ds_StringMap()
		self.headerMove = None
		self.modifier = haxe_ds_IntMap()
		self.mods = list()
		self.cmods = list()
		self.csv = Csv()
		self.rcOffset = 0
		self.currentRow = -1
		self.rowInfo = CellInfo()
		self.cellInfo = CellInfo()
		def _hx_local_0():
			self.patchInSourceCol = None
			return self.patchInSourceCol
		self.sourceInPatchCol = _hx_local_0()
		self.patchInSourceRow = haxe_ds_IntMap()
		self.indexes = None
		self.lastSourceRow = -1
		self.actions = list()
		self.rowPermutation = None
		self.rowPermutationRev = None
		self.colPermutation = None
		self.colPermutationRev = None
		self.haveDroppedColumns = False

	def apply(self):
		self.reset()
		if (Reflect.field(self.patch,"get_width")() < 2):
			return True
		if (Reflect.field(self.patch,"get_height")() < 1):
			return True
		self.payloadCol = (1 + self.rcOffset)
		self.payloadTop = Reflect.field(self.patch,"get_width")()
		corner = self.patch.getCellView().toString(self.patch.getCell(0,0))
		if (corner == "@:@"):
			self.rcOffset = 1
		else:
			self.rcOffset = 0
		_g1 = 0
		_g = Reflect.field(self.patch,"get_height")()
		while ((_g1 < _g)):
			r = _g1
			_g1 = (_g1 + 1)
			str = self.view.toString(self.patch.getCell(self.rcOffset,r))
			_this = self.actions
			_this.append((str if ((str is not None)) else ""))
		_g11 = 0
		_g2 = Reflect.field(self.patch,"get_height")()
		while ((_g11 < _g2)):
			r1 = _g11
			_g11 = (_g11 + 1)
			self.applyRow(r1)
		self.finishRows()
		self.finishColumns()
		return True

	def needSourceColumns(self):
		if (self.sourceInPatchCol is not None):
			return
		self.sourceInPatchCol = haxe_ds_IntMap()
		self.patchInSourceCol = haxe_ds_IntMap()
		av = self.source.getCellView()
		_g1 = 0
		_g = Reflect.field(self.source,"get_width")()
		while ((_g1 < _g)):
			i = _g1
			_g1 = (_g1 + 1)
			name = av.toString(self.source.getCell(i,0))
			at = self.headerPre.h.get(name,None)
			if (at is None):
				continue
			self.sourceInPatchCol.set(i,at)
			self.patchInSourceCol.set(at,i)

	def needSourceIndex(self):
		if (self.indexes is not None):
			return
		state = TableComparisonState()
		state.a = self.source
		state.b = self.source
		comp = CompareTable()
		comp.storeIndexes()
		comp.attach(state)
		comp.align()
		self.indexes = comp.getIndexes()
		self.needSourceColumns()

	def applyRow(self,r):
		self.currentRow = r
		code = (self.actions[r] if r >= 0 and r < python_lib_Builtin.len(self.actions) else None)
		if ((r == 0) and ((self.rcOffset > 0))):
			pass
		elif (code == "@@"):
			self.applyHeader()
			self.applyAction("@@")
		elif (code == "!"):
			self.applyMeta()
		elif (code == "+++"):
			self.applyAction(code)
		elif (code == "---"):
			self.applyAction(code)
		elif ((code == "+") or ((code == ":"))):
			self.applyAction(code)
		elif (code.find("->") >= 0):
			self.applyAction("->")
		else:
			self.lastSourceRow = -1

	def getDatum(self,c):
		return self.patch.getCell(c,self.currentRow)

	def getString(self,c):
		return self.view.toString(self.getDatum(c))

	def applyMeta(self):
		_g1 = self.payloadCol
		_g = self.payloadTop
		while ((_g1 < _g)):
			i = _g1
			_g1 = (_g1 + 1)
			name = self.getString(i)
			if (name == ""):
				continue
			self.modifier.set(i,name)

	def applyHeader(self):
		_g1 = self.payloadCol
		_g = self.payloadTop
		while ((_g1 < _g)):
			i = _g1
			_g1 = (_g1 + 1)
			name = self.getString(i)
			if (name == "..."):
				self.modifier.set(i,"...")
				self.haveDroppedColumns = True
				continue
			mod = self.modifier.h.get(i,None)
			move = False
			if (mod is not None):
				if (HxString.charCodeAt(mod,0) == 58):
					move = True
					mod = HxString.substr(mod,1,python_lib_Builtin.len(mod))
			self.header.set(i,name)
			if (mod is not None):
				if (HxString.charCodeAt(mod,0) == 40):
					prev_name = HxString.substr(mod,1,(python_lib_Builtin.len(mod) - 2))
					self.headerPre.h[prev_name] = i
					self.headerPost.h[name] = i
					self.headerRename.h[prev_name] = name
					continue
			if (mod != "+++"):
				self.headerPre.h[name] = i
			if (mod != "---"):
				self.headerPost.h[name] = i
			if move:
				if (self.headerMove is None):
					self.headerMove = haxe_ds_StringMap()
				self.headerMove.h[name] = 1
		if (Reflect.field(self.source,"get_height")() == 0):
			self.applyAction("+++")

	def lookUp(self,_hx_del = 0):
		if (_hx_del is None):
			_hx_del = 0
		at = self.patchInSourceRow.h.get((self.currentRow + _hx_del),None)
		if (at is not None):
			return at
		result = -1
		_hx_local_0 = self
		_hx_local_1 = _hx_local_0.currentRow
		_hx_local_0.currentRow = (_hx_local_1 + _hx_del)
		_hx_local_0.currentRow
		if ((self.currentRow >= 0) and ((self.currentRow < Reflect.field(self.patch,"get_height")()))):
			_g = 0
			_g1 = self.indexes
			while ((_g < python_lib_Builtin.len(_g1))):
				idx = (_g1[_g] if _g >= 0 and _g < python_lib_Builtin.len(_g1) else None)
				_g = (_g + 1)
				match = idx.queryByContent(self)
				if (match.spot_a != 1):
					continue
				result = python_internal_ArrayImpl._get(match.item_a.lst, 0)
				break
		self.patchInSourceRow.set(self.currentRow,result)
		result
		_hx_local_3 = self
		_hx_local_4 = _hx_local_3.currentRow
		_hx_local_3.currentRow = (_hx_local_4 - _hx_del)
		_hx_local_3.currentRow
		return result

	def applyAction(self,code):
		mod = HighlightPatchUnit()
		mod.code = code
		mod.add = (code == "+++")
		mod.rem = (code == "---")
		mod.update = (code == "->")
		self.needSourceIndex()
		if (self.lastSourceRow == -1):
			self.lastSourceRow = self.lookUp(-1)
		mod.sourcePrevRow = self.lastSourceRow
		nextAct = python_internal_ArrayImpl._get(self.actions, (self.currentRow + 1))
		if ((nextAct != "+++") and ((nextAct != "..."))):
			mod.sourceNextRow = self.lookUp(1)
		if mod.add:
			if (python_internal_ArrayImpl._get(self.actions, (self.currentRow - 1)) != "+++"):
				mod.sourcePrevRow = self.lookUp(-1)
			mod.sourceRow = mod.sourcePrevRow
			if (mod.sourceRow != -1):
				mod.sourceRowOffset = 1
		else:
			def _hx_local_0():
				self.lastSourceRow = self.lookUp()
				return self.lastSourceRow
			mod.sourceRow = _hx_local_0()
		if (python_internal_ArrayImpl._get(self.actions, (self.currentRow + 1)) == ""):
			self.lastSourceRow = mod.sourceNextRow
		mod.patchRow = self.currentRow
		if (code == "@@"):
			mod.sourceRow = 0
		_this = self.mods
		_this.append(mod)

	def checkAct(self):
		act = self.getString(self.rcOffset)
		if (self.rowInfo.value != act):
			DiffRender.examineCell(0,0,act,"",act,"",self.rowInfo)

	def getPreString(self,txt):
		self.checkAct()
		if (not self.rowInfo.updated):
			return txt
		DiffRender.examineCell(0,0,txt,"",self.rowInfo.value,"",self.cellInfo)
		if (not self.cellInfo.updated):
			return txt
		return self.cellInfo.lvalue

	def getRowString(self,c):
		at = self.sourceInPatchCol.h.get(c,None)
		if (at is None):
			return "NOT_FOUND"
		return self.getPreString(self.getString(at))

	def sortMods(self,a,b):
		if ((b.code == "@@") and ((a.code != "@@"))):
			return 1
		if ((a.code == "@@") and ((b.code != "@@"))):
			return -1
		if (((a.sourceRow == -1) and (not a.add)) and ((b.sourceRow != -1))):
			return 1
		if (((a.sourceRow != -1) and (not b.add)) and ((b.sourceRow == -1))):
			return -1
		if ((a.sourceRow + a.sourceRowOffset) > ((b.sourceRow + b.sourceRowOffset))):
			return 1
		if ((a.sourceRow + a.sourceRowOffset) < ((b.sourceRow + b.sourceRowOffset))):
			return -1
		if (a.patchRow > b.patchRow):
			return 1
		if (a.patchRow < b.patchRow):
			return -1
		return 0

	def processMods(self,rmods,fate,len):
		rmods.sort(key= python_lib_FuncTools.cmp_to_key(self.sortMods))
		offset = 0
		last = -1
		target = 0
		_g = 0
		while ((_g < python_lib_Builtin.len(rmods))):
			mod = (rmods[_g] if _g >= 0 and _g < python_lib_Builtin.len(rmods) else None)
			_g = (_g + 1)
			if (last != -1):
				_g2 = last
				_g1 = (mod.sourceRow + mod.sourceRowOffset)
				while ((_g2 < _g1)):
					i = _g2
					_g2 = (_g2 + 1)
					fate.append((i + offset))
					target = (target + 1)
					last = (last + 1)
			if mod.rem:
				fate.append(-1)
				offset = (offset - 1)
			elif mod.add:
				mod.destRow = target
				target = (target + 1)
				offset = (offset + 1)
			else:
				mod.destRow = target
			if (mod.sourceRow >= 0):
				last = (mod.sourceRow + mod.sourceRowOffset)
				if mod.rem:
					last = (last + 1)
			else:
				last = -1
		if (last != -1):
			_g3 = last
			while ((_g3 < len)):
				i1 = _g3
				_g3 = (_g3 + 1)
				fate.append((i1 + offset))
				target = (target + 1)
				last = (last + 1)
		return (len + offset)

	def computeOrdering(self,mods,permutation,permutationRev,dim):
		to_unit = haxe_ds_IntMap()
		from_unit = haxe_ds_IntMap()
		meta_from_unit = haxe_ds_IntMap()
		ct = 0
		_g = 0
		while ((_g < python_lib_Builtin.len(mods))):
			mod = (mods[_g] if _g >= 0 and _g < python_lib_Builtin.len(mods) else None)
			_g = (_g + 1)
			if (mod.add or mod.rem):
				continue
			if (mod.sourceRow < 0):
				continue
			if (mod.sourcePrevRow >= 0):
				v = mod.sourceRow
				to_unit.set(mod.sourcePrevRow,v)
				v
				v1 = mod.sourcePrevRow
				from_unit.set(mod.sourceRow,v1)
				v1
				if ((mod.sourcePrevRow + 1) != mod.sourceRow):
					ct = (ct + 1)
			if (mod.sourceNextRow >= 0):
				v2 = mod.sourceNextRow
				to_unit.set(mod.sourceRow,v2)
				v2
				v3 = mod.sourceRow
				from_unit.set(mod.sourceNextRow,v3)
				v3
				if ((mod.sourceRow + 1) != mod.sourceNextRow):
					ct = (ct + 1)
		if (ct > 0):
			cursor = None
			logical = None
			starts = []
			_g1 = 0
			while ((_g1 < dim)):
				i = _g1
				_g1 = (_g1 + 1)
				u = from_unit.h.get(i,None)
				if (u is not None):
					meta_from_unit.set(u,i)
					i
				else:
					starts.append(i)
			used = haxe_ds_IntMap()
			len = 0
			_g2 = 0
			while ((_g2 < dim)):
				i1 = _g2
				_g2 = (_g2 + 1)
				if logical in meta_from_unit.h:
					cursor = meta_from_unit.h.get(logical,None)
				else:
					cursor = None
				if (cursor is None):
					v4 = None
					if (python_lib_Builtin.len(starts) == 0):
						v4 = None
					else:
						v4 = starts.pop(0)
					cursor = v4
					logical = v4
				if (cursor is None):
					cursor = 0
				while (cursor in used.h):
					cursor = (((cursor + 1)) % dim)
				logical = cursor
				permutationRev.append(cursor)
				used.set(cursor,1)
				1
			_g11 = 0
			_g3 = python_lib_Builtin.len(permutationRev)
			while ((_g11 < _g3)):
				i2 = _g11
				_g11 = (_g11 + 1)
				python_internal_ArrayImpl._set(permutation, i2, -1)
			_g12 = 0
			_g4 = python_lib_Builtin.len(permutation)
			while ((_g12 < _g4)):
				i3 = _g12
				_g12 = (_g12 + 1)
				python_internal_ArrayImpl._set(permutation, (permutationRev[i3] if i3 >= 0 and i3 < python_lib_Builtin.len(permutationRev) else None), i3)

	def permuteRows(self):
		self.rowPermutation = list()
		self.rowPermutationRev = list()
		self.computeOrdering(self.mods,self.rowPermutation,self.rowPermutationRev,Reflect.field(self.source,"get_height")())

	def finishRows(self):
		fate = list()
		self.permuteRows()
		if (python_lib_Builtin.len(self.rowPermutation) > 0):
			_g = 0
			_g1 = self.mods
			while ((_g < python_lib_Builtin.len(_g1))):
				mod = (_g1[_g] if _g >= 0 and _g < python_lib_Builtin.len(_g1) else None)
				_g = (_g + 1)
				if (mod.sourceRow >= 0):
					mod.sourceRow = python_internal_ArrayImpl._get(self.rowPermutation, mod.sourceRow)
		if (python_lib_Builtin.len(self.rowPermutation) > 0):
			self.source.insertOrDeleteRows(self.rowPermutation,python_lib_Builtin.len(self.rowPermutation))
		len = self.processMods(self.mods,fate,Reflect.field(self.source,"get_height")())
		self.source.insertOrDeleteRows(fate,len)
		_g2 = 0
		_g11 = self.mods
		while ((_g2 < python_lib_Builtin.len(_g11))):
			mod1 = (_g11[_g2] if _g2 >= 0 and _g2 < python_lib_Builtin.len(_g11) else None)
			_g2 = (_g2 + 1)
			if (not mod1.rem):
				if mod1.add:
					_hx_local_2 = self.headerPost.iterator()
					while (_hx_local_2.hasNext()):
						c = _hx_local_2.next()
						offset = self.patchInSourceCol.h.get(c,None)
						if ((offset is not None) and ((offset >= 0))):
							self.source.setCell(offset,mod1.destRow,self.patch.getCell(c,mod1.patchRow))
				elif mod1.update:
					self.currentRow = mod1.patchRow
					self.checkAct()
					if (not self.rowInfo.updated):
						continue
					_hx_local_3 = self.headerPre.iterator()
					while (_hx_local_3.hasNext()):
						c1 = _hx_local_3.next()
						txt = self.view.toString(self.patch.getCell(c1,mod1.patchRow))
						DiffRender.examineCell(0,0,txt,"",self.rowInfo.value,"",self.cellInfo)
						if (not self.cellInfo.updated):
							continue
						if self.cellInfo.conflicted:
							continue
						d = self.view.toDatum(self.csv.parseSingleCell(self.cellInfo.rvalue))
						self.source.setCell(self.patchInSourceCol.h.get(c1,None),mod1.destRow,d)

	def permuteColumns(self):
		if (self.headerMove is None):
			return
		self.colPermutation = list()
		self.colPermutationRev = list()
		self.computeOrdering(self.cmods,self.colPermutation,self.colPermutationRev,Reflect.field(self.source,"get_width")())
		if (python_lib_Builtin.len(self.colPermutation) == 0):
			return

	def finishColumns(self):
		self.needSourceColumns()
		_g1 = self.payloadCol
		_g = self.payloadTop
		while ((_g1 < _g)):
			i = _g1
			_g1 = (_g1 + 1)
			act = self.modifier.h.get(i,None)
			hdr = self.header.h.get(i,None)
			if (act is None):
				act = ""
			if (act == "---"):
				at = self.patchInSourceCol.h.get(i,None)
				mod = HighlightPatchUnit()
				mod.code = act
				mod.rem = True
				mod.sourceRow = at
				mod.patchRow = i
				_this = self.cmods
				_this.append(mod)
			elif (act == "+++"):
				mod1 = HighlightPatchUnit()
				mod1.code = act
				mod1.add = True
				prev = -1
				cont = False
				mod1.sourceRow = -1
				if (python_lib_Builtin.len(self.cmods) > 0):
					mod1.sourceRow = python_internal_ArrayImpl._get(self.cmods, (python_lib_Builtin.len(self.cmods) - 1)).sourceRow
				if (mod1.sourceRow != -1):
					mod1.sourceRowOffset = 1
				mod1.patchRow = i
				_this1 = self.cmods
				_this1.append(mod1)
			elif (act != "..."):
				mod2 = HighlightPatchUnit()
				mod2.code = act
				mod2.patchRow = i
				mod2.sourceRow = self.patchInSourceCol.h.get(i,None)
				_this2 = self.cmods
				_this2.append(mod2)
		at1 = -1
		rat = -1
		_g11 = 0
		_g2 = (python_lib_Builtin.len(self.cmods) - 1)
		while ((_g11 < _g2)):
			i1 = _g11
			_g11 = (_g11 + 1)
			icode = (self.cmods[i1] if i1 >= 0 and i1 < python_lib_Builtin.len(self.cmods) else None).code
			if ((icode != "+++") and ((icode != "---"))):
				at1 = (self.cmods[i1] if i1 >= 0 and i1 < python_lib_Builtin.len(self.cmods) else None).sourceRow
			python_internal_ArrayImpl._get(self.cmods, (i1 + 1)).sourcePrevRow = at1
			j = ((python_lib_Builtin.len(self.cmods) - 1) - i1)
			jcode = (self.cmods[j] if j >= 0 and j < python_lib_Builtin.len(self.cmods) else None).code
			if ((jcode != "+++") and ((jcode != "---"))):
				rat = (self.cmods[j] if j >= 0 and j < python_lib_Builtin.len(self.cmods) else None).sourceRow
			python_internal_ArrayImpl._get(self.cmods, (j - 1)).sourceNextRow = rat
		fate = list()
		self.permuteColumns()
		if (self.headerMove is not None):
			if (python_lib_Builtin.len(self.colPermutation) > 0):
				_g3 = 0
				_g12 = self.cmods
				while ((_g3 < python_lib_Builtin.len(_g12))):
					mod3 = (_g12[_g3] if _g3 >= 0 and _g3 < python_lib_Builtin.len(_g12) else None)
					_g3 = (_g3 + 1)
					if (mod3.sourceRow >= 0):
						mod3.sourceRow = python_internal_ArrayImpl._get(self.colPermutation, mod3.sourceRow)
				self.source.insertOrDeleteColumns(self.colPermutation,python_lib_Builtin.len(self.colPermutation))
		len = self.processMods(self.cmods,fate,Reflect.field(self.source,"get_width")())
		self.source.insertOrDeleteColumns(fate,len)
		_g4 = 0
		_g13 = self.cmods
		while ((_g4 < python_lib_Builtin.len(_g13))):
			cmod = (_g13[_g4] if _g4 >= 0 and _g4 < python_lib_Builtin.len(_g13) else None)
			_g4 = (_g4 + 1)
			if (not cmod.rem):
				if cmod.add:
					_g21 = 0
					_g31 = self.mods
					while ((_g21 < python_lib_Builtin.len(_g31))):
						mod4 = (_g31[_g21] if _g21 >= 0 and _g21 < python_lib_Builtin.len(_g31) else None)
						_g21 = (_g21 + 1)
						if ((mod4.patchRow != -1) and ((mod4.destRow != -1))):
							d = self.patch.getCell(cmod.patchRow,mod4.patchRow)
							self.source.setCell(cmod.destRow,mod4.destRow,d)
					hdr1 = self.header.h.get(cmod.patchRow,None)
					self.source.setCell(cmod.destRow,0,self.view.toDatum(hdr1))
		_g14 = 0
		_g5 = Reflect.field(self.source,"get_width")()
		while ((_g14 < _g5)):
			i2 = _g14
			_g14 = (_g14 + 1)
			name = self.view.toString(self.source.getCell(i2,0))
			next_name = self.headerRename.h.get(name,None)
			if (next_name is None):
				continue
			self.source.setCell(i2,0,self.view.toDatum(next_name))

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.source = None
		_hx_o.patch = None
		_hx_o.view = None
		_hx_o.csv = None
		_hx_o.header = None
		_hx_o.headerPre = None
		_hx_o.headerPost = None
		_hx_o.headerRename = None
		_hx_o.headerMove = None
		_hx_o.modifier = None
		_hx_o.currentRow = None
		_hx_o.payloadCol = None
		_hx_o.payloadTop = None
		_hx_o.mods = None
		_hx_o.cmods = None
		_hx_o.rowInfo = None
		_hx_o.cellInfo = None
		_hx_o.rcOffset = None
		_hx_o.indexes = None
		_hx_o.sourceInPatchCol = None
		_hx_o.patchInSourceCol = None
		_hx_o.patchInSourceRow = None
		_hx_o.lastSourceRow = None
		_hx_o.actions = None
		_hx_o.rowPermutation = None
		_hx_o.rowPermutationRev = None
		_hx_o.colPermutation = None
		_hx_o.colPermutationRev = None
		_hx_o.haveDroppedColumns = None


@_hx_classes.registerClass("HighlightPatchUnit", fields=["add","rem","update","code","sourceRow","sourceRowOffset","sourcePrevRow","sourceNextRow","destRow","patchRow"], methods=["toString"])
class HighlightPatchUnit:

	def __init__(self):
		self.add = None
		self.rem = None
		self.update = None
		self.code = None
		self.sourceRow = None
		self.sourceRowOffset = None
		self.sourcePrevRow = None
		self.sourceNextRow = None
		self.destRow = None
		self.patchRow = None
		self.add = False
		self.rem = False
		self.update = False
		self.sourceRow = -1
		self.sourceRowOffset = 0
		self.sourcePrevRow = -1
		self.sourceNextRow = -1
		self.destRow = -1
		self.patchRow = -1
		self.code = ""

	def toString(self):
		return ((((((((((HxOverrides.stringOrNull(self.code) + " patchRow ") + Std.string(self.patchRow)) + " sourceRows ") + Std.string(self.sourcePrevRow)) + ",") + Std.string(self.sourceRow)) + ",") + Std.string(self.sourceNextRow)) + " destRow ") + Std.string(self.destRow))

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.add = None
		_hx_o.rem = None
		_hx_o.update = None
		_hx_o.code = None
		_hx_o.sourceRow = None
		_hx_o.sourceRowOffset = None
		_hx_o.sourcePrevRow = None
		_hx_o.sourceNextRow = None
		_hx_o.destRow = None
		_hx_o.patchRow = None


@_hx_classes.registerClass("Index", fields=["items","keys","top_freq","height","cols","v","indexed_table"], methods=["addColumn","indexTable","toKey","toKeyByContent","getTable"])
class Index:

	def __init__(self):
		self.items = None
		self.keys = None
		self.top_freq = None
		self.height = None
		self.cols = None
		self.v = None
		self.indexed_table = None
		self.items = haxe_ds_StringMap()
		self.cols = list()
		self.keys = list()
		self.top_freq = 0
		self.height = 0

	def addColumn(self,i):
		_this = self.cols
		_this.append(i)

	def indexTable(self,t):
		self.indexed_table = t
		_g1 = 0
		_g = Reflect.field(t,"get_height")()
		while ((_g1 < _g)):
			i = _g1
			_g1 = (_g1 + 1)
			key = None
			if (python_lib_Builtin.len(self.keys) > i):
				key = (self.keys[i] if i >= 0 and i < python_lib_Builtin.len(self.keys) else None)
			else:
				key = self.toKey(t,i)
				_this = self.keys
				_this.append(key)
			item = self.items.h.get(key,None)
			if (item is None):
				item = IndexItem()
				self.items.h[key] = item
			ct = item.add(i)
			if (ct > self.top_freq):
				self.top_freq = ct
		self.height = Reflect.field(t,"get_height")()

	def toKey(self,t,i):
		wide = ""
		if (self.v is None):
			self.v = t.getCellView()
		_g1 = 0
		_g = python_lib_Builtin.len(self.cols)
		while ((_g1 < _g)):
			k = _g1
			_g1 = (_g1 + 1)
			d = t.getCell((self.cols[k] if k >= 0 and k < python_lib_Builtin.len(self.cols) else None),i)
			txt = self.v.toString(d)
			if ((((txt is None) or ((txt == ""))) or ((txt == "null"))) or ((txt == "undefined"))):
				continue
			if (k > 0):
				wide = (HxOverrides.stringOrNull(wide) + " // ")
			wide = (HxOverrides.stringOrNull(wide) + HxOverrides.stringOrNull(txt))
		return wide

	def toKeyByContent(self,row):
		wide = ""
		_g1 = 0
		_g = python_lib_Builtin.len(self.cols)
		while ((_g1 < _g)):
			k = _g1
			_g1 = (_g1 + 1)
			txt = row.getRowString((self.cols[k] if k >= 0 and k < python_lib_Builtin.len(self.cols) else None))
			if ((((txt is None) or ((txt == ""))) or ((txt == "null"))) or ((txt == "undefined"))):
				continue
			if (k > 0):
				wide = (HxOverrides.stringOrNull(wide) + " // ")
			wide = (HxOverrides.stringOrNull(wide) + HxOverrides.stringOrNull(txt))
		return wide

	def getTable(self):
		return self.indexed_table

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.items = None
		_hx_o.keys = None
		_hx_o.top_freq = None
		_hx_o.height = None
		_hx_o.cols = None
		_hx_o.v = None
		_hx_o.indexed_table = None


@_hx_classes.registerClass("IndexItem", fields=["lst"], methods=["add"])
class IndexItem:

	def __init__(self):
		self.lst = None
		pass

	def add(self,i):
		if (self.lst is None):
			self.lst = list()
		_this = self.lst
		_this.append(i)
		return python_lib_Builtin.len(self.lst)

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.lst = None


@_hx_classes.registerClass("IndexPair", fields=["ia","ib","quality"], methods=["addColumn","addColumns","indexTables","queryByKey","queryByContent","queryLocal","getTopFreq","getQuality"])
class IndexPair:

	def __init__(self):
		self.ia = None
		self.ib = None
		self.quality = None
		self.ia = Index()
		self.ib = Index()
		self.quality = 0

	def addColumn(self,i):
		self.ia.addColumn(i)
		self.ib.addColumn(i)

	def addColumns(self,ca,cb):
		self.ia.addColumn(ca)
		self.ib.addColumn(cb)

	def indexTables(self,a,b):
		self.ia.indexTable(a)
		self.ib.indexTable(b)
		good = 0
		_hx_local_1 = self.ia.items.keys()
		while (_hx_local_1.hasNext()):
			key = _hx_local_1.next()
			item_a = self.ia.items.h.get(key,None)
			spot_a = python_lib_Builtin.len(item_a.lst)
			item_b = self.ib.items.h.get(key,None)
			spot_b = 0
			if (item_b is not None):
				spot_b = python_lib_Builtin.len(item_b.lst)
			if ((spot_a == 1) and ((spot_b == 1))):
				good = (good + 1)
		def _hx_local_2():
			b1 = Reflect.field(a,"get_height")()
			return (1.0 if (python_lib_Math.isnan(1.0)) else (b1 if (python_lib_Math.isnan(b1)) else python_lib_Builtin.max(1.0,b1)))
		self.quality = (good / _hx_local_2())

	def queryByKey(self,ka):
		result = CrossMatch()
		result.item_a = self.ia.items.h.get(ka,None)
		result.item_b = self.ib.items.h.get(ka,None)
		def _hx_local_0():
			result.spot_b = 0
			return result.spot_b
		result.spot_a = _hx_local_0()
		if (ka != ""):
			if (result.item_a is not None):
				result.spot_a = python_lib_Builtin.len(result.item_a.lst)
			if (result.item_b is not None):
				result.spot_b = python_lib_Builtin.len(result.item_b.lst)
		return result

	def queryByContent(self,row):
		result = CrossMatch()
		ka = self.ia.toKeyByContent(row)
		return self.queryByKey(ka)

	def queryLocal(self,row):
		ka = self.ia.toKey(self.ia.getTable(),row)
		return self.queryByKey(ka)

	def getTopFreq(self):
		if (self.ib.top_freq > self.ia.top_freq):
			return self.ib.top_freq
		return self.ia.top_freq

	def getQuality(self):
		return self.quality

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.ia = None
		_hx_o.ib = None
		_hx_o.quality = None


@_hx_classes.registerClass("Lambda", statics=["array","map","has"])
class Lambda:

	@staticmethod
	def array(it):
		a = list()
		_hx_local_0 = HxOverrides.iterator(it)
		while (_hx_local_0.hasNext()):
			i = _hx_local_0.next()
			a.append(i)
		return a

	@staticmethod
	def map(it,f):
		l = List()
		_hx_local_0 = HxOverrides.iterator(it)
		while (_hx_local_0.hasNext()):
			x = _hx_local_0.next()
			l.add(f(x))
		return l

	@staticmethod
	def has(it,elt):
		_hx_local_0 = HxOverrides.iterator(it)
		while (_hx_local_0.hasNext()):
			x = _hx_local_0.next()
			if (x == elt):
				return True
		return False


@_hx_classes.registerClass("List", fields=["h","q","length"], methods=["add","iterator"])
class List:

	def __init__(self):
		self.h = None
		self.q = None
		self.length = None
		self.length = 0

	def add(self,item):
		x = [item]
		if (self.h is None):
			self.h = x
		else:
			python_internal_ArrayImpl._set(self.q, 1, x)
		self.q = x
		_hx_local_0 = self
		_hx_local_1 = _hx_local_0.length
		_hx_local_0.length = (_hx_local_1 + 1)
		_hx_local_1

	def iterator(self):
		h = self.h
		def _hx_local_2():
			def _hx_local_0():
				return (h is not None)
			def _hx_local_1():
				nonlocal h
				if (h is None):
					return None
				x = (h[0] if 0 < python_lib_Builtin.len(h) else None)
				h = (h[1] if 1 < python_lib_Builtin.len(h) else None)
				return x
			return _hx_AnonObject({'hasNext': _hx_local_0, 'next': _hx_local_1})
		return _hx_local_2()

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.h = None
		_hx_o.q = None
		_hx_o.length = None


@_hx_classes.registerClass("IMap")
class IMap:	pass


@_hx_classes.registerClass("Mover", statics=["moveUnits","moveWithExtras","moveWithoutExtras"])
class Mover:

	def __init__(self):
		pass

	@staticmethod
	def moveUnits(units):
		isrc = list()
		idest = list()
		len = python_lib_Builtin.len(units)
		ltop = -1
		rtop = -1
		in_src = haxe_ds_IntMap()
		in_dest = haxe_ds_IntMap()
		_g = 0
		while ((_g < len)):
			i = _g
			_g = (_g + 1)
			unit = (units[i] if i >= 0 and i < python_lib_Builtin.len(units) else None)
			if ((unit.l >= 0) and ((unit.r >= 0))):
				if (ltop < unit.l):
					ltop = unit.l
				if (rtop < unit.r):
					rtop = unit.r
				in_src.set(unit.l,i)
				i
				in_dest.set(unit.r,i)
				i
		v = None
		_g1 = 0
		_g2 = (ltop + 1)
		while ((_g1 < _g2)):
			i1 = _g1
			_g1 = (_g1 + 1)
			v = in_src.h.get(i1,None)
			if (v is not None):
				isrc.append(v)
		_g11 = 0
		_g3 = (rtop + 1)
		while ((_g11 < _g3)):
			i2 = _g11
			_g11 = (_g11 + 1)
			v = in_dest.h.get(i2,None)
			if (v is not None):
				idest.append(v)
		return Mover.moveWithoutExtras(isrc,idest)

	@staticmethod
	def moveWithExtras(isrc,idest):
		len = python_lib_Builtin.len(isrc)
		len2 = python_lib_Builtin.len(idest)
		in_src = haxe_ds_IntMap()
		in_dest = haxe_ds_IntMap()
		_g = 0
		while ((_g < len)):
			i = _g
			_g = (_g + 1)
			in_src.set((isrc[i] if i >= 0 and i < python_lib_Builtin.len(isrc) else None),i)
			i
		_g1 = 0
		while ((_g1 < len2)):
			i1 = _g1
			_g1 = (_g1 + 1)
			in_dest.set((idest[i1] if i1 >= 0 and i1 < python_lib_Builtin.len(idest) else None),i1)
			i1
		src = list()
		dest = list()
		v = None
		_g2 = 0
		while ((_g2 < len)):
			i2 = _g2
			_g2 = (_g2 + 1)
			v = (isrc[i2] if i2 >= 0 and i2 < python_lib_Builtin.len(isrc) else None)
			if v in in_dest.h:
				src.append(v)
		_g3 = 0
		while ((_g3 < len2)):
			i3 = _g3
			_g3 = (_g3 + 1)
			v = (idest[i3] if i3 >= 0 and i3 < python_lib_Builtin.len(idest) else None)
			if v in in_src.h:
				dest.append(v)
		return Mover.moveWithoutExtras(src,dest)

	@staticmethod
	def moveWithoutExtras(src,dest):
		if (python_lib_Builtin.len(src) != python_lib_Builtin.len(dest)):
			return None
		if (python_lib_Builtin.len(src) <= 1):
			return []
		len = python_lib_Builtin.len(src)
		in_src = haxe_ds_IntMap()
		blk_len = haxe_ds_IntMap()
		blk_src_loc = haxe_ds_IntMap()
		blk_dest_loc = haxe_ds_IntMap()
		_g = 0
		while ((_g < len)):
			i = _g
			_g = (_g + 1)
			in_src.set((src[i] if i >= 0 and i < python_lib_Builtin.len(src) else None),i)
			i
		ct = 0
		in_cursor = -2
		out_cursor = 0
		next = None
		blk = -1
		v = None
		while ((out_cursor < len)):
			v = (dest[out_cursor] if out_cursor >= 0 and out_cursor < python_lib_Builtin.len(dest) else None)
			next = in_src.h.get(v,None)
			if (next != ((in_cursor + 1))):
				blk = v
				ct = 1
				blk_src_loc.set(blk,next)
				blk_dest_loc.set(blk,out_cursor)
			else:
				ct = (ct + 1)
			blk_len.set(blk,ct)
			in_cursor = next
			out_cursor = (out_cursor + 1)
		blks = list()
		_hx_local_2 = blk_len.keys()
		while (_hx_local_2.hasNext()):
			k = _hx_local_2.next()
			blks.append(k)
		def _hx_local_3(a,b):
			return (blk_len.h.get(b,None) - blk_len.h.get(a,None))
		blks.sort(key= python_lib_FuncTools.cmp_to_key(_hx_local_3))
		moved = list()
		while ((python_lib_Builtin.len(blks) > 0)):
			blk1 = None
			if (python_lib_Builtin.len(blks) == 0):
				blk1 = None
			else:
				blk1 = blks.pop(0)
			blen = python_lib_Builtin.len(blks)
			ref_src_loc = blk_src_loc.h.get(blk1,None)
			ref_dest_loc = blk_dest_loc.h.get(blk1,None)
			i1 = (blen - 1)
			while ((i1 >= 0)):
				blki = (blks[i1] if i1 >= 0 and i1 < python_lib_Builtin.len(blks) else None)
				blki_src_loc = blk_src_loc.h.get(blki,None)
				to_left_src = (blki_src_loc < ref_src_loc)
				to_left_dest = (blk_dest_loc.h.get(blki,None) < ref_dest_loc)
				if (to_left_src != to_left_dest):
					ct1 = blk_len.h.get(blki,None)
					_g1 = 0
					while ((_g1 < ct1)):
						j = _g1
						_g1 = (_g1 + 1)
						moved.append((src[blki_src_loc] if blki_src_loc >= 0 and blki_src_loc < python_lib_Builtin.len(src) else None))
						blki_src_loc = (blki_src_loc + 1)
					pos = i1
					if (pos < 0):
						pos = (python_lib_Builtin.len(blks) + pos)
					if (pos < 0):
						pos = 0
					res = blks[pos:(pos + 1)]
					del blks[pos:(pos + 1)]
					res
				i1 = (i1 - 1)
		return moved


@_hx_classes.registerClass("Ordering", fields=["order","ignore_parent"], methods=["add","getList","toString","ignoreParent"])
class Ordering:

	def __init__(self):
		self.order = None
		self.ignore_parent = None
		self.order = list()
		self.ignore_parent = False

	def add(self,l,r,p = -2):
		if (p is None):
			p = -2
		if self.ignore_parent:
			p = -2
		_this = self.order
		x = Unit(l, r, p)
		_this.append(x)

	def getList(self):
		return self.order

	def toString(self):
		txt = ""
		_g1 = 0
		_g = python_lib_Builtin.len(self.order)
		while ((_g1 < _g)):
			i = _g1
			_g1 = (_g1 + 1)
			if (i > 0):
				txt = (HxOverrides.stringOrNull(txt) + ", ")
			txt = (HxOverrides.stringOrNull(txt) + Std.string((self.order[i] if i >= 0 and i < python_lib_Builtin.len(self.order) else None)))
		return txt

	def ignoreParent(self):
		self.ignore_parent = True

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.order = None
		_hx_o.ignore_parent = None


@_hx_classes.registerClass("Reflect", statics=["field","setField","callMethod","isFunction"])
class Reflect:

	@staticmethod
	def field(o,field):
		return python_Boot.field(o,field)

	@staticmethod
	def setField(o,field,value):
		field1 = None
		if field in python_Boot.keywords:
			field1 = ("_hx_" + field)
		elif ((((python_lib_Builtin.len(field) > 2) and ((python_internal_HxBuiltin.ord(field[0]) == 95))) and ((python_internal_HxBuiltin.ord(field[1]) == 95))) and ((python_internal_HxBuiltin.ord(field[(python_lib_Builtin.len(field) - 1)]) != 95))):
			field1 = ("_hx_" + field)
		else:
			field1 = field
		return python_lib_Builtin.setattr(o,field1,value)

	@staticmethod
	def callMethod(o,func,args):
		args1 = args
		if python_lib_Builtin.callable(func):
			return func(*(python_lib_Builtin.list(args1) if ((not Std._hx_is(args1,list))) else args1))
		else:
			return None

	@staticmethod
	def isFunction(f):
		return (python_lib_Inspect.isfunction(f) or python_lib_Inspect.ismethod(f))


@_hx_classes.registerClass("Report", fields=["changes"], methods=["toString","clear"])
class Report:

	def __init__(self):
		self.changes = None
		self.changes = list()

	def toString(self):
		return (("[" + HxOverrides.stringOrNull(python_internal_ArrayImpl.join(self.changes,","))) + "]")

	def clear(self):
		self.changes = list()

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.changes = None


@_hx_classes.registerClass("SimpleCell", fields=["datum"], methods=["toString"])
class SimpleCell:

	def __init__(self,x):
		self.datum = None
		self.datum = x

	def toString(self):
		return self.datum

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.datum = None


@_hx_classes.registerClass("Table", fields=["height","width"], methods=["getCell","setCell","getCellView","isResizable","resize","clear","insertOrDeleteRows","insertOrDeleteColumns","trimBlank"])
class Table:	pass


@_hx_classes.registerClass("SimpleTable", fields=["data","w","h"], props=["height","width","size"], methods=["getTable","get_width","get_height","get_size","getCell","setCell","toString","getCellView","isResizable","resize","clear","insertOrDeleteRows","insertOrDeleteColumns","trimBlank"], statics=["tableToString"], interfaces=[Table])
class SimpleTable:

	def __init__(self,w,h):
		self.data = None
		self.w = None
		self.h = None
		self.data = haxe_ds_IntMap()
		self.w = w
		self.h = h

	def getTable(self):
		return self

	def get_width(self):
		return self.w

	def get_height(self):
		return self.h

	def get_size(self):
		return self.h

	def getCell(self,x,y):
		return self.data.h.get((x + ((y * self.w))),None)

	def setCell(self,x,y,c):
		value = c
		self.data.set((x + ((y * self.w))),value)

	def toString(self):
		return SimpleTable.tableToString(self)

	def getCellView(self):
		return SimpleView()

	def isResizable(self):
		return True

	def resize(self,w,h):
		self.w = w
		self.h = h
		return True

	def clear(self):
		self.data = haxe_ds_IntMap()

	def insertOrDeleteRows(self,fate,hfate):
		data2 = haxe_ds_IntMap()
		_g1 = 0
		_g = python_lib_Builtin.len(fate)
		while ((_g1 < _g)):
			i = _g1
			_g1 = (_g1 + 1)
			j = (fate[i] if i >= 0 and i < python_lib_Builtin.len(fate) else None)
			if (j != -1):
				_g3 = 0
				_g2 = self.w
				while ((_g3 < _g2)):
					c = _g3
					_g3 = (_g3 + 1)
					idx = ((i * self.w) + c)
					if idx in self.data.h:
						value = self.data.h.get(idx,None)
						data2.set(((j * self.w) + c),value)
		self.h = hfate
		self.data = data2
		return True

	def insertOrDeleteColumns(self,fate,wfate):
		data2 = haxe_ds_IntMap()
		_g1 = 0
		_g = python_lib_Builtin.len(fate)
		while ((_g1 < _g)):
			i = _g1
			_g1 = (_g1 + 1)
			j = (fate[i] if i >= 0 and i < python_lib_Builtin.len(fate) else None)
			if (j != -1):
				_g3 = 0
				_g2 = self.h
				while ((_g3 < _g2)):
					r = _g3
					_g3 = (_g3 + 1)
					idx = ((r * self.w) + i)
					if idx in self.data.h:
						value = self.data.h.get(idx,None)
						data2.set(((r * wfate) + j),value)
		self.w = wfate
		self.data = data2
		return True

	def trimBlank(self):
		if (self.h == 0):
			return True
		h_test = self.h
		if (h_test >= 3):
			h_test = 3
		view = self.getCellView()
		space = view.toDatum("")
		more = True
		while (more):
			_g1 = 0
			_g = self.get_width()
			while ((_g1 < _g)):
				i = _g1
				_g1 = (_g1 + 1)
				c = self.getCell(i,(self.h - 1))
				if (not ((view.equals(c,space) or ((c is None))))):
					more = False
					break
			if more:
				_hx_local_0 = self
				_hx_local_1 = _hx_local_0.h
				_hx_local_0.h = (_hx_local_1 - 1)
				_hx_local_1
		more = True
		nw = self.w
		while (more):
			if (self.w == 0):
				break
			_g2 = 0
			while ((_g2 < h_test)):
				i1 = _g2
				_g2 = (_g2 + 1)
				c1 = self.getCell((nw - 1),i1)
				if (not ((view.equals(c1,space) or ((c1 is None))))):
					more = False
					break
			if more:
				nw = (nw - 1)
		if (nw == self.w):
			return True
		data2 = haxe_ds_IntMap()
		_g3 = 0
		while ((_g3 < nw)):
			i2 = _g3
			_g3 = (_g3 + 1)
			_g21 = 0
			_g11 = self.h
			while ((_g21 < _g11)):
				r = _g21
				_g21 = (_g21 + 1)
				idx = ((r * self.w) + i2)
				if idx in self.data.h:
					value = self.data.h.get(idx,None)
					data2.set(((r * nw) + i2),value)
		self.w = nw
		self.data = data2
		return True

	@staticmethod
	def tableToString(tab):
		x = ""
		_g1 = 0
		_g = Reflect.field(tab,"get_height")()
		while ((_g1 < _g)):
			i = _g1
			_g1 = (_g1 + 1)
			_g3 = 0
			_g2 = Reflect.field(tab,"get_width")()
			while ((_g3 < _g2)):
				j = _g3
				_g3 = (_g3 + 1)
				if (j > 0):
					x = (HxOverrides.stringOrNull(x) + " ")
				x = (HxOverrides.stringOrNull(x) + Std.string(tab.getCell(j,i)))
			x = (HxOverrides.stringOrNull(x) + "\n")
		return x

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.data = None
		_hx_o.w = None
		_hx_o.h = None


@_hx_classes.registerClass("View", methods=["toString","getBag","getTable","hasStructure","equals","toDatum"])
class View:	pass


@_hx_classes.registerClass("SimpleView", methods=["toString","getBag","getTable","hasStructure","equals","toDatum"], interfaces=[View])
class SimpleView:

	def __init__(self):
		pass

	def toString(self,d):
		if (d is None):
			return None
		return ("" + Std.string(d))

	def getBag(self,d):
		return None

	def getTable(self,d):
		return None

	def hasStructure(self,d):
		return False

	def equals(self,d1,d2):
		if ((d1 is None) and ((d2 is None))):
			return True
		if ((d1 is None) and ((("" + Std.string(d2)) == ""))):
			return True
		if ((("" + Std.string(d1)) == "") and ((d2 is None))):
			return True
		return (("" + Std.string(d1)) == (("" + Std.string(d2))))

	def toDatum(self,str):
		if (str is None):
			return None
		return SimpleCell(str)

	@staticmethod
	def _hx_empty_init(_hx_o):		pass


@_hx_classes.registerClass("SparseSheet", fields=["h","w","row","zero"], methods=["resize","nonDestructiveResize","get","set"])
class SparseSheet:

	def __init__(self):
		self.h = None
		self.w = None
		self.row = None
		self.zero = None
		def _hx_local_0():
			self.w = 0
			return self.w
		self.h = _hx_local_0()

	def resize(self,w,h,zero):
		self.row = haxe_ds_IntMap()
		self.nonDestructiveResize(w,h,zero)

	def nonDestructiveResize(self,w,h,zero):
		self.w = w
		self.h = h
		self.zero = zero

	def get(self,x,y):
		cursor = self.row.h.get(y,None)
		if (cursor is None):
			return self.zero
		val = cursor.h.get(x,None)
		if (val is None):
			return self.zero
		return val

	def set(self,x,y,val):
		cursor = self.row.h.get(y,None)
		if (cursor is None):
			cursor = haxe_ds_IntMap()
			self.row.set(y,cursor)
		cursor.set(x,val)

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.h = None
		_hx_o.w = None
		_hx_o.row = None
		_hx_o.zero = None


@_hx_classes.registerClass("Std", statics=["is","string","parseInt","shortenPossibleNumber","parseFloat"])
class Std:

	@staticmethod
	def _hx_is(v,t):
		if ((v is None) and ((t is None))):
			return False
		if (t is None):
			return False
		if (t == Dynamic):
			return True
		isBool = python_lib_Builtin.isinstance(v,python_lib_Builtin.bool)
		if ((t == Bool) and isBool):
			return True
		if ((((not isBool) and (not (t == Bool))) and (t == Int)) and python_lib_Builtin.isinstance(v,python_lib_Builtin.int)):
			return True
		vIsFloat = python_lib_Builtin.isinstance(v,python_lib_Builtin.float)
		def _hx_local_0():
			f = v
			return (((f != Math.POSITIVE_INFINITY) and ((f != Math.NEGATIVE_INFINITY))) and (not python_lib_Math.isnan(f)))
		def _hx_local_1():
			x = v
			def _hx_local_4():
				def _hx_local_3():
					_hx_local_2 = None
					try:
						_hx_local_2 = python_lib_Builtin.int(x)
					except Exception as _hx_e:
						_hx_e1 = _hx_e.val if isinstance(_hx_e, _HxException) else _hx_e
						e = _hx_e1
						_hx_local_2 = None
					return _hx_local_2
				return _hx_local_3()
			return _hx_local_4()
		if (((((((not isBool) and vIsFloat) and (t == Int)) and _hx_local_0()) and ((v == _hx_local_1()))) and ((v <= 2147483647))) and ((v >= -2147483648))):
			return True
		if (((not isBool) and (t == Float)) and python_lib_Builtin.isinstance(v,(float,int))):
			return True
		if (t == python_lib__Builtin_Builtin_Impl_.str):
			return python_lib_Builtin.isinstance(v,String)
		isEnumType = (t == Enum)
		if ((isEnumType and python_lib_Inspect.isclass(v)) and python_internal_HxBuiltin.hasattr(v,"_hx_constructs")):
			return True
		if isEnumType:
			return False
		isClassType = (t == Class)
		if ((((isClassType and (not python_lib_Builtin.isinstance(v,Enum))) and python_lib_Inspect.isclass(v)) and python_internal_HxBuiltin.hasattr(v,"_hx_class_name")) and (not python_internal_HxBuiltin.hasattr(v,"_hx_constructs"))):
			return True
		if isClassType:
			return False
		def _hx_local_6():
			_hx_local_5 = None
			try:
				_hx_local_5 = python_lib_Builtin.isinstance(v,t)
			except Exception as _hx_e:
				_hx_e1 = _hx_e.val if isinstance(_hx_e, _HxException) else _hx_e
				e1 = _hx_e1
				_hx_local_5 = False
			return _hx_local_5
		if _hx_local_6():
			return True
		if python_lib_Inspect.isclass(t):
			loop = None
			loop1 = None
			def _hx_local_8(intf):
				f1 = None
				if python_internal_HxBuiltin.hasattr(intf,"_hx_interfaces"):
					f1 = intf._hx_interfaces
				else:
					f1 = []
				if (f1 is not None):
					_g = 0
					while ((_g < python_lib_Builtin.len(f1))):
						i = (f1[_g] if _g >= 0 and _g < python_lib_Builtin.len(f1) else None)
						_g = (_g + 1)
						if HxOverrides.eq(i,t):
							return True
						else:
							l = loop1(i)
							if l:
								return True
					return False
				else:
					return False
			loop1 = _hx_local_8
			loop = loop1
			currentClass = v.__class__
			while ((currentClass is not None)):
				if loop(currentClass):
					return True
				currentClass = python_Boot.getSuperClass(currentClass)
			return False
		else:
			return False

	@staticmethod
	def string(s):
		return python_Boot.toString1(s,"")

	@staticmethod
	def parseInt(x):
		if (x is None):
			return None
		try:
			return python_lib_Builtin.int(x)
		except Exception as _hx_e:
			_hx_e1 = _hx_e.val if isinstance(_hx_e, _HxException) else _hx_e
			e = _hx_e1
			try:
				prefix = None
				_this = HxString.substr(x,0,2)
				prefix = _this.lower()
				if (prefix == "0x"):
					return python_lib_Builtin.int(x,16)
				raise _HxException("fail")
			except Exception as _hx_e:
				_hx_e1 = _hx_e.val if isinstance(_hx_e, _HxException) else _hx_e
				e1 = _hx_e1
				r = None
				x1 = Std.parseFloat(x)
				try:
					r = python_lib_Builtin.int(x1)
				except Exception as _hx_e:
					_hx_e1 = _hx_e.val if isinstance(_hx_e, _HxException) else _hx_e
					e2 = _hx_e1
					r = None
				if (r is None):
					r1 = Std.shortenPossibleNumber(x)
					if (r1 != x):
						return Std.parseInt(r1)
					else:
						return None
				return r

	@staticmethod
	def shortenPossibleNumber(x):
		r = ""
		_g1 = 0
		_g = python_lib_Builtin.len(x)
		while ((_g1 < _g)):
			i = _g1
			_g1 = (_g1 + 1)
			c = None
			if ((i < 0) or ((i >= python_lib_Builtin.len(x)))):
				c = ""
			else:
				c = x[i]
			_g2 = HxString.charCodeAt(c,0)
			if (_g2 is not None):
				if ((((((((((((_g2) == 46) or (((_g2) == 57))) or (((_g2) == 56))) or (((_g2) == 55))) or (((_g2) == 54))) or (((_g2) == 53))) or (((_g2) == 52))) or (((_g2) == 51))) or (((_g2) == 50))) or (((_g2) == 49))) or (((_g2) == 48))):
					r = (HxOverrides.stringOrNull(r) + HxOverrides.stringOrNull(c))
				else:
					break
			else:
				break
		return r

	@staticmethod
	def parseFloat(x):
		try:
			return python_lib_Builtin.float(x)
		except Exception as _hx_e:
			_hx_e1 = _hx_e.val if isinstance(_hx_e, _HxException) else _hx_e
			e = _hx_e1
			if (x is not None):
				r1 = Std.shortenPossibleNumber(x)
				if (r1 != x):
					return Std.parseFloat(r1)
			return Math.NaN


@_hx_classes.registerAbstract("Void")
class Void:
	pass


@_hx_classes.registerAbstract("Float")
class Float:
	pass


@_hx_classes.registerAbstract("Int")
class Int:
	pass


@_hx_classes.registerAbstract("Bool")
class Bool:
	pass


@_hx_classes.registerAbstract("Dynamic")
class Dynamic:
	pass


@_hx_classes.registerClass("StringBuf", fields=["b"])
class StringBuf:

	def __init__(self):
		self.b = None
		self.b = python_lib_io_StringIO()

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.b = None


@_hx_classes.registerClass("StringTools", statics=["lpad","replace"])
class StringTools:

	@staticmethod
	def lpad(s,c,l):
		if (python_lib_Builtin.len(c) <= 0):
			return s
		while ((python_lib_Builtin.len(s) < l)):
			s = (HxOverrides.stringOrNull(c) + HxOverrides.stringOrNull(s))
		return s

	@staticmethod
	def replace(s,sub,by):
		_this = None
		if (sub == ""):
			_this = python_internal_HxBuiltin.list(s)
		else:
			_this = s.split(sub)
		return by.join([python_Boot.toString1(x1,'') for x1 in _this])


@_hx_classes.registerClass("haxe.ds.StringMap", fields=["h"], methods=["keys","iterator"], interfaces=[IMap])
class haxe_ds_StringMap:

	def __init__(self):
		self.h = None
		self.h = python_lib_Dict()

	def keys(self):
		a = []
		key = None
		for key in self.h:
			a.append(key)
		return python_HaxeIterator(a.__iter__())

	def iterator(self):
		iter = self.keys()
		ref = self.h
		def _hx_local_2():
			def _hx_local_0():
				return iter.hasNext()
			def _hx_local_1():
				i = iter.next()
				return ref.get(i,None)
			return _hx_AnonObject({'hasNext': _hx_local_0, 'next': _hx_local_1})
		return _hx_local_2()

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.h = None


@_hx_classes.registerClass("python.HaxeIterator", fields=["it","x","has","checked"], methods=["next","hasNext"])
class python_HaxeIterator:

	def __init__(self,it):
		self.it = None
		self.x = None
		self.has = None
		self.checked = None
		self.checked = False
		self.has = False
		self.x = None
		self.it = it

	def next(self):
		self.checked = False
		return self.x

	def hasNext(self):
		if self.checked:
			return self.has
		else:
			try:
				self.x = self.it.__next__()
				self.has = True
			except Exception as _hx_e:
				_hx_e1 = _hx_e.val if isinstance(_hx_e, _HxException) else _hx_e
				if python_lib_Builtin.isinstance(_hx_e1, StopIteration):
					s = _hx_e1
					self.has = False
					self.x = None
				else:
					raise _hx_e
			self.checked = True
			return self.has

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.it = None
		_hx_o.x = None
		_hx_o.has = None
		_hx_o.checked = None


@_hx_classes.registerClass("Sys", statics=["args","stdout","stderr"])
class Sys:

	@staticmethod
	def args():
		argv = python_lib_Sys.argv
		return argv[1:None]

	@staticmethod
	def stdout():
		return python_io_IoTools.createFileOutputFromText(python_lib_Sys.stdout)

	@staticmethod
	def stderr():
		return python_io_IoTools.createFileOutputFromText(python_lib_Sys.stderr)


@_hx_classes.registerClass("TableComparisonState", fields=["p","a","b","completed","run_to_completion","is_equal","is_equal_known","has_same_columns","has_same_columns_known"], methods=["reset"])
class TableComparisonState:

	def __init__(self):
		self.p = None
		self.a = None
		self.b = None
		self.completed = None
		self.run_to_completion = None
		self.is_equal = None
		self.is_equal_known = None
		self.has_same_columns = None
		self.has_same_columns_known = None
		self.reset()

	def reset(self):
		self.completed = False
		self.run_to_completion = True
		self.is_equal_known = False
		self.is_equal = False
		self.has_same_columns = False
		self.has_same_columns_known = False

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.p = None
		_hx_o.a = None
		_hx_o.b = None
		_hx_o.completed = None
		_hx_o.run_to_completion = None
		_hx_o.is_equal = None
		_hx_o.is_equal_known = None
		_hx_o.has_same_columns = None
		_hx_o.has_same_columns_known = None


@_hx_classes.registerClass("TableDiff", fields=["align","flags","l_prev","r_prev"], methods=["getSeparator","quoteForDiff","isReordered","spreadContext","reportUnit","hilite"])
class TableDiff:

	def __init__(self,align,flags):
		self.align = None
		self.flags = None
		self.l_prev = None
		self.r_prev = None
		self.align = align
		self.flags = flags

	def getSeparator(self,t,t2,root):
		sep = root
		w = Reflect.field(t,"get_width")()
		h = Reflect.field(t,"get_height")()
		view = t.getCellView()
		_g = 0
		while ((_g < h)):
			y = _g
			_g = (_g + 1)
			_g1 = 0
			while ((_g1 < w)):
				x = _g1
				_g1 = (_g1 + 1)
				txt = view.toString(t.getCell(x,y))
				if (txt is None):
					continue
				while ((txt.find(sep) >= 0)):
					sep = ("-" + HxOverrides.stringOrNull(sep))
		if (t2 is not None):
			w = Reflect.field(t2,"get_width")()
			h = Reflect.field(t2,"get_height")()
			_g2 = 0
			while ((_g2 < h)):
				y1 = _g2
				_g2 = (_g2 + 1)
				_g11 = 0
				while ((_g11 < w)):
					x1 = _g11
					_g11 = (_g11 + 1)
					txt1 = view.toString(t2.getCell(x1,y1))
					if (txt1 is None):
						continue
					while ((txt1.find(sep) >= 0)):
						sep = ("-" + HxOverrides.stringOrNull(sep))
		return sep

	def quoteForDiff(self,v,d):
		nil = "NULL"
		if v.equals(d,None):
			return nil
		str = v.toString(d)
		score = 0
		_g1 = 0
		_g = python_lib_Builtin.len(str)
		while ((_g1 < _g)):
			i = _g1
			_g1 = (_g1 + 1)
			if (HxString.charCodeAt(str,score) != 95):
				break
			score = (score + 1)
		if (HxString.substr(str,score,None) == nil):
			str = ("_" + HxOverrides.stringOrNull(str))
		return str

	def isReordered(self,m,ct):
		reordered = False
		l = -1
		r = -1
		_g = 0
		while ((_g < ct)):
			i = _g
			_g = (_g + 1)
			unit = m.h.get(i,None)
			if (unit is None):
				continue
			if (unit.l >= 0):
				if (unit.l < l):
					reordered = True
					break
				l = unit.l
			if (unit.r >= 0):
				if (unit.r < r):
					reordered = True
					break
				r = unit.r
		return reordered

	def spreadContext(self,units,_hx_del,active):
		if ((_hx_del > 0) and ((active is not None))):
			mark = (-_hx_del - 1)
			skips = 0
			_g1 = 0
			_g = python_lib_Builtin.len(units)
			while ((_g1 < _g)):
				i = _g1
				_g1 = (_g1 + 1)
				if ((active[i] if i >= 0 and i < python_lib_Builtin.len(active) else None) == -3):
					skips = (skips + 1)
					continue
				if (((active[i] if i >= 0 and i < python_lib_Builtin.len(active) else None) == 0) or (((active[i] if i >= 0 and i < python_lib_Builtin.len(active) else None) == 3))):
					if ((i - mark) <= ((_hx_del + skips))):
						python_internal_ArrayImpl._set(active, i, 2)
					elif ((i - mark) == (((_hx_del + 1) + skips))):
						python_internal_ArrayImpl._set(active, i, 3)
				elif ((active[i] if i >= 0 and i < python_lib_Builtin.len(active) else None) == 1):
					mark = i
					skips = 0
			mark = ((python_lib_Builtin.len(units) + _hx_del) + 1)
			skips = 0
			_g11 = 0
			_g2 = python_lib_Builtin.len(units)
			while ((_g11 < _g2)):
				j = _g11
				_g11 = (_g11 + 1)
				i1 = ((python_lib_Builtin.len(units) - 1) - j)
				if ((active[i1] if i1 >= 0 and i1 < python_lib_Builtin.len(active) else None) == -3):
					skips = (skips + 1)
					continue
				if (((active[i1] if i1 >= 0 and i1 < python_lib_Builtin.len(active) else None) == 0) or (((active[i1] if i1 >= 0 and i1 < python_lib_Builtin.len(active) else None) == 3))):
					if ((mark - i1) <= ((_hx_del + skips))):
						python_internal_ArrayImpl._set(active, i1, 2)
					elif ((mark - i1) == (((_hx_del + 1) + skips))):
						python_internal_ArrayImpl._set(active, i1, 3)
				elif ((active[i1] if i1 >= 0 and i1 < python_lib_Builtin.len(active) else None) == 1):
					mark = i1
					skips = 0

	def reportUnit(self,unit):
		txt = unit.toString()
		reordered = False
		if (unit.l >= 0):
			if (unit.l < self.l_prev):
				reordered = True
			self.l_prev = unit.l
		if (unit.r >= 0):
			if (unit.r < self.r_prev):
				reordered = True
			self.r_prev = unit.r
		if reordered:
			txt = (("[" + HxOverrides.stringOrNull(txt)) + "]")
		return txt

	def hilite(self,output):
		if (not output.isResizable()):
			return False
		output.resize(0,0)
		output.clear()
		row_map = haxe_ds_IntMap()
		col_map = haxe_ds_IntMap()
		order = self.align.toOrderPruned(True)
		units = order.getList()
		has_parent = (self.align.reference is not None)
		a = None
		b = None
		p = None
		ra_header = 0
		rb_header = 0
		is_index_p = haxe_ds_IntMap()
		is_index_a = haxe_ds_IntMap()
		is_index_b = haxe_ds_IntMap()
		if has_parent:
			p = self.align.getSource()
			a = self.align.reference.getTarget()
			b = self.align.getTarget()
			ra_header = self.align.reference.meta.getTargetHeader()
			rb_header = self.align.meta.getTargetHeader()
			if (self.align.getIndexColumns() is not None):
				_g = 0
				_g1 = self.align.getIndexColumns()
				while ((_g < python_lib_Builtin.len(_g1))):
					p2b = (_g1[_g] if _g >= 0 and _g < python_lib_Builtin.len(_g1) else None)
					_g = (_g + 1)
					if (p2b.l >= 0):
						is_index_p.set(p2b.l,True)
					if (p2b.r >= 0):
						is_index_b.set(p2b.r,True)
			if (self.align.reference.getIndexColumns() is not None):
				_g2 = 0
				_g11 = self.align.reference.getIndexColumns()
				while ((_g2 < python_lib_Builtin.len(_g11))):
					p2a = (_g11[_g2] if _g2 >= 0 and _g2 < python_lib_Builtin.len(_g11) else None)
					_g2 = (_g2 + 1)
					if (p2a.l >= 0):
						is_index_p.set(p2a.l,True)
					if (p2a.r >= 0):
						is_index_a.set(p2a.r,True)
		else:
			a = self.align.getSource()
			b = self.align.getTarget()
			p = a
			ra_header = self.align.meta.getSourceHeader()
			rb_header = self.align.meta.getTargetHeader()
			if (self.align.getIndexColumns() is not None):
				_g3 = 0
				_g12 = self.align.getIndexColumns()
				while ((_g3 < python_lib_Builtin.len(_g12))):
					a2b = (_g12[_g3] if _g3 >= 0 and _g3 < python_lib_Builtin.len(_g12) else None)
					_g3 = (_g3 + 1)
					if (a2b.l >= 0):
						is_index_a.set(a2b.l,True)
					if (a2b.r >= 0):
						is_index_b.set(a2b.r,True)
		column_order = self.align.meta.toOrderPruned(False)
		column_units = column_order.getList()
		show_rc_numbers = False
		row_moves = None
		col_moves = None
		if self.flags.ordered:
			row_moves = haxe_ds_IntMap()
			moves = Mover.moveUnits(units)
			_g13 = 0
			_g4 = python_lib_Builtin.len(moves)
			while ((_g13 < _g4)):
				i = _g13
				_g13 = (_g13 + 1)
				row_moves.set((moves[i] if i >= 0 and i < python_lib_Builtin.len(moves) else None),i)
				i
			col_moves = haxe_ds_IntMap()
			moves = Mover.moveUnits(column_units)
			_g14 = 0
			_g5 = python_lib_Builtin.len(moves)
			while ((_g14 < _g5)):
				i1 = _g14
				_g14 = (_g14 + 1)
				col_moves.set((moves[i1] if i1 >= 0 and i1 < python_lib_Builtin.len(moves) else None),i1)
				i1
		active = list()
		active_column = None
		if (not self.flags.show_unchanged):
			_g15 = 0
			_g6 = python_lib_Builtin.len(units)
			while ((_g15 < _g6)):
				i2 = _g15
				_g15 = (_g15 + 1)
				python_internal_ArrayImpl._set(active, i2, 0)
		allow_insert = self.flags.allowInsert()
		allow_delete = self.flags.allowDelete()
		allow_update = self.flags.allowUpdate()
		if (not self.flags.show_unchanged_columns):
			active_column = list()
			_g16 = 0
			_g7 = python_lib_Builtin.len(column_units)
			while ((_g16 < _g7)):
				i3 = _g16
				_g16 = (_g16 + 1)
				v = 0
				unit = (column_units[i3] if i3 >= 0 and i3 < python_lib_Builtin.len(column_units) else None)
				if ((unit.l >= 0) and is_index_a.h.get(unit.l,None)):
					v = 1
				if ((unit.r >= 0) and is_index_b.h.get(unit.r,None)):
					v = 1
				if ((unit.p >= 0) and is_index_p.h.get(unit.p,None)):
					v = 1
				python_internal_ArrayImpl._set(active_column, i3, v)
		outer_reps_needed = None
		if (self.flags.show_unchanged and self.flags.show_unchanged_columns):
			outer_reps_needed = 1
		else:
			outer_reps_needed = 2
		v1 = a.getCellView()
		sep = ""
		conflict_sep = ""
		schema = list()
		have_schema = False
		_g17 = 0
		_g8 = python_lib_Builtin.len(column_units)
		while ((_g17 < _g8)):
			j = _g17
			_g17 = (_g17 + 1)
			cunit = (column_units[j] if j >= 0 and j < python_lib_Builtin.len(column_units) else None)
			reordered = False
			if self.flags.ordered:
				if j in col_moves.h:
					reordered = True
				if reordered:
					show_rc_numbers = True
			act = ""
			if ((cunit.r >= 0) and ((cunit.lp() == -1))):
				have_schema = True
				act = "+++"
				if (active_column is not None):
					if allow_update:
						python_internal_ArrayImpl._set(active_column, j, 1)
			if ((cunit.r < 0) and ((cunit.lp() >= 0))):
				have_schema = True
				act = "---"
				if (active_column is not None):
					if allow_update:
						python_internal_ArrayImpl._set(active_column, j, 1)
			if ((cunit.r >= 0) and ((cunit.lp() >= 0))):
				if ((Reflect.field(a,"get_height")() >= ra_header) and ((Reflect.field(b,"get_height")() >= rb_header))):
					aa = a.getCell(cunit.lp(),ra_header)
					bb = b.getCell(cunit.r,rb_header)
					if (not v1.equals(aa,bb)):
						have_schema = True
						act = "("
						act = (HxOverrides.stringOrNull(act) + HxOverrides.stringOrNull(v1.toString(aa)))
						act = (HxOverrides.stringOrNull(act) + ")")
						if (active_column is not None):
							python_internal_ArrayImpl._set(active_column, j, 1)
			if reordered:
				act = (":" + HxOverrides.stringOrNull(act))
				have_schema = True
				if (active_column is not None):
					active_column = None
			schema.append(act)
		if have_schema:
			at = Reflect.field(output,"get_height")()
			output.resize((python_lib_Builtin.len(column_units) + 1),(at + 1))
			output.setCell(0,at,v1.toDatum("!"))
			_g18 = 0
			_g9 = python_lib_Builtin.len(column_units)
			while ((_g18 < _g9)):
				j1 = _g18
				_g18 = (_g18 + 1)
				output.setCell((j1 + 1),at,v1.toDatum((schema[j1] if j1 >= 0 and j1 < python_lib_Builtin.len(schema) else None)))
		top_line_done = False
		if self.flags.always_show_header:
			at1 = Reflect.field(output,"get_height")()
			output.resize((python_lib_Builtin.len(column_units) + 1),(at1 + 1))
			output.setCell(0,at1,v1.toDatum("@@"))
			_g19 = 0
			_g10 = python_lib_Builtin.len(column_units)
			while ((_g19 < _g10)):
				j2 = _g19
				_g19 = (_g19 + 1)
				cunit1 = (column_units[j2] if j2 >= 0 and j2 < python_lib_Builtin.len(column_units) else None)
				if (cunit1.r >= 0):
					if (Reflect.field(b,"get_height")() > 0):
						output.setCell((j2 + 1),at1,b.getCell(cunit1.r,rb_header))
				elif (cunit1.lp() >= 0):
					if (Reflect.field(a,"get_height")() > 0):
						output.setCell((j2 + 1),at1,a.getCell(cunit1.lp(),ra_header))
				col_map.set((j2 + 1),cunit1)
			top_line_done = True
		_g20 = 0
		while ((_g20 < outer_reps_needed)):
			out = _g20
			_g20 = (_g20 + 1)
			if (out == 1):
				self.spreadContext(units,self.flags.unchanged_context,active)
				self.spreadContext(column_units,self.flags.unchanged_column_context,active_column)
				if (active_column is not None):
					_g21 = 0
					_g110 = python_lib_Builtin.len(column_units)
					while ((_g21 < _g110)):
						i4 = _g21
						_g21 = (_g21 + 1)
						if ((active_column[i4] if i4 >= 0 and i4 < python_lib_Builtin.len(active_column) else None) == 3):
							python_internal_ArrayImpl._set(active_column, i4, 0)
			showed_dummy = False
			l = -1
			r = -1
			_g22 = 0
			_g111 = python_lib_Builtin.len(units)
			while ((_g22 < _g111)):
				i5 = _g22
				_g22 = (_g22 + 1)
				unit1 = (units[i5] if i5 >= 0 and i5 < python_lib_Builtin.len(units) else None)
				reordered1 = False
				if self.flags.ordered:
					if i5 in row_moves.h:
						reordered1 = True
					if reordered1:
						show_rc_numbers = True
				if ((unit1.r < 0) and ((unit1.l < 0))):
					continue
				if (((unit1.r == 0) and ((unit1.lp() == 0))) and top_line_done):
					continue
				act1 = ""
				if reordered1:
					act1 = ":"
				publish = self.flags.show_unchanged
				dummy = False
				if (out == 1):
					publish = ((active[i5] if i5 >= 0 and i5 < python_lib_Builtin.len(active) else None) > 0)
					dummy = ((active[i5] if i5 >= 0 and i5 < python_lib_Builtin.len(active) else None) == 3)
					if (dummy and showed_dummy):
						continue
					if (not publish):
						continue
				if (not dummy):
					showed_dummy = False
				at2 = Reflect.field(output,"get_height")()
				if publish:
					output.resize((python_lib_Builtin.len(column_units) + 1),(at2 + 1))
				if dummy:
					_g41 = 0
					_g31 = (python_lib_Builtin.len(column_units) + 1)
					while ((_g41 < _g31)):
						j3 = _g41
						_g41 = (_g41 + 1)
						output.setCell(j3,at2,v1.toDatum("..."))
						showed_dummy = True
					continue
				have_addition = False
				skip = False
				if (((unit1.p < 0) and ((unit1.l < 0))) and ((unit1.r >= 0))):
					if (not allow_insert):
						skip = True
					act1 = "+++"
				if (((((unit1.p >= 0) or (not has_parent))) and ((unit1.l >= 0))) and ((unit1.r < 0))):
					if (not allow_delete):
						skip = True
					act1 = "---"
				if skip:
					if (not publish):
						if (active is not None):
							python_internal_ArrayImpl._set(active, i5, -3)
					continue
				_g42 = 0
				_g32 = python_lib_Builtin.len(column_units)
				while ((_g42 < _g32)):
					j4 = _g42
					_g42 = (_g42 + 1)
					cunit2 = (column_units[j4] if j4 >= 0 and j4 < python_lib_Builtin.len(column_units) else None)
					pp = None
					ll = None
					rr = None
					dd = None
					dd_to = None
					have_dd_to = False
					dd_to_alt = None
					have_dd_to_alt = False
					have_pp = False
					have_ll = False
					have_rr = False
					if ((cunit2.p >= 0) and ((unit1.p >= 0))):
						pp = p.getCell(cunit2.p,unit1.p)
						have_pp = True
					if ((cunit2.l >= 0) and ((unit1.l >= 0))):
						ll = a.getCell(cunit2.l,unit1.l)
						have_ll = True
					if ((cunit2.r >= 0) and ((unit1.r >= 0))):
						rr = b.getCell(cunit2.r,unit1.r)
						have_rr = True
						if (((cunit2.p if (have_pp) else cunit2.l)) < 0):
							if (rr is not None):
								if (v1.toString(rr) != ""):
									if self.flags.allowUpdate():
										have_addition = True
					if have_pp:
						if (not have_rr):
							dd = pp
						elif v1.equals(pp,rr):
							dd = pp
						else:
							dd = pp
							dd_to = rr
							have_dd_to = True
							if (not v1.equals(pp,ll)):
								if (not v1.equals(pp,rr)):
									dd_to_alt = ll
									have_dd_to_alt = True
					elif have_ll:
						if (not have_rr):
							dd = ll
						elif v1.equals(ll,rr):
							dd = ll
						else:
							dd = ll
							dd_to = rr
							have_dd_to = True
					else:
						dd = rr
					txt = None
					if (have_dd_to and allow_update):
						if (active_column is not None):
							python_internal_ArrayImpl._set(active_column, j4, 1)
						txt = self.quoteForDiff(v1,dd)
						if (sep == ""):
							sep = self.getSeparator(a,b,"->")
						is_conflict = False
						if have_dd_to_alt:
							if (not v1.equals(dd_to,dd_to_alt)):
								is_conflict = True
						if (not is_conflict):
							txt = ((HxOverrides.stringOrNull(txt) + HxOverrides.stringOrNull(sep)) + HxOverrides.stringOrNull(self.quoteForDiff(v1,dd_to)))
							if (python_lib_Builtin.len(sep) > python_lib_Builtin.len(act1)):
								act1 = sep
						else:
							if (conflict_sep == ""):
								conflict_sep = (HxOverrides.stringOrNull(self.getSeparator(p,a,"!")) + HxOverrides.stringOrNull(sep))
							txt = ((((HxOverrides.stringOrNull(txt) + HxOverrides.stringOrNull(conflict_sep)) + HxOverrides.stringOrNull(self.quoteForDiff(v1,dd_to_alt))) + HxOverrides.stringOrNull(conflict_sep)) + HxOverrides.stringOrNull(self.quoteForDiff(v1,dd_to)))
							act1 = conflict_sep
					if ((act1 == "") and have_addition):
						act1 = "+"
					if (act1 == "+++"):
						if have_rr:
							if (active_column is not None):
								python_internal_ArrayImpl._set(active_column, j4, 1)
					if publish:
						if ((active_column is None) or (((active_column[j4] if j4 >= 0 and j4 < python_lib_Builtin.len(active_column) else None) > 0))):
							if (txt is not None):
								output.setCell((j4 + 1),at2,v1.toDatum(txt))
							else:
								output.setCell((j4 + 1),at2,dd)
				if publish:
					output.setCell(0,at2,v1.toDatum(act1))
					row_map.set(at2,unit1)
				if (act1 != ""):
					if (not publish):
						if (active is not None):
							python_internal_ArrayImpl._set(active, i5, 1)
		if (not show_rc_numbers):
			if self.flags.always_show_order:
				show_rc_numbers = True
			elif self.flags.ordered:
				show_rc_numbers = self.isReordered(row_map,Reflect.field(output,"get_height")())
				if (not show_rc_numbers):
					show_rc_numbers = self.isReordered(col_map,Reflect.field(output,"get_width")())
		admin_w = 1
		if (show_rc_numbers and (not self.flags.never_show_order)):
			admin_w = (admin_w + 1)
			target = list()
			_g112 = 0
			_g23 = Reflect.field(output,"get_width")()
			while ((_g112 < _g23)):
				i6 = _g112
				_g112 = (_g112 + 1)
				target.append((i6 + 1))
			output.insertOrDeleteColumns(target,(Reflect.field(output,"get_width")() + 1))
			self.l_prev = -1
			self.r_prev = -1
			_g113 = 0
			_g24 = Reflect.field(output,"get_height")()
			while ((_g113 < _g24)):
				i7 = _g113
				_g113 = (_g113 + 1)
				unit2 = row_map.h.get(i7,None)
				if (unit2 is None):
					continue
				output.setCell(0,i7,self.reportUnit(unit2))
			target = list()
			_g114 = 0
			_g25 = Reflect.field(output,"get_height")()
			while ((_g114 < _g25)):
				i8 = _g114
				_g114 = (_g114 + 1)
				target.append((i8 + 1))
			output.insertOrDeleteRows(target,(Reflect.field(output,"get_height")() + 1))
			self.l_prev = -1
			self.r_prev = -1
			_g115 = 1
			_g26 = Reflect.field(output,"get_width")()
			while ((_g115 < _g26)):
				i9 = _g115
				_g115 = (_g115 + 1)
				unit3 = col_map.h.get((i9 - 1),None)
				if (unit3 is None):
					continue
				output.setCell(i9,0,self.reportUnit(unit3))
			output.setCell(0,0,"@:@")
		if (active_column is not None):
			all_active = True
			_g116 = 0
			_g27 = python_lib_Builtin.len(active_column)
			while ((_g116 < _g27)):
				i10 = _g116
				_g116 = (_g116 + 1)
				if ((active_column[i10] if i10 >= 0 and i10 < python_lib_Builtin.len(active_column) else None) == 0):
					all_active = False
					break
			if (not all_active):
				fate = list()
				_g28 = 0
				while ((_g28 < admin_w)):
					i11 = _g28
					_g28 = (_g28 + 1)
					fate.append(i11)
				at3 = admin_w
				ct = 0
				dots = list()
				_g117 = 0
				_g29 = python_lib_Builtin.len(active_column)
				while ((_g117 < _g29)):
					i12 = _g117
					_g117 = (_g117 + 1)
					off = ((active_column[i12] if i12 >= 0 and i12 < python_lib_Builtin.len(active_column) else None) == 0)
					if off:
						ct = (ct + 1)
					else:
						ct = 0
					if (off and ((ct > 1))):
						fate.append(-1)
					else:
						if off:
							dots.append(at3)
						fate.append(at3)
						at3 = (at3 + 1)
				output.insertOrDeleteColumns(fate,at3)
				_g30 = 0
				while ((_g30 < python_lib_Builtin.len(dots))):
					d = (dots[_g30] if _g30 >= 0 and _g30 < python_lib_Builtin.len(dots) else None)
					_g30 = (_g30 + 1)
					_g210 = 0
					_g118 = Reflect.field(output,"get_height")()
					while ((_g210 < _g118)):
						j5 = _g210
						_g210 = (_g210 + 1)
						output.setCell(d,j5,"...")
		return True

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.align = None
		_hx_o.flags = None
		_hx_o.l_prev = None
		_hx_o.r_prev = None


@_hx_classes.registerClass("TableIO", methods=["getContent","saveContent","args","writeStdout","writeStderr"])
class TableIO:

	def __init__(self):
		pass

	def getContent(self,name):
		return sys_io_File.getContent(name)

	def saveContent(self,name,txt):
		sys_io_File.saveContent(name,txt)
		return True

	def args(self):
		return Sys.args()

	def writeStdout(self,txt):
		Sys.stdout().writeString(txt)

	def writeStderr(self,txt):
		Sys.stderr().writeString(txt)

	@staticmethod
	def _hx_empty_init(_hx_o):		pass


@_hx_classes.registerClass("TableModifier", fields=["t"], methods=["removeColumn"])
class TableModifier:

	def __init__(self,t):
		self.t = None
		self.t = t

	def removeColumn(self,at):
		fate = []
		_g1 = 0
		_g = Reflect.field(self.t,"get_width")()
		while ((_g1 < _g)):
			i = _g1
			_g1 = (_g1 + 1)
			if (i < at):
				fate.append(i)
			elif (i > at):
				fate.append((i - 1))
			else:
				fate.append(-1)
		return self.t.insertOrDeleteColumns(fate,(Reflect.field(self.t,"get_width")() - 1))

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.t = None


@_hx_classes.registerClass("TableText", fields=["rows","view"], methods=["getCellText"])
class TableText:

	def __init__(self,rows):
		self.rows = None
		self.view = None
		self.rows = rows
		self.view = rows.getCellView()

	def getCellText(self,x,y):
		return self.view.toString(self.rows.getCell(x,y))

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.rows = None
		_hx_o.view = None


@_hx_classes.registerClass("TableView", methods=["toString","getBag","getTable","hasStructure","equals","toDatum"], interfaces=[View])
class TableView:

	def __init__(self):
		pass

	def toString(self,d):
		return ("" + Std.string(d))

	def getBag(self,d):
		return None

	def getTable(self,d):
		table = d
		return table

	def hasStructure(self,d):
		return True

	def equals(self,d1,d2):
		haxe_Log.trace("TableView.equals called",_hx_AnonObject({'fileName': "TableView.hx", 'lineNumber': 30, 'className': "TableView", 'methodName': "equals"}))
		return False

	def toDatum(self,str):
		return SimpleCell(str)

	@staticmethod
	def _hx_empty_init(_hx_o):		pass

@_hx_classes.registerEnum("ValueType", ["TNull","TInt","TFloat","TBool","TObject","TFunction","TClass","TEnum","TUnknown"])
class ValueType(Enum):
	def __init__(self, t, i, p):
		super(ValueType,self).__init__(t, i, p)

	@staticmethod
	def TClass(c):
		return ValueType("TClass", 6, [c])

	@staticmethod
	def TEnum(e):
		return ValueType("TEnum", 7, [e])
ValueType.TNull = ValueType("TNull", 0, list())
ValueType.TInt = ValueType("TInt", 1, list())
ValueType.TFloat = ValueType("TFloat", 2, list())
ValueType.TBool = ValueType("TBool", 3, list())
ValueType.TObject = ValueType("TObject", 4, list())
ValueType.TFunction = ValueType("TFunction", 5, list())
ValueType.TUnknown = ValueType("TUnknown", 8, list())


@_hx_classes.registerClass("Type", statics=["typeof"])
class Type:

	@staticmethod
	def typeof(v):
		if (v is None):
			return ValueType.TNull
		elif python_lib_Builtin.isinstance(v,python_lib_Builtin.bool):
			return ValueType.TBool
		elif python_lib_Builtin.isinstance(v,python_lib_Builtin.int):
			return ValueType.TInt
		elif python_lib_Builtin.isinstance(v,python_lib_Builtin.float):
			return ValueType.TFloat
		elif python_lib_Builtin.isinstance(v,String):
			return ValueType.TClass(String)
		elif python_lib_Builtin.isinstance(v,list):
			return ValueType.TClass(list)
		elif (python_lib_Builtin.isinstance(v,_hx_AnonObject) or python_lib_Inspect.isclass(v)):
			return ValueType.TObject
		elif python_lib_Builtin.isinstance(v,Enum):
			return ValueType.TEnum(v.__class__)
		elif (python_lib_Builtin.isinstance(v,python_lib_Builtin.type) or python_internal_HxBuiltin.hasattr(v,"_hx_class")):
			return ValueType.TClass(v.__class__)
		elif python_lib_Builtin.callable(v):
			return ValueType.TFunction
		else:
			return ValueType.TUnknown


@_hx_classes.registerClass("Unit", fields=["l","r","p"], methods=["lp","toString","fromString"], statics=["describe"])
class Unit:

	def __init__(self,l = -2,r = -2,p = -2):
		if (l is None):
			l = -2
		if (r is None):
			r = -2
		if (p is None):
			p = -2
		self.l = None
		self.r = None
		self.p = None
		self.l = l
		self.r = r
		self.p = p

	def lp(self):
		if (self.p == -2):
			return self.l
		else:
			return self.p

	def toString(self):
		if (self.p >= -1):
			return ((((HxOverrides.stringOrNull(Unit.describe(self.p)) + "|") + HxOverrides.stringOrNull(Unit.describe(self.l))) + ":") + HxOverrides.stringOrNull(Unit.describe(self.r)))
		return ((HxOverrides.stringOrNull(Unit.describe(self.l)) + ":") + HxOverrides.stringOrNull(Unit.describe(self.r)))

	def fromString(self,txt):
		txt = (HxOverrides.stringOrNull(txt) + "]")
		at = 0
		_g1 = 0
		_g = python_lib_Builtin.len(txt)
		while ((_g1 < _g)):
			i = _g1
			_g1 = (_g1 + 1)
			ch = HxString.charCodeAt(txt,i)
			if ((ch >= 48) and ((ch <= 57))):
				at = (at * 10)
				at = (at + ((ch - 48)))
			elif (ch == 45):
				at = -1
			elif (ch == 124):
				self.p = at
				at = 0
			elif (ch == 58):
				self.l = at
				at = 0
			elif (ch == 93):
				self.r = at
				return True
		return False

	@staticmethod
	def describe(i):
		if (i >= 0):
			return ("" + Std.string(i))
		else:
			return "-"

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.l = None
		_hx_o.r = None
		_hx_o.p = None


@_hx_classes.registerClass("ViewedDatum", fields=["datum","view"], methods=["toString","getBag","getTable","hasStructure"], statics=["getSimpleView"])
class ViewedDatum:

	def __init__(self,datum,view):
		self.datum = None
		self.view = None
		self.datum = datum
		self.view = view

	def toString(self):
		return self.view.toString(self.datum)

	def getBag(self):
		return self.view.getBag(self.datum)

	def getTable(self):
		return self.view.getTable(self.datum)

	def hasStructure(self):
		return self.view.hasStructure(self.datum)

	@staticmethod
	def getSimpleView(datum):
		return ViewedDatum(datum, SimpleView())

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.datum = None
		_hx_o.view = None


@_hx_classes.registerClass("Viterbi", fields=["K","T","index","mode","path_valid","best_cost","cost","src","path"], methods=["reset","setSize","assertMode","addTransition","endTransitions","beginTransitions","calculatePath","toString","length","get","getCost"])
class Viterbi:

	def __init__(self):
		self.K = None
		self.T = None
		self.index = None
		self.mode = None
		self.path_valid = None
		self.best_cost = None
		self.cost = None
		self.src = None
		self.path = None
		def _hx_local_0():
			self.T = 0
			return self.T
		self.K = _hx_local_0()
		self.reset()
		self.cost = SparseSheet()
		self.src = SparseSheet()
		self.path = SparseSheet()

	def reset(self):
		self.index = 0
		self.mode = 0
		self.path_valid = False
		self.best_cost = 0

	def setSize(self,states,sequence_length):
		self.K = states
		self.T = sequence_length
		self.cost.resize(self.K,self.T,0)
		self.src.resize(self.K,self.T,-1)
		self.path.resize(1,self.T,-1)

	def assertMode(self,next):
		if ((next == 0) and ((self.mode == 1))):
			_hx_local_0 = self
			_hx_local_1 = _hx_local_0.index
			_hx_local_0.index = (_hx_local_1 + 1)
			_hx_local_1
		self.mode = next

	def addTransition(self,s0,s1,c):
		resize = False
		if (s0 >= self.K):
			self.K = (s0 + 1)
			resize = True
		if (s1 >= self.K):
			self.K = (s1 + 1)
			resize = True
		if resize:
			self.cost.nonDestructiveResize(self.K,self.T,0)
			self.src.nonDestructiveResize(self.K,self.T,-1)
			self.path.nonDestructiveResize(1,self.T,-1)
		self.path_valid = False
		self.assertMode(1)
		if (self.index >= self.T):
			self.T = (self.index + 1)
			self.cost.nonDestructiveResize(self.K,self.T,0)
			self.src.nonDestructiveResize(self.K,self.T,-1)
			self.path.nonDestructiveResize(1,self.T,-1)
		sourced = False
		if (self.index > 0):
			c = (c + self.cost.get(s0,(self.index - 1)))
			sourced = (self.src.get(s0,(self.index - 1)) != -1)
		else:
			sourced = True
		if sourced:
			if ((c < self.cost.get(s1,self.index)) or ((self.src.get(s1,self.index) == -1))):
				self.cost.set(s1,self.index,c)
				self.src.set(s1,self.index,s0)

	def endTransitions(self):
		self.path_valid = False
		self.assertMode(0)

	def beginTransitions(self):
		self.path_valid = False
		self.assertMode(1)

	def calculatePath(self):
		if self.path_valid:
			return
		self.endTransitions()
		best = 0
		bestj = -1
		if (self.index <= 0):
			self.path_valid = True
			return
		_g1 = 0
		_g = self.K
		while ((_g1 < _g)):
			j = _g1
			_g1 = (_g1 + 1)
			if ((((self.cost.get(j,(self.index - 1)) < best) or ((bestj == -1)))) and ((self.src.get(j,(self.index - 1)) != -1))):
				best = self.cost.get(j,(self.index - 1))
				bestj = j
		self.best_cost = best
		_g11 = 0
		_g2 = self.index
		while ((_g11 < _g2)):
			j1 = _g11
			_g11 = (_g11 + 1)
			i = ((self.index - 1) - j1)
			self.path.set(0,i,bestj)
			if (not (((bestj != -1) and (((bestj >= 0) and ((bestj < self.K))))))):
				haxe_Log.trace("Problem in Viterbi",_hx_AnonObject({'fileName': "Viterbi.hx", 'lineNumber': 119, 'className': "Viterbi", 'methodName': "calculatePath"}))
			bestj = self.src.get(bestj,i)
		self.path_valid = True

	def toString(self):
		self.calculatePath()
		txt = ""
		_g1 = 0
		_g = self.index
		while ((_g1 < _g)):
			i = _g1
			_g1 = (_g1 + 1)
			if (self.path.get(0,i) == -1):
				txt = (HxOverrides.stringOrNull(txt) + "*")
			else:
				txt = (HxOverrides.stringOrNull(txt) + Std.string(self.path.get(0,i)))
			if (self.K >= 10):
				txt = (HxOverrides.stringOrNull(txt) + " ")
		txt = (HxOverrides.stringOrNull(txt) + HxOverrides.stringOrNull(((" costs " + Std.string(self.getCost())))))
		return txt

	def length(self):
		if (self.index > 0):
			self.calculatePath()
		return self.index

	def get(self,i):
		self.calculatePath()
		return self.path.get(0,i)

	def getCost(self):
		self.calculatePath()
		return self.best_cost

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.K = None
		_hx_o.T = None
		_hx_o.index = None
		_hx_o.mode = None
		_hx_o.path_valid = None
		_hx_o.best_cost = None
		_hx_o.cost = None
		_hx_o.src = None
		_hx_o.path = None


@_hx_classes.registerClass("Workspace", fields=["parent","local","remote","report","tparent","tlocal","tremote","p2l","p2r","l2r"])
class Workspace:

	def __init__(self):
		self.parent = None
		self.local = None
		self.remote = None
		self.report = None
		self.tparent = None
		self.tlocal = None
		self.tremote = None
		self.p2l = None
		self.p2r = None
		self.l2r = None
		pass

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.parent = None
		_hx_o.local = None
		_hx_o.remote = None
		_hx_o.report = None
		_hx_o.tparent = None
		_hx_o.tlocal = None
		_hx_o.tremote = None
		_hx_o.p2l = None
		_hx_o.p2r = None
		_hx_o.l2r = None


@_hx_classes.registerClass("haxe.Log", statics=["trace"])
class haxe_Log:

	@staticmethod
	def trace(v,infos = None):
		str = None
		if (infos is not None):
			str = ((((HxOverrides.stringOrNull(infos.fileName) + ":") + Std.string(infos.lineNumber)) + ": ") + Std.string(v))
			if (Reflect.field(infos,"customParams") is not None):
				str = (HxOverrides.stringOrNull(str) + HxOverrides.stringOrNull((("," + HxOverrides.stringOrNull(",".join([python_Boot.toString1(x1,'') for x1 in Reflect.field(infos,"customParams")]))))))
		else:
			str = v
		python_Lib.println(str)


@_hx_classes.registerClass("haxe.ds.IntMap", fields=["h"], methods=["set","remove","keys","toString"], interfaces=[IMap])
class haxe_ds_IntMap:

	def __init__(self):
		self.h = None
		self.h = python_lib_Dict()

	def set(self,key,value):
		self.h[key] = value

	def remove(self,key):
		if (not key in self.h):
			return False
		del self.h[key]
		return True

	def keys(self):
		this1 = None
		_this = self.h.keys()
		this1 = python_lib_Builtin.iter(_this)
		return python_HaxeIterator(this1)

	def toString(self):
		s_b = python_lib_io_StringIO()
		s = "{"
		s_b.write(s)
		it = self.keys()
		_hx_local_0 = it
		while (_hx_local_0.hasNext()):
			i = _hx_local_0.next()
			s1 = Std.string(i)
			s_b.write(s1)
			s2 = " => "
			s_b.write(s2)
			x = Std.string(self.h.get(i,None))
			s3 = Std.string(x)
			s_b.write(s3)
			if it.hasNext():
				s4 = ", "
				s_b.write(s4)
		s5 = "}"
		s_b.write(s5)
		return s_b.getvalue()

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.h = None


@_hx_classes.registerClass("haxe.format.JsonPrinter", fields=["buf","replacer","indent","pretty","nind"], methods=["write","fieldsString","quote"], statics=["print"])
class haxe_format_JsonPrinter:

	def __init__(self,replacer,space):
		self.buf = None
		self.replacer = None
		self.indent = None
		self.pretty = None
		self.nind = None
		self.replacer = replacer
		self.indent = space
		self.pretty = (space is not None)
		self.nind = 0
		self.buf = StringBuf()

	def write(self,k,v):
		if (self.replacer is not None):
			v = self.replacer(k,v)
		_g = Type.typeof(v)
		if ((_g.index) == 8):
			s = "\"???\""
			self.buf.b.write(s)
		elif ((_g.index) == 4):
			self.fieldsString(v,python_Boot.fields(v))
		elif ((_g.index) == 1):
			v1 = v
			s1 = Std.string(v1)
			self.buf.b.write(s1)
		elif ((_g.index) == 2):
			v2 = None
			def _hx_local_0():
				f = v
				return (((f != Math.POSITIVE_INFINITY) and ((f != Math.NEGATIVE_INFINITY))) and (not python_lib_Math.isnan(f)))
			if _hx_local_0():
				v2 = v
			else:
				v2 = "null"
			s2 = Std.string(v2)
			self.buf.b.write(s2)
		elif ((_g.index) == 5):
			s3 = "\"<fun>\""
			self.buf.b.write(s3)
		elif ((_g.index) == 6):
			c = _g.params[0]
			if (c == String):
				self.quote(v)
			elif (c == list):
				v3 = v
				s4 = None
				c1 = 91
				s4 = "".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c1]))
				self.buf.b.write(s4)
				len = python_lib_Builtin.len(v3)
				last = (len - 1)
				_g1 = 0
				while ((_g1 < len)):
					i = _g1
					_g1 = (_g1 + 1)
					if (i > 0):
						s5 = None
						c2 = 44
						s5 = "".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c2]))
						self.buf.b.write(s5)
					else:
						_hx_local_1 = self
						_hx_local_2 = _hx_local_1.nind
						_hx_local_1.nind = (_hx_local_2 + 1)
						_hx_local_2
					if self.pretty:
						s6 = None
						c3 = 10
						s6 = "".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c3]))
						self.buf.b.write(s6)
					if self.pretty:
						v4 = StringTools.lpad("",self.indent,(self.nind * python_lib_Builtin.len(self.indent)))
						s7 = Std.string(v4)
						self.buf.b.write(s7)
					self.write(i,(v3[i] if i >= 0 and i < python_lib_Builtin.len(v3) else None))
					if (i == last):
						_hx_local_3 = self
						_hx_local_4 = _hx_local_3.nind
						_hx_local_3.nind = (_hx_local_4 - 1)
						_hx_local_4
						if self.pretty:
							s8 = None
							c4 = 10
							s8 = "".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c4]))
							self.buf.b.write(s8)
						if self.pretty:
							v5 = StringTools.lpad("",self.indent,(self.nind * python_lib_Builtin.len(self.indent)))
							s9 = Std.string(v5)
							self.buf.b.write(s9)
				s10 = None
				c5 = 93
				s10 = "".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c5]))
				self.buf.b.write(s10)
			elif (c == haxe_ds_StringMap):
				v6 = v
				o = _hx_AnonObject({})
				_hx_local_5 = v6.keys()
				while (_hx_local_5.hasNext()):
					k1 = _hx_local_5.next()
					Reflect.setField(o,k1,v6.h.get(k1,None))
				self.fieldsString(o,python_Boot.fields(o))
			elif (c == Date):
				v7 = v
				self.quote(v7.toString())
			else:
				self.fieldsString(v,python_Boot.fields(v))
		elif ((_g.index) == 7):
			i1 = None
			e = v
			i1 = e.index
			v8 = i1
			s11 = Std.string(v8)
			self.buf.b.write(s11)
		elif ((_g.index) == 3):
			v9 = v
			s12 = Std.string(v9)
			self.buf.b.write(s12)
		elif ((_g.index) == 0):
			s13 = "null"
			self.buf.b.write(s13)
		else:
			pass

	def fieldsString(self,v,fields):
		s = None
		c = 123
		s = "".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c]))
		self.buf.b.write(s)
		len = python_lib_Builtin.len(fields)
		last = (len - 1)
		first = True
		_g = 0
		while ((_g < len)):
			i = _g
			_g = (_g + 1)
			f = (fields[i] if i >= 0 and i < python_lib_Builtin.len(fields) else None)
			value = Reflect.field(v,f)
			if Reflect.isFunction(value):
				continue
			if first:
				_hx_local_0 = self
				_hx_local_1 = _hx_local_0.nind
				_hx_local_0.nind = (_hx_local_1 + 1)
				_hx_local_1
				first = False
			else:
				s1 = None
				c1 = 44
				s1 = "".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c1]))
				self.buf.b.write(s1)
			if self.pretty:
				s2 = None
				c2 = 10
				s2 = "".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c2]))
				self.buf.b.write(s2)
			if self.pretty:
				v1 = StringTools.lpad("",self.indent,(self.nind * python_lib_Builtin.len(self.indent)))
				s3 = Std.string(v1)
				self.buf.b.write(s3)
			self.quote(f)
			s4 = None
			c3 = 58
			s4 = "".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c3]))
			self.buf.b.write(s4)
			if self.pretty:
				s5 = None
				c4 = 32
				s5 = "".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c4]))
				self.buf.b.write(s5)
			self.write(f,value)
			if (i == last):
				_hx_local_2 = self
				_hx_local_3 = _hx_local_2.nind
				_hx_local_2.nind = (_hx_local_3 - 1)
				_hx_local_3
				if self.pretty:
					s6 = None
					c5 = 10
					s6 = "".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c5]))
					self.buf.b.write(s6)
				if self.pretty:
					v2 = StringTools.lpad("",self.indent,(self.nind * python_lib_Builtin.len(self.indent)))
					s7 = Std.string(v2)
					self.buf.b.write(s7)
		s8 = None
		c6 = 125
		s8 = "".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c6]))
		self.buf.b.write(s8)

	def quote(self,s):
		s1 = None
		c = 34
		s1 = "".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c]))
		self.buf.b.write(s1)
		i = 0
		while (True):
			c1 = None
			index = i
			i = (i + 1)
			if (index >= python_lib_Builtin.len(s)):
				c1 = -1
			else:
				c1 = python_lib_Builtin.ord(s[index])
			if (c1 == -1):
				break
			if ((c1) == 34):
				s2 = "\\\""
				self.buf.b.write(s2)
			elif ((c1) == 92):
				s3 = "\\\\"
				self.buf.b.write(s3)
			elif ((c1) == 10):
				s4 = "\\n"
				self.buf.b.write(s4)
			elif ((c1) == 13):
				s5 = "\\r"
				self.buf.b.write(s5)
			elif ((c1) == 9):
				s6 = "\\t"
				self.buf.b.write(s6)
			elif ((c1) == 8):
				s7 = "\\b"
				self.buf.b.write(s7)
			elif ((c1) == 12):
				s8 = "\\f"
				self.buf.b.write(s8)
			else:
				s9 = None
				c2 = c1
				s9 = "".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c2]))
				self.buf.b.write(s9)
		s10 = None
		c3 = 34
		s10 = "".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c3]))
		self.buf.b.write(s10)

	@staticmethod
	def _hx_print(o,replacer = None,space = None):
		printer = haxe_format_JsonPrinter(replacer, space)
		printer.write("",o)
		return printer.buf.b.getvalue()

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.buf = None
		_hx_o.replacer = None
		_hx_o.indent = None
		_hx_o.pretty = None
		_hx_o.nind = None


@_hx_classes.registerClass("haxe.io.Bytes", fields=["length","b"], statics=["ofString"])
class haxe_io_Bytes:

	def __init__(self,length,b):
		self.length = None
		self.b = None
		self.length = length
		self.b = b

	@staticmethod
	def ofString(s):
		b = python_lib_Builtin.bytearray(s,"UTF-8")
		return haxe_io_Bytes(python_lib_Builtin.len(b), b)

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.length = None
		_hx_o.b = None


@_hx_classes.registerClass("haxe.io.Output", methods=["writeByte","writeBytes","writeFullBytes","writeString"])
class haxe_io_Output:

	def writeByte(self,c):
		raise _HxException("Not implemented")

	def writeBytes(self,s,pos,len):
		k = len
		b = s.b
		if (((pos < 0) or ((len < 0))) or (((pos + len) > s.length))):
			raise _HxException(haxe_io_Error.OutsideBounds)
		while ((k > 0)):
			self.writeByte(b[pos])
			pos = (pos + 1)
			k = (k - 1)
		return len

	def writeFullBytes(self,s,pos,len):
		while ((len > 0)):
			k = self.writeBytes(s,pos,len)
			pos = (pos + k)
			len = (len - k)

	def writeString(self,s):
		b = haxe_io_Bytes.ofString(s)
		self.writeFullBytes(b,0,b.length)

	@staticmethod
	def _hx_empty_init(_hx_o):		pass


@_hx_classes.registerClass("haxe.io.Eof", methods=["toString"])
class haxe_io_Eof:

	def toString(self):
		return "Eof"

	@staticmethod
	def _hx_empty_init(_hx_o):		pass

@_hx_classes.registerEnum("haxe.io.Error", ["Blocked","Overflow","OutsideBounds","Custom"])
class haxe_io_Error(Enum):
	def __init__(self, t, i, p):
		super(haxe_io_Error,self).__init__(t, i, p)

	@staticmethod
	def Custom(e):
		return haxe_io_Error("Custom", 3, [e])
haxe_io_Error.Blocked = haxe_io_Error("Blocked", 0, list())
haxe_io_Error.Overflow = haxe_io_Error("Overflow", 1, list())
haxe_io_Error.OutsideBounds = haxe_io_Error("OutsideBounds", 2, list())


@_hx_classes.registerClass("python.Lib", statics=["println","dictToAnon"])
class python_Lib:

	@staticmethod
	def println(v):
		str = Std.string(v)
		python_lib_Sys.stdout.buffer.write((("" + HxOverrides.stringOrNull(str)) + "\n").encode("utf-8", "strict"))
		python_lib_Sys.stdout.flush()

	@staticmethod
	def dictToAnon(v):
		return _hx_AnonObject(v.copy())


@_hx_classes.registerClass("python.NativeStringTools", statics=["encode"])
class python_NativeStringTools:

	@staticmethod
	def encode(s,encoding = "utf-8",errors = "strict"):
		if (encoding is None):
			encoding = "utf-8"
		if (errors is None):
			errors = "strict"
		return s.encode(encoding, errors)


@_hx_classes.registerClass("_HxException", fields=["val"], superClass=Exception)
class _HxException(Exception):

	def __init__(self,val):
		self.val = None
		message = Std.string(val)
		super().__init__(message)
		self.val = val

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.val = None


@_hx_classes.registerClass("HxString", statics=["split","charCodeAt","charAt","lastIndexOf","toUpperCase","toLowerCase","indexOf","toString","get_length","fromCharCode","substring","substr"])
class HxString:

	@staticmethod
	def split(s,d):
		if (d == ""):
			return python_internal_HxBuiltin.list(s)
		else:
			return s.split(d)

	@staticmethod
	def charCodeAt(s,index):
		if ((((s is None) or ((python_lib_Builtin.len(s) == 0))) or ((index < 0))) or ((index >= python_lib_Builtin.len(s)))):
			return None
		else:
			return python_internal_HxBuiltin.ord(s[index])

	@staticmethod
	def charAt(s,index):
		if ((index < 0) or ((index >= python_lib_Builtin.len(s)))):
			return ""
		else:
			return s[index]

	@staticmethod
	def lastIndexOf(s,str,startIndex = None):
		if (startIndex is None):
			return s.rfind(str, 0, python_lib_Builtin.len(s))
		else:
			i = s.rfind(str, 0, (startIndex + 1))
			startLeft = None
			if (i == -1):
				startLeft = python_internal_HxBuiltin.max(0, ((startIndex + 1) - python_lib_Builtin.len(str)))
			else:
				startLeft = (i + 1)
			check = s.find(str, startLeft, python_lib_Builtin.len(s))
			if ((check > i) and ((check <= startIndex))):
				return check
			else:
				return i

	@staticmethod
	def toUpperCase(s):
		return s.upper()

	@staticmethod
	def toLowerCase(s):
		return s.lower()

	@staticmethod
	def indexOf(s,str,startIndex = None):
		if (startIndex is None):
			return s.find(str)
		else:
			return s.find(str, startIndex)

	@staticmethod
	def toString(s):
		return s

	@staticmethod
	def get_length(s):
		return python_internal_HxBuiltin.len(s)

	@staticmethod
	def fromCharCode(code):
		c = code
		return "".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c]))

	@staticmethod
	def substring(s,startIndex,endIndex = None):
		if (startIndex < 0):
			startIndex = 0
		if (endIndex is None):
			return s[startIndex:]
		else:
			if (endIndex < 0):
				endIndex = 0
			if (endIndex < startIndex):
				return s[endIndex:startIndex]
			else:
				return s[startIndex:endIndex]

	@staticmethod
	def substr(s,startIndex,len = None):
		if (len is None):
			return s[startIndex:]
		else:
			if (len == 0):
				return ""
			return s[startIndex:(startIndex + len)]


@_hx_classes.registerClass("python.io.NativeOutput", fields=["stream"], superClass=haxe_io_Output)
class python_io_NativeOutput(haxe_io_Output):

	def __init__(self,stream):
		self.stream = None
		self.stream = stream
		if (not stream.writable()):
			raise _HxException("Read only stream")

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.stream = None


@_hx_classes.registerClass("python.io.IOutput", methods=["writeByte","writeBytes","writeFullBytes","writeString"])
class python_io_IOutput:	pass


@_hx_classes.registerClass("python.io.IFileOutput", interfaces=[python_io_IOutput])
class python_io_IFileOutput:	pass


@_hx_classes.registerClass("python.io.NativeTextOutput", methods=["writeByte"], superClass=python_io_NativeOutput)
class python_io_NativeTextOutput(python_io_NativeOutput):

	def __init__(self,stream):
		super().__init__(stream)
		if (not stream.writable()):
			raise _HxException("Read only stream")

	def writeByte(self,c):
		def _hx_local_0():
			c1 = c
			return "".join(python_internal_HxBuiltin.map(python_internal_HxBuiltin.chr, [c1]))
		self.stream.write(_hx_local_0())

	@staticmethod
	def _hx_empty_init(_hx_o):		pass


@_hx_classes.registerClass("python.io.FileTextOutput", interfaces=[python_io_IFileOutput], superClass=python_io_NativeTextOutput)
class python_io_FileTextOutput(python_io_NativeTextOutput):

	def __init__(self,stream):
		super().__init__(stream)


@_hx_classes.registerClass("python.io.IoTools", statics=["createFileOutputFromText"])
class python_io_IoTools:

	@staticmethod
	def createFileOutputFromText(t):
		return sys_io_FileOutput(python_io_FileTextOutput(t))


@_hx_classes.registerClass("python.lib._Builtin.Builtin_Impl_", statics=["str"])
class python_lib__Builtin_Builtin_Impl_:

	@staticmethod
	def str(o):
		return python_lib_Builtin.str(o)


@_hx_classes.registerClass("sys.io.File", statics=["getContent","saveContent"])
class sys_io_File:

	@staticmethod
	def getContent(path):
		f = python_lib_Builtin.open(path,"r",-1,"utf-8",None,"")
		content = f.read(-1)
		f.close()
		return content

	@staticmethod
	def saveContent(path,content):
		f = python_lib_Builtin.open(path,"w",-1,"utf-8",None,"")
		f.write(content)
		f.close()


@_hx_classes.registerClass("sys.io.FileOutput", fields=["impl"], methods=["writeByte","writeBytes","writeFullBytes","writeString"], superClass=haxe_io_Output)
class sys_io_FileOutput(haxe_io_Output):

	def __init__(self,impl):
		self.impl = None
		self.impl = impl

	def writeByte(self,c):
		self.impl.writeByte(c)

	def writeBytes(self,s,pos,len):
		return self.impl.writeBytes(s,pos,len)

	def writeFullBytes(self,s,pos,len):
		self.impl.writeFullBytes(s,pos,len)

	def writeString(self,s):
		self.impl.writeString(s)

	@staticmethod
	def _hx_empty_init(_hx_o):
		_hx_o.impl = None
Math.NEGATIVE_INFINITY = python_lib_Builtin.float("-inf")
Math.POSITIVE_INFINITY = python_lib_Builtin.float("inf")
Math.NaN = python_lib_Builtin.float("nan")
Math.PI = python_lib_Math.pi
python_Boot.keywords = python_internal_HxBuiltin.set(["and", "del", "from", "not", "while", "as", "elif", "global", "or", "with", "assert", "else", "if", "pass", "yield", "break", "except", "import", "print", "float", "class", "exec", "in", "raise", "continue", "finally", "is", "return", "def", "for", "lambda", "try", "None", "list", "True", "False"])
python_Boot.prefixLength = python_lib_Builtin.len("_hx_")


class PythonTableView(Table):
    def __init__(self,data):
        self.data = data
        self.height = len(data)
        self.width = 0
        if self.height>0:
            self.width = len(data[0])

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def getCell(self,x,y):
        return self.data[y][x]

    def setCell(self,x,y,c):
        self.data[y][x] = c

    def toString(self):
        return SimpleTable.tableToString(self)

    def getCellView(self):
        return SimpleView()

    def isResizable(self):
        return True

    def resize(self,w,h):
        self.width = w
        self.height = h
        for i in range(len(self.data)):
            row = self.data[i]
            if row == None:
                row = self.data[i] = []
            while len(row)<w:
                row.append(None)
        while len(self.data)<h:
            row = []
            for i in range(w):
                row.append(None)
            self.data.append(row)
        return True

    def clear(self):
        for i in range(len(self.data)):
            row = self.data[i]
            for j in range(len(row)):
                row[j] = None

    def trimBlank(self): 
        return False

    def getData(self):
        return self.data

    def insertOrDeleteRows(self,fate,hfate):
        ndata = []
        for i in range(len(fate)):
            j = fate[i];
            if j!=-1:
                ndata[j] = self.data[i]

        del self.data[:]
        for i in range(len(ndata)):
            self.data[i] = ndata[i]
        self.resize(self.width,hfate)
        return True

    def insertOrDeleteColumns(self,fate,wfate):
        if wfate==self.width and wfate==self.length:
            eq = True
            for i in range(wfate):
                if fate[i]!=i:
                    eq = False
                    break

        if eq:
            return True

        for i in range(self.height):
            row = self.data[i]
            nrow = []
            for j in range(self.width):
                if fate[j]==-1:
                    continue
                nrow[fate[j]] = row[j]
            while nrow.length<wfate:
                nrow.append(None)
            self.data[i] = nrow
        self.width = wfate
        return True

    def isSimilar(self,alt):
        if alt.width!=self.width:
            return False
        if alt.height!=self.height:
            return False
        for c in range(self.width):
            for r in range(self.height):
                v1 = "" + self.getCell(c,r)
                v2 = "" + alt.getCell(c,r) 
                if (v1!=v2):
                    print("MISMATCH "+ v1 + " " + v2);
                    return False
        return True
if __name__ == '__main__':
	Coopy.main()
