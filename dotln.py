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


CONFIG = os.path.expanduser("~/.dotln")


def config_wrap(f):
    """
    Decorater to get config directory
    """
    def config_check(*args, **kwargs):
        '''
        Check for config file
        '''
        if os.path.exists(CONFIG):
            with open(CONFIG, 'r') as config:
                config_dir = config.read().rstrip()
            print "Config found %s" % config_dir
        else:
            print "No Config Found"
            config_dir = raw_input("Please enter dotfiles directory: ")
            if config_dir[-1] != '/':
                config_dir = config_dir + '/'
            with open(CONFIG, 'w') as config:
                config.write(config_dir)

        return f(config_dir)

    # Hide Decorator
    config_check.__name__ = f.__name__
    config_check.__doc__ = f.__doc__
    config_check.__dict__.update(f.__dict__)
    return config_check


def update():
    """
    Run git pull if there are no local changes for all found repos
    """
    print "Updating Repos..."
    for repo in find_repos(None):
        print repo
        # Check for local changes
        try:
            out = cmd_utils.run_cmd("git diff-index --quiet HEAD --", repo)
        except cmd_utils.CommandException:
            print "WARN: Local changes in %s" % repo
            print "Not pulling"
        else:
            out = cmd_utils.run_cmd("git pull", repo)
            print "-" + out.rstrip()


def link():
    """
    Symlink dotfiles into home directory
    """
    print "Symlinking Dotfiles..."
    for f in find_files(None):
        dest = f.split("/")[-1]
        dest = os.path.expanduser("~/.") + dest
        if os.path.exists(dest) is False:
            print "Symlinking %s as %s" % (f, dest)
            os.symlink(f, dest)
        else:
            print "%s already exists, not linking." % dest


def remove():
    """
    Remove symlinks to dotfiles
    """
    print "Removing Dotfiles..."
    for f in find_files(None):
        print f
        f = f.split("/")[-1]
        f = os.path.expanduser("~/.") + f
        if os.path.exists(f):
            if os.path.islink(f):
                do_it = raw_input("Remove %s [y/n]" % f)
                if do_it == 'y':
                    print "Removing %s" % f
                    os.remove(f)
                else:
                    print "Not Removing %s" % f
            else:
                print "File not Link found, no action taken"


@config_wrap
def find_repos(config_dir):
    repos = glob.glob(config_dir + "*/.git")
    repos = [r.split("/.git")[0] for r in repos]
    return repos


@config_wrap
def find_files(config_dir):
    files = glob.glob(config_dir + "*/*")
    return files


if __name__ == "__main__":
    ACTIONS = {"update": update, "remove": remove, "link": link}
    parser = argparse.ArgumentParser(description="Dot(file) L(i)n(ker)")
    parser.add_argument("action", choices=ACTIONS.keys())
    args = vars(parser.parse_args())
    if args['action'] in ACTIONS.keys():
        ACTIONS[args['action']]()
