# -*- coding: utf-8 -*-
import genshi
from genshi.builder import tag

from .options import GoToFormRenderOptions
from .options import PagedListDisplayMode
from .options import PagedListRenderOptions


class Builder(object):
    @classmethod
    def _wrap_text_in_list_item(cls, text):
        li = tag.li(text)
        return li

    @classmethod
    def _element_with_classes(cls, element, *classes):
        old_class = element.attrib.get('class', '')
        if old_class and classes and not old_class.endswith(' '):
            old_class += ' '
        new_class = old_class + ' '.join(classes)
        element(class_=new_class)
        return element

    @classmethod
    def _wrap_in_list_item(cls, inner, options, *classes):
        li = tag.li
        cls._element_with_classes(li, *classes)
        if options.function_to_transform_each_page_link:
            return options.function_to_transform_each_page_link(li, inner)
        li(genshi.core.Markup(inner.generate().render()))
        return li

    @classmethod
    def _first(cls, paged_list, page_url_generator, options):
        target_page_number = 1
        first = tag.a(genshi.core.Markup(
            options.link_to_first_page_format.format(target_page_number)))

        if paged_list.is_first_page:
            return cls._wrap_in_list_item(
                first, options, 'PagedList-skipToFirst', 'disabled')

        first(href=page_url_generator(target_page_number))
        return cls._wrap_in_list_item(first, options, 'PagedList-skipToFirst')

    @classmethod
    def _previous(cls, paged_list, page_url_generator, options):
        target_page_number = paged_list.page_number - 1
        previous = tag.a(genshi.core.Markup(
            options.link_to_previous_page_format.format(target_page_number)))
        previous(rel='prev')

        if not paged_list.has_previous_page:
            return cls._wrap_in_list_item(
                previous, options, 'PagedList-skipToPrevious', 'disabled')

        previous(href=page_url_generator(target_page_number))
        return cls._wrap_in_list_item(previous, options,
                                      'PagedList-skipToPrevious')

    @classmethod
    def _page(cls, target_page_number, paged_list, page_url_generator, options):
        format_func = options.function_to_display_each_page_number
        if not format_func:
            format_func = lambda page_number: (
                options.link_to_individual_page_format.format(page_number))

        page = tag.a(format_func(target_page_number))

        if paged_list.page_number == target_page_number:
            return cls._wrap_in_list_item(page, options, 'active')

        page(href=page_url_generator(target_page_number))
        return cls._wrap_in_list_item(page, options)

    @classmethod
    def _next(cls, paged_list, page_url_generator, options):
        target_page_number = paged_list.page_number + 1
        next_tag = tag.a(genshi.core.Markup(
            options.link_to_next_page_format.format(target_page_number)))
        next_tag(rel='next')

        if not paged_list.has_next_page:
            return cls._wrap_in_list_item(
                next_tag, options, 'PagedList-skipToNext', 'disabled')

        next_tag(href=page_url_generator(target_page_number))
        return cls._wrap_in_list_item(next_tag, options, 'PagedList-skipToNext')

    @classmethod
    def _last(cls, paged_list, page_url_generator, options):
        target_page_number = paged_list.page_count
        last = tag.a(genshi.core.Markup(
            options.link_to_last_page_format.format(target_page_number)))

        if paged_list.is_last_page:
            return cls._wrap_in_list_item(
                last, options, 'PagedList-skipToLast', 'disabled')

        last(href=page_url_generator(target_page_number))
        return cls._wrap_in_list_item(last, options, 'PagedList-skipToLast')

    @classmethod
    def _page_count_and_location_text(cls, paged_list, options):
        text = tag.a(options.page_count_and_current_location_format.format(
            paged_list.page_number, paged_list.page_count))

        return cls._wrap_in_list_item(
            text, options, 'PagedList-pageCountAndLocation', 'disabled')

    @classmethod
    def _item_slice_and_total_text(cls, paged_list, options):
        text = tag.a(options.item_slice_and_total_format.format(
            paged_list.first_item_on_page, paged_list.last_item_on_page,
            paged_list.total_item_count))

        return cls._wrap_in_list_item(
            text, options, 'PagedList-pageCountAndLocation', 'disabled')

    @classmethod
    def _ellipses(cls, options):
        a = tag.a(genshi.core.Markup(options.ellipses_format))

        return cls._wrap_in_list_item(
            a, options, 'PagedList-ellipses', 'disabled')

    @classmethod
    def paged_list_pager(cls, paged_list, page_url_generator, options=None):
        """Displays a configurable paging control for instances of PagedList."""
        if options is None:
            options = PagedListRenderOptions()

        if options.display == PagedListDisplayMode.Never or \
                (options.display == PagedListDisplayMode.IfNeeded and
                 paged_list.page_count <= 1):
            return None

        list_item_links = []

        # Calculate start and end of range of page numbers
        first_page_to_display = 1
        last_page_to_display = paged_list.page_count
        page_numbers_to_display = last_page_to_display

        if options.maximum_page_numbers_to_display is not None and \
                paged_list.page_count > options.maximum_page_numbers_to_display:
            # Cannot fit all pages into pager
            max_page_numbers_to_display = \
                options.maximum_page_numbers_to_display
            first_page_to_display = \
                paged_list.page_number - max_page_numbers_to_display / 2
            if first_page_to_display < 1:
                first_page_to_display = 1

            page_numbers_to_display = max_page_numbers_to_display
            last_page_to_display = \
                first_page_to_display + page_numbers_to_display - 1
            if last_page_to_display > paged_list.page_count:
                first_page_to_display = \
                    paged_list.page_count - max_page_numbers_to_display + 1

        # First
        if (options.display_link_to_first_page == PagedListDisplayMode.Always or
                (options.display_link_to_first_page ==
                 PagedListDisplayMode.IfNeeded and first_page_to_display > 1)):
            list_item_links.append(
                cls._first(paged_list, page_url_generator, options))

        # Previous
        if (options.display_link_to_previous_page ==
                PagedListDisplayMode.Always or
                (options.display_link_to_previous_page ==
                 PagedListDisplayMode.IfNeeded and
                 not paged_list.is_first_page)):
            list_item_links.append(
                cls._previous(paged_list, page_url_generator, options))

        # Text
        if options.display_page_count_and_current_location:
            list_item_links.append(
                cls._page_count_and_location_text(paged_list, options))

        # Text
        if options.display_item_slice_and_total:
            list_item_links.append(
                cls._item_slice_and_total_text(paged_list, options))

        # Page
        if options.display_link_to_individual_pages:
            # If there are previous page numbers not displayed, show an ellipsis
            if options.display_ellipses_when_not_showing_all_page_numbers and \
                    first_page_to_display > 1:
                list_item_links.append(cls._ellipses(options))

            for i in range(first_page_to_display,
                           first_page_to_display + page_numbers_to_display):
                # Show delimiter between page numbers
                if i > first_page_to_display and \
                        options.delimiter_between_page_numbers:
                    list_item_links.append(cls._wrap_text_in_list_item(
                        options.delimiter_between_page_numbers))

                # Show page number link
                list_item_links.append(
                    cls._page(i, paged_list, page_url_generator, options))

            # If there are subsequent page numbers not displayed, show ellipsis
            if options.display_ellipses_when_not_showing_all_page_numbers and \
                    ((first_page_to_display + page_numbers_to_display - 1) <
                     paged_list.page_count):
                list_item_links.append(cls._ellipses(options))

        # Next
        if options.display_link_to_next_page == PagedListDisplayMode.Always or \
                (options.display_link_to_next_page ==
                 PagedListDisplayMode.IfNeeded and
                 not paged_list.is_last_page):
            list_item_links.append(
                cls._next(paged_list, page_url_generator, options))

        # Last
        if options.display_link_to_last_page == PagedListDisplayMode.Always or \
                (options.display_link_to_last_page ==
                 PagedListDisplayMode.IfNeeded and
                 last_page_to_display < paged_list.page_count):
            list_item_links.append(
                cls._last(paged_list, page_url_generator, options))

        if list_item_links:
            # Append class to first item in list?
            if options.class_to_apply_to_first_list_item_in_pager:
                cls._element_with_classes(
                    list_item_links[0],
                    options.class_to_apply_to_first_list_item_in_pager
                )

            # Append class to last item in list?
            if options.class_to_apply_to_last_list_item_in_pager:
                cls._element_with_classes(
                    list_item_links[-1],
                    options.class_to_apply_to_last_list_item_in_pager
                )

            # Append classes to all list item links
            for li in list_item_links:
                cls._element_with_classes(li, *options.li_element_classes)

        # Collapse all of the list items into one big strings
        list_items_string = ''.join([li.generate().render()
                                     for li in list_item_links])

        ul = tag.ul(genshi.core.Markup(list_items_string))
        cls._element_with_classes(ul, *options.ul_element_classes)

        outer_div = tag.div
        cls._element_with_classes(outer_div, *options.container_div_classes)
        outer_div(genshi.core.Markup(ul.generate().render()))

        return outer_div.generate().render()

    @classmethod
    def paged_list_goto_page_form(cls, paged_list, form_action,
                                  options=None):
        """
        Displays a configurable "Go To Page:" form for instances of
        PagedList.
        """
        if not options:
            options = GoToFormRenderOptions()

        form = tag.form
        cls._element_with_classes(form, 'PagedList-goToPage')
        form(action=form_action, method='get', **options.extra_form_attrs)

        fieldset = tag.fieldset

        label = tag.label
        label(for_=options.input_field_name)
        label(options.label_format)

        input_tag = tag.input
        input_tag(type=options.input_field_type,
                  name=options.input_field_name,
                  value=str(paged_list.page_number))

        submit = tag.input
        submit(type='submit',
               value=options.submit_button_format)

        fieldset(genshi.core.Markup(
            (label + input_tag + submit).generate().render()))
        form(genshi.core.Markup(fieldset.generate().render()))
        return str(form)
