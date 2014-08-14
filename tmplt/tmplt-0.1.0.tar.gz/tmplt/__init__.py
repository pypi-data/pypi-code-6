import re

def render(tmpl, data):

  def follow_path(path, data):
    for key in path.split('.'):
      key = key.strip();
      if isinstance(data, dict):
        try:
          data = data[key]
        except KeyError:
          return ''
      elif isinstance(data, list) or isinstance(data, tuple):
        try:
          key = int(key)
          data = data[key]
        except (IndexError, ValueError):
          return ''
      else:
        return ''
    return data

  def repl(match):
    val = follow_path(match.group(1), data)
    return val(data) if hasattr(val, '__call__') else str(val)

  return re.sub('{{(.+?)}}', repl, tmpl)
