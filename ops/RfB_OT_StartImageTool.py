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

# python imports
import os
import platform
import subprocess

# blender imports
import bpy

# RfB imports
from .. utils import (
    stdout,
    stdadd
)
#
# TODO: refactor 'gues_rmantree'
#
from .. util import guess_rmantree


class RfB_OT_StartImageTool(bpy.types.Operator):
    bl_idname = 'renderman.start_image_tool'
    bl_label = "Start/Focus IT"
    bl_description = "Start RenderMan's Image Tool (IT)."

    @staticmethod
    def get_cli():
        stdout("OT_StartImageTool >> get_cli() static method call ...")
        #
        # TODO: refactor guess_rmantree()
        #
        rmtree = guess_rmantree()

        if rmtree:
            binpath = os.path.join(rmtree, 'bin')
            #
            # Windows
            #
            if platform.system() == 'Windows':
                cli = os.path.join(
                    binpath, 'it.exe'
                )
            #
            # MacOS
            #
            elif platform.system() == 'Darwin':
                cli = os.path.join(
                    binpath, 'it.app', 'Contents', 'MacOS', 'it'
                )
            #
            # Linux
            #
            elif platform.system() == 'Linux':
                cli = os.path.join(
                    binpath, 'it'
                )
            if os.path.exists(cli):
                return cli
        return None

    def execute(self, context):
        cli = self.get_cli()
        slug = ""
        if len(cli) > 32:
            slug = "(...) " + cli[-32:]
        stdadd("OT_StartImageTool >> get_cli() returned:  %s" % slug)

        if cli:
            environ = os.environ.copy()
            subprocess.Popen([cli], env=environ, shell=True)
        else:
            self.report(
                {"ERROR"},
                "Could not find 'Image Tool'. Check console for Details."
            )
            stdadd("OT_StartImageTool >> ERROR - Image Tool not found ...")
            stdadd("OT_StartImageTool >> ERROR - Check Installation of RenderMan Pro Server ...")
            stdadd("OT_StartImageTool >> ERROR - and restart Blender."
                   "Saving your work may be a good idea!")

        return {'FINISHED'}
