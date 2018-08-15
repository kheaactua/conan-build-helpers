#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile


class HelpersConan(ConanFile):
    name        = 'helpers'
    version     = '0.3'
    license     = 'MIT'
    description = 'Helper functions for conan'
    exports     = '*'
    url         = 'https://github.com/kheaactua/conan-build-helpers'
    build_policy = 'missing'

    def package(self):
        self.copy('*helpers.py')
        self.copy('source_cache.py')

    def package_info(self):
        self.env_info.PYTHONPATH.append(self.package_folder)

# vim: ts=4 sw=4 expandtab ffs=unix ft=python foldmethod=marker :
