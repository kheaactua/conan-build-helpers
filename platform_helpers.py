import os, re, platform

# TODO rename this function to toUnixPath, or see if I can replace this with https://github.com/conan-io/conan/blob/1afadb5cca9e1c688c7b37c69a0ff3c6a6dbe257/conans/client/build/compiler_flags.py
def adjustPath(path):
    """
    If on windows, convert unix paths to Windows.  Note, this function is quite
    simple and does not yet escape spaces or other special characters (just
    slashes right now.)  The purpose of this is to be able to send paths to
    CMake and pkg-config.
    """

    newpath = path
    if 'Windows' == platform.system():
        newpath = re.sub(r'\\', r'/', path)

    return newpath

def joinPaths(paths):
    """
    Join paths with a ':' on *nix systems, or a ';' on Windows systems

    # TODO This function can likely be deleted.
    """

    if isinstance(paths, list):
        return (';' if 'Windows' == platform.system() else ':').join(paths)
    else:
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

    # Convert our paaths to a list
    if isinstance(paths, str):
        paths = splitPaths(paths)

    # Make sure we keep the default path
    if 'PKG_CONFIG_PATH' in os.environ:
        paths += splitPaths(os.environ['PKG_CONFIG_PATH'])

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


def check_hash(file_path, hash_file, fnc=None):
    """
    Some vendors provide a file full of hashes, this function takes that as
    an input and performs the check.

    @param file_path File to confirm the hash
    @param hash_file File with a list (columns: hash, filename) of hashes
    @param algorithm_function For md5, use tools.check_md5, etc.
    """

    with open(hash_file, 'r') as f: contents = f.read()

    fname = os.path.basename(file_path)
    hash_str = ''
    m = re.search(r'(?P<hash>\w+)\s+(?P<archive>%s)'%fname, contents)
    if m:
        hash_str = m.group('hash')
    else:
        raise ValueError('Could not find a hash for %s in %s'%(fname, hash_file))

    return fnc(file_path=file_path, signature=hash_str)

def which(program):
    """
    Locate a command.

    Originally found in conan-qt script, and also at https://stackoverflow.com/a/377028/1861346
    """
    def is_exe(fpath):
        """
        Check if a path is executable.
        """
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

# vim: ts=4 sw=4 expandtab ffs=unix ft=python foldmethod=marker :
