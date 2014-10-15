from zope import interface

class IImages(interface.Interface):
    """ Provider for images contained in an article
    """

    def getImages(**kwargs):
        """ Returns a list of images based on the criteria passed as kwargs (catalog brains)
        """

class IImage(interface.Interface):
    """ Handler for image thumbing and captioning
    """

    def getImageURL(size="original"):
        """
        Returns the url to the image in the specific size

        The sizes are taken from the raptus_article properties sheet
        and are formed by the following name schema:

            images_<size>_(height|width)

        if the property images_<size>_scale is set, we're using a
        plone.app.imaging scale in favour of the width and height
        """

    def getImage(size="orginal"):
        """
        Returns the html tag of the image in the specific size

        The sizes are taken from the raptus_article properties sheet
        and are formed by the following name schema:

            images_<size>_(height|width)

        if the property image<size>_scale is set, we're using a
        plone.app.imaging scale in favour of the width and height
        """

    def getScale(size):
        """
        Returns the name of the image scale used for the specific size.
        None if size is given via width and height properties.
        """

    def getSize(size):
        """
        Returns the width and height registered for the specific size
        """

    def getCaption():
        """
        Returns the caption for the image
        """
