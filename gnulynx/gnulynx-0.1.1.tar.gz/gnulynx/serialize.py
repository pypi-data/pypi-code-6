#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import ujson 
import cStringIO
import gzip

def from_json(s):
  return ujson.loads(s)

def to_json(obj):
  return ujson.dumps(obj)

def from_jsonlines(s):
  l = s.split('\n')
  if len(l) == 1:
    l = l[0].split('\\n')
  for s in l:
    if s.strip() != '':
      yield from_json(s)

def to_jsonlines(obj):
  if isinstance(obj, list):
    return "\\n".join([to_json(o) for o in obj])
    
  elif isinstance(obj, dict):
    return "\\n".join([to_json(obj)])

def from_yaml(s):
  return yaml.load(s)

def to_yaml(obj):
  return yaml.dump(obj, encoding=('utf-8'), indent=4, canonical=True)

def from_yml(s):
  return from_yaml(s)

def to_yml(obj):
  return to_yaml(obj)

def to_gz(s):
  out = cStringIO.StringIO()
  with gzip.GzipFile(fileobj=out, mode="w") as f:
    f.write(s)
  return out.getvalue()

def from_gz(s):
  fileobj = cStringIO.StringIO(s)
  with gzip.GzipFile(fileobj=fileobj, mode="r") as f:
    return f.read()
