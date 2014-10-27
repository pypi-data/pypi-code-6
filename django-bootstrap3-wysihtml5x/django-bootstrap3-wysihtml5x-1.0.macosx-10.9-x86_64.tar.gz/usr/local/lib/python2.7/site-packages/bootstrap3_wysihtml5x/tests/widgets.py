#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup, NavigableString

from django.forms.models import modelform_factory
from django.test import TestCase as DjangoTestCase
from django.utils.html import conditional_escape

from bootstrap3_wysihtml5x.tests.models import ModelTest
from bootstrap3_wysihtml5x.widgets import Wysihtml5xTextareaWidget

class Wysihtml5xToolbarTestCase(DjangoTestCase):
    def setUp(self):
        ModelForm = modelform_factory(ModelTest)
        # self.soup = BeautifulSoup(unicode(ModelForm()))
        self.soup = BeautifulSoup(ModelForm().__str__())

    def test_command_disabled_in_settings(self):        
        # check an active command and the disabled one
        cmd_format_block = self.soup.find('span', attrs={
                'data-bootstrap3_wysihtml5x-command-group': 'formatBlock'})
        cmd_fore_color = self.soup.find('span', attrs={
                'data-bootstrap3_wysihtml5x-command-group': 'foreColor'})
        self.assert_(cmd_format_block != None)
        self.assert_(cmd_fore_color == None) # tests.settings disabled

    def test_dialog_disabled_in_settings(self):        
        # check the active dialog and the disabled one
        dialog_insert_image = self.soup.find('div', attrs={
                'data-bootstrap3_wysihtml5x-dialog': 'insertImage'})
        dialog_create_link = self.soup.find('span', attrs={
                'data-bootstrap3_wysihtml5x-dialog': 'createLink'})
        self.assert_(dialog_insert_image != None)
        self.assert_(dialog_create_link == None) # tests.settings disabled


class Wysihtml5xTextareaWidgetTestCase(DjangoTestCase):
    def test_render_wysihtml5admintextarea_widget(self):
        neilmsg = ModelTest.objects.create(
            first_text="One small step for man", 
            second_text="One giant leap for mankind")
        w = Wysihtml5xTextareaWidget()
        rendered = conditional_escape(w.render("test", neilmsg.second_text))
        expected = '\
<div style="display:inline-block"><div id="unknown-toolbar" class="bootstrap3_wysihtml5x-editor-toolbar">\
  <div class="commands">\
    <span data-bootstrap3_wysihtml5x-command-group="formatBlock" title="Format text header" class="heading-selector">\
      <div>\
        <span data-bootstrap3_wysihtml5x-command="formatBlock" data-bootstrap3_wysihtml5x-command-value="h1">H1</span>\
        <span data-bootstrap3_wysihtml5x-command="formatBlock" data-bootstrap3_wysihtml5x-command-value="h2">H2</span>\
        <span data-bootstrap3_wysihtml5x-command="formatBlock" data-bootstrap3_wysihtml5x-command-value="h3">H3</span>\
        <span data-bootstrap3_wysihtml5x-command="formatBlock" data-bootstrap3_wysihtml5x-command-value="h4">H4</span>\
        <span data-bootstrap3_wysihtml5x-command="formatBlock" data-bootstrap3_wysihtml5x-command-value="h5">H5</span>\
        <span data-bootstrap3_wysihtml5x-command="formatBlock" data-bootstrap3_wysihtml5x-command-value="h6">H6</span>\
      </div>\
    </span>\
    <span data-bootstrap3_wysihtml5x-command="formatBlock" title="Make a paragraph block" data-bootstrap3_wysihtml5x-command-value="p" class="command format-block-p"></span>\
    <span data-bootstrap3_wysihtml5x-command="bold" title="Make text bold (CTRL + B)" class="command"></span>\
    <span data-bootstrap3_wysihtml5x-command="italic" title="Make text italic (CTRL + I)" class="command"></span>\
    <span data-bootstrap3_wysihtml5x-command="underline" title="Underline text (CTRL + U)" class="command"></span>\
    <span data-bootstrap3_wysihtml5x-command="justifyLeft" title="Paragraph left justified" class="command"></span>\
    <span data-bootstrap3_wysihtml5x-command="justifyCenter" title="Paragraph center justified" class="command"></span>\
    <span data-bootstrap3_wysihtml5x-command="justifyRight" title="Paragraph right justified" class="command"></span>\
    <span data-bootstrap3_wysihtml5x-command="insertOrderedList" title="Insert an ordered list" class="command"></span>\
    <span data-bootstrap3_wysihtml5x-command="insertUnorderedList" title="Insert an unordered list" class="command"></span>\
    <span data-bootstrap3_wysihtml5x-command="insertImage" title="Insert an image" class="command insert-image"></span>\
    <span data-bootstrap3_wysihtml5x-command="insertHTML" title="Insert a quote" class="command" data-bootstrap3_wysihtml5x-command-value="<blockquote>quote</blockquote>"></span>\
    <span data-bootstrap3_wysihtml5x-action="change_view" title="Show HTML" class="action" unselectable="on"></span>\
  </div>\
  <div class="bootstrap3_wysihtml5x-dialogs">\
    <div data-bootstrap3_wysihtml5x-dialog="insertImage" style="display:none">  <label>Image:</label>&nbsp;  <input data-bootstrap3_wysihtml5x-dialog-field="src" value="http://">  <a data-bootstrap3_wysihtml5x-dialog-action="save" class="button">Ok</a>&nbsp;  <a data-bootstrap3_wysihtml5x-dialog-action="cancel" class="button">Cancel</a></div>  </div></div><textarea rows="25" cols="40" name="test" class="vLargeTextField">One giant leap for mankind</textarea></div>\
<script>\
new bootstrap3_wysihtml5x.Editor("unknown",{ name: null, style: true, toolbar: "unknown-toolbar", autoLink: true, parserRules: bootstrap3_wysihtml5x_parserRules, parser: bootstrap3_wysihtml5x.dom.parse || Prototype.K, composerClassName: "bootstrap3_wysihtml5x-editor", bodyClassName: "bootstrap3_wysihtml5x-supported", useLineBreaks: true, stylesheets: ["/static/bootstrap3_wysihtml5x/css/stylesheet.css"], placeholderText: null, allowObjectResizing: true, supportTouchDevices: true });\
</script>'
        self.maxDiff = None
        self.assertHTMLEqual(expected, rendered)
