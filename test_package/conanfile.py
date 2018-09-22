#!/usr/bin/env python
# -*- coding: future_fstrings -*-
# -*- coding: utf-8 -*-

import os, re, sys, platform
import unittest
from io import StringIO
from conans import ConanFile, tools

class HelpersTestConan(ConanFile):
    requires = 'helpers/0.3@ntc/stable'

    def test(self):
        from test_package.test_merge_dicts import Test_merge_two_dicts
        suite = unittest.TestLoader().loadTestsFromModule(Test_merge_two_dicts)
        # Doesn't actually run the tests yet, not sure why not
        unittest.TextTestRunner(verbosity=0).run(suite)


# vim: ts=4 sw=4 expandtab ffs=unix ft=python foldmethod=marker :
