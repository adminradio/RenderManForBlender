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
from . exceptions import RegistryKeyNotFound
from . exceptions import RegistryKeyAlreadyUsed

from .. import utils
from .. utils import stdmsg
from .. utils import stdadd
from .. utils import slugify


class Registry():

    _env = OrderedDict()

    # _env['DEV_TEST'] = 'foo/bar'
    _env['OS'] = platform.system()
    _env['RFB_PREFS'] = __package__.split(".")[0]
    _env['BLENDER_ROOT'] = str(Path(__file__).resolve().parents[4])
    _env['RFB_ROOT'] = str(Path(__file__).resolve().parents[1])
    _env['RFB_DATA'] = str(Path(_env['RFB_ROOT'], 'data'))
    _env['RFB_ARGS'] = str(Path(_env['RFB_DATA'], 'args'))
    _env['RFB_ROAMING'] = str(Path(_env['BLENDER_ROOT'], 'datafiles'))
    _env['RFB_TABNAME'] = "RenderMan"
    _env['BL_CATEGORY'] = "RenderMan"
    #
    # TODO:   Socket colors should be go into user prefs, and have more
    #         specific names.
    # DATE:   2018-01-14
    # AUTHOR: Timm Wimmers
    # STATUS: -unassigned-
    #
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
    #         - include version numbers of tools (prman, txmake)
    # DATE:   2018-01-14
    # AUTHOR: Timm Wimmers
    # STATUS: -unassigned-
    #
    # _env['RMANTREE']   = "TODO"
    # _env['BL_MAJOR']   = "TODO"  # Blender version major
    # _env['BL_MINOR']   = "TODO"  # Blender version minor
    # _env['BL_REVIS']   = "TODO"  # Blender revision (is it really needed?)
    # _env['IT_PATH']    = "TODO"  # IT
    # _env['IT_MAJOR']   = "TODO"  # IT
    # _env['IT_MINOR']   = "TODO"  # IT
    # _env['PRM_PATH']   = "TODO"  # PRMAN
    # _env['PRM_MAJOR']  = "TODO"  # PRMAN
    # _env['PRM_MINOR']  = "TODO"  # PRMAN
    # _env['TX_PATH']    = "TODO"  # TXMAKE
    # _env['TX_MAJOR']   = "TODO"  # TXMAKE
    # _env['TX_MINOR']   = "TODO"  # TXMAKE
    # _env['TC_PATH']    = "TODO"  # Tractor
    # _env['TC_MAJOR']   = "TODO"  # Tractor
    # _env['TC_MINOR']   = "TODO"  # Tractor
    # _env['LQ_PATH']    = "TODO"  # Local Queue
    # _env['LQ_MAJOR']   = "TODO"  # Local Queue
    # _env['LQ_MINOR']   = "TODO"  # Local Queue
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
            raise RegistryKeyAlreadyUsed(
                #
                # FIXME: only string values have to be in quotes.
                #
                "Use <set('{}', '{}')> to set this key explicitly (and you "
                "know what's going on). Nothing changed - current operation"
                "canced".format(key, value))
        else:
            cls._env[key] = value
            stdmsg("Key '{}' added as '{}' in registry with "
                   "value '{}'.".format(ident, key, value))

    @classmethod
    def get(cls, ident):
        key = ident.upper()
        try:
            return cls._env[key]
            #
            # TODO:   Check if its useful to return none
            # DATE:   2018-01-15
            # AUTHOR: Timm Wimmers
            # STATUS: -unassigned-
            #
        except KeyError:
            raise RegistryKeyNotFound(
                "Use <add('{}', value)> first to add one explicitly. Nothing "
                "changed - current operation canceled.".format(key))

    @classmethod
    def set(cls, ident, value):
        key = ident.upper()
        if key in cls._env.keys():
            cls._env[key] = value
        else:
            raise RegistryKeyNotFound(
                "Use <add('{}', value)> first to add one explicitly. Nothing "
                "changed - current operation canceled.".format(key))

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
