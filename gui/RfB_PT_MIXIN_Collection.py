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

from . utils import split_lr
from . RfB_PT_MIXIN_Panel import RfB_PT_MIXIN_Panel


class RfB_PT_MIXIN_Collection(RfB_PT_MIXIN_Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return rd.engine == 'PRMAN_RENDER'

    def _draw_collection(
        self,
        context,
        layout,
        ptr,
        name,
        operator,
        opcontext,
        prop_coll,
        collection_index,
        default_name=''
    ):

        left, right = split_lr(layout)
        # TODO: name is empty on light groups and object groups ???
        # ll.label(name)
        # FIXME: Removing a group can't be undone!
        left.label("ATTENTION: Removing a group can't be undone!")

        op = right.operator(operator, icon="ZOOMOUT", text="")
        op.context = opcontext
        op.collection = prop_coll
        op.collection_index = collection_index
        op.action = 'REMOVE'

        op = right.operator(operator, icon="ZOOMIN", text="")
        op.context = opcontext
        op.collection = prop_coll
        op.collection_index = collection_index
        op.defaultname = default_name
        op.action = 'ADD'

        row = layout.row()
        row.template_list(
            "UI_UL_list",
            "PRMAN",
            ptr,
            prop_coll,
            ptr,
            collection_index,
            rows=1
        )

        if (hasattr(ptr, prop_coll)
            and len(getattr(ptr, prop_coll)) > 0
            and getattr(ptr, collection_index) >= 0
            ):

            item = getattr(ptr, prop_coll)[getattr(ptr, collection_index)]
            self.draw_item(layout, context, item)
