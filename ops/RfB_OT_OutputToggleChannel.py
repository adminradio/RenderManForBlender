
#
# Blender Imports
#
import bpy
from bpy.props import StringProperty


class RfB_OT_OutputToggleChannel(bpy.types.Operator):
    bl_idname = "rfb.output_toggle_channel"
    bl_label = "Add or remove channel from output"
    info_string = StringProperty()

    def execute(self, context):
        self.report({'INFO'}, self.info_string)
        return {'FINISHED'}
