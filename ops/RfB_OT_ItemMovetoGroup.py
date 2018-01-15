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
from bpy.props import IntProperty
from bpy.props import StringProperty


class RfB_OT_ItemMovetoGroup(bpy.types.Operator):
    bl_idname = 'rfb.item_moveto_group'
    bl_label = 'Move Item to Object Group'

    group_index = IntProperty(default=0)
    item_type = StringProperty(default='object')

    def execute(self, context):
        scene = context.scene
        group_index = self.properties.group_index
        item_type = self.properties.item_type

        object_group = (
            scene.renderman.object_groups
            if item_type == 'object'
            else scene.renderman.light_groups)

        object_group = object_group[group_index].members
        if hasattr(context, 'selected_objects'):

            members = object_group.keys()

            for ob in context.selected_objects:
                if ob.name not in members:
                    if item_type != 'light' or ob.type == 'LAMP':
                        do_add = True
                        if item_type == 'light' and ob.type == 'LAMP':
                            # check if light is already in another group
                            # can only be in one
                            for lg in scene.renderman.light_groups:
                                if ob.name in lg.members.keys():
                                    do_add = False
                                    self.report(
                                        {'WARNING'},
                                        "Lamp %s cannot be added to light group %s, already a member of %s" % (
                                            ob.name, scene.renderman.light_groups[group_index].name, lg.name)
                                    )

                        if do_add:
                            ob_in_group = object_group.add()
                            ob_in_group.name = ob.name

        return {'FINISHED'}
