#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2010 ROMAND Fabrice <fabrice.romand@reims.fnclcc.fr>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import hl7v2
import ADTformats

message =  "MSH|^~\\&|CLINICOM|SHS|BPH-ADT_R|BPH-ADT_R|||ADT^A01|20100606233845315|P|2.3.1||||||8859/1\r"
message += "EVN|A01|201006062338||||201006062338\r"
message += "PID|1||0002389^^^CLINICOM||GUIMOND^Alexandre^^^^^L~GUIMOND^Alexandre^^^^^M||19720124|M|||11 rue des pénitents blancs^Appartement 806^TOULOUSE^^31000^F||0952694264|||0||100009873^^^CLINICOM\r"
message += "PV1|1|I|A7N|R|||||||||||||||100009873^^^CLINICOM|||||||||||||||||||||||||201006062338\r"
message += "ZFU|||||1701|201006062338\r"

badmessage =  "MSH|^~\\&|CLINICOM|SHS|BPH-ADT_R|BPH-ADT_R|||ADT^A01|20100606233845315|P|2.3.1||||||8859/1\r"
badmessage += "EVN|A01|201006062338||||201006062338\r"
badmessage += "PID|1||0002389^^^CLINICOM||GUIMOND^Alexandre^^^^^L~GUIMOND^Alexandre^^^^^M||19720124|M|||11 rue des pénitents blancs^Appartement 806^TOULOUSE^^31000^F||0952694264|||0||100009873^^^CLINICOM\r"
badmessage += "PV1|1|I|A7N|R|||||||||||||||100009873^^^CLINICOM|||||||||||||||||||||||||201006062338\r"
badmessage += "ZzU|||||1701|201006062338\r"

def test_event_is_ok():
    assert ADTformats.ADTFormat.event_is_ok('A01') == True

def test_event_is_NOT_ok():
    assert ADTformats.ADTFormat.event_is_ok('B99') == False

def test_segment_is_ok():
    assert ADTformats.ADTFormat.segment_is_ok('MSH') == True

def test_segment_is_NOT_ok():
    assert ADTformats.ADTFormat.segment_is_ok('ZZZ') == False

def test_event_segment_is_ok():
    assert ADTformats.ADTFormat.event_segment_is_ok('A40', 'MRG') == True

def test_event_segment_is_NOT_ok():
    assert ADTformats.ADTFormat.event_segment_is_ok('A40', 'ZFU') == False

def test_event_segment_is_NOT_ok_Bad_Event():
    assert ADTformats.ADTFormat.event_segment_is_ok('A99', 'ZFU') == False

def test_event_segment_is_NOT_ok_Bad_Segment():
    assert ADTformats.ADTFormat.event_segment_is_ok('A40', 'ZZZ') == False

def test_get_event_segments_sequence():
    assert ADTformats.ADTFormat.get_event_segments_sequence('A40') == ADTformats.ADTFormat.SEGSEQ2
    assert ADTformats.ADTFormat.get_event_segments_sequence('A01') == ADTformats.ADTFormat.SEGSEQ0
    assert ADTformats.ADTFormat.get_event_segments_sequence('A31') == ADTformats.ADTFormat.SEGSEQ1

def test_get_event_segments_sequence_Bad_Event():
    assert ADTformats.ADTFormat.get_event_segments_sequence('AAA') == None

def test_message_is_ok():
    hl7message = hl7v2.hl7Message(message)
    assert ADTformats.ADTFormat.message_is_ok(hl7message) > 0

    hl7message = hl7v2.hl7Message(badmessage)
    assert ADTformats.ADTFormat.message_is_ok(hl7message) < 0

if __name__ == '__main__':
    import doctest
    import nose
    doctest.testmod(ADTformats)
    nose.main()

