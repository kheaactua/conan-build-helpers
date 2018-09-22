#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from merge_dicts import *

class Test_merge_two_dicts(unittest.TestCase):
    def test_trivial(self):
        print("ran tests!!!\n\n\n\n")
        z = merge_two_dicts_with_paths({}, {})
        assert len(z.items()) == 0

    def test_concat(self):
        x = {'a': 1}
        y = {'b': 2}
        z = merge_two_dicts_with_paths(x, y)
        assert len(z.items()) == 2
        assert z['a'] == 1
        assert z['b'] == 2

    def test_no_clobber(self):
        x = {'a': 1}
        y = {'a': 2}
        with self.assertRaises(ValueError) as context:
            z = merge_two_dicts_with_paths(x, y)

    def test_no_merge_values(self):
        x = {'a': [1,2,3]}
        y = {'a': [4,5,6]}
        z = merge_two_dicts_with_paths(x, y)
        sorted(z)
        assert z['a'] == [1,2,3,4,5,6]

    def test_fail_on_different_types(self):
        x = {'a': 1}
        y = {'a': 'b'}
        with self.assertRaises(ValueError) as context:
            z = merge_two_dicts_with_paths(x, y)

    def test_no_merge_paths_list(self):
        x = {'PATH': ['a', 'b']}
        y = {'PATH': ['c', 'd']}
        z = merge_two_dicts_with_paths(x, y)
        sorted(z)
        assert z['PATH'] == ['a', 'b', 'c', 'd']

    def test_no_merge_paths_str(self):
        sep = ';' if 'Windows' == platform.system() else ':'
        x = {'PATH': 'a' + sep + 'b'}
        y = {'PATH': 'c' + sep + 'd'}
        z = merge_two_dicts_with_paths(x, y)
        assert z['PATH'] == 'a' + sep + 'b' + sep + 'c' + sep + 'd'

    def test_no_merge_paths_mixed(self):
        sep = ';' if 'Windows' == platform.system() else ':'
        x = {'PATH': 'a' + sep + 'b'}
        y = {'PATH': ['c', 'd']}
        z = merge_two_dicts_with_paths(x, y)
        assert z['PATH'] == 'a' + sep + 'b' + sep + 'c' + sep + 'd'

if __name__ == '__main__':
    unittest.main()

# vim: ts=4 sw=4 expandtab ffs=unix ft=python foldmethod=marker :
