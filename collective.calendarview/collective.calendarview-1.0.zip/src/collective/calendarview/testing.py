# -*- coding: utf-8 -*-
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import collective.calendarview


CALENDAR_BASE = PloneWithPackageLayer(
    zcml_package=collective.calendarview,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.calendarview:default',
    name="")

CALENDAR_INTEGRATION = IntegrationTesting(
    bases=(CALENDAR_BASE, ),
    name="CALENDAR_INTEGRATION")

# CALENDAR_FUNCTIONAL = FunctionalTesting(
#     bases=(CALENDAR_BASE, ),
#     name="CALENDAR_FUNCTIONAL")
