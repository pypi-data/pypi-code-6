# -*- coding: utf-8 -*-
"""
    The default highlighting style for the mkgmap style language.
    :copyright: Copyright 2006-2013 by the Pygments team, see AUTHORS.
    :copyright: Steve Ratcliffe
    :license: BSD, see LICENSE for details.
"""

from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Whitespace


class MkgmapStyle(Style):
    """
    Modified from the default style.
    """

    background_color = "#f8f8f8"
    default_style = ""

    styles = {
        Whitespace:                "#bbbbbb",
        Comment:                   "italic #20a0a0",
        Comment.Preproc:           "noitalic #BC7A00",

        Keyword:                   "bold #3B3B87",
        Keyword.Pseudo:            "nobold",
        Keyword.Type:              "nobold #B00040",

        Operator:                  "#666666",
        Operator.Word:             "bold #AA22FF",

		Name:                      "#b09000",
        Name.Builtin:              "#008000",
        Name.Function:             "#0000FF",
        Name.Class:                "bold #0000FF",
        Name.Namespace:            "bold #0000FF",
        Name.Exception:            "bold #D2413A",
        Name.Variable:             "#660E7A",
        Name.Constant:             "#880000",
        Name.Label:                "#A0A000",
        Name.Entity:               "bold #999999",
        Name.Attribute:            "#660E7A",
        Name.Tag:                  "bold #008000",
        Name.Decorator:            "#AA22FF",

        String:                    "#008000",
        String.Doc:                "italic",
        String.Interpol:           "bold #9B6F68",
        String.Escape:             "bold #668866",
        String.Regex:              "#66bb88",
        String.Symbol:             "#19177C",
        String.Other:              "#008000",
        Number:                    "#666666",

        Generic.Heading:           "bold #000080",
        Generic.Subheading:        "bold #800080",
        Generic.Deleted:           "#A00000",
        Generic.Inserted:          "#00A000",
        Generic.Error:             "#FF0000",
        Generic.Emph:              "italic",
        Generic.Strong:            "bold",
        Generic.Prompt:            "bold #000080",
        Generic.Output:            "#888",
        Generic.Traceback:         "#04D",

        Error:                     "border:#FF0000"
    }
