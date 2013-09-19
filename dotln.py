#!/usr/local/bin/python
'''
Dot(file) L(i)n(ker)
Simple script to link / remove and update dot files.
'''
import argparse
import cmd_utils
import glob
import os
import os.path


CONFIG_DIR = "/Users/mark/repos/mine/dotfiles/"


def update():
    print "Updating Repos..."
    for repo in find_repos():
        print repo
        out = cmd_utils.run_cmd("git pull", repo)
        print out[0]


def link():
    print "Symlinking Dotfiles..."
    for f in find_files():
        dest = f.split("/")[-1]
        dest = os.path.expanduser("~/.") + dest
        if os.path.exists(dest) is False:
            print "Symlinking %s as %s" % (f, dest)
            os.symlink(f, dest)
        else:
            print "%s already exists, not linking." % dest


def remove():
    print "Removing Dotfiles..."
    for f in find_files():
        f = f.split("/")[-1]
        f = os.path.expanduser("~/.") + f
        if os.path.exists(f):
            do_it = raw_input("Remove %s [y/n]" % f)
            if do_it == 'y':
                print "Removing %s" % f
                os.remove(f)
            else:
                print "Not Removing %s" % f


def find_repos():
    repos = glob.glob(CONFIG_DIR + "*/.git")
    repos = [r.split("/.git")[0] for r in repos]
    return repos


def find_files():
    files = glob.glob(CONFIG_DIR + "*/*")
    return files


if __name__ == "__main__":
    ACTIONS = {"update": update, "remove": remove, "link": link}
    parser = argparse.ArgumentParser(description="Dot(file) L(i)n(ker)")
    parser.add_argument("action", choices=ACTIONS.keys())
    args = vars(parser.parse_args())
    if args['action'] in ACTIONS.keys():
        ACTIONS[args['action']]()
