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

# <pep8-80 compliant>

#
# Blender Imports
#
from bpy.types import Panel

#
# RenderMan for Blender Imports
#
from . import icons
from . utils import splitlr

from . RfB_PT_MIXIN_Collection import RfB_PT_MIXIN_Collection


class RfB_PT_SCENE_LigthGroups(RfB_PT_MIXIN_Collection, Panel):
    # bl_idname = "renderman_light_panel"
    bl_label = "Light Groups"
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
        # if len(rm.light_groups) == 0:
        #    light_group = rm.object_groups.add()
        #    light_group.name = 'All'
        opr = "rfb.collection_toggle_path"
        ctx = "scene.renderman"
        grp = "light_groups"
        idx = "light_groups_index"
        self._draw_collection(context, layout, rm, "", opr, ctx, grp, idx,
                              default_name=str(len(rm.light_groups)))

    def draw_item(self, layout, context, item):
        scene = context.scene
        rm = scene.renderman
        light_group = rm.light_groups[rm.light_groups_index]
        # row.template_list(
        #   "RfB_UL_ObjectGroup", "Renderman_light_group_list",
        #    light_group, "members", light_group, 'members_index',
        #    rows=9, maxrows=100, type='GRID', columns=9
        # )

        row = layout.row()
        add = row.operator('rfb.item_moveto_group', 'Add Selected to Group')
        add.item_type = 'light'
        add.group_index = rm.light_groups_index

        opr = 'rfb.item_remove_group'
        lbl = 'Remove Selected from Group'
        remove = row.operator(opr, lbl)
        remove.item_type = 'light'
        remove.group_index = rm.light_groups_index

        light_names = [member.name for member in light_group.members]
        if light_group.name == 'All':
            light_names = [
                lamp.name for lamp in context.scene.objects
                if lamp.type == 'LAMP'
            ]

        if len(light_names) > 0:
            box = layout.box()
            lc, rc = splitlr(box)
            lc = lc.column(align=True)
            cl = rc.column(align=True)
            for light_name in light_names:
                if light_name not in scene.objects:
                    continue
                lamp = scene.objects[light_name].data
                lamp_rm = lamp.renderman
                if lamp_rm.renderman_type == 'FILTER':
                    continue

                lc.label(light_name)

                row = cl.row(align=True)
                iid = icons.toggle("solo", lamp_rm.solo)
                row.prop(lamp_rm, 'solo', text='', icon_value=iid, emboss=True)

                iid = icons.toggle("mute", lamp_rm.mute)
                row.prop(lamp_rm, 'mute', text='', icon_value=iid, emboss=True)

                light_shader = lamp.renderman.get_light_node()

                sub = row.row(align=True)

                if light_shader:
                    sub = row.row(align=True)
                    sub.prop(light_shader, 'intensity', text='')
                    sub.prop(light_shader, 'exposure', text='')
                    if light_shader.bl_label == 'PxrEnvDayLight':
                        row.prop(light_shader, 'skyTint', text='')

                        #
                        # TODO:   Add a 'picker' button to select the light
                        #         from UI right there.
                        # DATE:   2018-01-17
                        # AUTHOR: Timm Wimmers
                        # STATUS: assigned to self
                        #
                    else:
                        row.prop(light_shader, 'lightColor', text='')
                        #
                        # color temperatur, same item as before, so draw an
                        # empty label to keep things well aligned in column.
                        #
                        lc.label('')

                        sub = cl.row(align=True)
                        sub.label(icon='BLANK1', text='')

                        kelvin_enabled = (
                            lamp_rm.PxrDomeLight_settings.enableTemperature
                            if lamp_rm.renderman_type == 'ENV'
                            else lamp_rm.PxrRectLight_settings.enableTemperature
                        )
                        prp = 'enableTemperature'
                        iid = icons.toggle('kelvin', kelvin_enabled)
                        sub.prop(light_shader, prp, text='', icon_value=iid)
                        sub.prop(light_shader, 'temperature', text='')

                        #
                        # TODO:   Add a drop down menu with well known values
                        #         for color temperature like tungsten, sunrise,
                        #         candle light, flashlight, etc. and maybe
                        #         often used studio and filmin lights.
                        #         RESEARCH for manufacturer values, i.e. ARI
                        #
                        # DATE:   2018-01-17
                        # AUTHOR: Timm Wimmers
                        # STATUS: assigned to self
                else:
                    #
                    # Simple 'Lamp' (no light shader)
                    #
                    sub.prop(lamp, 'energy', text='')
                    sub.prop(lamp, 'color', text='')

                # finished item, add some space in left and right layout.
                lc.separator()
                cl.separator()
