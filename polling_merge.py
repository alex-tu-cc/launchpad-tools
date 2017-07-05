#!/usr/bin/env python
# -*- coding: utf-8 -*-

# get the merge url list


from argparse import ArgumentParser
from launchpadlib.launchpad import Launchpad
import logging
import os
import pdb




# https://stackoverflow.com/questions/14097061/easier-way-to-enable-verbose-logging
import argparse

#            logger.warning('Protocol problem: %s', 'connection reset', extra=d)

class LPTools(object):
    """Docstring for MyClass. """
    lp = None;
    cachedir = os.path.join(os.environ["HOME"], ".launchpadlib/cache")
    credental_application = None;
    current_project = None;
    def __init__(self, credental_application=None, project_url=None):
        """TODO: to be defined1. """
        self.credental_application = credental_application
        self.lp = Launchpad.login_with(credental_application, 'production', self.cachedir)
        self.setCurrentProject(project_url)

    def setCurrentProject(self, project_url):
        #pdb.set_trace()
        self.current_project = self.lp.load(project_url)
        return self.current_project

    def getCurrentProject(self):
        return self.current_project

    def get_mps(self):
        """get merge proposals of current project"""
        return self.current_project.getMergeProposals()


def main():
    parser = ArgumentParser(prog="launchpad_merge")
    #group = parser.add_mutually_exclusive_group()
    #parser.add_argument("type", type=str, choices=['view', 'message'])
    parser.add_argument('--url', required=True, help="api url, ex. https://api.launchpad.net/1.0/somerville")
    #group.add_argument('--project',require=True, help=" project name" )

    parser.add_argument('--credental_application', help='the credental application name')

    parser.add_argument('-d', '--disable', action="store_true", help = "boolean")
    parser.add_argument("-l", "--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help="Set the logging level")
    args = parser.parse_args()

    if args.logLevel:
        logging.basicConfig(level=logging.getLevelName(args.logLevel))

    lptool = LPTools(args.credental_application,args.url)
    mps = lptool.get_mps()
    for mp in mps:
        print mp.self_link
    # ex. ppa:alextu/test1

if __name__ == "__main__":
    main()
