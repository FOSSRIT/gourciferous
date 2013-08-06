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

import os
import shutil
import argparse
import sh
import requests
import hashlib
import imghdr


def create_gravatars(root_path, avatar_dir):
    # If dir is a repo, then slurp in the formatted log
    names = dict()

    for path, names, files in os.walk(root_path):
        if '.git' in names:
            gitpath = os.path.join(path, '.git')
            contributors = sh.git("--git-dir", gitpath, "--no-pager", "log",
                                  "--format='%aN|%aE'").strip().split("\n")

            # Get the author
            for entry in contributors:
                line_exp = entry.split('|')
                author = line_exp[0].strip().strip("'")
                email = line_exp[1].strip("'")
                #names[author] = email

                # Pull gravatar and save
                if not os.path.isfile(avatar_dir+author+'.png'):
                    gravatar_url = "http://www.gravatar.com/avatar/" + \
                                   hashlib.md5(email.lower()).hexdigest() + '?'
                    r = requests.get(gravatar_url, params={'d':'404'})

                    print(gravatar_url)
                    print(r.status_code)

                    if r.status_code != 200:
                        # Don't get anything
                        pass
                    else:
                        filename = avatar_dir + author
                        with open(filename, 'w') as file_:
                            file_.write(r.content)

                        # Adds the proper file extension
                        os.rename(filename, filename+'.'+imghdr.what(filename))


def create_files(root_path, domains, avatar_dir):
# Create copy of avatar image with Author name as filename

    # If dir is a repo then slurp in the formatted log
    for path, names, files in os.walk(root_path):
        if '.git' in names:
            gitpath = os.path.join(path, '.git')
            contributors = sh.git("--git-dir", gitpath, "--no-pager", "log",
                                  "--format='%aN|%aE'").strip().split("\n")

            # Get the author and their email host
            for entry in contributors:
                line_exp = entry.split('|')
                author = line_exp[0].strip().strip("'")
                host = line_exp[1].split('@').pop().strip("'")
                avatar = avatar_dir+author+'.png'

                # Create avatar file if it doesn't already exist
                if host in domains and not os.path.isfile(avatar):
                    shutil.copyfile(domains[host], avatar)

if __name__ == '__main__':

    p = argparse.ArgumentParser(description='Creates avatar files')
    p.add_argument('-g', '--gitDir', default=os.getcwd(),
                   help='The directory of git logs')
    p.add_argument('-d', '--domainFile',
                   help='A file with domains and avatar image path')
    p.add_argument('-a', '--avatarDir', default=os.getcwd()+'/avatars/',
                   help='Avatar directory')
    args = p.parse_args()

    root_path = args.gitDir
    avatar_dir = args.avatarDir

    # Create repository if it does not exist
    if not os.path.exists(avatar_dir):
        os.makedirs(avatar_dir)

    if args.domainFile:
        # Read in domain names and the corresponding avatar
        domain_file_location = args.domainFile
        domains = dict()

        with open(domain_file_location) as domain_file:
            for line in domain_file:
                contents = line.split('|')
                domains[contents[0].strip()] = contents[1].strip()

        create_files(root_path, domains, avatar_dir)
    else:
        # Create Gravatars instead
        create_gravatars(root_path, avatar_dir)
