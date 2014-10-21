from tethys_apps.base import TethysAppBase, PersistentStore, app_controller_maker


class ThisIsAnAppWithALongName(TethysAppBase):
    """
    Tethys App Class for This Is An App With A Long Name.
    """

    name = 'This Is An App With A Long Name'
    index = 'this_is_an_app_with_a_long_name:home'
    icon = 'this_is_an_app_with_a_long_name/images/icon.gif'
    package = 'this_is_an_app_with_a_long_name'
    root_url = 'this-is-an-app-with-a-long-name'
    color = '#e67e22'
        
    def controllers(self):
        """
        Add controllers
        """
        AppController = app_controller_maker(self.root_url)

        controllers = (AppController(name='home',
                                     url='this-is-an-app-with-a-long-name',
                                     controller='this_is_an_app_with_a_long_name.controllers.home'
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