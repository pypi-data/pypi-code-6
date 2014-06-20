#!/usr/bin/env python

import logging
import time

import workspace
import workspace_exception

logging.basicConfig()

with workspace.Workspace() as w:
  w.refresh()
  #while True:
  #  try:
  #    print w.get_object_record('123')
  #  except workspace_exception.WorkspaceException:
  #    print 'exception'
  #
  #  time.sleep(10 * 60)
  #  