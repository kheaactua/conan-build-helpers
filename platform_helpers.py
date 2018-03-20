# -*- coding: latin-1 -*-

import os, re, platform

def adjustPath(path):
    """
    If on windows, convert unix paths to Windows.  Note, this function is quite
    simple and does not yet escape spaces or other special characters (just
    slashes right now.)  The purpose of this is to be able to send paths to
    CMake and pkg-config.
    """

    if 'Windows' == platform.system():
        return re.sub(r'\\', r'/', path)
    else:
        return path

def joinPaths(paths):
    """
    Join paths with a ':' on *nix systems, or a ';' on Windows systems
    """

    return (';' if 'Windows' == platform.system() else ':').join(paths)

def splitPaths(paths):
    """
    Splits paths with a ':' on *nix systems, or a ';' on Windows systems
    """

    return paths.split(';' if 'Windows' == platform.system() else ':')

def appendPkgConfigPath(paths, conan_obj):
    """
    Append to the a conan's virtual environments pkg config path by taking the
    current environment's pkg-config path into consideration

    The result is that paths will be prepended to the current pkg-config path.
    """

    # Make sure we keep the default path
    if 'PKG_CONFIG_PATH' in os.environ:
        if isinstance(paths, list):
            paths += splitPaths(os.environ['PKG_CONFIG_PATH'])
        else:
            paths = splitPaths(paths) + splitPaths(os.environ['PKG_CONFIG_PATH'])

    conan_obj.env_info.PKG_CONFIG_PATH = paths

# vim: ts=4 sw=4 expandtab ffs=unix ft=python fileencoding=latin1 foldmethod=marker :
