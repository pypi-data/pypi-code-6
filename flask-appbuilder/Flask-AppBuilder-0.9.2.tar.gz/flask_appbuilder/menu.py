from flask import url_for


class MenuItem(object):
    name = ""
    href = ""
    icon = ""
    label = ""
    baseview = None
    childs = []

    def __init__(self, name, href="", icon="", label="", childs=[], baseview=None):
        self.name = name
        self.href = href
        self.icon = icon
        self.label = label
        if self.childs:
            self.childs = childs
        else:
            self.childs = []
        self.baseview = baseview

    def get_url(self):
        if not self.href:
            if not self.baseview:
                return ""
            else:
                return url_for('%s.%s' % (self.baseview.endpoint, self.baseview.default_view))
        else:
            return self.href

    def __repr__(self):
        return self.name


class Menu(object):
    menu = None
    reverse = True

    def __init__(self, reverse=True):
        self.menu = []
        self.reverse = reverse

    def get_list(self):
        return self.menu

    def find(self, name, menu=[]):
        """
            Finds a menu item by name and returns it.

            :param name:
                The menu item name.
        """
        menu = menu or self.menu
        for i in menu:
            if i.name == name:
                return i
            else:
                if i.childs:
                    ret_item = self.find(name, menu=i.childs)
                    if ret_item:
                        return ret_item

    def add_category(self, category, icon="", label="", parent_category=""):
        label = label or category
        if parent_category == "":
            self.menu.append(MenuItem(name=category, icon=icon, label=label))
        else:
            self.find(category).childs.append(MenuItem(name=category, icon=icon, label=label))


    def add_link(self, name, href="", icon="", label="", category="", category_icon="", category_label="",
                 baseview=None):
        label = label or name
        category_label = category_label or category
        if category == "":
            self.menu.append(MenuItem(name=name, href=href, icon=icon, label=label, baseview=baseview))
        else:
            menu_item = self.find(category)
            if menu_item:
                menu_item.childs.append(MenuItem(name=name, href=href, icon=icon, label=label, baseview=baseview))
            else:
                self.add_category(category=category, icon=category_icon, label=category_label)
                self.find(category).childs.append(MenuItem(name=name,
                                                           href=href, icon=icon, label=label,
                                                           baseview=baseview))


    def add_separator(self, category=""):
        menu_item = self.find(category)
        if menu_item:
            menu_item.childs.append(MenuItem("-"))
        else:
            raise Exception("Menu separator does not have correct category {}".format(category))

