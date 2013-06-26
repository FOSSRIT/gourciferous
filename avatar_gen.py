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

# Create copy of avatar image with Author name as filename
def create_files(log_path, domains, avatar_dir):
    with open(log_path) as log:

        # Extract email host and create file path with name
        # Currently designed to work with a file log_generator doesn't create
        for entry in log:
            entry = to_unicode(entry, 'utf-8')
            line_exp = entry.split('|')
            avatar = avatar_dir+line_exp[0].rstrip()+".png"
            host = line_exp[0]

            # Create file
            if host in domains and not os.path.isfile(avatar):
                shutil.copyfile(domains[host],avatar)

if __name__ == '__main__':

    p = argparse.ArgumentParser(description='Create an avatar file for each select contributors')
    p.add_argument('avatarFile', required=True, help='A log with all contributors and email host')
    p.add_argument('domainFile', required=True, help='A file with all domains and cooresponding avatar image')
    p.add_argument('-d', '--avatarDir', default=os.getcwd()+'/avatars/', help='Avatar directory')
    args = p.parse_args()

    log_path = args.avatarFile
    domain_file_location = args.domainFile
    avatar_dir = args.avatarDir
    domains=dict()

    # Read in domain names and the cooresponding avatar
    with open(domain_file_location) as domain_file:
        for line in domain_file:
            domains[line.split('|')[0].strip()] = line.split('|')[1].strip()

    # Create repository if it does not exist
    if not os.path.exists(avatar_dir):
       os.makedirs(avatar_dir)

    create_files(log_path, domains, avatar_dir)

