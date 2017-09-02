#!/usr/bin/python
import random
import pwd
import sys
import os
import re

USER = pwd.getpwuid(os.getuid())[0]
PATH = "/home/{}/passwdmgr/".format(USER)
PATTERN = r'(\/)+'

def new():
    try:
        reg = re.split(PATTERN, sys.argv[2])
    except IndexError:
        print("ERROR: File not specified\nType 'passwdmgr help' for help")
        return 0
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

def insert():
    try:
        file_ = open(PATH + sys.argv[2], "r+")
    except IsADirectoryError:
        print("ERROR: '%s' is a directory, not file." % (sys.argv[2]))
        return 0
    except FileNotFoundError:
        print("ERROR: '%s' not found." % (sys.argv[2]))
        return 0
    except IndexError:
        print("ERROR: File not specified\nType 'passwdmgr help' for help")
        return 0

    try:
        output = sys.argv[3]
        file_.truncate() # Delete previous lines
        file_.write(output)
    except IndexError:
        print("ERROR: Password not given.\n" + \
              "Command is 'passwdmgr insert <path> <password>'.")
        return 0

def generate():
    chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwYyXxZz!@#$%&"
    password = ""
    for i in range(0,16):
        password += chars[random.randint(0,57)]

    try:
        file_ = open(PATH + sys.argv[2], "r+")
    except IsADirectoryError:
        print("ERROR: '%s' is a directory, not file." % (sys.argv[2]))
        return 0
    except FileNotFoundError:
        print("ERROR: '%s' not found." % (sys.argv[2]))
        return 0
    except IndexError:
        print("ERROR: File not specified\nType 'passwdmgr help' for help")
        return 0

    file_.truncate()
    file_.write(password)
    print("The generated password to '%s' is: \n%s" % (sys.argv[2], password))

def remove():
    try:
        reg = re.split(PATTERN, sys.argv[2])
    except IndexError:
        print("ERROR: File not specified\nType 'passwdmgr help' for help")
        return 0

    path_ = "".join(reg[:-1])

    try:
        os.remove(PATH + sys.argv[2])
    except IsADirectoryError:
        os.rmdir(PATH + sys.argv[2])
    except FileNotFoundError:
        print("ERROR: No such file: '%s'." % (sys.argv[2]))
        return 0

    # Ask to remove the parent directory if it's empty
    if not os.listdir(PATH + path_):
        userinput = input("The '%s' directory is empty" % (path_) + \
                          "  - Do you want to remove it? (yes/no)\n> ")
        if userinput.lower() is "yes" or userinput.lower() is "y":
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
    except IndexError:
        print("ERROR: File not specified\nType 'passwdmgr help' for help")
        return 0

    password = "".join(file_.readlines())
    print(password)

def print_paths():
    for root, dirs, files in os.walk(PATH):
        level = root.replace(PATH, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print("%s%s/" % (indent, os.path.basename(root)))
        subindent = ((' ' * 4) + '|')  * (level + 1)
        for f in files:
            print("%s%s" % (subindent, f))

def search():
    pattern = r'{}'.format(sys.argv[2])
    for root, dirs, files in os.walk(PATH):
        level = root.replace(PATH, '').count(os.sep)
        indent = ' ' * 4 * (level)
        subindent = ((' ' * 4) + '|') * (level + 1)
        for f in files:
            if re.search(pattern, f):
                print("%s%s/" % (indent, os.path.basename(root)))
                print("%s%s" % (subindent, f))

def show_help():
    print("""
+++++++++++++++++++++++++++++++++++
|  passwdmgr: a password manager  |
|              v1.0               |
| github.com/apt-helion/passwdmgr |
+++++++++++++++++++++++++++++++++++

Usage:
    passwdmgr <new/add> [directory/file]
        Creates a new password file.
        e.g 'passwdmgr new Email/gmail'
    passwdmgr <insert> [directory/file] [password]
        Adds a password to a file.
        e.g 'passwdmgr insert Business/site.com goodpassword'
    passwdmgr <generate> [directory/file]
        Generates a random 16 character password into file
        e.g 'passwdmgr generate Email/hotmail.com'
    passwdmgr <remove/rm>
        Removes a file or directory.
        e.g 'passwdmgr rm Internet/reddit'
    passwdmgr <print> [directory/file]
        Prints a password from the file.
        e.g 'passwdmgr print Email/yahoo'
    passwdmgr <ls>
        Lists all files and folders.
    passwdmgr <search/find> [filename]
        Lists all files that match filename with regex.
        e.g 'passwdmgr search .com'
""")

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

    if sys.argv[1] == "new" or sys.argv[1] == "add":
        new()
    elif sys.argv[1] == "insert":
        insert()
    elif sys.argv[1] == "generate":
        generate()
    elif sys.argv[1] == "remove" or sys.argv[1] == "rm":
        remove()
    elif sys.argv[1] == "print":
        print_passwd()
    elif sys.argv[1] == "ls":
        print_paths()
    elif sys.argv[1] == "search" or sys.argv[1] == "find":
        search()
    elif sys.argv[1] == "help":
        show_help()
    else:
        print("ERROR: Unknown argument '%s'\n" % (sys.argv[1]) + \
              "Type 'passwdmgr help' for a list of commands.")


main()
