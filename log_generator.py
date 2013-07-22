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
#Author: David Gay (PEP8 work, fixes)
#March 18, 2013
#
#Author: Suzanne Reed
#June 6, 2013
#
#*****************************************************
from __future__ import print_function, unicode_literals

import time
import os
import string

import sh

import argparse

#**********************
#  USER DEFINED VALUES
#**********************
# Color Library
#  Just a handful of colors that look good in Gource.
colors = [
    'F0F0F0',  # default_color

    '454545',  # main_black

    'F03728',  # main_red
    'F8685D',  # lighter_red
    'F88E86',  # lightest_red
    'B44C43',  # darker_red
    '9C170D',  # darkest_red

    'F08828',  # main_orange
    'F8A75D',  # lighter_orange
    'F8BC86',  # lightest_orange
    'B47943',  # darker_orange
    '9C520D',  # darkest_orange

    'BFE626',  # main_yellow
    'D4F35B',  # lighter_yellow
    'DCF383',  # lightest_yellow
    '97AD41',  # darker_yellow
    '7A960C',  # darkest_yellow

    '1FB839',  # main_green
    '52DB6A',  # lighter_green
    '77DB88',  # lightest_green
    '348A43',  # darker_green
    '0A771D',  # darkest_green

    '1B8493',  # main_blue
    '4EBAC9',  # lighter_blue
    '6FBEC9',  # lightest_blue
    '2B666E',  # darker_blue
    '095560',  # darkest_blue

    '841B93',  # main_purple
    'BA4EC9',  # lighter_purple
    'BE6FC9',  # lightest_purple
    '662B6E',  # darker_purple
    '550960',  # darkest_purple
]


#**********************
# EXECUTABLE CODE
#**********************
def compile_commits(root_path, hlUser, hlColor, years):
    all_commits = dict()
    project_number = 0

    for path, names, files in os.walk(root_path):
        # If dir is a repo then slurp in the log
        if '.git' in names:
            gitpath = os.path.join(path, '.git')
            commits = sh.git("--git-dir", gitpath, "--no-pager", "log",
                             "--name-status").split("\n\n\x1b[33mcommit ")
            project_color = colors[(project_number % len(colors))]
            project_name = os.path.split(path)[1]
            all_commits = project_commits(project_name, commits, all_commits,
                                          project_color, hlUser, hlColor,
                                          years)
            project_number += 1

    return all_commits


#*************************
#  FUNCTIONS
#*************************
def project_commits(project, commits, all_commits, color,
                    hlUser, hlColor, years):
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

            # Extract author and email
            elif line[:8] == "Author: ":
                line_exp = line.split(': ')[1].split('<')
                author = string.capwords(line_exp[0])

            # Append files
            elif (line[:2] == "M\t") or (line[:2] == "A\t") \
                    or (line[:2] == "D\t"):
                #if filter(labmda x: re.match(x, line) is not None, ignore):
                #    continue
                if years:
                    modified_path = '/'.join([year, project, line[2:]])
                else:
                    modified_path = '/'.join([project, line[2:]])
                files.append('|'.join([line[:1], modified_path]))

        # Generate log lines
        for file in files:
            if author == hlUser:
                entry = '|'.join([date, author, file, hlColor]) + '\n'
            else:
                entry = '|'.join([date, author, file, color]) + '\n'
            entry = entry.encode('utf8')
            if not all_commits.get(date):
                all_commits[date] = [entry]
            else:
                all_commits[date].append(entry)

    return all_commits


if __name__ == '__main__':

    p = argparse.ArgumentParser(description='Create a custom Gource log file.')
    p.add_argument('-g', '--gitDirectory', default=os.getcwd(),
                   help='Directory with all Git logs (g for Git!)')
    p.add_argument('-o', '--outputLog', default='customLog.log',
                   help='Custom Log Name (o for Output!)')
    p.add_argument('-c', '--colorFile',
                   help='Custom Color File (c for Color!)')
    p.add_argument('-u', '--hlUser',
                   help='Highlight User Contributions. (u for User!)')
    p.add_argument('-l', '--hlColor', default='CC0000',
                   help='Color to highlight user commits. (l for highLight!)')
    p.add_argument('-y', '--years', action='store_true',
                   help='Seperate commits by Year.')
    args = p.parse_args()

    # Set filepaths
    root_path = args.gitDirectory
    output_file = args.outputLog

    # Use custom color file over default
    if args.colorFile:
        with open(args.colorFile) as colorFile:
            colors = colorFile.readlines()

    # Get highlighted User
    if args.hlUser:
        hlUser = args.hlUser
    else:
        hlUser = "No Highlight"

    # Get highlight Color
    hlColor = args.hlColor

    all_commits = compile_commits(root_path, hlUser, hlColor, args.years)

    commits = [all_commits[x] for x in sorted(all_commits)]

    with open(output_file, 'w') as f:
        for lines in commits:
            f.writelines(lines)
