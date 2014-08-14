
# -*- coding: utf-8 -*-

"""
Liquid is a form management tool for web frameworks.
Copyright (C) 2014, Bence Faludi (b.faludi@mito.hu)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, <see http://www.gnu.org/licenses/>.
"""

# dict
def flask( request_values ):

    """
    Flask web framework dialect to convert request.values variable into 
    Liquid Form compatible dictionary.

    @param request_values: Request variables
    @type request_values: MultiDict

    @return: Liquid Form compatible dictionary
    @rtype: dict
    """

    data = { key : ( request_values[ key ] \
        if len( request_values.getlist( key ) ) == 1 \
        else request_values.getlist( key ) ) \
        for key in request_values.keys() }

    return data
