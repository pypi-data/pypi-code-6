from ftw.testing.genericsetup import GenericSetupUninstallMixin
from ftw.testing.genericsetup import apply_generic_setup_layer
from unittest2 import TestCase


@apply_generic_setup_layer
class TestGenericSetupUninstall(TestCase, GenericSetupUninstallMixin):
    package = 'simplelayout.types.common'
    is_product = True

    skip_files = (
        # The Paragraph "version_on_revert" cannot be removed properly
        # using Generic Setup, but it is no longer relevant when the
        # type is no longer installed, so we can ignore it.
        'repositorytool.xml',
        )
