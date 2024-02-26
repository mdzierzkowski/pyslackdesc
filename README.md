# pyslackdesc

## Simple script to generate [Slackware](http://www.slackware.com)'s [slack-desc](https://www.slackwiki.com/Slack-desc) files. Useful if you write [SlackBuilds](https://www.slackwiki.com/Writing_A_SlackBuild_Script)

### Usage

    usage: pyslackdesc [-h] [-i] [-o filename] [-v] [-V] [-n name]
                    [-s "short description" ["short description" ...]]
                    [-d "long description" ["long description" ...]] [-u url]

    pyslackdesc - simple, interactive script to generate Slack-desc files

    optional arguments:
    -h, --help            show this help message and exit
    -i, --interactive     run script in interactive mode
    -o filename, --output filename
                            output file (default is slack-desc)
    -v, --verbose         show generated file
    -V, --version         show program's version number and exit
    commandline mode:
    -n name, --name name  program name (single word)
    -s "short description" ["short description" ...], --short "short description"
    ["short description" ...]
                            program short description (one line)
    -d "long description" ["long description" ...], --description "long description"
    ["long description" ...]
                            program long description (up to 6 lines)
    -u url, --url url     program URL

### Sample

commandline mode:

    pyslackdesc-runner.py -v -n pyslackdesc -s "pyslackdesc - simple script to generate slack-desc files" -d "Simple script to generate Slackware's slack-desc files. Useful if you write SlackBuilds." -u https://github.com/Carrion-Crow/pyslackdesc
    
    Content of /home/crow/dev/pyslackdesc/slack-desc:

    # HOW TO EDIT THIS FILE:
    # The "handy ruler" below makes it easier to edit a package description.  Line
    # up the first '|' above the ':' following the base package name, and the '|'
    # on the right side marks the last column you can put a character in.  You must
    # make exactly 11 lines for the formatting to be correct.  It's also
    # customary to leave one space after the ':'.

               |-----handy-ruler--------------------------------------------------|
    pyslackdesc: pyslackdesc - simple script to generate slack-desc files
    pyslackdesc:
    pyslackdesc: Simple script to generate Slackware's slack-desc files. Useful if
    pyslackdesc: you write SlackBuilds.
    pyslackdesc:
    pyslackdesc:
    pyslackdesc:
    pyslackdesc:
    pyslackdesc:
    pyslackdesc: https://github.com/mdzierzkowski/pyslackdesc
    pyslackdesc:

interactive mode:

    pyslackdesc-runner.py -v -i
