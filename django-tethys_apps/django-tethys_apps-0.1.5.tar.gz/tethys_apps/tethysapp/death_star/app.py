from tethys_apps.base import TethysAppBase, PersistentStore, app_controller_maker


class DeathStar(TethysAppBase):
    """
    Tethys App Class
    """

    name='Death Star'
    index='death_star:home'
    icon='death_star/images/icon.gif'
    package="death_star"
    root_url='death-star'
    color='#34495e'

    def controllers(self):
        """
        Add controllers
        """
        AppController = app_controller_maker(self.root_url)

        controllers = (AppController(name='home',
                                     url='death-star',
                                     controller='death_star.controllers.index.index'
                        ),
                       AppController(name='new_page',
                                     url='death-star/new-page',
                                     controller='death_star.controllers.index.new_page'
                        ),
        )

        return controllers

    def persistent_stores(self):
        """
        Add one or more persistent stores
        """
        stores = (PersistentStore(name='example_db',
                                  initializer='init_db:init_example_db',
                                  postgis=True
                ), 
        )

        return stores