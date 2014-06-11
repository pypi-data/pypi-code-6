#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demonstrates how colorise automatically reset colors when quit."""

__date__ = "2014-05-21"  # YYYY-MM-DD

import colorise

ipsum = """Lorem ipsum dolor sit amet, consectetuer adipiscing elit,
sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna
aliquam erat volutpat. Ut wisi enim ad minim veniam, quis
nostrud exerci tation ullamcorper suscipit lobortis nisl ut
aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor
in hendrerit in vulputate velit esse molestie consequat, vel
illum dolore eu feugiat nulla facilisis at vero eros et accumsan
et iusto odio dignissim qui blandit praesent luptatum zzril delenit
augue duis dolore te feugait nulla facilisi. Nam liber tempor
cum soluta nobis eleifend option congue nihil imperdiet doming
id quod mazim placerat facer possim assum. Typi non habent
claritatem insitam; est usus legentis in iis qui facit eorum
claritatem. Investigationes demonstraverunt lectores legere me
lius quod ii legunt saepius. Claritas est etiam processus
dynamicus, qui sequitur mutationem consuetudium lectorum.
Mirum est notare quam littera gothica, quam nunc putamus
parum claram, anteposuerit litterarum formas humanitatis per
seacula quarta decima et quinta decima. Eodem modo typi, qui
nunc nobis videntur parum clari, fiant sollemnes in futurum."""

if __name__ == '__main__':
    colorise.set_color('magenta')

    # All text print after the above call will be in that color...
    print(ipsum)

    # ...until colorise.set_color is called with no argument or colorise
    # is quit as it will automatically reset colorise
