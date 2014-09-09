class Widget:
    driver = None

    name = ""
    elements = {}

    def __init__(self):
        self.driver = None
        self.name = ""
        self.elements = {}

    def find_element(self, name):
        if name in self.elements:
            element = self.elements[name]
            element.driver = self.driver

            return element
        else:
            return None
