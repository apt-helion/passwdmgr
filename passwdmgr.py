#!/usr/bin/python
import sys
import os
import pwd
import re

from pathlib import Path

USER = pwd.getpwduid(os.getuid())[0]
PATH = "/home/" + USER + "/passdmgr/"
PATTERN = r'(\/)+'

def new():
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
               Type 'passwdmgr help' for help.")
        return 0

def insert():
    try:
        file_ = open(PATH + sys.argv[2], "r+")
    except IsADirectoryError:
        print("ERROR: '" + sys.argv[2] + "' is a directory, not file")
        return 0

    lines = file_.readlines()
    try:
        for lines in lines:
            file_.write(sys.argv[3])
    except IndexError:
        print("ERROR: Password not given.\n \
               Command is 'passwdmgr insert <path> <password>'")
        return 0

def remove():
    try:
        os.remove(PATH + sys.argv[2])
    except FileNotFoundError:
        print("ERROR: No such file: '" + sys.argv[2] + "'")
        return 0

    # Removes the directory if it's empty
    if not os.listdir(PATH + sys.argv[:-1]):
        os.rmdir(PATH + sys.argv[:-1])

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


main()
