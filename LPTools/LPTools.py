#!/usr/bin/env python
# -*- coding: utf-8 -*-

# get the merge url list


import argparse
from argparse import ArgumentParser
from launchpadlib.launchpad import Launchpad
import logging
import os
import pdb
import re

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

    def comment_bug(self,bugid,comment,dry_run = False):
        """ commented something in the bug id"""
        bug_url=self.bug_base_url+bugid
        bug=self.lp.load(bug_url)
        msg="Merge-Proposal: "+comment+"\n---\n"
        old_description = bug.description
        if msg not in old_description:
            new_description = msg + old_description
            if dry_run == False:
                bug.newMessage(content=msg)
                bug.description=new_description
                bug.lp_save()
            else:
                print("dry run...")
            self.logger.info("comment LP: "+bugid)
        else:
            self.logger.debug("message already there in LP: "+bugid)
