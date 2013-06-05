import math


projects = set()
with open('hfoss.log') as f:
    for line in f:
        split = line.strip().split('|')
        projects.add(split[3].split('/')[0])

    colors = ['F0F0F0', '454545', 'F03728', 'F8685D', 'F88E86', 'B44C43',
              '9C170D', 'F08828', 'F8A75D', 'F8BC86', 'B47943', '9C520D',
              '1B8493', '4EBAC9', '6FBEC9', '2B666E', '095560', '1FB839',
              '52DB6A', '77DB88', '348A43', '0A771D', 'BFE626', 'D4F35B',
              'DCF383', '97AD41', '7A960C', '841B93', 'BA4EC9', 'BE6FC9',
              '662B6E', '550960',]


    n_wraps = 1 + int(math.ceil(len(projects) / float(len(colors))))
    colors = colors * n_wraps
    color_lookup = dict(zip(projects, colors))

with open('hfoss.log') as f:
    for line in f:
        split = line.strip().split('|')
        project = split[3].split('/')[0]
        split[-1] = color_lookup[project]
        print '|'.join(split)



#['1278077105', 'Tim', 'A', 'mapwarper/public/javascripts/dig/mfbase/ext/air/samples/tasks/ext-2.0/resources/images/default/qtip/bg.gif', 'F0F0F0']
# Here's the plan:
# For each name in the list of projects, choose a color, and iterate through the list like Bean did in Fedmsg Colorizer
