
#
# Blender Imports
#
import bpy

#
# RenderMan for Blender Imports
#
from .. nodes import convert_cycles_nodetree
from .. nodes import is_renderman_nodetree


class RfB_OT_NodeCyclesConvertall(bpy.types.Operator):
    bl_idname = "rfb.node_cycles_convertall"
    bl_label = "Convert All Cycles to RenderMan"
    bl_description = "Convert all nodetrees to RenderMan"

    def execute(self, context):
        for mat in bpy.data.materials:
            mat.use_nodes = True
            nt = mat.node_tree
            if is_renderman_nodetree(mat):
                continue
            output = nt.nodes.new('RendermanOutputNode')
            try:
                if not convert_cycles_nodetree(mat, output, self.report):
                    default = nt.nodes.new('PxrSurfaceBxdfNode')
                    default.location = output.location
                    default.location[0] -= 300
                    nt.links.new(default.outputs[0], output.inputs[0])
            except Exception as e:
                self.report({'ERROR'}, "Error converting " + mat.name)
                # self.report({'ERROR'}, str(e))
                # uncomment to debug conversion
                import traceback
                traceback.print_exc()

        for lamp in bpy.data.lamps:
            if lamp.renderman.use_renderman_node:
                continue
            light_type = lamp.type
            lamp.renderman.light_primary_visibility = False
            if light_type == 'SUN':
                lamp.renderman.renderman_type = 'DIST'
            elif light_type == 'HEMI':
                lamp.renderman.renderman_type = 'ENV'
                lamp.renderman.light_primary_visibility = True
            else:
                lamp.renderman.renderman_type = light_type

            if light_type == 'AREA':
                lamp.shape = 'RECTANGLE'
                lamp.size = 1.0
                lamp.size_y = 1.0

            # lamp.renderman.primary_visibility = not lamp.use_nodes

            lamp.renderman.use_renderman_node = True

        # convert cycles vis settings
        for ob in context.scene.objects:
            if not ob.cycles_visibility.camera:
                ob.renderman.visibility_camera = False
            if not ob.cycles_visibility.diffuse or not ob.cycles_visibility.glossy:
                ob.renderman.visibility_trace_indirect = False
            if not ob.cycles_visibility.transmission:
                ob.renderman.visibility_trace_transmission = False
        return {'FINISHED'}
