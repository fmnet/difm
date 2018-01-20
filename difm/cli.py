#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import requests, json, argparse, re, tempfile, pickle, shutil, errno, os, sys
from difm.config import Config, APPDIR
from difm.channel import Channel
from difm.channellist import ChannelList

class DIFM(object):

    def __init__(self):
        self.chanfile = os.path.join(os.environ['HOME'], APPDIR, 'channels.dump')
        self.channels = ChannelList()
        self.load()
        self.cfg = Config()
        self.password = self.cfg.listenpw
        self.args = self.parser().parse_args()
        self.args.func(self.args)

    def valid_format(self, s):
        s = s.lower()
        if s in ('mp3', 'aac'):
            return s
        raise TypeError

    def valid_source(self, s):
        s = s.lower()
        if s in ('all', 'di', 'radiotunes', 'jazz', 'rock', 'classic'):
            return s
        raise TypeError

    def parser(self):
        parser = argparse.ArgumentParser(description='di.fm player',
                                         epilog='use <command> -h to get help for each command')
        subparsers = parser.add_subparsers(title='commands', dest='subname')

        play = subparsers.add_parser('play', help='play a channel')
        play.add_argument('channel', type=str, help='select channel')
        play.add_argument('-f', '--format', dest='fmt', type=self.valid_format, default=self.cfg.format, help='select format <aac|mp3>')
        play.add_argument('-s', '--src', dest='src', type=self.valid_source, default='di', help='select format <di|radiotunes|jazz|rock|classic>')
        play.set_defaults(func=self.play)

        rec = subparsers.add_parser('rec', help='record a channel')
        rec.add_argument('channel', type=str, help='select channel')
        rec.add_argument('-f', '--format', dest='fmt', type=self.valid_format, default=self.cfg.format, help='select format <aac|mp3>')
        rec.add_argument('-s', '--src', dest='src', type=self.valid_source, default='di', help='select format <di|radiotunes|jazz|rock|classic>')
        rec.set_defaults(func=self.rec)

        ls = subparsers.add_parser('ls', help='list available channels')
        ls.add_argument('src', type=self.valid_source, nargs='?', default='all', help='select source site <all|di|radiotunes|jazz|classic>')
        ls.add_argument('-f', '--format', dest='fmt', type=self.valid_format, default=self.cfg.format, help='show urls for format <aac|mp3>')
        ls.add_argument('-s', '--sort', action='store_true', help='sort channel list by name')
        ls.set_defaults(func=self.ls)

        return parser

    def play(self, args):
        chan = self.find(args.channel, args.fmt, args.src)
        if chan:
            chan.play(args.fmt, self.cfg)

    def rec(self, args):
        chan = self.find(args.channel, args.fmt, args.src)
        if chan:
            chan.record(args.fmt, self.cfg)

    def find(self, name, fmt, src=''):
        chans = self.channels.find(name)
        if len(chans) > 1 and src != '':
            chans = [x for x in chans if x.short_host == src]
        if len(chans) == 1:
            chan = chans[0]
            chan.password = self.password
            return chan
        else:
            for chan in chans:
                chan.fmt = fmt
                chan.password = self.password
                print(chan)

    def ls(self, args):
        if args.src == 'all':
            res = self.channels
        else:
            res = [c for c in self.channels if c.short_host == args.src]
        if args.sort:
            res = sorted(res, key=lambda c: c.name)
        for chan in res:
            chan.fmt = args.fmt
            chan.password = self.password
            print(chan)

    def update_channels(self):
        self.channels = ChannelList()
        self.channels.extend(self.get_channels('di.fm'))
        self.channels.extend(self.get_channels('radiotunes.com'))
        self.channels.extend(self.get_channels('jazzradio.com'))
        self.channels.extend(self.get_channels('rockradio.com'))
        self.channels.extend(self.get_channels('classicalradio.com'))
        self.save()

    def get_channels(self, host):
        chans = json.loads(requests.get('http://listen.%s/premium_high/' % host).text)
        cl = []
        for part in chans:
            name = part['key']
            c = Channel(host, name)
            cl.append(c)
        return cl

    def load(self):
        try:
            with open(self.chanfile, 'rb') as cfile:
                self.channels = pickle.load(cfile)
        except PermissionError as e:
            print("Can't read channel.dump file: {}".format(e), file=sys.stderr)
            sys.exit(1)
        except (IOError, OSError, EOFError) as e:
            self.update_channels()

    def save(self):
        ensure_path(os.path.dirname(self.chanfile))
        tmp = tempfile.NamedTemporaryFile(delete=False)
        pickle.dump(self.channels, tmp)
        tmp.close()
        shutil.move(tmp.name, self.chanfile)


def ensure_path(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

if __name__ == '__main__':
    DIFM()

