# -*- coding: latin-1 -*-

import re, platform

def adjustPath(path):
    """
    If on windows, convert unix paths to Windows.  Note, this function is quite
    simple and does not yet escape spaces or other special characters (just
    slashes right now.)  The purpose of this is to be able to send paths to
    CMake and pkg-config.
    """

    if 'Windows' == platform.system:
        return re.sub(r'\\', r'/', path)
    else:
        return path

def joinPaths(paths):
    """
    Join paths with a ':' on *nix systems, or a ';' on Windows systems
    """

    return (';' if 'Windows' == platform.system else ':').join(paths)


# vim: ts=4 sw=4 expandtab ffs=unix ft=python fileencoding=latin1 foldmethod=marker :
