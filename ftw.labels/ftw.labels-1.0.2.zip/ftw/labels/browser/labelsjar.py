from ftw.labels.config import COLORS
from ftw.labels.interfaces import ILabelJar
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zExceptions import BadRequest
import random


class LabelsJar(BrowserView):

    edit_label_template = ViewPageTemplateFile('templates/edit_label.pt')

    def create(self):
        """Create a new label.
        """

        title = self.request.form.get('title', None)
        if not title:
            raise BadRequest(
                '"title" request argument is required.')

        color = self.request.form.get('color', None)
        if not color:
            color = self._get_random_color()

        jar = ILabelJar(self.context)
        jar.get(jar.add(title, color))
        return self._redirect()

    def update(self):
        """Update a label.
        """

        if self.request.form.get('form.delete', None):
            return self.remove()

        label_id = self.request.form.get('label_id', None)
        if not label_id:
            raise BadRequest('The "label_id" request argument is required.')

        jar = ILabelJar(self.context)
        label = jar.get(label_id)

        title = self.request.form.get('title', None)
        if title:
            label['title'] = title

        color = self.request.form.get('color', None)
        if color:
            label['color'] = color

        jar.update(**label)
        return self._redirect()

    def remove(self):
        """Remove a label.
        """

        label_id = self.request.form.get('label_id', None)
        if not label_id:
            raise BadRequest('The "label_id" request argument is required.')

        ILabelJar(self.context).remove(label_id)
        return self._redirect()

    def edit_label(self):
        """Form for editing a label.
        """
        return self.edit_label_template()

    def get_label(self):
        label_id = self.request.form.get('label_id', None)
        if not label_id:
            raise BadRequest('The "label_id" request argument is required.')
        return ILabelJar(self.context).get(label_id)

    @property
    def colors(self):
        return [dict(
            normal=color,
            light='{0}-light'.format(color)
            ) for color in COLORS]

    def _redirect(self):
        response = self.request.RESPONSE
        referer = self.request.get('HTTP_REFERER')
        if referer and referer is not 'localhost':
            response.redirect(referer)
        else:
            response.redirect(self.context.absolute_url())

    def _get_random_color(self):
        all_colors = list(COLORS)
        all_colors.extend(
            ['{0}-light'.format(color) for color in COLORS])

        used_colors = [
            label.get('color') for label in ILabelJar(self.context).list()]

        available_colors = tuple(set(all_colors) - set(used_colors))

        if not available_colors:
            available_colors = all_colors

        return random.choice(available_colors)
