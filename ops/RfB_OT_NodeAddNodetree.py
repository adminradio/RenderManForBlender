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
from bpy.props import StringProperty

#
# RenderMan for Blender Imports
#
from .. nodes import convert_cycles_nodetree
from .. nodes import is_renderman_nodetree


class RfB_OT_NodeAddNodetree(bpy.types.Operator):
    bl_idname = "rfb.node_add_nodetree"
    bl_label = "Add RenderMan Nodetree"
    bl_description = "Add a RenderMan shader node tree linked to this material"

    idtype = StringProperty(name="ID Type", default="material")
    bxdf_name = StringProperty(name="Bxdf Name", default="PxrSurface")

    def execute(self, context):
        idtype = self.properties.idtype
        if idtype == 'node_editor':
            idblock = context.space_data.id
            idtype = 'material'
        else:
            context_data = {'material': context.material,
                            'lamp': context.lamp, 'world': context.scene.world}
            idblock = context_data[idtype]
        # nt = bpy.data.node_groups.new(idblock.name,
        #                              type='RendermanPatternGraph')
        # nt.use_fake_user = True
        idblock.use_nodes = True
        nt = idblock.node_tree

        if idtype == 'material':
            output = nt.nodes.new('RendermanOutputNode')
            if not convert_cycles_nodetree(idblock, output, self.report):
                default = nt.nodes.new('%sBxdfNode' %
                                       self.properties.bxdf_name)
                default.location = output.location
                default.location[0] -= 300
                nt.links.new(default.outputs[0], output.inputs[0])
        elif idtype == 'lamp':
            light_type = idblock.type
            if light_type == 'SUN':
                context.lamp.renderman.renderman_type = 'DIST'
            elif light_type == 'HEMI':

                context.lamp.renderman.renderman_type = 'ENV'
            else:
                context.lamp.renderman.renderman_type = light_type

            if light_type == 'AREA':
                context.lamp.shape = 'RECTANGLE'
                context.lamp.size = 1.0
                context.lamp.size_y = 1.0

            idblock.renderman.use_renderman_node = True

        else:
            idblock.renderman.renderman_type = "ENV"
            idblock.renderman.use_renderman_node = True
            # light_type = idblock.type
            # light_shader = 'PxrStdAreaLightLightNode'
            # if light_type == 'SUN':
            #     context.lamp.renderman.type=
            #     light_shader = 'PxrStdEnvDayLightLightNode'
            # elif light_type == 'HEMI':
            #     light_shader = 'PxrStdEnvMapLightLightNode'
            # elif light_type == 'AREA' or light_type == 'POINT':
            #     idblock.type = "AREA"
            #     context.lamp.size = 1.0
            #     context.lamp.size_y = 1.0

            # else:
            #     idblock.type = "AREA"

            # output = nt.nodes.new('RendermanOutputNode')
            # default = nt.nodes.new(light_shader)
            # default.location = output.location
            # default.location[0] -= 300
            # nt.links.new(default.outputs[0], output.inputs[1])

        return {'FINISHED'}
