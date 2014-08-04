class PageFactory:

    site = ""
    pages = {}

    def create_page(cls):
        pass

    def find_page(cls):
        pass

    def find_element(cls):
        pass

class PartialPage:
    name = ""
    elements = {}

    def __init__(self, name="!!!"):
        pass

    def find_element(self, name):
        pass

class Page:
    name = ""
    route = ""

    paths = {}
    elements = {}
    partials = {}

    def __init__(self, name="!!!"):
        pass

    def find_element(self, name):
        pass

    def find_partial(self, name):
        pass

    def get_route(self):
        pass

    def get_url(self, site):
        pass
