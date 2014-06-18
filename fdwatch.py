#!/usr/bin/python

# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8

"""
Copyright (c) 2014 Janne Blomqvist

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Watch and log the number of fd's a process has open.  Since /proc
doesn't support inotify, polling is needed.
"""

import logging
import os

logger = logging.getLogger(__name__)

def init_log(fname, level=logging.INFO):
    logging.basicConfig(filename=fname, format='%(asctime)s - %(levelname)s \
- %(message)s', \
                            level=level)
    logger.info('fdwatch started.')

def get_nthreads(pid):
    """Get the number of threads of PID"""
    with open('/proc/%d/stat' % pid) as f:
        l = f.readline().split(')')
        nt = l[1].split()[17]
        return int(nt)

def run_main(pid, freq):
    """Main loop"""
    import time
    fdir = '/proc/%d/fd' % pid
    stime = 1. / freq
    maxfds = 0
    alltimemaxfds = 0
    prevfds = 0
    prevday = time.localtime().tm_mday
    while True:
        d = os.listdir(fdir)
        nfds = len(d)
        curday = time.localtime().tm_mday
        if curday != prevday:
            # Day changed, rollover
            logger.info('Daily rollover, max fds for previous day was %d.', \
                            maxfds)
            maxfds = nfds
            prevday = curday
        if nfds > alltimemaxfds:
            alltimemaxfds = nfds
            maxfds = nfds
            logger.info('PID %d has new all time max fds: %d. Threads: %d.', \
                            pid, nfds, get_nthreads(pid))
        elif nfds > maxfds:
            maxfds = nfds
            logger.info('PID %d has new daily max fds: %d. Threads: %d.', pid, \
                            nfds, get_nthreads(pid))
        if nfds != prevfds:
            prevfds = nfds
            logger.debug('PID %d has %d fd:s open, %d threads.', pid, nfds, \
                             get_nthreads(pid))
        time.sleep(stime)

if __name__ == '__main__':
    from optparse import OptionParser
    import sys
    parser = OptionParser("""%prog [options] PID""")
    parser.add_option('-f', '--frequency', dest='freq', \
                          help='Polling frequency, default 100')
    parser.add_option('-d', '--debug', dest='debug', action='store_true', \
                          help='Debug mode, run in foreground, log to stdout')
    parser.add_option('-o', '--output', dest='ofile', \
                          help='Path for log file, default \
/var/log/fdwatch-[PID]')
    parser.add_option('-l', '--loglevel', dest='loglevel', \
                          help='Log level')
    (options, args) = parser.parse_args()
    if len(args) == 0:
        sys.stderr.write('FATAL: Required PID argument missing.\n')
        sys.exit(1)
    pid = int(args[0])
    if options.debug:
        ofile = None
    elif options.ofile:
        ofile = options.ofile
    else:
        ofile = '/var/log/fdwatch-%s' % args[0]
    if options.loglevel:
        loglevel = int(options.loglevel)
    else:
        loglevel = logging.INFO
    if options.freq:
        freq = int(options.freq)
    else:
        freq = 100
    if not options.debug:
        import daemon
        with daemon.DaemonContext():
            init_log(ofile, level=loglevel)
            run_main(pid, freq)
    else:
        init_log(ofile, level=loglevel)
        run_main(pid, freq)
