import os
import bpy

from .. utils import user_path


class RfB_OT_FileViewStats(bpy.types.Operator):
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
