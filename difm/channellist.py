#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re

class ChannelList(list):
    def __init__(self, *args):
        super(ChannelList, self).__init__(*args)

    def names(self):
        return [chan.name for chan in self]

    def urls(self):
        return [chan.url for chan in self]

    def find(self, name):
        res = [chan for chan in self if name == chan.name]
        if not res:
            res = [chan for chan in self if re.search(name, chan.name)]
        return res

