::

       _____                      _  __
      / ____|                    (_)/ _|
     | |  __  ___  _   _ _ __ ___ _| |_ ___ _ __ ___  _   _ ___
     | | |_ |/ _ \| | | | '__/ __| |  _/ _ \ '__/ _ \| | | / __|
     | |__| | (_) | |_| | | | (__| | ||  __/ | | (_) | |_| \__ \
      \_____|\___/ \__,_|_|  \___|_|_| \___|_|  \___/ \__,_|___/

MULTIGOURCE
Author: Christopher Clark (@Frencil)
March 24, 2012

MULTIGOURCE + GOURCIFEROUS
Author: Remy Decausemaker (@Remy_D)
April 17, 2012

Author: Nate Case (irc: Qalthos)
December 6, 2012

Author: David Gay (irc: oddshocks)
March 18, 2013

GOURCIFEROUS
Author: Suzanne Reed (irc: Zanarama)
June 5, 2013


Gource is an open source library for visualizing the growth of
a version controlled source code repository over time with
dynamic, colorful animations.

On GitHub:   https://github.com/acaudwell/Gource

MultiGource is a little script Frencil developed to recurse through
subdirectories containing multiple Git repositories and condense
their logs into a single custom-format log that can be fed to
Gource to produce one massive visualization of many repos.

On GitHub:   https://github.com/Frencil/MultiGource

log_generator.py is a script Qalthos developed based on
log_generator.php to do the same thing, but in Python.

Gourciferous is a collection of tools for configuring and
rendering MultiGource visualizations based on this work.

REQUIREMENTS
============

log_generator.py requires the ``sh`` python module.

GENERATING THE LOG
==================

1. Clone as many repositories as you like into a top-level
   directory. They can be buried in subdirectories.
   Only Git repositories are supported at this time.

2. From the location of log_generator.py::

       python log_generator.py [-h] [-g GIT_FOLDER] [-o LOGFILE] [-c COLORFILE]
                               [-u HLUSER] [-l HLCOLOR] [-y]

   Where {GIT_FOLDER} is the directory containing all of your git
   repositories, and {LOGFILE} is the destination of your custom-format
   log. {COLORFILE} is an optional file, with one color on each line
   in hexdecimal format (ie, '13579AC', with no quotes and no other
   characters) which details which colors to use and in which order.
   {HLUSER} is a name of a contributor whose commits should be highlighted,
   and {HLCOLOR} is the color of the highlighted commits.

GENERATING THE AVATARS
======================

1. Create a domain file that links an email host with a
   file path of the desired avatar png. It should be formatted as::

        emailhost.com|/path/to/avatar
        otherhost.net|/path/to/nextavatar

2. From the location of avatar_gen.py::

        python avatar_gen.py {GIT_FOLDER} {DOMAIN_FILE} [-d {AVATAR_DIR}]

   Where {GIT_FOLDER} is the directory containing all of you git
   repositories (the same as log_generator.py), and {DOMAIN_FILE} is
   the email host, image path file. {AVATAR_DIR} is an optional folder
   where avatars will be saved to. Otherwise, the default is /avatar/.

GENERATING THE VISUALIZATION
============================

Here's the basic command to get your visualization running at 720p::

    % gource --load-config /path/to/multigource.conf -1280x720 {LOGFILE}

WARNING! Running Gource on many big projects like this can take a
long time! Watching your visualization as it renders may be
excrutiatingly slow (and will vary in speed as the complexity of
the content varies).

RECOMMENDATION: Render your Gource visualization as a stream and pipe
it to ffmpeg to get a video file that runs at a consistent speed, can
be edited or uploaded to the internet, whatever.

To do this you'll need to install ffmpeg. Just get it, it's awesome.

Here's an updated command that turns Gource into a stream and pipes it
to ffmpeg. The extra flags on the ffmpeg part are tuned to produce a 720p
video file that has a good balance of high quality and decent file size.
The first is a command from MultiGource, the second is a command that
has worked well for Gourciferous::

    % gource --load-config  /path/to/gource.conf -1280x720 {LOGFILE} --output-ppm-stream - | \
    ffmpeg -an -threads 4 -y -vb 4000000 -s 1280x720 -r 30 -f image2pipe -vcodec ppm -i - {OUTPUTFILE}

    % gource --load-config /path/to/gourciferous.conf -1280x720 {LOGFILE} --output-ppm-stream -| \
    ffmpeg -y -b 3000K -r 60 -f image2pipe -vcodec ppm -i - -vcodec libx264 {OUTPUTFILE}

Please refer to ffmpeg documentation to understand these flags and how
to tweak them. {OUTPUTFILE} is the path to the final video and its format
will be automatically determined by the extension you choose.
(e.g. file.mov, file.flv, file.mp4)

RUNNING THE UNIT TESTS
======================

The test suite can be run with the following command::

    % ./test.py

This will run the log generator on gourciferous itself, which currently
assumes that you do not have any other nested git repositories within it.
