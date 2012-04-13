#!/usr/bin/env python
#-*- coding: utf-8 -*-

import argparse

class DIFM_CLI(object):
    def __init__(self):
        self.args = self.parser().parse_args()
        self.args.func(self.args)

    def valid_format(self, s):
        s = s.lower()
        if s in ('mp3', 'aac', 'wma'):
            return s
        raise TypeError

    def valid_source(self, s):
        s = s.lower()
        if s in ('all', 'di', 'sky', 'jazz'):
            return s
        raise TypeError

    def parser(self):
        parser = argparse.ArgumentParser(description='di.fm player',
                                         epilog='use <command> -h to get help for each command')
        parser.add_argument('-p', '--premium', action='store_true', help='use premium streams')
        subparsers = parser.add_subparsers(title='commands', dest='subname')

        play = subparsers.add_parser('play', help='play a channel')
        play.add_argument('channel', type=str, help='select channel')
        play.add_argument('-f', '--format', type=self.valid_format, default='aac', help='select format <aac|mp3|wma>')
        play.set_defaults(func=self.play)

        rec = subparsers.add_parser('rec', help='record a channel')
        rec.add_argument('channel', type=str, help='select channel')
        rec.add_argument('-f', '--format', type=self.valid_format, default='aac', help='select format <aac|mp3|wma>')
        rec.set_defaults(func=self.rec)

        ls = subparsers.add_parser('ls', help='list available channels')
        ls.add_argument('src', type=self.valid_source, help='select source site <all|di|sky|jazz>')
        ls.add_argument('-f', '--format', type=self.valid_format, default='aac', help='show urls for format <aac|mp3|wma>')
        ls.add_argument('-w', '--write', action='store_true', help='write channel list')
        ls.set_defaults(func=self.ls)

        return parser

    def play(self, args):
        print "play %s" % args

    def rec(self, args):
        print "record %s" % args

    def ls(self, args):
        print "list %s" % args

if __name__ == '__main__':
    DIFM_CLI()

