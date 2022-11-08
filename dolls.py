#!/usr/bin/env python
# -*- coding: ASCII -*-
# Enchanted Dolls 1.0
# A helper for making symbol links.
# Python 3 is recommended for interpreting.
import os, shutil
from os import listdir
from shutil import move
from os.path import basename, islink, realpath, exists
from sys import version_info, argv, stderr

usage = '''usage: dolls.py <command>

commands:

    link <path>             Set <path> as the target directory, then create symbol links (to the files in the target) in a new directory of the same name.

    update                  Update the current directory by removing broken links, then create a symbol link for each new file in the pre-set target directory.

    transfer [file]         Move a file into the pre-set target directory, then create a symbol link to the file. If [file] is not given, all non-symlink files in the current directory are moved. [file] must be a file name.

    sync                    Same as running "update" and then "transfer."

    delete <symlink>        Delete the file or directory that a symbol link points to, then remove the link. It is recursive when deleting directories. (Warning: This deletes the real file/directory)

    help                    Show this help message and exit.
'''

if version_info.major < 3:
    input = raw_input

storage = '.enchanted_doll_target'

def delete(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)

def symlink(target):
    os.symlink(target, basename(target))

def hint(kind = 'Transferring', file = ''):
    print('\033[1;96m' + kind + '\033[0m ' + file)

def ask(question):
    return input('\033[1;95m[?]\033[0m ' + question + ' [y/N] ')

def printErrMsg(msg):
    stderr.write('\033[1;91m[Error]\033[0m ' + msg + '\n')

def check_if_exists(path):
    if not exists(path):
        printErrMsg('"%s" not found.' % path)
        exit(2)

def remove_if_broken(link):
    path = os.readlink(link)
    if exists(path): #not broken
        return False
    else:
        print('\033[93m[!]\033[0m The link to "%s" was broken. Removing...' % path)
        os.remove(link)
        return True

def link_with(path):
    target = realpath(path)
    dirname = basename(target)
    check_if_exists(path)
    if exists(dirname):
        kind = ''
        if os.path.isdir(dirname):
            kind = 'subdirectory'
        else:
            kind = 'file'
        printErrMsg('A ' + kind + ' named "' + dirname + '" already exists in the current directory.')
        exit(-1)
    else:
        os.mkdir(dirname)
        print('\033[1;94m%s\033[0m created.' % dirname)
    os.chdir(dirname)
    target += os.sep
    for name in listdir(target):
        hint('Linking', target + name)
        symlink(target + name)
    with open(storage, 'w') as stored:
        stored.write(target)

def update():
    path = ''
    with open(storage, 'r') as stored:
        path = stored.readline().strip('\n')
    for name in listdir('.'):
        if islink(name):
            remove_if_broken(name)
    for name in listdir(path):
        file = path + name
        if exists(name):
            if islink(name):
                if os.readlink(name) == file:
                    continue
            elif ask(name + " exists. Overwrite local file?") in ('y', 'yes'):
                delete(name)
                hint('Linking', file)
            elif ask("Overwrite the remote file? (Warning: The file here will be replaced with a symbol link)") in ('y', 'yes'):
                delete(file)
                hint('Transferring', name)
                move(name, file)
            else:
                continue
        else:
            hint('Linking', file)
        symlink(file)

def transfer_to(directory, file, ignore_existing = False):
    new_path = directory + file
    if exists(new_path):
        if ignore_existing:
            return
        if ask(new_path + " exists. Overwrite remote file?") in ('y', 'yes'):
            delete(new_path)
        else:
            return
    hint('Transferring', file)
    move(file, new_path)
    symlink(new_path)

def transfer(filename = '', *, ignore_existing = False):
    path = ''
    with open(storage, 'r') as stored:
        path = stored.readline().strip('\n')
    if filename != '':
        transfer_to(path, file, ignore_existing)
    else:
        for file in listdir('.'):
            if file != storage:
                transfer_to(path, file, ignore_existing)

def delete_file_and_link(link):
    if islink(link):
        removed = remove_if_broken(link)
        if not removed:
            path = os.readlink(link)
            if ask('Delete ' + path + ' ?') in ('y', 'yes'):
                delete(path)
                os.remove(link)
            else:
                print("Nothing deleted. Quitting...")
                exit()
    else:
        printErrMsg('"%s" is not a symbol link.' % link)
        exit(-1)


if __name__ == '__main__':
    if len(argv) == 1:
        exit(usage)
    for i, a in enumerate(argv[1:]):
        if a in ('-h', '--help', 'help'):
            exit(usage)
        elif a == 'link':
            k = i + 2
            if len(argv) == k:
                printErrMsg('Expect a path after "%s"' % a)
                exit(-1)
            path = argv[k]
            check_if_exists(path)
            link_with(path)
            exit()
        elif a == 'update':
            update()
            exit()
        elif a == 'transfer':
            k = i + 2
            if len(argv) == k:
                transfer()
                exit()
            file = argv[k]
            check_if_exists(file)
            transfer(file)
            exit()
        elif a == 'sync':
            update()
            transfer(ignore_existing=True)
            exit()
        elif a == "delete":
            k = i + 2
            if len(argv) == k:
                printErrMsg('Expect a file name after "%s"' % a)
                exit(-1)
            link = argv[k]
            check_if_exists(link)
            delete_file_and_link(link)
            exit()
        else:
            printErrMsg('Unknown command: "%s"' % a)
            exit(-1)
