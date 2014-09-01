#!/usr/bin/env python
'''
VFS Device metrics module for ZTC

Copyright (c) 2010-2012 Vladimir Rusinov <vladimir@greenmice.info>
Copyright (c) Michal Ludvig <michal@logix.cz> http://www.logix.cz/michal/devel/nagios
Copyright (c) 2011 Murano Software [http://muranosoft.com]
Copyright (c) 2011 Wrike, Inc. [http://www.wrike.com]
Copyright (c) 2011 Artem Silenkov
Copyright (c) 2010 Alex Lov
License: GNU GPL v3

Requirements:
    * Linux 2.6
    * proc filesystem mounted on /proc/
    * /sys/ filesystem
    * smartmontools (for smart checks)
'''

import os
#import stat
import re
import unittest

#import ztc
from ztc.check import ZTCCheck, CheckFail
import ztc.myos

class DiskStats(object):
    major = 0
    minor = 0
    devname = None
    reads = 0
    reads_merged = 0
    sectors_read = 0
    time_read = 0
    writes = 0
    writes_merged = 0
    sectors_written = 0
    time_write = 0
    cur_ios = 0
    time_io = 0
    time_io_weidged = 0
    
    def __repr__(self):
        r = self
        return str( (r.major, r.minor, r.devname, r.reads, r.reads_merged, r.sectors_read,
            r.time_read, r.writes, r.writes_merged, r.sectors_written, r.time_write,
            r.cur_ios, r.time_io, r.time_io_weidged) )
    
    def __str__(self):
        r = self
        ret = """major number: %i
minor mumber: %i
device name: %s
reads completed succesfully: %i
reads merged: %i
sectors read: %i
time spent reading (ms): %i
writes completed: %i
writes merged: %i
sectors written: %i
time spent writing (ms): %i
I/Os currently in progress: %i
time spent doing I/Os (ms): %i
weighted time spent doing I/Os (ms): %i
""" % (r.major, r.minor, r.devname, r.reads, r.reads_merged, r.sectors_read,
            r.time_read, r.writes, r.writes_merged, r.sectors_written, r.time_write,
            r.cur_ios, r.time_io, r.time_io_weidged)
        return ret                 
        

class DiskStatsParser(object):
    """ Class to read and parse /proc/diskstats """
    
    def __init__(self, device, logger):
        self.device = device
        self.logger = logger
    
    def parse(self):
        """ Parse /proc/diskstats file and return DiskStats object """
        # check if device exists
        if os.path.exists('/sys/block/%s' % (self.device)):
            return self._read_diskstats()
        elif os.path.exists('/sys/block/%s' % (self.device + '1')):
            # ...and if it does not exists, look for 1st device partion
            # some installations may have for example /dev/sda1, but not /dev/sda
            # first seen on amazon ec2 instance with device attached as /dev/sda1, not /dev/sda
            self.device = self.device + '1'
            return self._read_diskstats()
        else:
            # there is probably no such device
            self.logger.warn("%s: no such device in /sys/block" % self.device)
            return self._read_diskstats()
    
    def _read_diskstats(self):
        f = open('/proc/diskstats', 'r')
        ret = None
        for l in f.readlines():
            d = self._parse_diskstats_line(l)
            if d.devname == self.device:
                ret = d
        f.close()
        return ret
    
    def _parse_diskstats_line(self, l):
        """ Parse line from /proc/diskstats
                The /proc/diskstats file displays the I/O statistics
                of block devices. Each line contains the following 14
                fields:
                 1 - major number
                 2 - minor mumber
                 3 - device name
                 4 - reads completed succesfully
                 5 - reads merged
                 6 - sectors read
                 7 - time spent reading (ms)
                 8 - writes completed
                 9 - writes merged
                10 - sectors written
                11 - time spent writing (ms)
                12 - I/Os currently in progress
                13 - time spent doing I/Os (ms)
                14 - weighted time spent doing I/Os (ms)
                For more details refer to Documentation/iostats.txt
        (for kernel 2.6)        
        """
        r = DiskStats()
        t = l.split()
        if len(t) == 7:
            # some 2.6 kernels (e.g. with old openvz patches) have 7 params, like in 2.4
            # fix by Artem Silenkov - not best, but working
            #t = t + [0, 0, 0, 0, 0, 0, 0]
            # different format:
            # Field  1 -- # of reads issued
            # Field  2 -- # of sectors read
            # Field  3 -- # of writes issued
            # Field  4 -- # of sectors written
            t = t[:2] + [t[2], t[3], 0, t[4], 0, t[5], 0, t[6], 0, 0, 0, 0] 
        (r.major, r.minor, r.devname, r.reads, r.reads_merged, r.sectors_read,
            r.time_read, r.writes, r.writes_merged, r.sectors_written, r.time_write,
            r.cur_ios, r.time_io, r.time_io_weidged) = \
            map(int, t[:2]) + [t[2], ] + map(int, t[3:])
        
        return r


class DiskStatus(ZTCCheck):
    OPTPARSE_MIN_NUMBER_OF_ARGS = 2
    OPTPARSE_MAX_NUMBER_OF_ARGS = 3
    
    name = 'DiskStatus'
    
    def _get(self, metric, *args, **kwargs):
        #print args
        device = args[0]
        dev_type = 'auto'
        if len(args) > 1:
             dev_type = args[1]
        if metric == 'health':
            return self.get_health(device, dev_type)
        else:
            #ds = DiskStats()
            p = DiskStatsParser(device, self.logger)
            ds = p.parse()
            return ds.__getattribute__(metric)
            raise CheckFail('uncknown metric')
    
    def get_health(self, dev, dev_type='auto'):
        """ get device health (from SMART) """
        dev = '/dev/%s' % (dev, )
        if not os.path.exists(dev):
            return 'NO_DEVICE'
        cmd = '%s -H %s' % (self.config.get('smartctl', '/usr/sbin/smartctl'),
                            dev)
        if dev_type != 'auto':
            cmd += " -d %s" % dev_type
        retcode, c = ztc.myos.popen(cmd, self.logger)
        c = c.strip().splitlines()
        ret = c[-1].split()[-1]
        if ret == '/dev/tweN':
            # this is 3ware raid device;
            # health should be handled in 3ware template
            ret = 'OK'
        return ret         

class MDStatus(ZTCCheck):
    """ Staus of linux software RAID
    Sample /proc/mdstat output:
    
    Personalities : [raid1] [raid5]
    md0 : active (read-only) raid1 sdc1[1]
          2096384 blocks [2/1] [_U]
    
    md1 : active raid5 sdb3[2] sdb4[3] sdb2[4](F) sdb1[0] sdb5[5](S)
          995712 blocks level 5, 64k chunk, algorithm 2 [3/2] [U_U]
          [=================>...]  recovery = 86.0% (429796/497856) finish=0.0min speed=23877K/sec
    
    unused devices: <none>
    """

    name = "mdstatus"

    def _get(self, metric, *arg, **kwarg):
        if metric == 'failed_devs':
            failed_devs = self.get_failed_devs()
            if failed_devs:
                return str(failed_devs)
            else:
                return 'OK'
    
    def get_failed_devs(self):
        failed_devs = []
        active_devs = []
        spare_devs = []
        
        md_re = re.compile('^(md\d+)+\s*:') # pattern to detect md1: bla-bla-bla lines
        dev_re = re.compile('(\w+)\[\d+\](\(.\))*') # pattern to detect sda1[1] (F) in bla-bla-bla md descriptions
        
        f = open('/proc/mdstat', 'r')
        for l in f.readlines():
            if not md_re.match(l):
                continue # skipping lines which are not md status
            #print l
            for d in l.split():
                st = dev_re.match(d)
                if not st:
                    continue # skip 'active', ':' and other
                (dev, status) = st.groups()
                if status == "(F)":
                    failed_devs.append(dev)
                elif status == "(S)":
                    spare_devs.append(dev)
                else:
                    active_devs.append(dev)
        return failed_devs
            
class MountStatus(object):
    """ class for checing mount points and mounted filesystems """
    
    def __init__(self, mount):
        """
            Params: mount - path to mount point
        """
        self.mount = mount
    
    def checkmount(self, required_fs=None):
        """ Chechs if required_fs mounted to mountpoint """
        if (required_fs is None):
            # simple check - no need to check filesystem name
            return os.path.ismount(self.mount)
        # else:
        ret = False
        f = open('/proc/mounts', 'r')
        mounts = f.readlines()
        for m in mounts:
            (dev, mountpoint, fs, flags, dump, pas) = m.split()
            try:
                if os.path.samefile(self.mount, mountpoint):
                    if fs.lower() == required_fs.lower():
                        ret = True
                        break
            except OSError:
                pass
        f.close()
        return ret

class DiskStatsParserTest(unittest.TestCase):

    def setUp(self):
        import logging
        self.logger = logging.getLogger('test')

    def test_diskstats_line_parser(self):
        """ Test parsing of /proc/diskstats file """
        dsp = DiskStatsParser('sda', self.logger)
        ds = DiskStats()

        # 1: simple sda line from 3.1.x kernel
        ds.major = 8
        ds.minor = 0
        ds.devname = 'sda'
        ds.reads = 148516
        ds.reads_merged = 118319
        ds.sectors_read = 7024128
        ds.time_read = 1863284
        ds.writes = 116304
        ds.writes_merged = 375629
        ds.sectors_written = 11643968
        ds.time_write = 17513572
        ds.cur_ios = 0
        ds.time_io = 1429389
        ds.time_io_weidged = 19461480
        assert str(dsp._parse_diskstats_line('   8       0 sda 148516 118319 7024128 1863284 116304 375629 11643968 17513572 0 1429389 19461480')) == str(ds)

        # 2: test for device with '/' in name
        # 104 0 cciss/c0d0 12746 1947 208311 37832 2424476 2120977 36390792 58162004 0 24766012 58198856
        ds.major = 104
        ds.minor = 0
        ds.devname = 'cciss/c0d0'
        ds.reads = 12746
        ds.reads_merged = 1947
        ds.sectors_read = 208311
        ds.time_read = 37832
        ds.writes = 2424476
        ds.writes_merged = 2120977
        ds.sectors_written = 36390792
        ds.time_write = 58162004
        ds.cur_ios = 0
        ds.time_io = 24766012
        ds.time_io_weidged = 58198856
        assert str(dsp._parse_diskstats_line('104 0 cciss/c0d0 12746 1947 208311 37832 2424476 2120977 36390792 58162004 0 24766012 58198856')) == str(ds)



if __name__ == '__main__':
    unittest.main()
