from bs4 import BeautifulSoup, NavigableString, Tag
from base64 import encodestring as encode, decodestring as decode
import re
import json
from path import compose_path


__DATA_CLASS = "data-class"
__DATA_PROP = "data-prop-"
__DATA_PROP_PLUS = "data-prop+"
__DATA_TEXT = "data-text-"
__DATA_TEXT_PLUS = "data-text+"
__DATA_HTML = "data-html-"
__DATA_HTML_PLUS = "data-html+"
__DATA_PROP_CSS = "data-prop-css-"
__DATA_TEXT_CSS = "data-text-css-"
__DATA_CSS = "data-css-"

__ABSOLUTE_PATH = "^"


class Renderer(object):

    def __init__(self, api, debug=False):
        self.api = api
        self.DEBUG = debug


class HTMLRenderer(Renderer):

    def render(self, stcl, skel):
        """
        Returns the skeleton completed.
        """

        self.document = BeautifulSoup(skel, "html5")
        self.document["data-path"] = stcl
        self.__expand(stcl, self.document.body)
        for child in self.document.body.children:
            return unicode(child)
        return ""

    def __expand(self, stcl, elt):

        #import ipdb; ipdb.set_trace()

        # check if the element should be rendered
        #path = self.__get_data_path(elt)
        #value = elt.get("data-value")
        #cond = elt.get("data-cond")
        #if not path and not value and not cond:
        #    return

        # check condition
        if not self.__satisfy_condition(stcl, elt):
            elt.decompose()
            return

        # set path attribute
        #if path:
        #    stcl = stcl if path.startswith("!") else compose_path(stcl, path)
        #self.__set_data_path(elt, stcl)

        # expand component
        if elt.name == "body":
            elt = self.__expand_children(stcl, elt)
        elif self.__is_container(elt):
            elt = self.__expand_container(stcl, elt)
        elif self.__is_final(elt):
            elt = self.__expand_final(stcl, elt)
        elif self.__is_post(elt):
            elt = self.__expand_post(stcl, elt)
        elif elt.name.lower() in ["optgroup", "datalist"]:
            elt = self.__expand_group_datalist(stcl, elt)
        elif elt.name.lower() in ["select"]:
            elt = self.__expand_select(stcl, elt)
        elif elt.name.lower() in ["option"]:
            elt = self.__expand_option(stcl, elt)
        elif elt.name.lower() in ["ol", "ul"]:
            elt = self.__expand_ol_ul(stcl, elt)
        elif elt.name.lower() in ["table"]:
            elt = self.__expand_table(stcl, elt)
        else:
            pass

        # should be done at last to remove all path attributes
        if elt:
            self.__remove_path(elt)

    def __expand_children(self, stcl, elt):

        # expand children
        for child in self.__get_children(elt):
            self.__expand(stcl, child)
        return elt

    def __expand_container(self, stcl, container):

        # expand children
        path = self.__get_data_path(container)
        if path:
            empty = self.__is_empty(stcl, path)
            if path.startswith("!"):
                if not empty:
                    container.decompose()
                    return None
            else:
                if not empty:
                    self.__expand_final(stcl, container)
                    self.__expand_children(compose_path(stcl, path), container)
                    return container
                else:
                    container.decompose()
                    return None
        else:
            self.__expand_final(stcl, container)
            return container

    def __expand_final(self, stcl, final):

        # check condition and expand attributes
        if not self.__satisfy_condition(stcl, final):
            final.decompose()
            return
        self.__expand_attributes(stcl, final)

        # expand to text value
        value_path, format = self.__get_property_path(final)
        if value_path:
            if value_path.startswith("http:"):
                value_path = value_path[5:]
                value = ""
                self.__expand_to_text(final, value, format)
            elif value_path.startswith("skel:"):
                # old skel prefix
                msg = "skel prefix should be replaced by include tag"
                final.string.replace_with(msg)

            # simple value
            else:
                value, prop_path = self.__get_property_value(stcl, value_path, format)
                span = BeautifulSoup("<span></span>").span
                span.append(value)
                self.__set_data_path(span, prop_path)
                final.append(span)
        return final

    def __expand_group_datalist(self, stcl, elt):
        pass

    def __expand_select(self, stcl, select):

        def set_selected(elt, value, mode, multiple=False):
            """ set selected option """
            for option in elt.find_all("option"):
                if mode == _Mode.BY_VALUE:
                    selected = option["value"]
                elif mode == _Mode.BY_LABEL:
                    selected = option.string
                if value and value == selected:
                    option["selected"] = "selected"
                    if not multiple:
                        break

        # check condition and expand attributes
        if not self.__satisfy_condition(stcl, select):
            select.decompose()
            return
        self.__expand_attributes(stcl, select)

        # replace by generated options
        path = self.__get_data_path(select)
        for child in self.__get_children(select):

            # check condition
            if not self.__satisfy_condition(stcl, child):
                child.decompose()
                continue

            # expand child
            if child.name == "optgroup":
                self.__expand_group_datalist(compose_path(stcl, path), child)
            elif child.name == "option":
                self.__expand_option(compose_path(stcl, path), select, child)

        # the selected stencil is a property
        value_path, format = self.__get_property_path(select)
        label_path = select.get("data-label")

        # get value
        p = compose_path(stcl, path, label_path if label_path else value_path)
        value, prop_path = self.__get_property_value(stcl, p, format)

        # set post parameter
        name = select.get('name')
        if not name:
            name = "%s_" % format if format else "s_"
        select["name"] = name + encode(prop_path)

        # comparaison mode
        mode = _Mode.BY_LABEL if label_path else _Mode.BY_VALUE

        # multiple selections
        if name.startswith("m_"):
            for v in value.split(':'):
                set_selected(select, v, mode, multiple=True)

        # single selection
        else:
            set_selected(select, value, mode)

        return select

    def __expand_ol_ul(self, stcl, elt):
        pass

    def __expand_option(self, stcl, select, option):

        # check condition
        if not self.__satisfy_condition(stcl, option):
            option.decompose()
            return

        path = self.__get_data_path(option)
        value_path, value_format = self.__get_property_path(option)
        label_path, label_format = self.__get_property_path(option, "data-label")

        # the options are not generated from the stencil
        if not path:

            # if value path defined, then changes label and value
            if value_path:
                self.__complete_option(stcl, stcl, value_path, value_format, label_path, label_format, option)

        # the options are generated
        else:

            # iterates over data-path of the option
            p = encode(compose_path(stcl, path))
            stencils = self.api.get_list(p, [value_path, label_path])
            for s in stencils.content:
                opt = self.__append_new_tag("option", select)
                self.__complete_option(stcl, s, value_path, value_format, label_path, label_format, opt)

            # remove option template
            option.decompose()

    def __complete_option(self, stcl, json, value_path, value_format, label_path, label_format, option):
        """ Complete option element """

        # expand attributes
        self.__expand_attributes(stcl, option)

        # set label and value
        if label_path:
            option.string = self.__get_prop_from_json(json, label_path, label_format)
        else:
            option.string = self.__get_prop_from_json(json, value_path, value_format)
        option["value"] = self.__get_prop_from_json(json, value_path, value_format)

    def __expand_table(self, stcl, table):

        # check condition and expand attributes
        if not self.__satisfy_condition(stcl, table):
            table.decompose()
            return

        # check path defined
        path = self.__get_data_path(table)
        if not path:
            return table
        if path:
            empty = self.__is_empty(stcl, path)
            if path.startswith("!"):
                if not empty:
                    table.decompose()
                    return None
                else:
                    self.__expand_children(compose_path(stcl, path), table)
            else:
                if empty:
                    table.decompose()
                    return None

        thead = table.thead
        if thead:
            self.__expand_to_simple_table(stcl, table)
        else:
            #completeChildren(stclContext, s, table);
            #expandToPivotTable(stclContext, s, table);
            pass

        return table

    def __expand_to_simple_table(self, stcl, table):

        # the last tr in thead serve as a template for each row
        thead = table.thead
        trs = thead.find_all("tr")
        if len(trs) == 0:
            self.__expand_children(stcl, table)
            return

        # last tr in header must have a path attribute
        thr = trs[-1]
        pr = self.__get_data_path(thr)
        if not pr:
            self.__expand_children(stcl, table)
            return

        # complete others elements in table
        for elt in self.__get_children(table):
            if not (elt.name.lower() == "thead" or elt.name.lower() == "tbody"):
                self.__expand(stcl, elt)

        # tr in body may serve as template
        thh = thr.find_all("th")
        tbody = table.tbody
        tbr = tbody.tr if tbody else None
        tbd = tbr.find_all("td") if tbr else None

        # create tbody if doesn't exists
        if not tbody:
            tbody = self.__append_new_tag("tbody", table)

        # create attribute list
        attrs = []
        for th in thh:
            value_path, _ = self.__get_property_path(th)
            if self.__td_from_header(th):
                attrs.append(value_path)

        # creates a row for each stencils
        stencils = self.api.get_list(stcl, pr, attrs)
        for elt in json.loads(stencils.content).get("data-value"):
            s = compose_path(stcl, elt.get("data-path"))
            #pwd = getPwd(stclContext, s);
            ntr = self.__append_new_tag("tr", tbody)
            if tbr:
                #copyAndExpandAttributes(stclContext, s, tbr, ntr)
                pass
            else:
                #copyAndExpandAttributes(stclContext, s, thr, ntr)
                pass
            #setDataAPath(stclContext, ntr, pwd);

            # for each column declared in the header
            tbdIndex = 0
            for th in thh:
                value_path, format = self.__get_property_path(th)

                # create td from template
                if self.__td_from_header(th):
                    td = self.__append_new_tag("td", ntr)

                    # adds attributes and data class
                    #copyAndExpandAttributes(stclContext, s, th, td);
                    #String classPath = th.attr(CLASS_ATTRIBUTE);
                    #addClassToElement(stclContext, s, td, classPath);

                    # expands container associated for each row (only if
                    # data-path
                    # defined)
                    # others children (note relative to path) stay in header
                    for f in th.select("[data-path]"):
                        if self.__is_container(f):
                            ff = self.__clone_tag(f)
                            td.append(ff)
                            self.__expand(s, ff)

                # td are defined in body (no content from stencil)
                else:
                    if tbd and len(tbd) > tbdIndex:
                        td = self.__clone_tag(tbd[tbdIndex])
                        tbdIndex = tbdIndex + 1
                        value_path, format = self.__get_property_path(td)
                        # expandAttributes(stclContext, s, td);
                        ntr.append(td)
                    else:
                        td = self.__append_new_tag("td", ntr)

                # adds cell content
                if self.__td_from_header(th):

                    # uses label for content (value can also be used)
                    if value_path and not value_path.startswith("!"):
                        value = elt.get(value_path)
                        td.string = unicode(value)
                else:
                    path = self.__get_data_path(td)
                    self.__expand_container(compose_path(s, path), td)

                # add apath
                #apath = compose(pwd, valuePath)
                #setDataAPath(stclContext, td, apath)

        # suppresses container with data-path from header (div, form)
        # (edit form should be first element)
        for th in thh:
            if self.__td_from_header(th):
                for f in th.select("[data-path]"):
                    if self.__is_container(f):
                        f.decompose()
            self.__expand_children(stcl, th)

        # removes initial tbody content
        if tbr:
            tbr.decompose()

        # expands the tfoot if exists
        # Element tfoot = table.select("tfoot").first();
        # if (tfoot != null) {
        # completeChildren(stclContext, stcl, tfoot);
        # }

        pass

    def __td_from_header(self, th):
        """ returns True is the tag has a value path or a label path """
        value_path = th.get("data-value")
        label_path = th.get("data-label")
        return value_path or label_path

    def __expand_post(self, stcl, post):

        # expand to text value
        value_path, format = self.__get_property_path(post)
        if not value_path:
            return
        value, prop_path = self.__get_property_value(stcl, value_path, format)

        # set value or select attribute
        tag = post.name.lower()
        if tag == "textarea":
            post["value"] = value
        elif tag == "input":
            type = post.get('type')
            if type == "checkbox":
                if value.lower() in ['true', '1', 'vrai', 'ok', 'o', 'oui']:
                    post["checked"] = "checked"
            elif type == "radio":
                if value.lower() == post.get("value"):
                    post["checked"] = "checked"
            else:
                post["value"] = value

        # expand attributes
        self.__expand_attributes(stcl, post)

        # complete name with absolute path
        name = post.get('name')
        if not name:
            name = "%s_" % format if format else "s_"
        post["name"] = name + encode(prop_path)

    def __satisfy_condition(self, stcl, elt):
        cond = elt.get('data-cond')

        # check only if condition defined
        if cond:

            # check slot empty or not
            container = re.compile(r"^(?P<not>[!])?(?P<slot>[\w\/]+)$")
            found = container.search(cond)
            if found:
                slot = found.group('slot')
                empty = self.__is_empty(stcl, slot)
                return not empty if found.group('not') is None else empty
            return False
        return True

    def __is_post(self, elt):
        tags = ["input", "textarea", "output"]
        return elt.name.lower() in tags

    def __is_final(self, elt):
        tags = ["img", "meter",  "progress"]
        return elt.name.lower() in tags

    def __is_container(self, elt):
        """ Return True if the element is a container DOM object """
        tags = ["a", "abbr", "address", "article", "aside", "button", "blockquote"]
        tags += ["caption", "div", "fieldset", "figcaption", "footer", "form", "legend"]
        tags += ["h1", "h2", "h3", "h4", "h5", "h6", "header", "hgroup", "label", "nav", "p"]
        tags += ["pre", "span", "section", "tbody", "tr", "td", "thead", "tfoot"]
        return elt.name.lower() in tags

    def __get_data_path(self, elt):
        """ should be changed to avoid using apath"""
        """ Return data path (data-apath first, the data-path) """

        apath = elt.get('data-apath')
        if apath:
            return decode(apath)
        return elt.get('data-path')

    def __get_property_path(self, elt, attr="data-value"):
        """ Return value path and value format """

        path = elt.get(attr)
        if path and path.find('%') != -1:
            return path.split('%')
        return path, "s"

    def __is_empty(self, stcl, slot):
        dom = "<span data-path='!%s'>empty</span>" % slot
        response = self.api.post_facet(encode(stcl), dom, facet="dom5text")
        return response.content.find('empty') != -1

    def __get_property_value(self, stcl, path, format):
        """ Return property value and property path """

        if not path:
            return "the property path should not be null", stcl

        if path.endswith("^"):
            prop = path[:-1]
            value = encode(prop)
            return value, prop

        if path == ".":
            value = self.api.get_prop(encode(stcl)).content
            return value, stcl

        value_path = compose_path(stcl, path)
        value = self.api.get_prop(encode(value_path)).content
        return value, value_path

    def __expand_attributes(self, stcl, elt):
        """ Expand the element attributes """

        if self.DEBUG:
            elt["debug"] = stcl

        # should be inlined here
        for key in elt.attrs:

            #if key == "data-class":
            #    self.__add_class(stcl, elt, elt[HTMLRenderer.__DATA_CLASS])

            """
            elif key.startswith(HTMLRenderer.__DATA_TEXT_CSS):
                name = key[len(HTMLRenderer.__DATA_TEXT_CSS):]
                value = self.render(stcl, elt[key])
                if value:
                    elt["style"] = "%s %s:%s;" % (elt["style"], name, value)

            else if (key.startsWith(DATA_PROP_CSS) || key.startsWith(DATA_CSS)) {
                String suffix = "";
                String valueName = attr.getValue();
                int indexOf = valueName.indexOf("|");
                /* check for suffix (SHOULD NOT BE USED ANY MORE AS DATA_TEXT_CSS can be used) */
                if (indexOf > 0) {
                    suffix = valueName.substring(indexOf + 1);
                    valueName = valueName.substring(0, indexOf);
                }
                String value = getPropertyValue(stclContext, stcl, valueName);
                if (StringUtils.isNotBlank(value)) {
                    String property = key.substring(DATA_CSS.length());
                    String attribute = elt.attr("style");
                    elt.attr("style", String.format("%s %s:%s%s;", attribute, property, value, suffix));
                }
                elt.removeAttr(key);
            }
            else if (key.startsWith(DATA_PROP)) {
                String name = key.substring(DATA_PROP.length());
                String value = getPropertyValue(stclContext, stcl, attr.getValue());
                if (StringUtils.isNotBlank(value)) {
                    elt.attr(name, value);
                } else {
                    elt.removeAttr(name);
                }
                elt.removeAttr(key);
            }
            else if (key.startsWith(DATA_PROP_PLUS)) {
                String value = getPropertyValue(stclContext, stcl, attr.getValue());
                if (StringUtils.isNotBlank(value)) {
                    String name = key.substring(DATA_PROP_PLUS.length());
                    elt.attr(name, elt.attr(name) + " " + value);
                }
                elt.removeAttr(key);
            }
            else if (key.startsWith(DATA_TEXT)) {
                String name = key.substring(DATA_TEXT.length());
                String value = stcl.getDOM5TextFacet(stclContext, attr.getValue());
                if (StringUtils.isNotBlank(value)) {
                    elt.attr(name, value);
                } else {
                    elt.removeAttr(name);
                }
                elt.removeAttr(key);
            }
            else if (key.startsWith(DATA_TEXT_PLUS)) {
                String value = stcl.getDOM5TextFacet(stclContext, attr.getValue());
                if (StringUtils.isNotBlank(value)) {
                    String name = key.substring(DATA_TEXT_PLUS.length());
                    elt.attr(name, elt.attr(name) + " " + value);
                }
                elt.removeAttr(key);
            }
            else if (key.startsWith(DATA_HTML)) {
                String name = key.substring(DATA_HTML.length());
                String value = stcl.getDOM5Facet(stclContext, attr.getValue());
                if (StringUtils.isNotBlank(value)) {
                    elt.attr(name, value);
                } else {
                    elt.removeAttr(name);
                }
                elt.removeAttr(key);
            }
            else if (key.startsWith(DATA_HTML_PLUS)) {
                String value = stcl.getDOM5Facet(stclContext, attr.getValue());
                if (StringUtils.isNotBlank(value)) {
                    String name = key.substring(DATA_HTML_PLUS.length());
                    elt.attr(name, elt.attr(name) + " " + value);
                }
                elt.removeAttr(key);
            }
            """

    def __add_class(self, stcl, elt, data_class):
        if not data_class:
            return

        # add class attributes
        for m in data_class.split(':'):
            slot = False
            n = False
            if m.endsWith("@"):
                m = m[:len(m)-1]
                slot = True
            if m.endsWith("!"):
                m = m[:len(m)-1]
                n = True

            added, _ = self.__get_property_value(stcl, m, None)
            if (slot and added == 'True') or (n and not added):
                added = m

            elt["class"] = "%s %s" % (elt["class"], added)

    def __set_data_path(self, elt, path):
        """ Set element path attribute """

        elt['data-path'] = path
        elt['data-apath'] = encode(path)

    def __remove_path(self, elt):
        """ Remove all path attributes for security """

        del elt['data-value']
        del elt['data-label']
        del elt['data-cond']

    def __get_children(self, elt):
        for child in elt.children:
            if isinstance(child, Tag):
                yield child

    def __append_new_tag(self, tag, parent):
        elt = self.document.new_tag(tag)
        parent.append(elt)
        return elt

    def __clone_tag(self, elt):
        if isinstance(elt, NavigableString):
            return type(elt)(elt)

        clone = Tag(None, elt.builder, elt.name, elt.namespace, elt.nsprefix)
        # work around bug where there is no builder set
        # https://bugs.launchpad.net/beautifulsoup/+bug/1307471
        clone.attrs = dict(elt.attrs)
        for attr in ('can_be_empty_element', 'hidden'):
            setattr(clone, attr, getattr(elt, attr))
        for child in elt.contents:
            clone.append(self.__clone_tag(child))
        return clone

    def __get_prop_from_json(self, json, path, format):
        return json.get(path)


class _Mode(object):
    BY_VALUE = 1
    BY_LABEL = 2


