# ##### BEGIN MIT LICENSE BLOCK #####
#
# Copyright (c) 2015 - 2017 Pixar
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
# Blender Imports
#
import bpy

from bpy.props import BoolProperty
from bpy.props import PointerProperty
from bpy.props import CollectionProperty
from bpy.props import FloatVectorProperty

#
# RenderMan for Blender Imports
#
from .. import engine
from .. export import write_archive_RIB


class RfB_OT_ObjectExportRIB(bpy.types.Operator):
    bl_idname = "rfb.object_export_rib"
    bl_label = "Export Object as RIB Archive."
    bl_description = "Export single object as a RIB archive for use in other blend files or for other uses"

    export_mat = BoolProperty(
        name="Export Material",
        description="Do you want to export the material?",
        default=True)

    export_all_frames = BoolProperty(
        name="Export All Frames",
        description="Export entire animation time frame",
        default=False)

    filepath = bpy.props.StringProperty(
        subtype="FILE_PATH")

    filename = bpy.props.StringProperty(
        subtype="FILE_NAME",
        default="")

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        export_path = self.filepath
        export_range = self.export_all_frames
        export_mats = self.export_mat
        rpass = engine.RPass(context.scene, interactive=False)
        object = context.active_object

        # rpass.convert_textures(get_texture_list(context.scene))
        rpass.ri.Option("rib", {"string asciistyle": "indented,wide"})

        # export_filename = write_single_RIB(rpass, context.scene, rpass.ri, object)
        export_sucess = write_archive_RIB(
            rpass, context.scene,
            rpass.ri, object, export_path,
            export_mats, export_range
        )

        ##
        if export_sucess[0]:
            self.report({'INFO'}, "Archive Exported Successfully!")
            object.renderman.geometry_source = 'ARCHIVE'
            object.renderman.path_archive = export_sucess[1]
            object.renderman.object_name = object.name
            if(export_mats):
                object.renderman.material_in_archive = True
            else:
                object.renderman.material_in_archive = False
            object.show_bounds = True
            ####
            if export_range:
                object.renderman.archive_anim_settings.animated_sequence = True
                object.renderman.archive_anim_settings.sequence_in = context.scene.frame_start
                object.renderman.archive_anim_settings.sequence_out = context.scene.frame_end
                object.renderman.archive_anim_settings.blender_start = context.scene.frame_current
            else:
                object.renderman.archive_anim_settings.animated_sequence = False
        else:
            self.report({'ERROR'}, "Archive Not Exported.")
        return {'FINISHED'}

    def invoke(self, context, event=None):

        context.window_manager.fileselect_add(self)
        return{'RUNNING_MODAL'}
