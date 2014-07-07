import sys
import json


def json(fn=None, indent=None, mimetype='application/json', ensure_ascii=False):
    def decorator(fn):
        def _fn(request, *args, **kwargs):
            data = fn(request, *args, **kwargs)
            return render_json(data, indent=indent, mimetype=mimetype, ensure_ascii=ensure_ascii)

        return _fn

    return decorator(fn) if fn else decorator


def render_json(data, indent=None, mimetype='application/json', ensure_ascii=False):
	import json
	from django.http import HttpResponse

	return HttpResponse(json.dumps(data, indent=indent), mimetype=mimetype, ensure_ascii=ensure_ascii)


