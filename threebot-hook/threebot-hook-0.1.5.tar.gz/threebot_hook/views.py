import logging

import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import ParseError
from rest_framework.authtoken.models import Token


from django.views.decorators.csrf import csrf_exempt
from .models import Hook, pre_hook_signal, post_hook_signal

from threebot.utils import order_workflow_tasks

from threebot.models import Worker
from threebot.models import Parameter
from threebot.models import ParameterList
from threebot.models import Workflow
from threebot.models import WorkflowLog
from threebot.models import WorkflowPreset
from threebot.runflow import run_workflow

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
        
        ans = run_workflow(workflow_log, worker)
        resp = {'ans': ans,
                'workflow_log_exit_code': workflow_log.exit_code,
                'workflow_log_id': workflow_log.id, 
                }
        post_hook_signal.send(HookView, request=request, payload=payload, resp=resp)
        return Response(resp)
                                        
                              