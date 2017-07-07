#!/usr/bin/env python
# -*- coding: utf-8 -*-

# get the merge url list


from argparse import ArgumentParser
from launchpadlib.launchpad import Launchpad
import logging
import os
import pdb
import re


# https://stackoverflow.com/questions/14097061/easier-way-to-enable-verbose-logging
import argparse

#            logger.warning('Protocol problem: %s', 'connection reset', extra=d)

class LPTools(object):
    """Docstring for MyClass. """
    # base url, refer to https://launchpad.net/+apidoc/1.0.html
    base_url = "https://api.launchpad.net/1.0/"
    bug_base_url = base_url+"bugs/"
    lp = None;
    cachedir = os.path.join(os.environ["HOME"], ".launchpadlib/cache")
    credental_application = "hello";
    current_project = None;
    logger=logging.getLogger()
    def __init__(self, credentials_file, credental_application=None, project=None):
        """TODO: to be defined1. """
        if credental_application != None:
            self.credental_application = credental_application
        self.lp = Launchpad.login_with(self.credental_application, 'production', self.cachedir,credentials_file= credentials_file )
        self.setCurrentProject(project)
        self.logger.debug("initiated LPTool")

    def setCurrentProject(self, project):
        self.current_project = self.lp.load(self.base_url + project)
        return self.current_project

    def getCurrentProject(self):
        return self.current_project

    def get_mps(self):
        """get merge proposals of current project"""
        return self.current_project.getMergeProposals()

    def comment_bug(self,bugid,comment):
        """ commented something in the bug id"""
        bug_url=self.bug_base_url+bugid
        bug=self.lp.load(bug_url)
        msg="Merge-Proposal: "+comment+"\n---\n"
        old_description = bug.description
        if msg not in old_description:
            new_description = msg + old_description
            exit()
            bug.newMessage(content=msg)
            bug.description=new_description
            bug.lp_save()
            self.logger.info("comment LP: "+bugid)
        else:
            self.logger.debug("message already there in LP: "+bugid)

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
        match = re.search('Bug:.*\+bug/([0-9]+)',mp.description)
        #pdb.set_trace()
        lptool.comment_bug(match.group(1),mp.web_link)
    # ex. ppa:alextu/test1

if __name__ == "__main__":
    main()
