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

    if isinstance(paths, list):
        return (';' if 'Windows' == platform.system() else ':').join(paths)
    else
        return paths

def splitPaths(paths):
    """
    Splits paths with a ':' on *nix systems, or a ';' on Windows systems
    """

    return paths.split(';' if 'Windows' == platform.system() else ':')

def appendPkgConfigPath(paths, env_obj):
    """
    Append to the a conan's virtual environments pkg config path by taking the
    current environment's pkg-config path into consideration

    The result is that paths will be prepended to the current pkg-config path.

    @param paths Either a string of paths or list of paths
    @param env_obj Either a conan.models.EnvInfo (usually used when called from
                   pkg_config), or a dict (usually when called from build)
    """

    # Make sure we keep the default path
    if 'PKG_CONFIG_PATH' in os.environ:
        if isinstance(paths, list):
            paths += splitPaths(os.environ['PKG_CONFIG_PATH'])
        else:
            paths = splitPaths(paths) + splitPaths(os.environ['PKG_CONFIG_PATH'])

    # Remove duplicates
    paths = remove_duplicates_keep_order(paths)

    if isinstance(env_obj, dict):
        env_obj['PKG_CONFIG_PATH'] = paths
    elif re.search('conans.model.env_info.EnvInfo', str(type(env_obj))):
        # Terrible way to detect type, but I can't import conans here, so I
        # can't check isinstance
        env_obj.PKG_CONFIG_PATH = paths
    else:
        raise ValueError('Unsure of how to use provided environment object, type=%s'%str(type(env_obj)))


def remove_duplicates_keep_order(seq):
    """ Source: https://stackoverflow.com/a/480227/1861346 """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

# vim: ts=4 sw=4 expandtab ffs=unix ft=python fileencoding=latin1 foldmethod=marker :
