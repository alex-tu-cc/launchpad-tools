#!/usr/bin/env python
# -*- coding: utf-8 -*-

# get the merge url list


from argparse import ArgumentParser
from launchpadlib.launchpad import Launchpad
import logging
import os
import pdb
import re
from LPTools import LPTools


# https://stackoverflow.com/questions/14097061/easier-way-to-enable-verbose-logging
import argparse


def main():
    parser = ArgumentParser(prog="launchpad_merge")
    #group = parser.add_mutually_exclusive_group()
    #parser.add_argument("type", type=str, choices=['view', 'message'])
    parser.add_argument('--project', required=True, help="project name")
    #group.add_argument('--project',require=True, help=" project name" )

    parser.add_argument('--credentials_file', help='the pull path of credental file which could be used to store unencrypted credential. without this, it will encrypt it by default')
    parser.add_argument('--credental_application', help='the credental application name')

    parser.add_argument("-l", "--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help="Set the logging level")
    args = parser.parse_args()

    if args.logLevel:
        logging.basicConfig(level=logging.getLevelName(args.logLevel))
    logger = logging.getLogger()
    lptool = LPTools(args.credentials_file, args.credental_application,args.project)
    mps = lptool.get_mps()
    for mp in mps:
        print mp.self_link
        match = re.search('Bug:.*\+bug/([0-9]+)',mp.description)
        pdb.set_trace()
        for index in range(1,match.lastindex+1):
            lptool.comment_bug(match.group(index),mp.web_link)
    # ex. ppa:alextu/test1

if __name__ == "__main__":
    main()
