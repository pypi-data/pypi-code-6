#!/usr/bin/env python

log_level = ['error']
#log_level.append('info')

def outputlog(text, level):
  if level in log_level:
    print text
