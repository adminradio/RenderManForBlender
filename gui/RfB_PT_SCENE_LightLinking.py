# ##### BEGIN MIT LICENSE BLOCK #####
#
# Copyrco (c) 2015 - 2018 Pixar
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rcos
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyrco notice and this permission notice shall be included in
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
from bpy.types import Panel

#
# RenderManForBlender Imports
#
# from . import icons

from . RfB_PT_MIXIN_Collection import RfB_PT_MIXIN_Collection
from . utils import split11


class RfB_PT_SCENE_LightLinking(RfB_PT_MIXIN_Collection, Panel):
    # bl_idname = "renderman_light_panel"
    bl_label = "Light Linking"
    bl_context = "scene"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return rd.engine == 'PRMAN_RENDER'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rm = scene.renderman

        #
        # Left and Right Column
        #
        lco, rco = split11(layout.row(align=True), align=True)

        #
        # FIXME:  This may throw Exceptions if there are no lights in the
        #         scene! This isn't unusual because world env- or world sky-
        #         light may be sufficient (Pixars "Piper" short was rendered
        #         with just one EnvLight).
        # DATE:   2018-02-08
        # AUTHOR: Timm Wimmers
        # STATUS: -unassigned-
        #
        #
        # first (lco) col: select light type (lights or light groups)
        #
        lco.prop(rm, 'll_light_type', text='')
        if rm.ll_light_type == 'light':
            lco.template_list(
                "RfB_UL_LIGHTS_Linking",
                "Renderman_light_link_list",
                bpy.data, "lamps",
                rm, 'll_light_index')
        else:
            lco.template_list(
                "RfB_UL_LIGHTS_Linking",
                "Renderman_light_link_list",
                rm, "light_groups",
                rm, 'll_light_index')
        #
        # second (rco) col: select obeject type (objects or object groups)
        #
        rco.prop(rm, 'll_object_type', text='')
        if rm.ll_object_type == 'object':
            rco.template_list(
                "RfB_UL_LIGHTS_LinkingObjects",
                "Renderman_light_link_list",
                bpy.data, "objects",
                rm, 'll_object_index')
        else:
            rco.template_list(
                "RfB_UL_LIGHTS_LinkingObjects",
                "Renderman_light_link_list",
                rm, "object_groups",
                rm, 'll_object_index')

        #
        # Add / Remove Light Linking Button Bar
        #
        row = layout.row(align=True)
        if rm.ll_light_index == -1 or rm.ll_object_index == -1:
            # nothing selected in lists, show simple info text.
            row.label("Select light and object")
        else:
            # something in lists is selected.
            from_name = (
                bpy.data.lamps[rm.ll_light_index]
                if rm.ll_light_type == 'light'
                else rm.light_groups[rm.ll_light_index]
            )

            to_name = (
                bpy.data.objects[rm.ll_object_index]
                if rm.ll_object_type == 'object'
                else rm.object_groups[rm.ll_object_index]
            )

            ll_name = "lg_%s>%s>obj_%s>%s" % (
                rm.ll_light_type,
                from_name.name,
                rm.ll_object_type,
                to_name.name
            )

            if ll_name in rm.ll:
                #
                # selected (lco|rco) items are linked, show edit ops
                #
                rem = row.operator(
                    'rfb.item_toggle_lightlink', 'Remove Light Link')
                rem.ll_name = ll_name
                rem.add_remove = "remove"
                row.prop(rm.ll[ll_name], 'illuminate', text='')
            else:
                #
                # selected (lco|rco) items are not linked, show single add op
                #
                add = row.operator(
                    'rfb.item_toggle_lightlink', 'Add Light Link')
                add.ll_name = ll_name
                add.add_remove = 'add'
