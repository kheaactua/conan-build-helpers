#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os, shutil

def wrapCMakeFile(source_folder, output_func=print, custom_cmakefile=None):
    """
    Given a source directory, this file wraps the parent CMakeLists.txt in
    another CMakeFile.  The purpose is to be able to append to certain values
    such as CMAKE_CXX_FLAGS that otherwise cannot be easily appended

    @param source_folder Folder containing the parent CMakeLists.txt file
    @param output_func   Print function or user defined output function (say,
                         self.output.info if calling from a Conan object)
    @param custom_cmakefile Path to custom CMakeLists.txt file if one exists
                         (say conan exports one), without this, a default wrapper CMakeLists.txt
                         file is added.
    """

    orig_cmake_file    = os.path.join(source_folder, 'CMakeLists.txt')
    wrapped_cmake_file = os.path.join(source_folder, 'orig.CMakeLists.txt')

    if not os.path.exists(orig_cmake_file):
        raise ValueError('Cannot find CMakeLists.txt file: %s'%orig_cmake_file)

    if os.path.exists(wrapped_cmake_file):
        output_func('Top CMakeLists.txt file already wrapped, skipping')
        return

    shutil.move(src=orig_cmake_file, dst=wrapped_cmake_file)

    new_cmake_contents = '''
PROJECT(conan_cmake_wrapper)

cmake_minimum_required(VERSION 2.8)
if (NOT "${ADDITIONAL_CXX_FLAGS}" STREQUAL "")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${ADDITIONAL_CXX_FLAGS}")
    message(STATUS "Appending CMAKE_CXX_FLAGS: ${CMAKE_CXX_FLAGS}")
endif()

if (NOT "${ADDITIONAL_C_FLAGS}" STREQUAL "")
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${ADDITIONAL_C_FLAGS}")
    message(STATUS "Appending CMAKE_C_FLAGS: ${CMAKE_C_FLAGS}")
endif()

include("%s")
'''%(wrapped_cmake_file)

    output_func('Writting wrapper CMakeLists.txt file to %s which will include %s'%(orig_cmake_file, wrapped_cmake_file))
    with open(orig_cmake_file, 'w') as f: f.write(new_cmake_contents)

# vim: ts=4 sw=4 expandtab ffs=unix ft=python foldmethod=marker :
