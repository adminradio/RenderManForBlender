
#
# Blender Imports
#
import bpy
from bpy.props import StringProperty


class RfB_OT_ToggleChannelOutput(bpy.types.Operator):
    bl_idname = "rfb.toggle_channel_output"
    bl_label = "Add or remove channel from output"
    info_string = StringProperty()

    def execute(self, context):
        self.report({'INFO'}, self.info_string)
        return {'FINISHED'}
