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
#Author: Suzanne Reed (irc: zanarama)
#June 20, 2013
#
#*****************************************************
from __future__ import print_function, unicode_literals
from kitchen.text.converters import to_unicode

import os
import string
import sys
import shutil
import argparse
import sh

# Create copy of avatar image with Author name as filename
def create_files(root_path, domains, avatar_dir):
    # If dir is a repo then slurp in the formatted log
    for path, names, files in os.walk(root_path):
        if '.git' in names:
            gitpath = os.path.join(path, '.git')
            contributors = sh.git("--git-dir", gitpath, "--no-pager", "log", "--format='%aN|%aE'").strip().split("\n")
            # Get the author and their email host
            for entry in contributors:
                line_exp = entry.split('|')
                author = line_exp[0].strip().strip("'")
                host = line_exp[1].split('@').pop().strip("'")

                avatar = avatar_dir+author+'.png'
                print(avatar)
                print(host)

                # Create avatar file if it doesn't already exist
                if host in domains and not os.path.isfile(avatar):
                    shutil.copyfile(domains[host],avatar)

if __name__ == '__main__':

    p = argparse.ArgumentParser(description='Create an avatar file for each select contributors')
    p.add_argument('gitDir', help='The directory of git logs')
    p.add_argument('domainFile', help='A file with all domains and cooresponding avatar image')
    p.add_argument('-d', '--avatarDir', default=os.getcwd()+'/avatars/', help='Avatar directory')
    args = p.parse_args()

    root_path = args.gitDir
    domain_file_location = args.domainFile
    avatar_dir = args.avatarDir
    domains=dict()

    # Read in domain names and the corresponding avatar
    with open(domain_file_location) as domain_file:
        for line in domain_file:
            domains[line.split('|')[0].strip()] = line.split('|')[1].strip()

    # Create repository if it does not exist
    if not os.path.exists(avatar_dir):
       os.makedirs(avatar_dir)

    create_files(root_path, domains, avatar_dir)

