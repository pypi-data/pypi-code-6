from ftw.lawgiver.tests.base import WorkflowTest
from onegov.edu.testing import EDU_INTEGRATION_TESTING


class TestOneGovSimpleWorkflow(WorkflowTest):

    workflow_path = '../profiles/default/workflows/onegov_edu_workflow'
    layer = EDU_INTEGRATION_TESTING