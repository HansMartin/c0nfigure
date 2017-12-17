#!/usr/bin/python
import os
import sys
from base.configparser import configparser
from base.github import github
from base.config import perror, psuccess, pinfo, base
from subprocess import Popen, PIPE


"""
 A tool to keep a System-Wide Configuration of dotfiles for
 * VIM
 * Terminal
 * ...

 Colorscheme: uses base16-colorscheme (https://github.com/chriskempson/base16)

uses a simple config file to keep all dotfiles in one place and up-to-date

"""


DEBUG = False
BACKUP = False


""" Runs the install.sh script if found """
def run_install(repo_dir, github_dir, script_name):

    base_path = "%s/%s" % (repo_dir, github_dir.split("/")[1])
    full_path = "%s/%s" % (base_path, script_name)


    proc = Popen(["bash", full_path, base_path], stdout=PIPE)

    stdout, stderr = proc.communicate()
    print stdout


"""Making a backup by renaming the File from <name> to <name>.backup"""
def mkBackup(bkFile):
    try:
        os.rename(bkFile, bkFile + ".backup")
        return 1
    except OSError:
        if DEBUG:
            perror("Error making backup of %s" % bkFile)
        return 0



""" Make the actuall symlink, and cares about backups"""
def symlink(source, dest):
	try:
		os.symlink(source, dest)
	except Exception as e:

            if e.errno == 17: # file already existent
                if BACKUP and mkBackup(dest):
                    symlink(source, dest)
                    return 1

            if DEBUG:
                    perror("Failed to Symlink %s to %s" %(source, dest))
                    pinfo("-> Reason: " + str(e))

"""
makes a symlink between program files
if BACKUP is True, make a backup if the file exists
"""
def makeSymlinks(prog_rel):
    global config

    for key, val in prog_rel.iteritems():
        for source, dest in val:
            if DEBUG:
                print "Linking %s to %s" %(source, dest)
            symlink("%s/%s/%s/%s" % (config["repo_dir"], config["github"].split("/")[1],
                key, source), dest)


if len(sys.argv) == 1:
	print """Usage: c0nfigure.py <option>

--init           \tUse this on first run
--config <config>\tPath to config file (=> default @ ~/.c0nfig.conf)
--link           \tmakes the symlink with given information
--push           \tUpdates the repository
--pull           \tRefreshes the files (git pull)
--verbose, -v    \tSome more output
--backup, -b     \tMake backup of prev. symlinks
	"""
	exit(1)


configName = ""
cBase = base()

# Get a config or the default config and parse the file
for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--init":
            cBase.firstRun()
            exit(1)
	if sys.argv[i] == "--config" and len(sys.argv) >= i+2:
            configName = sys.argv[i+1]
        if sys.argv[i] == "--verbose" or sys.argv[i] == "-v":
            DEBUG = True
        if sys.argv[i] == "--backup" or sys.argv[i] == "-b":
            BACKUP = True


cp = configparser(configName)

pResult = cp.parseConfig()

# some errors while parsing
if not pResult:
    exit(1)

# Global config variable & github instance
config = cp.config
gh = github(config)


# get install.sh candidat
if config["install"]:
    print "\n[*] Installation script found: %s" % config["install"]
    dec = raw_input("Do you like to run it? (Y/n): ")
    if dec.lower() == "y":
        run_install(config["repo_dir"], config["github"], config["install"])



for i in range(1, len(sys.argv)):
	if sys.argv[i] == "--push":
		gh.updateRepo()
	elif sys.argv[i] == "--pull":
		gh.refresh()

        elif sys.argv[i] == "--link":
            # Symlink making
            pinfo("Making symlinks...")
            makeSymlinks(cp.replacement_rel)


