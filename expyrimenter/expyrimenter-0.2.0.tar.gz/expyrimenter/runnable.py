class Runnable:
    def __init__(s):
        s._title = None

    @property
    def title(s):
        """
        The title is used in :class:`Expyrimenter <expyrimenter.Executor>` log.
        """
        return s._title

    @title.setter
    def title(s, value):
        s._title = value

    # Exceptions will be displayed to the user
    def run(self):
        raise NotImplementedError('Runnable.run not implemented')
