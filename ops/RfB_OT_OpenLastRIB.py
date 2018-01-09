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
import os

#
# Blender Imports
#
import bpy
import webbrowser

#
# RenderMan for Blender Imports
#
from .. import engine


class RfB_OT_OpenLastRIB(bpy.types.Operator):
    bl_idname = 'rfb.open_last_rib'
    bl_label = "Open Last RIB Scene file."
    bl_description = "Opens the last generated Scene.rib file in the system default text editor"
    #
    # TODO:   Editor customization via Preferences.
    #         The system editor may not be the preferred editor for RIB files.
    #         Cutter comes in mind: http://fundza.com/index.html
    # DATE:   2018-01-09
    # AUTHOR: Timm Wimmers
    # STATUS: -unassigned-
    #

    def invoke(self, context, event=None):
        rm = context.scene.renderman
        rpass = engine.RPass(context.scene, interactive=False)
        path = rpass.paths['rib_output']
        if rm.editor_override:
            command = rm.editor_override + " " + path
            try:
                os.system(command)
            except Exception:
                self.report(
                    {'ERROR'},
                    "File or text editor not available."
                    "(Check and make sure text editor is in system path.)"
                )
        else:
            try:
                webbrowser.open(path)
            except Exception:
                self.report(
                    {'ERROR'},
                    "File <" + path + "> not found."
                )

        return {'FINISHED'}
