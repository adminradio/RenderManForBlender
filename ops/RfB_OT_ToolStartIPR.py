# python imports

# blender imports
import bpy
import bgl
import blf

# RfB imports
from .. import rt
from .. import engine


class RfB_OT_ToolStartIPR(bpy.types.Operator):
    bl_idname = "rfb.tool_ipr"
    bl_label = "Start/Stop Interactive Rendering"
    bl_description = "Start/Stop Interactive Rendering, must have 'it' installed"
    rpass = None
    is_running = False

    def draw(self, context):
        w = context.region.width
        h = context.region.height

        # Draw text area that RenderMan is running.
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
        if engine.ipr is None:
            engine.ipr = engine.RPass(context.scene, interactive=True)

            engine.ipr.start_interactive()

            if rt.reg.prefs().draw_ipr_text:
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
            # TODO: Then we should disable editing the preferences.
            if rt.reg.prefs().draw_ipr_text:
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
