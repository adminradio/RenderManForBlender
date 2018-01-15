
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
