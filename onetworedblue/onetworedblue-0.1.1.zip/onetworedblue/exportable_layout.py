from kivy.graphics.context_instructions import Translate
from kivy.graphics.fbo import Fbo
from kivy.graphics.gl_instructions import ClearColor, ClearBuffers
from kivy.uix.relativelayout import RelativeLayout

class ExportableLayout(RelativeLayout):
    ''' This class is an RelativeLayout with only one modification: the addition of an "export to PNG" function.
    It will no longer be needed, as this functionality is built into Kivy 1.8.1, but as this is being written,
    the current release version of Kivy is 1.8.0
    '''

    def export_to_png(self, filename, *args):
        '''Saves an image of the widget and its children in png format at the
        specified filename. Works by removing the widget canvas from its
        parent, rendering to an :class:`~kivy.graphics.fbo.Fbo`, and calling
        :meth:`~kivy.graphics.texture.Texture.save`.

        .. note::

            The image includes only this widget and its children. If you want to
            include widgets elsewhere in the tree, you must call
            :meth:`~Widget.export_to_png` from their common parent, or use
            :meth:`~kivy.core.window.Window.screenshot` to capture the whole
            window.

        .. note::

            The image will be saved in png format, you should include the
            extension in your filename.

        .. versionadded:: 1.8.1
        '''

        if self.parent is not None:
            canvas_parent_index = self.parent.canvas.indexof(self.canvas)
            self.parent.canvas.remove(self.canvas)

        fbo = Fbo(size=self.size)

        with fbo:
            ClearColor(0, 0, 0, 1)
            ClearBuffers()
            Translate(-self.x, -self.y, 0)

        fbo.add(self.canvas)
        fbo.draw()
        fbo.texture.save(filename)
        fbo.remove(self.canvas)

        if self.parent is not None:
            self.parent.canvas.insert(canvas_parent_index, self.canvas)

        return True
