from tethys_apps.base import TethysAppBase, PersistentStore, app_controller_maker


class ThisIsAnAppWithAVeryVeryLongName(TethysAppBase):
    """
    Tethys App Class for This Is An App With A Very Very Long Name.
    """

    name = 'This Is An App With A Very Very Long Name'
    index = 'this_is_an_app_with_a_very_very_long_name:home'
    icon = 'this_is_an_app_with_a_very_very_long_name/images/icon.gif'
    package = 'this_is_an_app_with_a_very_very_long_name'
    root_url = 'this-is-an-app-with-a-very-very-long-name'
    color = '#e67e22'
        
    def controllers(self):
        """
        Add controllers
        """
        AppController = app_controller_maker(self.root_url)

        controllers = (AppController(name='home',
                                     url='this-is-an-app-with-a-very-very-long-name',
                                     controller='this_is_an_app_with_a_very_very_long_name.controllers.home'
                       ),
        )

        return controllers

    def persistent_stores(self):
        """
        Add persistent stores
        """
        stores = (PersistentStore(name='primary',
                                  initializer='init_stores:init_primary',
                                  postgis=True
                  ),
        )

        return stores