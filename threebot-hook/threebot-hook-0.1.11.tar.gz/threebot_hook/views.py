import logging

import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import ParseError
from rest_framework.authtoken.models import Token

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from .models import Hook, pre_hook_signal, post_hook_signal
from .forms import HookCreateForm, HookEditForm

from threebot.utils import order_workflow_tasks

from threebot.models import Worker
from threebot.models import Parameter
from threebot.models import ParameterList
from threebot.models import Workflow
from threebot.models import WorkflowLog
from threebot.models import WorkflowPreset
from threebot.tasks import run_workflow
from threebot.utils import get_my_orgs

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig()


class HookView(GenericAPIView):
    renderer_classes = [JSONRenderer]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        token = kwargs.get('token', None)
        identifier = kwargs.get('identifier', None)

        workflow_id = identifier.split("-")[0]
        worker_id = identifier.split("-")[1]
        param_list_id = identifier.split("-")[2]
        slug = "-".join(identifier.split("-")[3:])

        an_user = Token.objects.get(key=token).user
        workflow = Workflow.objects.get(id=workflow_id)
        worker = Worker.objects.get(id=worker_id)
        parameter_list = ParameterList.objects.get(id=param_list_id)

        # Git repo information from post-receive payload
        if request.content_type == "application/json":
            payload = request.DATA
        else:
            # Probably application/x-www-form-urlencoded
            payload = json.loads(request.DATA.get("payload", "{}"))

        info = payload.get('repository', {})
        repo = info.get('name', None)

        # GitHub: repository['owner'] = {'name': name, 'email': email}
        # BitBucket: repository['owner'] = name
        user = info.get('owner', {})
        if isinstance(user, dict):
            user = user.get('name', None)

        if not identifier and not repo and not user and not token:
            raise ParseError("No JSON data or URL argument : cannot identify hook")

        hook = Hook.objects.get(workflow=workflow, worker=worker, param_list=parameter_list)
        #TODO: Further security processing on this Hook
        #TODO: Validate user and team

        workflow_tasks = order_workflow_tasks(workflow)

        input_dict = {}

        for wf_task in workflow_tasks:
            l_input_dict = {}
            l_input_dict = {}
            for data_type in Parameter.DATA_TYPE_CHOICES:
                l_input_dict[data_type[0]] = {}
            for parameter in parameter_list.parameters.all():
                l_input_dict[parameter.data_type][parameter.name] = parameter.value
            input_dict['%s' % wf_task.id] = l_input_dict

        workflow_log = WorkflowLog(workflow=workflow, inputs=input_dict, performed_by=an_user, performed_on=worker)
        workflow_log.save()

        wf_preset, created = WorkflowPreset.objects.get_or_create(user=an_user, workflow=workflow)
        wf_preset.defaults.update({'worker_id': worker.id})
        wf_preset.defaults.update({'list_id': parameter_list.id})
        wf_preset.save()

        pre_hook_signal.send(HookView, request=request, payload=payload)

        workflow_log.inputs['payload'] = payload
        workflow_log.save()

        run_workflow(workflow_log.id)
        resp = {'workflow_log_exit_code': workflow_log.exit_code,

                'workflow_log_id': workflow_log.id,
                }

        post_hook_signal.send(HookView, request=request, payload=payload, resp=resp)
        return Response(resp)


@login_required
def hooks_list(request, wf_slug, template='threebot_hook/list.html'):
    orgs = get_my_orgs(request)
    workflow = workflow = Workflow.objects.get(slug=wf_slug, owner__in=orgs)
    hooks = Hook.objects.filter(workflow=workflow)

    for hook in hooks:
        hook.full_url = hook.make_full_url(request.user)

    return render_to_response(template, {'request': request,
                                         'workflow': workflow,
                                         'hooks': hooks,
                                        }, context_instance=RequestContext(request))


@login_required
def create(request, wf_slug, template='threebot_hook/create.html'):
    orgs = get_my_orgs(request)
    workflow = workflow = Workflow.objects.get(slug=wf_slug, owner__in=orgs)
    form = HookCreateForm(request.POST or None, request=request, workflow=workflow)

    if form.is_valid():
        hook = form.save()

        return redirect('hook_list', workflow.slug)

    return render_to_response(template, {'request': request,
                                         'form': form,
                                         'workflow': workflow,
                                        }, context_instance=RequestContext(request))


@login_required
def edit(request, wf_slug, hook_slug, template='threebot_hook/create.html'):
    orgs = get_my_orgs(request)
    workflow = Workflow.objects.get(slug=wf_slug, owner__in=orgs)
    hook = Hook.objects.get(slug=hook_slug, workflow=workflow)

    form = HookEditForm(request.POST or None, instance=hook, request=request, workflow=workflow)

    if form.is_valid():
        hook = form.save()

        return redirect('hook_list', workflow.slug)

    return render_to_response(template, {'request': request,
                                         'form': form,
                                         'workflow': workflow,
                                        }, context_instance=RequestContext(request))
