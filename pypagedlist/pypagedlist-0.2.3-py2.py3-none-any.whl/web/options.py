# -*- coding: utf-8 -*-
import genshi

from pagedlist.web.ajax import AjaxOptions


class GoToFormRenderOptions(object):
    __slots__ = ['label_format', 'submit_button_format', 'input_field_name',
                 'input_field_type', 'extra_form_attrs']

    def __init__(self, input_field_name="page"):
        self.label_format = "Go to page:"
        self.submit_button_format = "Go"
        self.input_field_name = input_field_name
        self.input_field_type = "number"
        self.extra_form_attrs = {}

    @classmethod
    def enable_unobtrusive_ajax_replacing(cls, options, ajax_options):
        options.extra_form_attrs.update(
            ajax_options.to_unobtrusive_html_attributes())
        return options

    @classmethod
    def enable_unobtrusive_ajax_replacing_id(cls, element_id):
        if element_id.startswith('#'):
            element_id = element_id[1:]

        ajax_options = AjaxOptions(
            http_method='GET',
            insertion_mode='replace',
            update_target_id=element_id,
        )

        return cls.enable_unobtrusive_ajax_replacing(cls(), ajax_options)

    @classmethod
    def enable_unobtrusive_ajax_replacing_options(cls, ajax_options):
        return cls.enable_unobtrusive_ajax_replacing(cls(), ajax_options)


class PagedListDisplayMode(object):
    Always = 0
    Never = 1
    IfNeeded = 2


class PagedListRenderOptions(object):
    def __init__(self,
                 display=PagedListDisplayMode.Always,
                 display_link_to_first_page=PagedListDisplayMode.IfNeeded,
                 display_link_to_last_page=PagedListDisplayMode.IfNeeded,
                 display_link_to_previous_page=PagedListDisplayMode.IfNeeded,
                 display_link_to_next_page=PagedListDisplayMode.IfNeeded,
                 display_link_to_individual_pages=True,
                 display_page_count_and_current_location=False,
                 maximum_page_numbers_to_display=10,
                 display_ellipses_when_not_showing_all_page_numbers=True,
                 ellipses_format="&#8230;",
                 link_to_first_page_format="&laquo;&laquo;",
                 link_to_previous_page_format="&laquo;",
                 link_to_individual_page_format="{0}",
                 link_to_next_page_format="&raquo;",
                 link_to_last_page_format="&raquo;&raquo;",
                 page_count_and_current_location_format="Page {0} of {1}.",
                 item_slice_and_total_format=
                 "Showing items {0} through {1} of {2}.",
                 function_to_display_each_page_number=None,
                 class_to_apply_to_first_list_item_in_pager=None,
                 class_to_apply_to_last_list_item_in_pager=None,
                 container_div_classes=None,
                 ul_element_classes=None,
                 li_element_classes=None,
                 display_item_slice_and_total=False,
                 function_to_transform_each_page_link=None,
                 delimiter_between_page_numbers=''):
        """
        The default settings render all navigation links and no descriptive
        text.

        :param display: If set to Always, always renders the paging control.
            If set to IfNeeded, render the paging control when there is more
            than one page.
        :param display_link_to_first_page: If set to Always, render a hyperlink
            to the first page in the list. If set to IfNeeded, render the
            hyperlink only when the first page isn't visible in the paging
            control.
        :param display_link_to_last_page:  If set to Always, render a hyperlink
            to the last page in the list. If set to IfNeeded, render the
            hyperlink only when the last page isn't visible in the paging
            control.
        :param display_link_to_previous_page: If set to Always, render a
            hyperlink to the previous page of the list. If set to IfNeeded,
            render the hyperlink only when there is a previous page in the list.
        :param display_link_to_next_page: If set to Always, render a hyperlink
            to the next page of the list. If set to IfNeeded, render the
            hyperlink only when there is a next page in the list.
        :param display_link_to_individual_pages: When true, includes hyperlinks
            for each page in the list.
        :param display_page_count_and_current_location: When true, shows the
            current page number and the total number of pages in the list.
        :param maximum_page_numbers_to_display: The maximum number of page
            numbers to display. Null displays all page numbers.
        :param display_ellipses_when_not_showing_all_page_numbers: If true,
            adds an ellipsis where not all page numbers are being displayed.
        :param ellipses_format: The pre-formatted text to display when not all
            page numbers are displayed at once.
        :param link_to_first_page_format: The pre-formatted text to display
            inside the hyperlink to the first page. The one-based index of the
            page (always 1 in this case) is passed into the formatting function
            - use {0} to reference it.
        :param link_to_previous_page_format:
        :param link_to_individual_page_format:
        :param link_to_next_page_format:
        :param link_to_last_page_format:
        :param page_count_and_current_location_format:
        :param item_slice_and_total_format:
        :param function_to_display_each_page_number:
        :param class_to_apply_to_first_list_item_in_pager: Specifies a CSS class
            to append to the first list item in the pager. If null or whitespace
            is defined, no additional class is added to first list item in list.
        :param class_to_apply_to_last_list_item_in_pager: Specifies a CSS class
            to append to the last list item in the pager. If null or whitespace
            is defined, no additional class is added to last list item in list.
        :param container_div_classes:  CSS Classes to append to the <div>
            element that wraps the paging control.
        :param ul_element_classes:  CSSClasses to append to the <ul>
            element in the paging control.
        :param li_element_classes: CSS Classes to append to every <li
            element in the paging control.
        :param display_item_slice_and_total: When true, shows the one-based
            index of the first and last items on the page, and the total number
            OF items in the list.
        :param function_to_transform_each_page_link:
        """

        self.display = display
        self.display_link_to_first_page = display_link_to_first_page
        self.display_link_to_last_page = display_link_to_last_page
        self.display_link_to_previous_page = display_link_to_previous_page
        self.display_link_to_next_page = display_link_to_next_page
        self.display_link_to_individual_pages = display_link_to_individual_pages
        self.display_page_count_and_current_location = \
            display_page_count_and_current_location
        self.maximum_page_numbers_to_display = maximum_page_numbers_to_display
        self.display_ellipses_when_not_showing_all_page_numbers = \
            display_ellipses_when_not_showing_all_page_numbers
        self.ellipses_format = ellipses_format
        self.link_to_first_page_format = link_to_first_page_format
        self.link_to_previous_page_format = link_to_previous_page_format
        self.link_to_individual_page_format = link_to_individual_page_format
        self.link_to_next_page_format = link_to_next_page_format
        self.link_to_last_page_format = link_to_last_page_format
        self.page_count_and_current_location_format = \
            page_count_and_current_location_format
        self.item_slice_and_total_format = item_slice_and_total_format
        self.function_to_display_each_page_number = \
            function_to_display_each_page_number
        self.class_to_apply_to_first_list_item_in_pager = \
            class_to_apply_to_first_list_item_in_pager
        self.class_to_apply_to_last_list_item_in_pager = \
            class_to_apply_to_last_list_item_in_pager
        if container_div_classes is None:
            container_div_classes = ["pagination-container"]
        self.container_div_classes = container_div_classes
        if ul_element_classes is None:
            ul_element_classes = ["pagination"]
        self.ul_element_classes = ul_element_classes
        if li_element_classes is None:
            li_element_classes = []
        self.li_element_classes = li_element_classes

        self.display_item_slice_and_total = display_item_slice_and_total
        self.function_to_transform_each_page_link = \
            function_to_transform_each_page_link
        self.delimiter_between_page_numbers = delimiter_between_page_numbers

    @classmethod
    def enable_unobtrusive_ajax_replacing(cls, options, ajax_options):
        """
        Enables unobtrusive AJAX feature. An XHR request will retrieve HTML
        from the clicked page and replace the innerHtml of the provided element
        ID.
        """

        def transformer(li_tag_builder, a_tag_builder):
            if 'class' in li_tag_builder.attrib:
                li_class = li_tag_builder.attrib.get('class', '')
            else:
                li_class = ''
            if ajax_options and 'disabled' not in li_class and \
                    'active' not in li_class:
                a_tag_builder(**ajax_options.to_unobtrusive_html_attributes())

            li_tag_builder(genshi.core.Markup(str(a_tag_builder)))
            return li_tag_builder

        options.function_to_transform_each_page_link = transformer
        return options

    @classmethod
    def enable_unobtrusive_ajax_replacing_id(cls, element_id):
        if element_id.startswith('#'):
            element_id = element_id[1:]

        ajax_options = AjaxOptions(
            http_method='GET',
            insertion_mode='replace',
            update_target_id=element_id,
        )

        return cls.enable_unobtrusive_ajax_replacing(cls(), ajax_options)

    @classmethod
    def enable_unobtrusive_ajax_replacing_options(cls, ajax_options):
        return cls.enable_unobtrusive_ajax_replacing(cls(), ajax_options)

    @classmethod
    def classic(cls):
        return cls(
            display_link_to_first_page=PagedListDisplayMode.Never,
            display_link_to_last_page=PagedListDisplayMode.Never,
            display_link_to_previous_page=PagedListDisplayMode.Always,
            display_link_to_next_page=PagedListDisplayMode.Always,
        )

    @classmethod
    def classic_plus_first_and_last(cls):
        """Also includes links to first and last pages."""
        return cls(
            display_link_to_first_page=PagedListDisplayMode.Always,
            display_link_to_last_page=PagedListDisplayMode.Always,
            display_link_to_previous_page=PagedListDisplayMode.Always,
            display_link_to_next_page=PagedListDisplayMode.Always,
        )

    @classmethod
    def minimal(cls):
        """Shows only the previous and next links."""
        return cls(
            display_link_to_first_page=PagedListDisplayMode.Never,
            display_link_to_last_page=PagedListDisplayMode.Never,
            display_link_to_previous_page=PagedListDisplayMode.Always,
            display_link_to_next_page=PagedListDisplayMode.Always,
            display_link_to_individual_pages=False,
        )

    @classmethod
    def minimal_with_page_count_text(cls):
        """
        Shows Previous and Next links along with current page number and page
        count.
        """
        return cls(
            display_link_to_first_page=PagedListDisplayMode.Never,
            display_link_to_last_page=PagedListDisplayMode.Never,
            display_link_to_previous_page=PagedListDisplayMode.Always,
            display_link_to_next_page=PagedListDisplayMode.Always,
            display_link_to_individual_pages=False,
            display_page_count_and_current_location=True,
        )

    @classmethod
    def minimal_with_item_count_text(cls):
        """
        Shows Previous and Next links along with index of first and last items
        on page and total number of items across all pages.
        """
        return cls(
            display_link_to_first_page=PagedListDisplayMode.Never,
            display_link_to_last_page=PagedListDisplayMode.Never,
            display_link_to_previous_page=PagedListDisplayMode.Always,
            display_link_to_next_page=PagedListDisplayMode.Always,
            display_link_to_individual_pages=False,
            display_item_slice_and_total=True,
        )

    @classmethod
    def page_numbers_only(cls):
        """Shows only links to each individual page."""
        return cls(
            display_link_to_first_page=PagedListDisplayMode.Never,
            display_link_to_last_page=PagedListDisplayMode.Never,
            display_link_to_previous_page=PagedListDisplayMode.Never,
            display_link_to_next_page=PagedListDisplayMode.Never,
            display_ellipses_when_not_showing_all_page_numbers=False,
        )

    @classmethod
    def only_show_five_pages_at_a_time(cls):
        """
        Shows Next and Previous while limiting to a max of 5 page numbers at
        a time.
        """
        return cls(
            display_link_to_first_page=PagedListDisplayMode.Never,
            display_link_to_last_page=PagedListDisplayMode.Never,
            display_link_to_previous_page=PagedListDisplayMode.Always,
            display_link_to_next_page=PagedListDisplayMode.Always,
            maximum_page_numbers_to_display=5,
        )

    @classmethod
    def twitter_bootstrap_pager(cls):
        """
        Twitter Bootstrap 2's basic pager format (just Previous and Next links).
        """
        return cls(
            display_link_to_first_page=PagedListDisplayMode.Never,
            display_link_to_last_page=PagedListDisplayMode.Never,
            display_link_to_previous_page=PagedListDisplayMode.Always,
            display_link_to_next_page=PagedListDisplayMode.Always,
            display_link_to_individual_pages=False,
            container_div_classes=None,
            ul_element_classes=['pager'],
            class_to_apply_to_first_list_item_in_pager=None,
            class_to_apply_to_last_list_item_in_pager=None,
            link_to_previous_page_format='Previous',
            link_to_next_page_format='Next',
        )

    @classmethod
    def twitter_bootstrap_pager_aligned(cls):
        """
        Twitter Bootstrap 2's basic pager format (just Previous and Next links),
        with aligned links.
        """
        return cls(
            display_link_to_first_page=PagedListDisplayMode.Never,
            display_link_to_last_page=PagedListDisplayMode.Never,
            display_link_to_previous_page=PagedListDisplayMode.Always,
            display_link_to_next_page=PagedListDisplayMode.Always,
            display_link_to_individual_pages=False,
            container_div_classes=None,
            ul_element_classes=['pager'],
            class_to_apply_to_first_list_item_in_pager='previous',
            class_to_apply_to_last_list_item_in_pager='next',
            link_to_previous_page_format='&larr; Older',
            link_to_next_page_format='Newer &rarr;',
        )
