from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.contrib import messages

import json
import logging
from django.utils import encoding


logger = logging.getLogger(__name__)


def save_form(request, form_class, template_name, form_kwargs=None, form_args=None,
              redirect_to=None, message="", after_save_callback=None, extra_context=None,
              include_html_in_ajax=True):
    """
    Handles the "display form"->"submit form"->"redisplay if errors or redirect to page" flow 

    If the request is ajax, it returns json with a "result": "success" flag.

    :type request: django.http.request.HttpRequest
    :type form_class: type
    :param template_name: Name of the template used to render the form
    :type template_name: str
    :param form_kwargs: Extra kwargs to be passed into the form upon initialization
    :type form_kwargs: dict
    :param form_args: Positional args to be passed into the form upin initialization
    :type form_args: list
    :param redirect_to: URL to redirect to upon successful form submission, or a function called
        with 2 arguments, the form and the save result
    :type redirect_to: str | function
    :param message: Message to add to django's messages framework upon successful form submission
    :type message: str
    :param after_save_callback: Called after a successful form submission. Called with 2 arguments,
        the form and the results of form.save()
    :type after_save_callback: function
    :param extra_context: Extra context variables used for template rendering
    :type extra_context: dict
    :param include_html_in_ajax: Should the template be rendered and returned in the AJAX
        json result packet?
    :type include_html_in_ajax: bool
    :rtype: HttpResponse
    """
    if not extra_context:
        extra_context = {}
    if not form_args:
        form_args = []
    if not form_kwargs:
        form_kwargs = {}
    context = RequestContext(request)
    context.update(extra_context)
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES,
                          **form_kwargs)
        context['form'] = form
        if form.is_valid():
            save_result = form.save()
            if not redirect_to:
                redirect_to = request.META['PATH_INFO']
            if after_save_callback:
                after_save_callback(form, save_result)
            if message:
                if callable(message):
                    message = message(form=form, saved_object=save_result)
                messages.add_message(request, messages.SUCCESS, message)
            if callable(redirect_to):
                redirect_to = redirect_to(form=form, saved_object=save_result)
            if request.is_ajax():
                result = {'result': 'success'}
                if include_html_in_ajax:
                    result['html'] = get_template(template_name).render(context)
                return HttpResponse(json.dumps(result))
            else:
                return HttpResponseRedirect(redirect_to)
        else:
            if logger.isEnabledFor(logging.DEBUG):
                logging.debug("# ValidationErrors when trying to save form for {0}. . .".format(
                    request.META['REMOTE_ADDR']))
                for field in form.errors.keys():
                    logging.debug("ValidationError: %s[%s] <- \"%s\" %s" % (
                        type(form), field,
                        encoding.smart_str(form.data.get(field), encoding='ascii', errors='ignore'),
                        form.errors[field].as_text()))
            if request.is_ajax():
                result = {'result': 'error', 'errors': form.errors}
                if include_html_in_ajax:
                    result['html'] = get_template(template_name).render(context)
                return HttpResponse(json.dumps(result))
    else:
        context['form'] = form_class(*form_args, **form_kwargs)
    return render_to_response(template_name, context_instance=context)
