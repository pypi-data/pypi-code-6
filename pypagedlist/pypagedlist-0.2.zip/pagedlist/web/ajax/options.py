# -*- coding: utf-8 -*-


class InsertionMode(object):
    Replace = 'replace'
    InsertBefore = 'before'
    InsertAfter = 'after'


class AjaxOptions(object):
    def __init__(self,
                 http_method=None,
                 url=None,
                 insertion_mode=InsertionMode.Replace,
                 update_target_id=None,
                 loading_element_duration=None,
                 loading_element_id=None,
                 confirm=None,
                 on_begin=None,
                 on_success=None,
                 on_failure=None,
                 on_complete=None):
        """

        :param http_method: the HTTP request method ("Get" or "Post").
        :param url: the URL to make the request to.
        :param insertion_mode: the mode that specifies how to insert the
            response into the target DOM element.
        :param update_target_id: the ID of the DOM element to update by using
            the response from the server.
        :param loading_element_duration: a value, in milliseconds, that
            controls the duration of the animation when showing or hiding the
            loading element.
        :param loading_element_id: the id attribute of an HTML element that is
            displayed while the Ajax function is loading.
        :param confirm: the message to display in a confirmation window before
            a request is submitted.
        :param on_begin: the name of the JavaScript function to call
            immediately before the page is updated.
        :param on_success: the JavaScript function to call after the page is
            successfully updated.
        :param on_failure: the JavaScript function to call if the page update
            fails.
        :param on_complete: the JavaScript function to call when response data
            has been instantiated but before the page is updated.
        """
        self.http_method = http_method
        self.url = url
        self.insertion_mode = insertion_mode
        self.update_target_id = update_target_id
        self.loading_element_duration = loading_element_duration
        self.loading_element_id = loading_element_id
        self.confirm = confirm

        self.on_begin = on_begin
        self.on_success = on_success
        self.on_failure = on_failure
        self.on_complete = on_complete

    def to_unobtrusive_html_attributes(self):
        result = {
            'data-ajax': 'true',
        }

        self._add_to_dict_if_specified(
            result, 'data-ajax-url', self.url)
        self._add_to_dict_if_specified(
            result, 'data-ajax-method', self.http_method)
        self._add_to_dict_if_specified(
            result, 'data-ajax-confirm', self.confirm)

        # Events
        self._add_to_dict_if_specified(
            result, 'data-ajax-begin', self.on_begin)
        self._add_to_dict_if_specified(
            result, 'data-ajax-complete', self.on_complete)
        self._add_to_dict_if_specified(
            result, 'data-ajax-failure', self.on_failure)
        self._add_to_dict_if_specified(
            result, 'data-ajax-success', self.on_success)

        if self.loading_element_id:
            self._add_to_dict_if_specified(
                result, 'data-ajax-loading',
                '#{0}'.format(self.loading_element_id))

            if self.loading_element_duration > 0:
                self._add_to_dict_if_specified(
                    result, 'data-ajax-loading-duration',
                    self.loading_element_duration)

        if self.update_target_id:
            self._add_to_dict_if_specified(
                result, 'data-ajax-update',
                '#{0}'.format(self.update_target_id))
            self._add_to_dict_if_specified(
                result, 'data-ajax-mode', self.insertion_mode)

        return result

    @staticmethod
    def _add_to_dict_if_specified(dct, name, value):
        if value:
            dct[name] = value
