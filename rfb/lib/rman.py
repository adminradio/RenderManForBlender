#!/usr/bin/env python3

# ##### BEGIN MIT LICENSE BLOCK #####
#
# Copyright (c) 2015 - 2018 Pixar
# Refactoring Copyright (c) 2018 Timm Wimmers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
# ##### END MIT LICENSE BLOCK #####

# <pep8-80 compliant>

#
# Python Imports
#
import os
import platform
from pathlib import Path

#
# Blender Imports
#

#
# RenderManForBlender Imports
#
from . deco import laptime


@laptime
def available():
    root = ""
    locs = {}  # forward declare return value 1
    cmds = {}  # forward declare return value 2

    ext = ".exe" if platform.system() == "Windows" else ""
    prg = ["it", "sho", "prman", "txmake", "denoise", "oslinfo", "LocalQueue"]

    if platform.system() == "Windows":
        root = Path(os.environ["PROGRAMFILES"])
        root = root / "Pixar"

    elif platform.system() == "Darwin":
        root = Path("/Applications/Pixar")

    elif platform.system() == "Linux":
        root = Path("/opt/pixar")

    if root.exists():
        for entry in root.iterdir():
            if entry.is_dir():
                d = str(entry)
                if "RenderManProServer" in d:
                    vstr = d.split('-')[1]
                    locs[vstr] = d
    else:
        msg = ("RenderManForBlender - No valid installation found under \"{}\", "
               "please correct your RMANTREE environment.".format(root))
        raise FileNotFoundError(msg)

    for item in prg:
        #
        # for conistency make all keys lower case
        #
        cmds[item.lower()] = "{}{}".format(item, ext)

    return locs, cmds


@laptime
def select(ident='RMANTREE'):
    path = None
    version = None
    #
    # get all installed from default installation directory
    #
    _locs, _cmds = available()

    #
    # default (or explicitly requested)
    #
    if ident == 'RMANTREE':
        try:
            _d_ = Path(os.environ['RMANTREE'])
            if _d_.exists():
                path = _d_
        except KeyError:
            ident = 'NEWEST'
    #
    # A specific version or 'NEWEST' was requested.
    #
    if not path:
        try:
            #
            # Falls back to 'NEWEST' if not found, or since 'NEWEST' was
            # requested anyway
            #
            path = _locs[ident]
        except KeyError:
            try:
                path = _locs[
                    sorted(_locs.keys())[-1]
                ]
            except IndexError:
                msg = ("RenderManForBlender - No valid installation found, "
                       "please correct your RMANTREE environment.")
                raise IndexError(msg)
    #
    # Validation
    #
    abs_cmds = {}
    for item in _cmds.items():
        _p_ = Path("{}/bin/{}".format(path, item[1]))
        if _p_.exists():
            abs_cmds[item[0]] = _p_
        else:
            msg = ("RenderManForBlender - Utility could not be found: \"{}\". "
                   "Since selected RMANTREE looks valid, try reinstalling "
                   "RenderMan with an official installer.".format(_p_))
            raise FileNotFoundError(msg)

    version = str(path).split('-')[-1]
    return version, abs_cmds