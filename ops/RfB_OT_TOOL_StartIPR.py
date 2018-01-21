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
# Blender imports
#
import bpy
import bgl
import blf

#
# RenderMan for Bender Imports
#
from .. import rfb
from .. import engine


class RfB_OT_TOOL_StartIPR(bpy.types.Operator):
    bl_idname = "rfb.tool_ipr"
    bl_label = "Start/Stop Interactive Rendering"
    bl_description = "Start/Stop Interactive Rendering, must have 'it' installed"
    rpass = None
    is_running = False

    def draw(self, context):
        w = context.region.width
        h = context.region.height

        #
        # Draw text area that RenderMan is running.
        #
        #
        #
        # TODO:   Implement GL drawing of viewport frame like Boxcutter,
        #         HardOPS & Co.
        # DATE:   2018-01-17
        # AUTHOR: Timm Wimmers
        # STATUS: -unassigned-
        #
        pos_x = w / 2 - 100
        pos_y = 20
        blf.enable(0, blf.SHADOW)
        blf.shadow_offset(0, 1, -1)
        blf.shadow(0, 5, 0.0, 0.0, 0.0, 0.8)
        blf.size(0, 32, 36)
        blf.position(0, pos_x, pos_y, 0)
        bgl.glColor4f(1.0, 0.0, 0.0, 1.0)
        blf.draw(0, "%s" % ('RenderMan Interactive Mode Running'))
        blf.disable(0, blf.SHADOW)

    def invoke(self, context, event=None):

        # IPR is running
        if not engine.ipr:  # is None:
            engine.ipr = engine.RPass(context.scene, interactive=True)

            engine.ipr.start_interactive()

            if rfb.reg.prefs().draw_ipr_text:
                engine.ipr_handle = (
                    bpy.types.SpaceView3D.draw_handler_add(
                        self.draw, (context,), 'WINDOW', 'POST_PIXEL'
                    )
                )

            bpy.app.handlers.scene_update_post.append(
                engine.ipr.issue_transform_edits
            )

            bpy.app.handlers.load_pre.append(
                self.invoke
            )

        # IPR isn't running
        else:

            bpy.app.handlers.scene_update_post.remove(
                engine.ipr.issue_transform_edits
            )
            #
            # The user should not turn this on and off during IPR rendering.
            #
            # TODO:   Then we should disabel this property in prefs if IPR
            #         is running.
            # DATE:   2018-01-17
            # AUTHOR: Timm Wimmers
            # STATUS: -unassigned-
            #
            if rfb.reg.prefs().draw_ipr_text:
                bpy.types.SpaceView3D.draw_handler_remove(
                    engine.ipr_handle, 'WINDOW'
                )

            engine.ipr.end_interactive()

            engine.ipr = None

            if context:
                for area in context.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()

        return {'FINISHED'}
