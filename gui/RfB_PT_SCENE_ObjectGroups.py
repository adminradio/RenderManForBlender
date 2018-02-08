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
from bpy.types import Panel

#
# RenderMan for Blender Imports
#
from . import icons

from . RfB_PT_MIXIN_Collection import RfB_PT_MIXIN_Collection


class RfB_PT_SCENE_ObjectGroups(RfB_PT_MIXIN_Collection, Panel):
  bl_idname = "renderman_object_groups_panel"
  bl_label = "Object Groups"
  bl_context = "scene"
  bl_space_type = 'PROPERTIES'
  bl_region_type = 'WINDOW'  # bl_category = "Renderman"

  @classmethod
  def poll(cls, context):
    rd = context.scene.render
    return rd.engine == 'PRMAN_RENDER'

  def draw(self, context):
    layout = self.layout
    scene = context.scene
    rm = scene.renderman
    # if len(rm.object_groups) == 0:
    #    collector_group = rm.object_groups.add()
    #    collector_group.name = 'collector'

    self._draw_collection(context, layout, rm, "",
                          "rfb.collection_toggle_path",
                          "scene.renderman",
                          "object_groups", "object_groups_index",
                          default_name=str(len(rm.object_groups)))

  def draw_item(self, layout, context, item):
    row = layout.row()
    scene = context.scene
    rm = scene.renderman
    group = rm.object_groups[rm.object_groups_index]

    row = layout.row()
    row.operator('rfb.item_moveto_group',
                 'Add Selected to Group').group_index = rm.object_groups_index
    row.operator('rfb.item_remove_group',
                 'Remove Selected from Group').group_index = rm.object_groups_index

    row = layout.row()
    row.template_list("RfB_UL_ObjectGroup", "Renderman_group_list",
                      group, "members", group, 'members_index',
                      item_dyntip_propname='name',
                      type='GRID', columns=3)
