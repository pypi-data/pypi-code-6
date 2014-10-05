import sys
import json


def json(fn=None, indent=None, ensure_ascii=False, mimetype='application/json'):
    def decorator(fn):
        def _fn(request, *args, **kwargs):
            data = fn(request, *args, **kwargs)
            return render_json(data, indent=indent, ensure_ascii=ensure_ascii, mimetype=mimetype)

        return _fn

    return decorator(fn) if fn else decorator


def render_json(data, indent=None, ensure_ascii=False, mimetype='application/json'):
	import json
	from django.http import HttpResponse

	return HttpResponse(json.dumps(data, indent=indent, ensure_ascii=ensure_ascii), content_type=mimetype)

