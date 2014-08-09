from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .models import Validation
from .signals import user_signed_up, user_activated
from .utils import import_dotted_path


def signup_allowed():
	if isinstance(settings.SIGNUP_ALLOWED, bool):
		return settings.SIGNUP_ALLOWED
	else:
		to_call = import_dotted_path(settings.SIGNUP_ALLOWED)
		return to_call()


class SignUpView(FormView):
	template_name = 'registration/signup_form.html'
	success_url = reverse_lazy('signup_signup_complete')

	def dispatch(self, request, *args, **kwargs):
		if not signup_allowed():
			return redirect('signup_closed')

		if request.method.lower() in self.http_method_names:
			handler = getattr(
				self, request.method.lower(), self.http_method_not_allowed)
		else:
			handler = self.http_method_not_allowed
		return handler(request, *args, **kwargs)

	def get_form_class(self):
		if self.form_class is None:
			form_class_name = settings.SIGNUP_FORM_CLASS
			if form_class_name is None:
				from .forms import DefaultUserCreationForm
				self.form_class = DefaultUserCreationForm
			else:
				self.form_class = import_dotted_path(form_class_name)

		return self.form_class
	
	def form_valid(self, form):
		user = Validation.objects.create_inactive_user(**form.cleaned_data)
		validation = Validation.objects.create_validation(user)

		user_signed_up.send(
			sender=self.__class__,
			user=user,
			request=self.request
		)

		validation.send_activation_email(get_current_site(self.request))

		return super(SignUpView, self).form_valid(form)

class SignupClosedView(TemplateView):
	template_name = 'registration/signup_closed.html'
		
class SignUpCompleteView(TemplateView):
	template_name = 'registration/signup_complete.html'
	
class ActivateView(TemplateView):
	template_name = 'registration/activation_failed.html'

	def get(self, request, *args, **kwargs):
		try:
			validation = Validation.objects.get(key=kwargs['activation_key'])
			user = validation.user

			validation.activate_user()
			validation.delete()

			user_activated.send(
				sender=self.__class__,
				user=user,
				request=request
			)

			return redirect('signup_activate_complete')
		except Validation.DoesNotExist:
			pass

		return super(ActivateView, self).get(request, *args, **kwargs)
	
class ActivateCompleteView(TemplateView):
	template_name = 'registration/activation_complete.html'

