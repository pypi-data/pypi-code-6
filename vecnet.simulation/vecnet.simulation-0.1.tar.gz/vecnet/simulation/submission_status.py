"""
Status codes for the script that submits the simulations in a group to the cluster's batch system..
"""

READY_TO_RUN    = 'ready'
STARTED_SCRIPT  = 'start'
CACHING_FILES   = 'cache'
SUBMITTING_JOBS = 'submit'
SCRIPT_DONE     = 'done'
SCRIPT_ERROR    = 'error'

MAX_LENGTH = 6

ALL = (
    READY_TO_RUN,
    STARTED_SCRIPT,
    CACHING_FILES,
    SUBMITTING_JOBS,
    SCRIPT_DONE,
    SCRIPT_ERROR
)


def is_valid(status_code):
    """
    Is a status code valid (known)?
    """
    return status_code in ALL


_descriptions = {
    READY_TO_RUN:    'ready to run script',
    STARTED_SCRIPT:  'script started',
    CACHING_FILES:   'caching input files',
    SUBMITTING_JOBS: 'submitting simulations',
    SCRIPT_DONE:     'script done',
    SCRIPT_ERROR:    'error occurred',
}


def get_description(status_code):
    """
    Get the description for a status code.
    """
    description = _descriptions.get(status_code)
    if description is None:
        description = 'code = %s (no description)' % str(status_code)
    return description