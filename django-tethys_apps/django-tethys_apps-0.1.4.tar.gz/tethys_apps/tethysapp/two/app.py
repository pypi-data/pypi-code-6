from tethys_apps.base import TethysAppBase, PersistentStore, app_controller_maker


class Two(TethysAppBase):
    """
    Tethys App Class for Two.
    """

    name = 'Two'
    index = 'two:home'
    icon = 'two/images/icon.gif'
    package = 'two'
    root_url = 'two'
    color = '#9b59b6'
        
    def controllers(self):
        """
        Add controllers
        """
        AppController = app_controller_maker(self.root_url)

        controllers = (AppController(name='home',
                                     url='two',
                                     controller='two.controllers.home'
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