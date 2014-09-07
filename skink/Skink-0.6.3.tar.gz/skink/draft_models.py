
class superlist(list):

    def __init__(self):
        self.rts = []
        super().__init__(self)

    def save(self):
        for page, id_, registered_template in self.rts:
            page.document.getElementById(id_).innerHTML = registered_template(self).build()


def template(list):
    return t.ul(
        t.li(i)
        for i in list
        )

l = superlist()
superlist.rts.append((page, 'unique_id', template))
