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
# Blender Imports
#
import bpy
from bpy.props import EnumProperty

#
# RenderMan for Blender Imports
#
# from .. export import EXCLUDED_OBJECT_TYPES
# FIXME: has to be in export.py or in RfB-Registry?
EXCLUDED_OBJECT_TYPES = ['LAMP', 'CAMERA', 'ARMATURE']


class RfB_OT_MATERIAL_AddBXDF(bpy.types.Operator):
    bl_idname = "rfb.material_add_bxdf"
    bl_label = "Add BXDF"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def get_type_items(self, context):
        items = [
            ("PxrSurface",
                "PxrSurface",
                'PxrSurface Uber shader. For most hard surfaces'),
            ("PxrLayerSurface",
                "PxrLayerSurface",
                "PxrLayerSurface, creates a surface with two Layers"),
            ("PxrMarschnerHair",
                "PxrMarschnerHair",
                "Hair Shader"),
            ("PxrDisney",
                "PxrDisney",
                "Disney Bxdf, a simple uber shader with no layering"),
            ("PxrVolume",
                "PxrVolume",
                "Volume Shader")
        ]
        # for nodetype in RendermanPatternGraph.nodetypes.values():
        #    if nodetype.renderman_node_type == 'bxdf':
        #        items.append((nodetype.bl_label, nodetype.bl_label,
        #                      nodetype.bl_label))
        return items

    bxdf_name = EnumProperty(items=get_type_items, name="Bxdf Name")

    def execute(self, context):
        selection = bpy.context.selected_objects if hasattr(
            bpy.context, 'selected_objects') else []
        # selection = bpy.context.selected_objects
        bxdf_name = self.properties.bxdf_name
        mat = bpy.data.materials.new(bxdf_name)

        mat.use_nodes = True
        nt = mat.node_tree

        output = nt.nodes.new('RendermanOutputNode')
        default = nt.nodes.new('%sBxdfNode' % bxdf_name)
        default.location = output.location
        default.location[0] -= 300
        nt.links.new(default.outputs[0], output.inputs[0])

        if bxdf_name == 'PxrLayerSurface':
            mixer = nt.nodes.new("PxrLayerMixerPatternNode")
            layer1 = nt.nodes.new("PxrLayerPatternNode")
            layer2 = nt.nodes.new("PxrLayerPatternNode")

            mixer.location = default.location
            mixer.location[0] -= 300

            layer1.location = mixer.location
            layer1.location[0] -= 300
            layer1.location[1] += 300

            layer2.location = mixer.location
            layer2.location[0] -= 300
            layer2.location[1] -= 300

            nt.links.new(mixer.outputs[0], default.inputs[0])
            nt.links.new(layer1.outputs[0], mixer.inputs['baselayer'])
            nt.links.new(layer2.outputs[0], mixer.inputs['layer1'])

        for obj in selection:
            if(obj.type not in EXCLUDED_OBJECT_TYPES):
                bpy.ops.object.material_slot_add()

                obj.material_slots[-1].material = mat

        return {"FINISHED"}
