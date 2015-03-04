#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
from . import Pitman


def stype(bytestring):
    unicode_string = bytestring.decode(sys.getfilesystemencoding())
    return unicode_string


def parse_options():
    parser = argparse.ArgumentParser(description='CLR Podcast tool.')
    parser.add_argument('-p', '--podcast', type=stype, choices=['CLR',
                        'Mobilee', 'Drumcode', 'Sleaze'], default='CLR')
    subparsers = parser.add_subparsers()

    parser_show = subparsers.add_parser('show')
    parser_show.set_defaults(show=True)
    parser_show.add_argument('-l', '--limit', type=int, default=0,
                             help='limit show to last N episodes')
    parser_show.add_argument('-v', '--verbose', action="store_true",
                             help='verbose output')

    parser_search = subparsers.add_parser('search')
    parser_search.set_defaults(search=True)
    parser_search.add_argument('artist', type=stype, nargs='+',
                               help='search for artist')

    parser_get = subparsers.add_parser('get')
    parser_get.set_defaults(get=True)
    parser_get.add_argument('episode', type=int, nargs='+',
                            help='download episode')

    return parser.parse_args()


def run(args):
    pitman = Pitman(args.podcast)
    pitman.parse()
    if hasattr(args, 'show'):
        pitman.show(args.limit, args.verbose)
    elif hasattr(args, 'search'):
        pitman.search(args.artist)
    elif hasattr(args, 'get'):
        pitman.get(args.episode)


def main():
    args = parse_options()
    run(args)


if __name__ == '__main__':
    main()
