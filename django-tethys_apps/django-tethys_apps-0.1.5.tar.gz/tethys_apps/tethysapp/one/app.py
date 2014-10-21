from tethys_apps.base import TethysAppBase, PersistentStore, app_controller_maker


class One(TethysAppBase):
    """
    Tethys App Class for One.
    """

    name = 'One'
    index = 'one:home'
    icon = 'one/images/icon.gif'
    package = 'one'
    root_url = 'one'
    color = '#34495e'
        
    def controllers(self):
        """
        Add controllers
        """
        AppController = app_controller_maker(self.root_url)

        controllers = (AppController(name='home',
                                     url='one',
                                     controller='one.controllers.home'
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