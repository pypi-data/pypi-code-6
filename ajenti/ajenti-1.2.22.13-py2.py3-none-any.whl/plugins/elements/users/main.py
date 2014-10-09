from reconfigure.items.ajenti import UserData
from ajenti.plugins.main.api import SectionPlugin
from ajenti.api import plugin
from ajenti.ui import on
from ajenti.ui.binder import Binder
from ajenti.plugins import manager
from ajenti.usersync.adsync import ActiveDirectorySyncProvider
import ajenti

from ..projects.main import ElementsProjectManager
from ..usermgr import ElementsGroup, ElementsGroupMembership, ElementsUserManager
from ajenti.users import UserManager


@plugin
class ElementsUsers (SectionPlugin):
    def init(self):
        self.title = 'Users'
        self.icon = 'group'
        self.category = 'Elements'
        self.append(self.ui.inflate('elements:users-main'))

        self.mgr = ElementsProjectManager.get(manager.context)
        self.umgr = ElementsUserManager.get(manager.context)

        def post_user_bind(o, c, i, u):
            u.find('name-edit').visible = i.name != 'root'
            u.find('name-label').visible = i.name == 'root'
            u.find('status').text = 'Online' if i.name in self.mgr.active_users else 'Offline'
            u.find('projects').text = ', '.join(x.name for x in self.mgr.active_users.get(i.name, []))

        def post_user_update(object, collection, item, ui):
            if ui.find('password').value:
                item.password = UserManager.get().hash_password(ui.find('password').value)
                self.umgr.ensure_unix_user(item.name, ui.find('password').value)

        self.find('users').post_item_bind = post_user_bind
        self.find('users').post_item_update = post_user_update

        def new_user(c):
            self.save()
            return UserData()

        def new_group(c):
            self.save()
            return ElementsGroup()

        self.find('users').new_item = new_user
        self.find('groups').new_item = new_group

        self.find('group-members').new_item = lambda c: ElementsGroupMembership()

        self.binder_users = Binder(ajenti.config.tree, self)
        self.binder_groups = Binder(self.umgr, self.find('groups-root'))

    def on_page_load(self):
        self.refresh()

    def refresh(self):
        self.ad_mode = type(UserManager.get(manager.context).get_sync_provider()) is ActiveDirectorySyncProvider

        self.binder_users.unpopulate()
        self.binder_groups.unpopulate()

        self.find('user-dropdown').labels = self.find('user-dropdown').values = [x.name for x in ajenti.config.tree.users.values()]

        self.binder_users.populate()
        self.binder_groups.populate()

    @on('save', 'click')
    def save(self):
        self.binder_users.update()
        self.binder_groups.update()
        ajenti.config.save()
        self.umgr.save()
        self.refresh()
