#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os, shutil

def copyFromCache(filename, dst=None, cache_dir = None, output_func=print):
    """ Copy a file from a directory """

    try:
        from urllib.parse import urlparse
    except:
        from urlparse import urlparse

    def is_url(url):
        return urlparse(url).scheme != ""


    if cache_dir is None:
        if 'CONAN_SOURCE_CACHE_DIR' in os.environ:
            cache_dir = os.environ.get('CONAN_SOURCE_CACHE_DIR')

    if cache_dir is None:
        output_func('Warning: No source cache directory set, please manually set or use the CONAN_SOURCE_CACHE_DIR environment variable')
        if os.path.basename(filename) == filename and not os.path.exists(filename):
            # No chance of finding this without CONAN_SOURCE_CACHE_DIR
            return False

    if dst is None:
        dst = filename

    if is_url(cache_dir):
        path = ''
        if cache_dir:
            path = str(cache_dir) + '/'
        path += filename

        from conans import tools
        from conans.errors import ConanException

        try:
            tools.download(path, dst)
        except ConanException as e:
            output_func('Error: Could not download %s:\n%s'%(path, e))
            return False

        return True

    else:
        path = os.path.join(cache_dir, filename)
        if os.path.exists(path):
            shutil.copy(src=path, dst=dst)
            return True
        else:
            output_func('Warning: no file "%s" found in %s'%(filename, cache_dir))
            return False

# vim: ts=4 sw=4 expandtab ffs=unix ft=python foldmethod=marker :
