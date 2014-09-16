from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import ityou.esi.viewlets


ITYOU_ESI_VIEWLETS = PloneWithPackageLayer(
    zcml_package=ityou.esi.viewlets,
    zcml_filename='testing.zcml',
    gs_profile_id='ityou.esi.viewlets:testing',
    name="ITYOU_ESI_VIEWLETS")

ITYOU_ESI_VIEWLETS_INTEGRATION = IntegrationTesting(
    bases=(ITYOU_ESI_VIEWLETS, ),
    name="ITYOU_ESI_VIEWLETS_INTEGRATION")

ITYOU_ESI_VIEWLETS_FUNCTIONAL = FunctionalTesting(
    bases=(ITYOU_ESI_VIEWLETS, ),
    name="ITYOU_ESI_VIEWLETS_FUNCTIONAL")
