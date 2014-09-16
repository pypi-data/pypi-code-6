from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import ityou.esi.theme


ITYOU_ESI_THEME = PloneWithPackageLayer(
    zcml_package=ityou.esi.theme,
    zcml_filename='testing.zcml',
    gs_profile_id='ityou.esi.theme:testing',
    name="ITYOU_ESI_THEME")

ITYOU_ESI_THEME_INTEGRATION = IntegrationTesting(
    bases=(ITYOU_ESI_THEME, ),
    name="ITYOU_ESI_THEME_INTEGRATION")

ITYOU_ESI_THEME_FUNCTIONAL = FunctionalTesting(
    bases=(ITYOU_ESI_THEME, ),
    name="ITYOU_ESI_THEME_FUNCTIONAL")
