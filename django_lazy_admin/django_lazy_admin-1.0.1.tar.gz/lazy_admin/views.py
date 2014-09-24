from django.db import models
from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@staff_member_required
def lazy_column_view(request):
	'''
	Handles all lazy column ajax requests. Decorator allows only
	admin users access to this view.
	'''
	if request.method == 'POST':
		# Extract data from POST
		try:
			app = request.POST['app']
			model_name = request.POST['model']
			method = request.POST['method']
			objid = request.POST['objid']
		except KeyError:
			return HttpResponseNotFound()

		# Make sure Object ID is a number
		try:
			objid = long(objid)
		except ValueError:
			return HttpResponseNotFound()

		# Get the model class
		model = models.get_model(app, model_name)
		if model is None:
			return HttpResponseNotFound()

		# Now get the actual object
		obj = get_object_or_404(model, pk=objid)

		# Validate if the user has change permission for this object
		model_admin = None
		try:
			model_admin = admin.site._registry[model]
			if not model_admin.has_change_permission(request, obj):
				return HttpResponseNotFound()
		except KeyError:
			return HttpResponseNotFound()

		# Get the admin method to be called
		try:
			func = getattr(model_admin, method)
		except AttributeError:
			return HttpResponseNotFound()

		# Finally! Call the method and send the output
        return HttpResponse(func(obj, delay=False))
