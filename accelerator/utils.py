import os
import sys
import urlparse
import urllib
import urllib2
import random
import logging
import re

from math import log
from concurrent import futures

def combine_files(parts, dest):
    with open(dest, 'wb') as output:
        for part in parts:
            with open(part, 'rb') as f:
                output.writelines(f.readlines())
            os.remove(part)
            
def url_fix(s, charset='utf-8'):
    if sys.version_info < (3, 0) and isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))
    
def progress_bar(progress, length=20):
    length -= 2
    if progress < 0:
        progress = 0
    if progress > 1:
        progress = 1
    return "[" + "|"*int(progress*length) + "-"*(length-int(progress*length)) + "]"
    
def is_HTTPRange_supported(url, timeout=15):
    url = url.replace(' ', '%20')
    
    fullsize = get_filesize(url)
    if not fullsize:
        return False
    
    headers = {'Range': 'bytes=0-3'}
    req = urllib2.Request(url, headers=headers)
    urlObj = urllib2.urlopen(req, timeout=timeout)
    filesize = int(urlObj.headers["Content-Length"])
    
    urlObj.close()
    return (filesize != fullsize)

def get_filesize(url, timeout=15):
    try:
        urlObj = urllib2.urlopen(url, timeout=timeout)
    except (urllib2.HTTPError, urllib2.URLError) as e:
        return 0
    try:
        file_size = int(urlObj.headers["Content-Length"])
    except (IndexError,KeyError):
        return 0
        
    return file_size
    
def get_random_useragent():
    l = [   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.73.11 (KHTML, like Gecko) Version/7.0.1 Safari/537.73.11',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:26.0) Gecko/20100101 Firefox/26.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 5.1; rv:26.0) Gecko/20100101 Firefox/26.0',
                ]
    return random.choice(l)

def sizeof_human(num):
    unit_list = zip(['B', 'kB', 'MB', 'GB', 'TB', 'PB'], [0, 0, 1, 2, 2, 2])
    
    if num > 1:
        exponent = min(int(log(num, 1024)), len(unit_list) - 1)
        quotient = float(num) / 1024**exponent
        unit, num_decimals = unit_list[exponent]
        
        if sys.version_info >= (2, 7): 
            format_string = '{:,.%sf} {}' % (num_decimals)
            return format_string.format(quotient, unit)
        else: 
            if quotient != int(quotient): 
                x, y = str(quotient).split('.')
                x = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % int(x))
                y = y[:num_decimals]
                quotient = "%s.%s" % (x, y) if y else x
                return "%s %s" % (quotient, unit)
            else:
                quotient = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % quotient)
                return "%s %s" % (quotient, unit)
            
    if num == 0:
        return '0 bytes'
    if num == 1:
        return '1 byte'

def time_human(duration, fmt_short=False):
    duration = int(duration)
    if duration == 0:
        return "0s" if fmt_short else "0 seconds"
            
    INTERVALS = [1, 60, 3600, 86400, 604800, 2419200, 29030400]
    if fmt_short:
        NAMES = ['s'*2, 'm'*2, 'h'*2, 'd'*2, 'w'*2, 'y'*2]
    else:
        NAMES = [('second', 'seconds'),
             ('minute', 'minutes'),
             ('hour', 'hours'),
             ('day', 'days'),
             ('week', 'weeks'),
             ('month', 'months'),
             ('year', 'years')]
    
    result = []
    
    for i in range(len(NAMES)-1, -1, -1):
        a = duration // INTERVALS[i]
        if a > 0:
            result.append( (a, NAMES[i][1 % a]) )
            duration -= a * INTERVALS[i]
    
    if fmt_short:
        return "".join(["%s%s" % x for x in result])
    return ", ".join(["%s %s" % x for x in result])
    
def create_debugging_logger():
    t_log = logging.getLogger('testingLog')
    t_log.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    t_log.addHandler(console)
    return t_log
    
class DummyLogger(object):

    def __init__(self):
        pass

    def dummy_func(self, *args, **kargs):
        pass

    def __getattr__(self, name):
        if name.startswith('__'):
            return object.__getattr__(name)
        return self.dummy_func
        
class ManagedThreadPoolExecutor(futures.ThreadPoolExecutor):
    def __init__(self, max_workers):
        futures.ThreadPoolExecutor.__init__(self, max_workers)
        self._futures = []
    
    def submit(self, fn, *args, **kwargs):
        future = super(ManagedThreadPoolExecutor, self).submit(fn, *args, **kwargs)
        self._futures.append(future)
        return future
    
    def done(self):
        return all([x.done() for x in self._futures])
       
    def get_exceptions(self):
        l = []
        for x in self._futures:
            if x.exception():
                l.append(x.exception())
        return l
