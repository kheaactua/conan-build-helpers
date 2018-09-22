#!/usr/bin/env python

import platform

def merge_two_dicts_with_paths(x, y):
    z = x.copy()   # start with x's keys and values
    for k,v in y.items():
        if k not in z:
            # Copy key if it doesn't exist
            z[k] = v
        else:
            # Attempt to merge
            if 'PATH' in k:
                if (type(x[k]) is not str and type(x[k]) is not list) or (type(y[k]) is not str and type(y[k]) is not list):
                    raise ValueError('PATH variables must either be a list or stirng')

                # Special case
                if type(x[k]) is str:
                    paths_x = x[k].split(';' if 'Windows' == platform.system() else ':')
                else:
                    paths_x = x[k]

                if type(y[k]) is str:
                    paths_y = y[k].split(';' if 'Windows' == platform.system() else ':')
                else:
                    paths_y = y[k]

                paths_z = paths_x + paths_y
                if type(x[k]) is str:
                    z[k] = (';' if 'Windows' == platform.system() else ':').join(paths_z)
                else:
                    z[k] = paths_z

            elif type(x[k]) is not type(y[k]):
                raise ValueError('Can only implement mixed types for PATH variables, error with %s'%k)

            elif type(v) is list:
                z[k].extend(v)

            elif type(v) is dict:
                z[k] = merge_two_dicts_with_paths(x[k], y[k])

            elif type(v) is str:
                raise ValueError('Unsure how to merge string values for %s'%(k))

            else:
                raise ValueError('Unsure how to merge type %s for %s'%(type(v), k))

    return z

# vim: ts=4 sw=4 expandtab ffs=unix ft=python foldmethod=marker :
