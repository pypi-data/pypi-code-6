from ftw.upgrade import UpgradeStep


class FixInternetWorkflow(UpgradeStep):
    def __call__(self):
        self.setup_install_profile('profile-onegov.edu.upgrades:1002')

        self.update_workflow_security(
            ['onegov_edu_workflow'],
            reindex_security=True)
