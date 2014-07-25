__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"


class Review(object):
    """
    Review holds all the data from a review in MAL about an anime.

    Properties:
        date - string
        account - Account
        helpful - int
        watched - int
        when_written - string
        rating - int
        data - string
    """
    def __init__(self, div):
        """
        :param div: The div of the review to parse all the data from it.
        :type: bs4.element.Tag
        """
        from pymal import Account

        time_div, general_data_div, text_div, _ = div.findAll(name="div", recursive=False)

        self.date = time_div.div.text

        general_data_row = general_data_div.table.tbody.tr
        _, user_cell, general_data_cell = general_data_row.findAll(name="td", recursive=False)

        self.account = Account.Account(user_cell.a.text)
        helpful_span, watched_span = user_cell.find(name="div", attrs={"class": "lightLink spaceit"}).findAll(name="span")

        self.helpful = int(helpful_span.text)
        self.watched = int(watched_span.text)

        _, when_written, rating = general_data_cell.findAll(name="div")

        self.when_written = when_written.text
        self.rating = int(rating.text.split()[-1])

        self.data = text_div.text

    def __repr__(self):
        return "<{0:s} written by {1:s} when {2:s}, rated {3:d} ({4:d}/{5:d})>".format(
            self.__class__.__name__,
            self.account.username,
            self.when_written,
            self.rating,
            self.helpful,
            self.watched
        )
