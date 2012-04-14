#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os, ConfigParser
from difm.defaults import APPDIR

class ConfigSection(object): pass

class Config(object):

    _int_opts = ()

    def __init__(self):
        self._file = os.path.join(os.environ['HOME'], APPDIR, 'config.ini')
        self._config = ConfigParser.RawConfigParser()
        self.defaults()
        self.load()

    def defaults(self):
        self._config.add_section('main')
        self._config.set('main', 'listenpw', '')
        self._config.set('main', 'play', 'mplayer -cache 128 -quiet -playlist "%s"')
        self._config.set('main', 'record', 'mplayer -cache 128 -quiet -dumpstream -dumpfile "%s" -playlist "%s"')
        self._config.set('main', 'rec_dir', '')
        self._objectify()
        self.save()

    def load(self):
        if not os.path.isfile(self._file):
            self.defaults()
        elif not os.access(self._file, os.R_OK):
            self.defaults()
        else:
            self._config.read(self._file)
            if self._config.sections():
                self._objectify()
            else:
                self.defaults()

    def save(self, force=False):
        if not os.path.isdir(os.path.dirname(self._file)):
            dirname = os.path.dirname(self._file)
            os.mkdir(dirname)
        if os.path.isfile(self._file) and os.access(self._file, os.W_OK):
            if force:
                self._write()
        elif not os.path.isfile(self._file):
            self._write()

    def _objectify(self):
        for section in self._config.sections():
            if not hasattr(self, section) and section != 'main':
                setattr(self, section, ConfigSection)
            for name, value in self._config.items(section):
                if name in self._int_opts:
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                if section == 'main':
                    setattr(self, name, value)
                else:
                    setattr(eval('self.%s' % section), name, value)

    def _write(self):
        cfile = file(self._file, 'wb')
        self._config.write(cfile)
        cfile.close()

    def __str__(self):
        s = ''
        for section in self._config.sections():
            for name, value in self._config.items(section):
                if s == '':
                    s = '%s=%s' % (name, value)
                else:
                    s = '%s, %s=%s' % (s, name, value)
        return s

