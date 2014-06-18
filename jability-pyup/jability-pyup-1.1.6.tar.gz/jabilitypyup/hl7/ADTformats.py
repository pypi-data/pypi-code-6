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

class ADTFormat:

    EVENT_LIST = {  'A01' : 'Admit / Visit Notification',
                    'A02' : 'Transfer a Patient',
                    'A03' : 'Discharge / End Visit',
                    'A04' : 'Register a Patient',
                    'A05' : 'Pre-Admit a Patient',
                    'A06' : 'Change an Outpatient to an Inpatient',
                    'A07' : 'Change an Inpatient to an Outpatient' ,
                    'A08' : 'Update Patient Information',
                    'A11' : 'Cancel Admit / Visit notification',
                    'A12' : 'Cancel Transfer',
                    'A13' : 'Cancel Discharge / End Visit',
                    'A21' : 'Patient Goes on a Leave of Absence',
                    'A22' : 'Patient Returns from a Leave of Absence',
                    'A28' : 'Add Person or Patient Information',
                    'A31' : 'Update Person Information',
                    'A38' : 'Cancel Pre-Admit',
                    'A40' : 'Merge Patient - Patient Identifier List',
                    'A44' : 'Move Account Information - Patient Account Number'
                }

    SEGMENT_LIST = {    'MSH' : 'Message Header',
                        'EVN' : 'Event Type',
                        'PID' : 'Patient Identification',
                        'MRG' : 'Merge patient Information',
                        'PV1' : 'Patient Visit',
                        'ZFU' : 'Functionnal Unit'
                    }

    SEGSEQ0 = [ 'MSH', 'EVN', 'PID', 'PV1', 'ZFU' ]
    SEGSEQ1 = [ 'MSH', 'EVN', 'PID' ]
    SEGSEQ2 = [ 'MSH', 'EVN', 'PID', 'MRG' ]

    STANDARD_SEQUENCE_EVENT_LIST = SEGSEQ0

    NON_STANDARD_SEQUENCE_EVENT_LIST = {    'A28': SEGSEQ1,
                                            'A31': SEGSEQ1,
                                            'A40': SEGSEQ2,
                                            'A44': SEGSEQ2 }

    @staticmethod
    def event_is_ok(event_code):
        if not ADTFormat.EVENT_LIST.has_key(event_code):
            return False
        return True

    @staticmethod
    def segment_is_ok(segment_code):
        if not ADTFormat.SEGMENT_LIST.has_key(segment_code):
            return False
        return True

    @staticmethod
    def event_segment_is_ok(event_code, segment_code):
        if ADTFormat.segment_is_ok(segment_code) and ADTFormat.event_is_ok(event_code):
                seq = ADTFormat.get_event_segments_sequence(event_code)
                if segment_code in seq:
                    return True
        return False

    @staticmethod
    def get_event_segments_sequence(event_code):
        if not ADTFormat.event_is_ok(event_code):
            return None
        if ADTFormat.NON_STANDARD_SEQUENCE_EVENT_LIST.has_key(event_code):
            return ADTFormat.NON_STANDARD_SEQUENCE_EVENT_LIST[event_code]
        return ADTFormat.STANDARD_SEQUENCE_EVENT_LIST

    @staticmethod
    def message_is_ok(hl7message):
        if isinstance(hl7message, hl7v2.hl7Message):
            if hl7message.is_hl7v2():
                smsh = hl7message.get_segment_by_name('MSH')
                type = smsh.fields[8].values[0].components[0].value
                event = smsh.fields[8].values[0].components[1].value
                if not type == 'ADT' or not ADTFormat.event_is_ok(event):
                    return -1
                for segment in hl7message.segments:
                    if not ADTFormat.event_segment_is_ok(event, segment.name):
                        return -2
                for segmentname in ADTFormat.get_event_segments_sequence(event):
                    if segmentname not in [segment.name for segment in hl7message.segments]:
                        return -3
                return 1
            return -8
        return -9
