# ##### BEGIN MIT LICENSE BLOCK #####
#
# Copyright (c) 2015 - 2018 Pixar
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


#
# Python imports
#
import os
import platform
from pathlib import Path
from collections import OrderedDict

#
# Blender imports
#
import bpy


#
# RenderMan for Blender imports
#
# from . import exceptions
from . exceptions import RegistryKeyNotFound
from . exceptions import RegistryKeyAlreadyUsed

from .. utils import stdmsg
from .. utils import stdadd
from .. utils import slugify


class Registry():

    _env = OrderedDict()
    _env['OS'] = platform.system()
    _env['RFB_PREFS'] = __package__.split(".")[0]
    _env['BLENDER_ROOT'] = str(Path(__file__).resolve().parents[4])
    _env['RFB_ROOT'] = str(Path(__file__).resolve().parents[1])
    _env['RFB_DATA'] = str(Path(_env['RFB_ROOT'], 'data'))
    _env['RFB_ARGS'] = str(Path(_env['RFB_DATA'], 'args'))
    _env['RFB_ROAMING'] = str(Path(_env['BLENDER_ROOT'], 'datafiles'))

    #
    # TODO:   Implement the (commented) items afterwards.
    #         - have to be fully validated
    #         - include version numbers of tools (prman, txmake)
    # DATE:   2018-01-14
    # AUTHOR: Timm Wimmers
    # STATUS: -unassigned-
    #
    # _env['BL_MAJOR']  = "TODO"  # Blender version major
    # _env['BL_MINOR']  = "TODO"  # Blender version minor
    # _env['BL_REVIS']  = "TODO"  # Blender revision (is it really needed?)
    # _env['IT_PATH']   = "TODO"  # IT
    # _env['RM_PATH']   = "TODO"  # PRMAN
    # _env['RM_MAJOR']  = "TODO"  # PRMAN
    # _env['RM_MINOR']  = "TODO"  # PRMAN
    # _env['TM_PATH']   = "TODO"  # TSMAKE
    # _env['RIBEDIT']   = "TODO"  # should be go into user prefs
    # _env['XMLVIEW']   = "TODO"  # should be go into user prefs
    # _env['OSLEDIT']   = "TODO"  # should be go into user prefs
    # _env['WEBVIEW']   = "TODO"  # should be go into user prefs
    # _env['RMANTREE']  = "TODO"

    @classmethod
    def prefs(cls):
        addon = bpy.context.user_preferences.addons[cls._env['RFB_PREFS']]
        return addon.preferences
        # return rt.reg.get('RFB_PREFS')

    @classmethod
    def list(cls):
        return cls._env.items()

    @classmethod
    def add(cls, ident, value):
        key = ident.upper()
        if key in cls._env.keys():
            raise RegistryKeyAlreadyUsed(
                "All keys (including '{}') are write protected.".format(key))
        else:
            cls._env[key] = value
            stdmsg(
                "Added '{}' as '{}' to runtime registry.".format(ident, key))

    @classmethod
    def get(cls, ident):
        # return cls._env[ident.upper()]
        try:
            return cls._env[ident.upper()]
        except KeyError:
            #
            # TODO:   Check if its useful to return none
            # DATE:   2018-01-15
            # AUTHOR: Timm Wimmers
            # STATUS: -unassigned-
            #
            raise RegistryKeyNotFound

    @classmethod
    def display(cls, title="Current registry values:"):
        stdmsg(title)
        stdadd("")
        for k, v in cls.list():
            display_k = k.ljust(14)
            display_v = slugify(v)
            stdadd("{}= {}".format(display_k, display_v))
        stdadd("")
        stdadd("Registry initialised, looks good so far.")
