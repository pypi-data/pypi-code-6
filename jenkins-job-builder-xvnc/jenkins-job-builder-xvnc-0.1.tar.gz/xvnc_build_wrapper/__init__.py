# -*- coding: utf-8 -*-

import xml.etree.ElementTree as XML


def xvnc(parser, xml_parent, data):
    root = XML.SubElement(xml_parent, 'hudson.plugins.xvnc.Xvnc')

    take_screen_shot = data.get('take-screenshot-upon-build-completion', False)
    XML.SubElement(root, 'takeScreenshot').text = str(take_screen_shot).lower()

    use_x_authority = data.get('create-a-dedicated-x-authority-file-per-build', True)
    XML.SubElement(root, 'useXauthority').text = str(use_x_authority).lower()
