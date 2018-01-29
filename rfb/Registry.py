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
# import os
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
from . err import KeyNotFoundError
from . err import KeyOverrideError


class Registry():

    _env = OrderedDict()

    _env['OS'] = platform.system()
    _env['RFB_PREFS'] = __package__.split(".")[0]
    _env['BLENDER_ROOT'] = str(Path(__file__).resolve().parents[5])
    _env['RFB_ROOT'] = str(Path(__file__).resolve().parents[1])
    _env['RFB_DATA'] = str(Path(_env['RFB_ROOT'], 'data'))
    _env['RFB_ARGS'] = str(Path(_env['RFB_DATA'], 'args'))
    _env['RFB_DEBUG'] = True
    _env['RFB_INFOS'] = True
    _env['RFB_ROAMING'] = str(Path(_env['BLENDER_ROOT'], 'datafiles'))
    _env['RFB_TABNAME'] = "RenderMan"
    _env['BL_CATEGORY'] = "RenderMan"
    _env['RFB_TIME_IT'] = True
    _env['BXDF'] = (0.25, 1.00, 0.25, 1.00)
    _env['FLOAT'] = (0.50, 0.50, 0.50, 1.00)
    _env['VECTOR'] = (0.00, 0.00, 0.50, 1.00)
    _env['RGB'] = (1.00, 0.50, 0.00, 1.00)
    _env['EULER'] = (0.00, 0.50, 0.50, 1.00)
    _env['STRUCT'] = (1.00, 1.00, 0.00, 1.00)
    _env['STRING'] = (0.00, 0.00, 1.00, 1.00)
    _env['INT'] = (1.00, 1.00, 1.00, 1.00)
    #
    # TODO:   Implement the (commented) items afterwards.
    #         - have to be fully validated at startup
    # DATE:   2018-01-14
    # AUTHOR: Timm Wimmers
    # STATUS: -unassigned-
    #
    # _env['BL_MAJOR']   = "TODO"  # Blender version major
    # _env['BL_MINOR']   = "TODO"  # Blender version minor
    # _env['RIBEDIT']    = "TODO"  # should be go into user prefs
    # _env['XMLVIEW']    = "TODO"  # should be go into user prefs
    # _env['OSLEDIT']    = "TODO"  # should be go into user prefs
    # _env['WEBVIEW']    = "TODO"  # should be go into user prefs

    @classmethod
    def prefs(cls):
        addon = bpy.context.user_preferences.addons[cls._env['RFB_PREFS']]
        return addon.preferences

    @classmethod
    def list(cls):
        return cls._env.items()

    @classmethod
    def add(cls, ident, value):
        key = ident.upper()
        if key in cls._env.keys():
            q = "'" if type(value) == str else ""  # noqa
            raise KeyOverrideError(
                "Use <set('{}', {}{}{})> to set this key explicitly (and you "
                "know what's going on). Nothing changed - current operation"
                "canceled.".format(key, q, value, q)
            )

    @classmethod
    def get(cls, ident):
        key = ident.upper()
        try:
            return cls._env[key]
        except KeyError:
            return None

    @classmethod
    def set(cls, ident, value):
        key = ident.upper()
        if key in cls._env.keys():
            cls._env[key] = value
        else:
            q = "'" if type(value) == str else ""
            raise KeyNotFoundError(
                "Use <add('{}', {}{}{})> to set this key explicitly (and you "
                "know what's going on). Nothing changed - current operation"
                "canceled.".format(key, q, value, q)
            )
