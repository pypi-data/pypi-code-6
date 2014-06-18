from asserts import assert_true
from ftw.testbrowser import browser


def portlet():
    return browser.css('.labelJarPortlet').first_or_none


def labels():
    assert_true(portlet())
    return dict((label.text, label_color(label))
                for label in portlet().css('.labelListing .labelColor .labelTitle'))


def label_color(label_li):
    return label_li.parent().css('.labelColor').first.attrib.get('data-color')
