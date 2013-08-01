..title:: Gource: Storytelling via Sourcecode

Gourciferous
============

**Storytelling via Sourcecode**

*Suzanne Reed, Red Hat Intern*

----

About Me
========

I'm **Suzanne Reed**, and I am a **Red Hat** intern.

I'm also part of the RIT Lab for Technological Literacy, or **the FOSSBox**.

I'm in my third year at **RIT** for **Computer Engineering**.

----

Don't tell, Show
================

Gource is a **version control visualization** tool.

It turns the revision history log into an **animated tree**.

Directories are branches, and files are leaves.

----

Writing the Story
=================

Gource can use **custom logs** to affect how a story plays.

**log_generator.py** is a tool to create custom logs. It has a lot of options:

-   Multi-Gource

-   Colorizing

-   User Highlighting

-   Branches by Year

----

The Plot Thickens
=================

Settings can be controlled either command-line or in a **config file**.

The overall message of a Gource story is told in the **setting**, **timing**,
and **characters**. A lot of trial and error can be needed to get them just
right.

----

Character Development
=====================

Custom avatars are a way to highlight individuals and groups. **avatar_gen.py**
is a helpful tool to quickly create the avatar files.

It takes a file that contains email domains and an image to user as an avatar.

    *redhat.com|shadowman.png*
    *fedoraproject.org|fedora_logo.png*

Or Gravatars can be used for avatars.

----

Publishing
==========

To record Gource visualizations a **ppm stream** is outputted and piped into
**ffmpeg**.

% gource --load-config /path/to/gourciferous.conf -1280x720 {LOGFILE} --output-ppm-stream -| \
ffmpeg -y -b 3000K -r 60 -f image2pipe -vcodec ppm -i - -vcodec libx264 {OUTPUTFILE}

----

A Tribute
=========

This visualization highlights the contributions in **YUM** by **Seth Vidal**.
It uses many of the techniques discussed.

http://youtu.be/OARZB0jGziQ

----

Acknowledgements
================

Gource - https://github.com/acaudwell/Gource
            Andrew Caudwell

Multi-Gource - https://github.com/Frencil/MultiGource
            Christopher Clark

Red Hat Mentors and Fellow FossBoxers
            Remy Decausemaker
            Nathanial Case
            Ralph Bean
            Luke Macken
            David Gay

----
