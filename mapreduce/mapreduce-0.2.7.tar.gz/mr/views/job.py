import logging
import flask
import json
import socket

import mr.models.kv.job
import mr.models.kv.step
import mr.models.kv.handler
import mr.workflow_manager
import mr.job_engine

_HOSTNAME = socket.gethostname()

_logger = logging.getLogger(__name__)

job_bp = flask.Blueprint('job', __name__, url_prefix='/job')

def _get_arguments_from_request():
    request_data = flask.request.get_json()

    _logger.debug("Job data:\n%s", request_data)

    if request_data is None:
        raise ValueError("No arguments given (1)")

    assert issubclass(request_data['arguments'].__class__, dict) is True

    try:
        return request_data['arguments'].items()
    except KeyError:
        raise ValueError("No arguments given (2)")

@job_bp.route('/<workflow_name>/<job_name>', methods=['POST'])
def job_submit(workflow_name, job_name):
    # Use the workflow-manager in order to verify that we're managing this 
    # workflow.
    wm = mr.workflow_manager.get_wm()
    managed_workflow = wm.get(workflow_name)
    workflow = managed_workflow.workflow

    job = mr.models.kv.job.get(workflow, job_name)
    step = mr.models.kv.step.get(workflow, job.initial_step_name)
    handler = mr.models.kv.handler.get(workflow, step.map_handler_name)

    arguments = _get_arguments_from_request()

    remote_addr_header = mr.config.request.REMOTE_ADDR_HEADER

    _IS_BLOCKING = (flask.request.args.get('asynchronous', 'false') == 'false')

    context = {
        'requester_ip': flask.request.environ[remote_addr_header]
    }

    rr = mr.job_engine.get_request_receiver()

    message_parameters = rr.package_request(
                            workflow, 
                            job, 
                            step, 
                            handler, 
                            arguments, 
                            context)

    request = message_parameters.request
    response = {}

    try:
        result = rr.process_request(
                    message_parameters, 
                    block=_IS_BLOCKING)
    except Exception as e:
        _logger.exception("Request failed.")

        code = 500
        exception_type = e.__class__.__name__
        exception_message = e.message
    else:
        code = 200
        exception_type = None
        exception_message = None

        response['result'] = result

# TODO(dustin): Asynchronous requests fail when we exit too soon. Since we've confirmed that we can read it back immediately after writing it and we don't have a cache, we don't know why the message-handlers can't read it.

    raw_response = flask.jsonify(response)
    response = flask.make_response(raw_response)
    response.headers['X-MR-REQUEST-ID'] = request.request_id
    response.headers['X-FULFILLED-BY'] = _HOSTNAME

    if exception_type is not None:
        response.headers['X-MR-EXCEPTION-TYPE'] = exception_type
        response.headers['X-MR-EXCEPTION-MESSAGE'] = exception_message

    managed_workflow.cleanup_queue.add_request(request)

    return (response, code)
