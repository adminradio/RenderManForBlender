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

#
# Blender imports
#
import bpy

#
# RfB imports
#
from .. utils import user_path


class RfB_OT_FILE_ViewStats(bpy.types.Operator):
    bl_idname = 'rfb.file_view_stats'
    bl_label = "View Frame Statistics"
    bl_description = "View current frame statistics in Browser (extern)."

    def execute(self, context):
        scene = context.scene
        rm = scene.renderman

        out_path = os.path.dirname(
            user_path(rm.path_rib_output, scene=scene)
        )

        # Create something similiar to:
        # file://stats/path/stats.NNNN.xml
        #
        uri = os.path.join(
            "file://",
            out_path,
            "stats.%04d.xml" % scene.frame_current
        )

        bpy.ops.wm.url_open(url=uri)
        return {'FINISHED'}
