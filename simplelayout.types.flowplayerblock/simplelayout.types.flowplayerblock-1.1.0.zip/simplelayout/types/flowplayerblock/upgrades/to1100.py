from ftw.upgrade import UpgradeStep


class UpdateFileFTI(UpgradeStep):

    def __call__(self):
        self.actions_remove_type_action('File', 'sl-dummy-dummy-dummy')

        self.setup_install_profile(
            'profile-simplelayout.types.flowplayerblock.upgrades:1100')
