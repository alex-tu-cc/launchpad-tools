#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import logging
import re
from LPTools import LPTools


def main():
    " Because so far, launchpad doesn't support associate merge proposal to \
      bugs, so this tool is used to literally check all merge proposal of \
      project, and past their \"Bug: xxxx\" descripton to associated bugs. "

    parser = ArgumentParser(prog="launchpad_merge")
    parser.add_argument('--project', required=True, help="project name")
    parser.add_argument('--dry_run', action="store_true", help=" dry run")
    parser.add_argument('--credentials_file', help='the pull path of credental \
                        file which could be used to store unencrypted \
                        credential. without this, it will encrypt it by \
                        default')
    parser.add_argument('--credental_application', help='the credental \
                        application name')
    parser.add_argument("-l", "--log", dest="logLevel", choices=['DEBUG',
                        'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="Set the logging level")
    args = parser.parse_args()

    if args.logLevel:
        logging.basicConfig(level=logging.getLevelName(args.logLevel))
    logger = logging.getLogger()
    lptool = LPTools(args.credentials_file, args.credental_application,
                     args.project)
    mps = lptool.get_mps()
    for mp in mps:
        print mp.self_link
        match = re.search('Bug:.*\+bug/([0-9]+)', mp.description)
        for index in range(1, match.lastindex+1):
            logger.debug("comment LP:"+match.group(index))
            lptool.comment_bug(match.group(index), mp.web_link,
                               dry_run=args.dry_run)


if __name__ == "__main__":
    main()
