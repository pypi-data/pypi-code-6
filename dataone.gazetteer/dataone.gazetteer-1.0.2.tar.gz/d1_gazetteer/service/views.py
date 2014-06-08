#!/usr/bin/env python

import os
import pprint
import json
import re
import subprocess

import django.http

import settings


def region_tree(request, west, south, east, north):
  #p1 = subprocess.Popen('whoami', stdout=subprocess.PIPE, shell=True)
  #return django.http.HttpResponse(p1.communicate()[0])

  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  # If region is too large, return a tree containing a single entry called "wide area".
  n_adms = _get_number_of_administrative_areas_in_bounding_box(west, south, east, north)
  if n_adms > 1000:
    return django.http.HttpResponse(json.dumps({'Wide Area': {}}))

  names = _get_administrative_areas_in_bounding_box(west, south, east, north)
  region_tree = _region_tree_from_ogr_names(names)
  return django.http.HttpResponse(json.dumps(region_tree))


def _region_tree_from_ogr_names(names):
  tree = {}
  for name in names.split('\n'):
    m = re.match(r'NAME_(\d) \(String\) = (.*)', name.strip())
    if not m:
      continue
    level = int(m.group(1))
    value = m.group(2)
    if value == '(null)':
      continue
    if level == 0:
      c = tree
    if value not in c:
      c[value] = {}
    c = c[value]
  return tree


def _get_administrative_areas_in_bounding_box(west, south, east, north):
  cmd = '{0} -ro -spat {1} {2} {3} {4} {5} {6} | grep " NAME_"'\
    .format(settings.OGRINFO_PATH, west, south, east, north, settings.DATASET_PATH, settings.DATASET_NAME)
  p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
  return p1.communicate()[0]


def _get_number_of_administrative_areas_in_bounding_box(west, south, east, north):
  cmd = '{0} -ro -sql "select count(*) FROM {1}" -spat {2} {3} {4} {5} {6}'\
    .format(settings.OGRINFO_PATH, settings.DATASET_NAME, west, south, east, north, settings.DATASET_PATH)
  p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
  out, err = p1.communicate()
  if len(err):
    return err
  m = re.search(r'COUNT_\* \(Integer\) = (\d+)', out, re.MULTILINE)
  return int(m.group(1))
