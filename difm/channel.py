#!/usr/bin/env python
#-*- coding: utf-8 -*-

class Channel(object):
    extmap = {'mp3': 'pls', 'aac': 'pls', 'wma': 'asx'}
    def __init__(self, host='di', name='progressive', fmt='aac', password=''):
        self.host = host
        self.name = name
        self.fmt = fmt
        self.password = password

    @property
    def host(self):
        return self._host

    @property
    def short_host(self):
        return self._host.split('.')[0].replace('radio', '')

    @host.setter
    def host(self, s):
        if s == 'di':
            self._host = 'di.fm'
        elif s == 'sky':
            self._host = 'sky.fm'
        elif s == 'jazz':
            self._host = 'jazzradio.com'
        elif '.' in s:
            self._host = s
        else:
            raise TypeError, 'invalid host %s' % s

    @property
    def fmt(self):
        if not self._fmt:
            return 'aac'
        return self._fmt

    @fmt.setter
    def fmt(self, s):
        s = s.lower()
        if s in ('mp3', 'aac', 'wma'):
            self._fmt = s
        else:
            raise TypeError, 'invalid format %s' % s

    @property
    def password(self):
        return self._pw

    @password.setter
    def password(self, s):
        self._pw = s

    @property
    def public_url(self):
        if self.host == 'di.fm':
            fmtmap = {'mp3': 'public3', 'aac': 'public2', 'wma': 'public5'}
        else:
            fmtmap = {'mp3': 'public3', 'aac': 'public1', 'wma': 'public5'}
        return 'http://listen.%s/%s/%s.%s' % (self.host, fmtmap[self.fmt], self.name, self.extmap[self.fmt])

    @property
    def premium_url(self):
        return 'http://listen.%s/premium_high/%s.%s?%s' % (self.host, self.name, self.extmap[self.fmt], self.password)

    def url(self, fmt):
        self.fmt = fmt
        if self.password:
            return self.premium_url
        else:
            return self.public_url

    def play(self, fmt):
        print self.url(fmt)
        raise NotImplementedError

    def record(self, fmt):
        print self.url(fmt)
        raise NotImplementedError

    def __str__(self):
        if self.password:
            return '%-19s %3s prem %s' % (self.name, self.fmt, self.premium_url)
        else:
            return '%-19s %3s free %s' % (self.name, self.fmt, self.public_url)

