#!/usr/bin/python
import sys
import os
import pwd
import re

from pathlib import Path

USER = pwd.getpwduid(os.getuid())[0]
PATH = "/home/" + USER + "/passdmgr/"
PATTERN = r'(\/)+'

def new(parent):
    reg = re.split(PATTERN, sys.argv[2])
    path_ = "".join(reg[:-1])
    file_ = reg[-1]

    new_path = Path(PATH + path_)
    try:
        new_path.mkdir(parents=True)
    except FileExistsError:
        pass

    new_file = Path(PATH + path_ + file_)
    try:
        new_file.touch()
    except FileExistsError:
        print("ERROR: File '" + file_ + "' already exists.\n \
               Type 'passdmgr help' for help.")

def main():
    parent = Path(PATH)
    if len(sys.argv) == 1:
        try:
            parent.mkdir()
            print("'$HOME/password' directory not found...\n \
                   Creating new directory...")
            return 1
        except FileExistsError:
            print_paths()
            return 1

    if sys.argv[1] is "new":
        new()
    elif sys.argv[1] is "insert":
        insert()
    elif sys.argv[1] is "remove":
        remove()
    elif sys.argv[1] is "print":
        print_pwd()
    elif sys.argv[1] is "help":
        show_help()

    return 1

main()
