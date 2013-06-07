#!/usr/bin/env python
#
#*****************************************************
#   _____                      _  __
#  / ____|                    (_)/ _|
# | |  __  ___  _   _ _ __ ___ _| |_ ___ _ __ ___  _   _ ___
# | | |_ |/ _ \| | | | '__/ __| |  _/ _ \ '__/ _ \| | | / __|
# | |__| | (_) | |_| | | | (__| | ||  __/ | | (_) | |_| \__ \
#  \_____|\___/ \__,_|_|  \___|_|_| \___|_|  \___/ \__,_|___/
#
#MultiGource (log_generator.php)
#Author: Christopher Clark (@Frencil)
#March 24, 2012
#
#Gourciferous (log_generator.py)
#Author: Nate Case (irc: Qalthos)
#December 6, 2012
#
#Author: David Gay (PEP8 work)
#March 18, 2013
#
#Author: Suzanne Reed
#June 6, 2013
#
#*****************************************************
from __future__ import print_function, unicode_literals

import time
import os
import re
import string

import sh

#**********************
#  USER DEFINED VALUES
#**********************
#
# Root path
#   EXAMPLE: '/home/chris/repos'
root_path = '/home/nate/workspace/foss@rit'

# Color Regexes
#  Gource has some default colors it applies based on file type but
#  this can make it hard to tell which repos are which. Here you can
#  define regular expressions that will map whole directories to a
#  color. It can be a top-level directory of a repo or a subdirectory
#  at any depth.
#  FORMAT: {REGEX} : {COLOR}
#          Where {REGEX} is your directory (from root_path) with
#      a leading pipe (| - prevents false positives)
#      and {COLOR} is either a six-digit hex (e.g. '#FF0000' or 'c75d39')
#      or a key in the pre-defined color library (e.g. 'main_green').
#  EXAMPLES: '/\|big_repos\/big_repo_A\//': 'main_green',
#            '/\|little_repos\/little_repo_B\//': '#FF0000',
#            '/\|weird_repos\/weird_repo_C\//': 'c75d39',
color_reg = {
    r'^[AMD]\|(\d+)/hanginwit-threebean/': 'lightest_red',
    r'^[AMD]\|(\d+)/Open-Video-Chat/': 'darker_red',
    r'^[AMD]\|(\d+)/hfoss/': 'darkest_red',
    r'^[AMD]\|(\d+)/tos-rit-projects-seminar/': 'main_orange',
    r'^[AMD]\|(\d+)/Gold-Rush-Server/': 'lightest_yellow',
    r'^[AMD]\|(\d+)/FortuneEngine/': 'lighter_yellow',
    r'^[AMD]\|(\d+)/fortune_hunter/': 'main_yellow',
    r'^[AMD]\|(\d+)/lemonade-stand/': 'darker_yellow',
    r'^[AMD]\|(\d+)/lazorz/': 'darkest_yellow',
    r'^[AMD]\|(\d+)/civx/': 'main_green',
    r'^[AMD]\|(\d+)/election/': 'darker_green',
    r'^[AMD]\|(\d+)/monroe-elections-data/': 'darkest_green',
    r'^[AMD]\|(\d+)/RITRemixerator/': 'lightest_blue',
    r'^[AMD]\|(\d+)/WebBot/': 'darker_blue',
    r'^[AMD]\|(\d+)/blocku/': 'darkest_blue',
}

# Color Library
#  Just a handful of colors that look good in Gource.
color_lib = {
    'default_color': 'F0F0F0',

    'main_black': '454545',

    'main_red': 'F03728',
    'lighter_red': 'F8685D',
    'lightest_red': 'F88E86',
    'darker_red': 'B44C43',
    'darkest_red': '9C170D',

    'main_orange': 'F08828',
    'lighter_orange': 'F8A75D',
    'lightest_orange': 'F8BC86',
    'darker_orange': 'B47943',
    'darkest_orange': '9C520D',

    'main_blue': '1B8493',
    'lighter_blue': '4EBAC9',
    'lightest_blue': '6FBEC9',
    'darker_blue': '2B666E',
    'darkest_blue': '095560',

    'main_green': '1FB839',
    'lighter_green': '52DB6A',
    'lightest_green': '77DB88',
    'darker_green': '348A43',
    'darkest_green': '0A771D',

    'main_yellow': 'BFE626',
    'lighter_yellow': 'D4F35B',
    'lightest_yellow': 'DCF383',
    'darker_yellow': '97AD41',
    'darkest_yellow': '7A960C',

    'main_purple': '841B93',
    'lighter_purple': 'BA4EC9',
    'lightest_purple': 'BE6FC9',
    'darker_purple': '662B6E',
    'darkest_purple': '550960',
}


#**********************
# EXECUTABLE CODE
#**********************


def main():
    all_commits = dict()

    for path, names, files in os.walk(root_path):
        # If dir is a repo then slurp in the log
        if '.git' in names:
            os.chdir(path)
            #print('Checking log at %s' % path)
            commits = sh.git("--no-pager", "log", "--name-status") \
                .split("\n\n\x1b[33mcommit ")
            #print('Done!')
            all_commits = slurp_commits(path, commits, all_commits)

    all_commits = sorted(all_commits.values())
    scalar_log = ''.join(all_commits)
    try:
        scalar_log = scalar_log.encode('utf8')
    except UnicodeEncodeError:
        scalar_log = scalar_log.encode('windows-1252')
    print(scalar_log)


#*************************
#  FUNCTIONS
#*************************


def slurp_commits(path, commits, all_commits):
    year = None
    for commit in commits:
        commit = commit.split("\n")
        files = list()
        date = 0
        author = ''

        for line in commit:
            # Skip blanks
            if not line.strip():
                continue

            # Extract date
            if line[:8] == "Date:   ":
                # Python and %z don't get along
                date = line[8:].split(' -')[0].split(' +')[0]
                year = date.split()[-1]
                date = time.mktime(
                    time.strptime(date, '%a %b %d %H:%M:%S %Y'))
                date = str(int(date))

            # Extract author
            elif line[:8] == "Author: ":
                line_exp = line.split(': ')[1].split('<')[0]
                author = string.capwords(line_exp)

            # Append files
            elif (line[:2] == "M\t") or (line[:2] == "A\t") \
                 or (line[:2] == "D\t"):
                #if filter(labmda x: re.match(x, line) is not None, ignore):
                #    continue
                files.append('|'.join([line[:1],
                                       '/'.join([year,
                                                 os.path.split(path)[1],
                                                 line[2:]])]))

        # Generate log lines
        for file in files:
            color = color_lib['default_color']
            for regex in filter(lambda regex: re.match(regex, file),
                                color_reg):
                color = color_lib.get(color_reg[regex]) or color

            if not all_commits.get(date):
                all_commits[date] = ''
            entry = '|'.join([date, author, file, color]) + "\n"
            all_commits[date] += entry

        # Remove newline at end of each date's commits so that colorize.py
        # doesn't crash due to reading in a blank line.
        for date, entries in all_commits.items():
            all_commits[date] = all_commits[date][:-1]
            

    return all_commits


if __name__ == '__main__':
    main()
