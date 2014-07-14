"""This module can auto to check there have any lists

inside the list and print they."""

def looptext(the_list):
        """Thie function will check your lists have any others list inside

        and print they untill have no any."""

        for B in (the_list):
                if isinstance(B, list):
                        looptext(B)
                else:
                        print(B)
