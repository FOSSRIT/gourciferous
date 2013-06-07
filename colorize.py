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
import sys

colors = ['F0F0F0', '454545', 'F03728', 'F8685D', 'F88E86', 'B44C43',
          '9C170D', 'F08828', 'F8A75D', 'F8BC86', 'B47943', '9C520D',
          '1B8493', '4EBAC9', '6FBEC9', '2B666E', '095560', '1FB839',
          '52DB6A', '77DB88', '348A43', '0A771D', 'BFE626', 'D4F35B',
          'DCF383', '97AD41', '7A960C', '841B93', 'BA4EC9', 'BE6FC9',
          '662B6E', '550960',]


def recolorize_log(input_file):
    """Change colors in log per project."""
    output = []
    projects = []
    with open(input_file) as f:
        for line in f:
            # Split it up into pieces by the '|' character. 
            split = line.strip().split('|')
            
            # Pick out the third one, that's the file that was modified.
            # If the file was foo/bar/baz.rb, pick out just the 'foo' part.  That's
            # the "project name". 
            project = split[3].split('/')[0]

            # Add it (once) to a list of projects to generate an abslute
            # ordering of projects.
            if project not in projects:
                projects.append(project)
            
            # Tack a new color on the end based on that project's index.
            color_index = projects.index(project) % len(colors)
            split[-1] = colors[color_index]
            
            # Sew it all back up with the '|' character and add it to a list of
            # lines to be written out. 
            output.append('|'.join(split))
    return output
    

if __name__ == '__main__':
    if not len(sys.argv) >= 2:
        print("Usage: colorize.py <input_file> [output_file]")
        sys.exit(1)
    input_file = output_file = sys.argv[1]
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    
    output_lines = recolorize_log(input_file)
    with open(output_file, 'w') as f:
        for line in output_lines:
            f.write('{}\n'.format(line))
    

#['1278077105', 'Tim', 'A', 'mapwarper/public/javascripts/dig/mfbase/ext/air/samples/tasks/ext-2.0/resources/images/default/qtip/bg.gif', 'F0F0F0']
# Here's the plan:
# For each name in the list of projects, choose a color, and iterate through the list like Bean did in Fedmsg Colorizer
