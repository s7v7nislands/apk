#!/usr/bin/env python
# -*- utf-8 -*-

# https://github.com/s7v7nislands/apk

import sys
import fnmatch
import os
import getopt
import zipfile
import json


def get_file(z, ext):
    for i in z.namelist():
        if i.endswith(ext):
            yield i, z.read(i)

def get_json(f, key):
    j = json.loads(f)
    return j.get(key, "%s Not exist" % key)

def get_apk(dirname):
    for root, dirs, files in os.walk(dirname, topdown=False):
        for f in files:
            if f.endswith('apk'):
                yield os.path.join(root, f)

def color(raw):
    if sys.platform == "win32":
        return raw
    else:
        return "\033[91m%s\033[0m" % raw

def main(files, print_all, key):
    for f in files:
        if not zipfile.is_zipfile(f):
            print "%s is not a valid apk file" % f
            continue
        z = zipfile.ZipFile(f, 'r')
        print "%s:" % f
        for i in get_file(z, '.json'):
            if print_all:
                print "%s:\n%s" % (i[0], i[1])
            else:
                print "\t%s %s" % (i[0], color(get_json(i[1], key)))

def usage():
    print """\
usage:
%s [-a] [-k key] [dir]
-a: print whole json file
-k: print value of key, default distro_id
""" % sys.argv[0]


if __name__ == "__main__":
    try:
            opts, args = getopt.gnu_getopt(sys.argv[1:], "hak:", ["help", "all", "key="])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    print opts, args
    print_all = False
    key = "distro_id"
    for o, a in opts:
        if o in ('-a', '--all'):
            print_all = True
        elif o in ('-k', '--key'):
            key = a
    if len(args) == 0:
        args.append('.')
    for d in sys.argv[1:]:
        main(get_apk(d), print_all, key)

