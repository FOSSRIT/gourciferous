#*****************************************************
#   _____                      _  __                         
#  / ____|                    (_)/ _|                        
# | |  __  ___  _   _ _ __ ___ _| |_ ___ _ __ ___  _   _ ___ 
# | | |_ |/ _ \| | | | '__/ __| |  _/ _ \ '__/ _ \| | | / __|
# | |__| | (_) | |_| | | | (__| | ||  __/ | | (_) | |_| \__ \
#  \_____|\___/ \__,_|_|  \___|_|_| \___|_|  \___/ \__,_|___/
#
#Author: Remy Decausemaker (@Remy_D)
#March 15, 2013
#
#*****************************************************
import math

# These are a lot of colors
colors = ['F0F0F0', '454545', 'F03728', 'F8685D', 'F88E86', 'B44C43',
          '9C170D', 'F08828', 'F8A75D', 'F8BC86', 'B47943', '9C520D',
          '1B8493', '4EBAC9', '6FBEC9', '2B666E', '095560', '1FB839',
          '52DB6A', '77DB88', '348A43', '0A771D', 'BFE626', 'D4F35B',
          'DCF383', '97AD41', '7A960C', '841B93', 'BA4EC9', 'BE6FC9',
          '662B6E', '550960']

projects = set()
with open('LOGFILE.log') as f:
    for line in f:
        split = line.strip().split('|')
        projects.add(split[3].split('/')[0])

n_wraps = 1 + int(math.ceil(len(projects) / float(len(colors))))
colors = colors * n_wraps
color_lookup = dict(zip(projects, colors))

with open('LOGFILE.log') as f:

    # For each line in the old log
    for line in f:

        # Split it up into pieces by the '|' character.
        split = line.strip().split('|')

        # Pick out the third one, that's the file that was modified.
        # If the file was foo/bar/baz.rb, pick out just the 'foo' part.  That's
        # the "project name".
        project = split[3].split('/')[0]

        # Tack a new color on the end based on that project name.
        split[-1] = color_lookup[project]

        # Sew it all back up with the '|' character and print it out.
        print '|'.join(split)


#['1278077105', 'Tim', 'A', 'mapwarper/public/javascripts/dig/mfbase/ext/air/samples/tasks/ext-2.0/resources/images/default/qtip/bg.gif', 'F0F0F0']
# Here's the plan:
# For each name in the list of projects, choose a color, and iterate through the list like Bean did in Fedmsg Colorizer
