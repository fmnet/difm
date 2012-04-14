#!/usr/bin/env python
#-*- coding: utf-8 -*-

import subprocess, shlex, datetime

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

    @property
    def rec_name(self):
        timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M')
        return '%sfm.%s.%s.%s' % (self.short_host, self.name, timestamp, self.fmt)

    def url(self, fmt):
        self.fmt = fmt
        if self.password:
            return self.premium_url
        else:
            return self.public_url

    def play(self, fmt, cfg):
        cmd = cfg.play % self.url(fmt)
        subprocess.call(shlex.split(cmd))

    def record(self, fmt, cfg):
        if cfg.rec_dir:
            rec_path = '%s/%s' % (cfg.rec_dir, self.rec_name)
        else:
            rec_path = './%s' % self.rec_name
        cmd = cfg.record % (rec_path, self.url(fmt))
        print cmd
        subprocess.call(shlex.split(cmd))

    def __str__(self):
        if self.password:
            return '%-19s %3s prem %s' % (self.name, self.fmt, self.premium_url)
        else:
            return '%-19s %3s free %s' % (self.name, self.fmt, self.public_url)

