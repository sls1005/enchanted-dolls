# Enchanted Dolls

A helper for making and maintaining symbol links.

### Requirements

+ Python (version 3+ is recommended, while 2.7 is also supported.)

+ OS: Unix-like systems, or Windows (Unfortunately, Windows with Python 2 is not supported.)

### Usage

After adding `dolls.py` to your `PATH`, use the following command to link with a directory (`path/to/mydir` in this example.)
```sh
dolls.py link /path/to/mydir
```
This will create a symbol link to each file under `path/to/mydir` and put the links into a new directory. (On Windows, you might have to use `python /path/to/dolls.py` to launch this script.)

If a new file or subdirectory is added in either directory, use the following command in the directory with symbol links (generated by `dolls`) to synchronize.
```sh
dolls.py sync
```
This moves all non-symlink files into the pre-set target directory, then creates a symbol link to each new file in the target.

For linking new files without moving any, use:
```sh
dolls.py update
```

Use the following command to see the files linked.
```sh
dolls.py list
```

### Why needed?

Soon after I started using [Termux](https://github.com/termux/termux-app), I 
realized that it's impossible to run a binary executable within the interal shared storage, due to the restriction of the permission system of Android. Therefore, a directory for developing must be in the own storage of Termux, however if it is, its files wouldn't be accessible from other apps.

So I made this to mirror the whole directory. The resulted directory is not in the shared storage, so it's not subject to the restriction.

In theory, this can also be used as a workaround, in a system where some form of binary executables are not allowed to exist in particular directories.

### Note

+ This program creates a file named `.enchanted_doll_target` (which is usually invisible in a file manager) in the generated directory, for storing data. Please do not edit or create any file of the name. It is (the only file) not moved into the target directory when synchronizing.

+ This is tested on Android with Termux. Other platforms are (currently) not tested for.
