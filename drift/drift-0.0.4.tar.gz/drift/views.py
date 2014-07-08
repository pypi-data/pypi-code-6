import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Image


@csrf_exempt
@require_POST
@login_required
def upload_photos(request):
    for f in request.FILES.getlist("file"):
        obj = Image.objects.create(file=f)
        images = {"filelink": obj.file.url}
    return HttpResponse(json.dumps(images), content_type="application/json")


@login_required
def recent_photos(request):
    images = [
        {"thumb": obj.file.url, "image": obj.file.url}
        for obj in Image.objects.all().order_by("-created")[:20]
    ]
    return HttpResponse(json.dumps(images), content_type="application/json")
