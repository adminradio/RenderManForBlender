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
# Python Imports
#
import sys
import os
import platform
import subprocess

#
# Blender Imports
#
import bpy

#
# RenderMan for Blender Imports
#
from .. utils import stdmsg
from .. utils import stdadd
from .. utils import guess_rmantree
#
#
# TODO:   Refactor 'guess_rmantree' into RfB registry.
# DATE:   2018-01-17
# AUTHOR: Timm Wimmers
# STATUS: -unassigned-
#


class RfB_OT_TOOL_StartIT(bpy.types.Operator):
    bl_idname = 'rfb.tool_it'
    bl_label = "Start ═ Focus IT"
    bl_description = "Start RenderMan's Image Tool (IT)."

    @staticmethod
    def get_cmd():
        classname = os.path.splitext(os.path.basename(__file__))[0]
        stdmsg("{}.{}()".format(classname, sys._getframe().f_code.co_name))
        #
        # TODO: refactor guess_rmantree()
        #
        rmt = guess_rmantree()

        if rmt:
            binpath = os.path.join(rmt, 'bin')

            #
            # Windows
            #
            if platform.system() == 'Windows':
                cmd = os.path.join(
                    binpath, 'it.exe'
                )
            #
            # MacOS
            #
            elif platform.system() == 'Darwin':
                cmd = os.path.join(
                    binpath, 'it.app', 'Contents', 'MacOS', 'it'
                )
            #
            # Linux
            #
            elif platform.system() == 'Linux':
                cmd = os.path.join(
                    binpath, 'it'
                )
            if os.path.exists(cmd):
                return cmd
        return None

    def execute(cls, context):
        cmd = cls.get_cmd()
        if cmd:
            environ = os.environ.copy()
            subprocess.Popen([cmd], env=environ, shell=True)
        else:
            cls.report(
                {"ERROR"},
                "Could not find 'Image Tool'. Check console for Details."
            )
        slug = ("... (snip) ... {}".format(cmd[-40:])
                if len(cmd) > 60
                else cmd
                )
        stdadd(slug)
        return {'FINISHED'}
