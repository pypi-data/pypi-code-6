
#          Copyright Jamie Allsop 2013-2014
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

#-------------------------------------------------------------------------------
#   Timer
#-------------------------------------------------------------------------------

# Python Standard Library Imports
import ctypes
import os
import exceptions
import functools
import timeit

# Custom Imports
import cuppa.build_platform



class LinuxTimesException( exceptions.Exception ):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)



clock_t   = ctypes.c_long
clockid_t = ctypes.c_int
time_t    = ctypes.c_long


class struct_tms( ctypes.Structure ):

    _fields_ = [
        ( 'tms_utime',  clock_t ),
        ( 'tms_stime',  clock_t ),
        ( 'tms_cutime', clock_t ),
        ( 'tms_cstime', clock_t ),
    ]


class struct_timespec( ctypes.Structure ):

    _fields_ = [
        ( 'tv_sec', time_t ),
        ( 'tv_nsec', ctypes.c_long )
    ]


from ctypes.util import find_library

_library = 'rt'

_times = ctypes.CDLL( find_library(_library), use_errno=True ).times
_times.argtypes = [ ctypes.POINTER( struct_tms ) ]

_clock_gettime = ctypes.CDLL( find_library(_library), use_errno=True ).clock_gettime
_clock_gettime.argtypes = [ clockid_t, ctypes.POINTER( struct_timespec ) ]


def _clock_ticks():
    tick_factor = os.sysconf( os.sysconf_names['SC_CLK_TCK'] )
    if tick_factor != -1:
        tick_factor = 1000000000/tick_factor
    else:
        raise TimerException( "os.sysconf_names['SC_CLK_TCK'] returned with error" )
    return tick_factor

_tick_factor = _clock_ticks()


def _process_times():
    times = struct_tms()
    result = _times( ctypes.byref( times ) )

    if result != -1:
        system_time = ( times.tms_stime + times.tms_cstime ) * _tick_factor;
        user_time   = ( times.tms_utime + times.tms_cutime ) * _tick_factor;
    else:
        raise LinuxTimesException( "times() returned with error" )

    return system_time, user_time


def _call_clock_gettime( clk_id ):
    timespec = struct_timespec()

    if _clock_gettime( clk_id, ctypes.byref(timespec) ) < 0:
        error   = ctypes.get_errno()
        message = "clock_gettime failed with with error [{}] - {}".format( error, errno.errorcode[ error ] )
        if error == errno.EINVAL:
            message += " The clock specified [{}] is not supported on this system".format( clk_id )
        raise LinuxTimesException( message )

    return timespec.tv_sec * 1000000000 + timespec.tv_nsec


perf_counter = functools.partial(
        _call_clock_gettime,
        build_platform.constants().CLOCK_MONOTONIC_RAW )


process_time = functools.partial(
        _call_clock_gettime,
        build_platform.constants().CLOCK_PROCESS_CPUTIME_ID )


def wall_time_nanosecs():
    return perf_counter()


def process_times_nanosecs():
    system, user = _process_times()
    return process_time(), user, system

