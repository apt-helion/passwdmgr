#!/usr/bin/python
import sys
import os
import pwd
import re

USER = pwd.getpwuid(os.getuid())[0]
PATH = "/home/" + USER + "/passwdmgr/"
PATTERN = r'(\/)+'

def new():
    reg = re.split(PATTERN, sys.argv[2])
    path_ = "".join(reg[:-1])
    file_ = reg[-1]

    if not os.path.exists(PATH + path_):
        os.makedirs(PATH + path_)
        print("Created the '%s' path." % (path_))

    if not os.path.exists(PATH + sys.argv[2]):
        os.mknod(PATH + sys.argv[2])
        print("Created file: '%s'." % (file_))
    else:
        print("ERROR: File '%s' already exists.\n" % (file_) + \
              "Type 'passwdmgr help' for help.")
        return 0

def insert():
    try:
        file_ = open(PATH + sys.argv[2], "r+")
    except IsADirectoryError:
        print("ERROR: '%s' is a directory, not file." % (sys.argv[2]))
        return 0
    except FileNotFoundError:
        print("ERROR: '%s' not found." % (sys.argv[2]))
        return 0

    try:
        output = sys.argv[3]
        file_.truncate() # Delete previous lines
        file_.write(output)
    except IndexError:
        print("ERROR: Password not given.\n" + \
              "Command is 'passwdmgr insert <path> <password>'.")
        return 0

def remove():
    reg = re.split(PATTERN, sys.argv[2])
    path_ = "".join(reg[:-1])

    try:
        os.remove(PATH + sys.argv[2])
    except FileNotFoundError:
        print("ERROR: No such file: '%s'." % (sys.argv[2]))
        return 0

    # Ask to remove the directory if it's empty
    if not os.listdir(PATH + path_):
        userinput = input("The '%s' directory is empty" % (path_) + \
                          "  - Do you want to remove it? (yes/no)\n> ")
        if userinput.lower() is "yes" or "y":
            os.rmdir(PATH + path_)
            print("Removed empty directory '%s'." % (path_))

def print_passwd():
    try:
        file_ = open(PATH + sys.argv[2], "r")
    except IsADirectoryError:
        print("ERROR: '%s' is a directory, not file." % (sys.argv[2]))
        return 0
    except FileNotFoundError:
        print("ERROR: '%s' not found." % (sys.argv[2]))
        return 0

    password = "".join(file_.readlines())
    print(password)

def main():
    if len(sys.argv) == 1:
        if not os.path.exists(PATH):
            os.mkdir(PATH)
            print("'$HOME/password' directory not found...\n" + \
                  "Creating new directory...")
            return 1
        else:
            print_paths()
            return 1

    if sys.argv[1] == "new":
        new()
    elif sys.argv[1] == "insert":
        insert()
    elif sys.argv[1] == "remove":
        remove()
    elif sys.argv[1] == "print":
        print_passwd()
    elif sys.argv[1] == "help":
        show_help()
    else:
        print("ERROR: Unknown argument '%s'\n" % (sys.argv[1]) + \
              "Type 'passwdmgr help' for a list of commands.")


main()
