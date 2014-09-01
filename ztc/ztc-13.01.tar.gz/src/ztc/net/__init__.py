#!/usr/bin/env python
"""
net module for ZTC - contains additional network metrics 

Copyright (c) 2010-2011 Vladimir Rusinov <vladimir@greenmice.info>
Copyright (c) 2010 Murano Software [http://muranosoft.com]
Copyright (c) 2010 Wrike, Inc. [http://wrike.com]
Licensed under GNU GPL v.3
"""

import os

from ztc.check import ZTCCheck

class Conn(ZTCCheck):
    """ Conn class - allows calculate number of connections in various states from netstat """
    
    name = 'net_conn'
    
    OPTPARSE_MIN_NUMBER_OF_ARGS = 0
    OPTPARSE_MAX_NUMBER_OF_ARGS = 1    
    
    _tcp_conn_states = [ 'ESTABLISHED', # = 1
        'SYN_SENT',
        'SYN_RECV',
        'FIN_WAIT1',
        'FIN_WAIT2',
        'TIME_WAIT',
        'CLOSE',
        'CLOSE_WAIT',
        'LAST_ACK',
        'LISTEN',
        'CLOSING'
    ] # use indexof('ESTABLISHED' +1 )
    # ^^^ should be a list, because tuples does not have .index() method til 2.6
    
    def _get_num_sockets(self, proto='tcp', status=None):
        """ reads /proc/net/$proto and calculates number of connections in various states
        
            /proc/net/{tcp,udp,raw} fields:
            0: sl - number of the line
            1: local address
            2: remote address
            3: st - socket status
            4: tx_queue:rx_queue - size of the transmit and receive queues
            5: tr:tm->when - indicates whether a timer is active for this socket
            6: retrnsmt - unused
            7: uid - used id
            8: timeout - unused
            9: inode  
        """
        cnt = 0 # number of connections in requested state
        status_num = 0 # index of requested state
        if status:
            self.logger.debug('Getting field /proc/net/$proto field number for %s' % status)
            # get numeric representation of status text
            status_num = self._tcp_conn_states.index(status) + 1
        f = open(os.path.join('/proc/net/', proto), 'r')
        for l in f.readlines():
            l = l.strip()
            if l.startswith('sl'):
                continue # skip first line
            if status:
                l = l.split()
                if int(l[3], 16) != status_num:
                    # skip statuses we are not looking for
                    continue
            cnt += 1
        f.close()
        return cnt
    
    def _get(self, attr):
        attr = attr.upper()
        if attr == 'ALL':
            attr = None
        return self._get_num_sockets('tcp', attr) + self._get_num_sockets('udp', attr) + self._get_num_sockets('raw', attr)

# test
if __name__ == '__main__':
    c = Conn()
    print c.all
    print c.established
    print c.syn_sent
