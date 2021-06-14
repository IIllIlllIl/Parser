#
# wang.tr@outlook.com
#

import os

def read_file(path):
    if not os.path.isfile(path):
        return ""
    file = open(path, "r")
    buf = file.read()
    file.close()
    return buf


def write_file(path, msg):
    if os.path.isfile(path):
        os.remove(path)

    file = open(path, "a")
    for line in msg:
        file.write(str(line) + "\n")
    file.close()

def add_file(path, msg):
    if os.path.isfile(path):
        file = open(path, "a")
        for line in msg:
            file.write(str(line) + "\n")
        file.close()
        return 0

    return -1


def str_file(path, msg):
    if os.path.isfile(path):
        os.remove(path)

    file = open(path, "a")
    for line in msg:
        file.write(line.str() + "\n")
    file.close()

