from asserts import assert_true
from ftw.testbrowser import browser


def portlet():
    return browser.css('.labelingPortlet').first_or_none


def active_labels():
    assert_true(portlet(), 'labeling portlet is not visible')
    return portlet().css('.activeLabels .labelItem').text


def form():
    node = portlet().css('.updateLabeling').first_or_none
    assert_true(node, 'The updateLabeling form is missing.')
    return node


def form_checkboxes():
    result = {}
    for input in form().inputs:
        if not input.label:
            continue  # submit button
        result[input.label.text] = bool(input.attrib.get('checked'))
    return result
