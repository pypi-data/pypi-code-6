from core import *
import cmi


class LineCodeGen(Gen):

    """Generate code on a line by line basis.

    """

    @cmi.nonNoneCMI(lambda: LineCodeGen)
    def matchComment(self, comm):
        return HookedRegex(r'Line Gen:\n(.+)\n(.+)\n',
                            '{}\n', comm)
