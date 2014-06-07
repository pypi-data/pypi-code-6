#!/usr/bin/env python
 # -*- coding: utf-8 -*-

def turn_empty_string_to_none(node):
  if isinstance(node, basestring):
    if len(node) == 0:
      return None
  return node

def to_unicode(s):
  # This is meant to convert str strings to unicode strings, but
  # pass anything else, especially lxml.etree._Element.  lxml seems
  # to parse anything non-ascii to unicode strings (good), and using
  # 'ascii' here ensures that we get an exception if that's not the case.
  if isinstance(s, str):
    return s.decode('ascii')
  return s

def try_get(node, xpath, xform=None, keep_as_list=False):
  """
  If our search returns a set of text nodes, we want to look at each and not consider it a found result if it consists entirely of whitespace.
  lxml provides us only XPath 1.0, which forces us to do a little extra work to achieve this goal.
  If in the future we come to discover that we _do_ sometimes want to return results that are entirely whitespace, this func will need a parameter
  that will regulate whether this behavior happens or not.
  We might want to consider moving to XPath 2.0, which will allow us to use normalize-space to clean our results before we even get them from the xml.
  """
  successful_candidates = list()
  if xform is None:
    xform = lambda x: x
  xform_to_use = lambda x: turn_empty_string_to_none(xform(x))
  if node is not None:
    resultset = node.xpath(xpath)
    if isinstance(resultset, list):
      for one_result in resultset:
        candidate = xform_to_use(one_result)
        if candidate is not None:
          successful_candidates.append(candidate)
    else:
      successful_candidates.append(xform_to_use(resultset))
  if not keep_as_list and len(successful_candidates) == 1:
    return to_unicode(successful_candidates[0])
  elif len(successful_candidates) == 0:
    if not keep_as_list:
      return None
    else:
      return []
  return map(to_unicode, successful_candidates)
