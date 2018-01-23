# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import time
import bpy
import bgl
from bgl import *
from bpy.types import SpaceNodeEditor

from sverchok import node_tree
from sverchok.node_tree import SverchCustomTree
from sverchok.node_tree import SverchCustomTreeNode

callback_dict = {}
point_dict = {}


def node_id(oper):
    return str(hash(oper) ^ hash(time.monotonic()))


def tag_redraw_all_nodeviews():
    for window in bpy.context.window_manager.windows:
        areas = window.screen.areas
        for area in (a for a in areas if a.type == 'NODE_EDITOR'):
            for region in (r for r in area.regions if r.type == 'WINDOW'):
                region.tag_redraw()


def callback_enable(n_id, nt):
    global callback_dict
    if n_id in callback_dict:
        return

    data = {}
    data['tree_name'] = nt.name
    args = n_id, data

    handle_pixel = SpaceNodeEditor.draw_handler_add(draw_callback_px, args, 'WINDOW', 'PRE_VIEW')
    callback_dict[n_id] = handle_pixel
    tag_redraw_all_nodeviews()


def callback_disable(n_id):
    global callback_dict
    handle_pixel = callback_dict.get(n_id, None)
    if not handle_pixel:
        return
    SpaceNodeEditor.draw_handler_remove(handle_pixel, 'WINDOW')
    del callback_dict[n_id]
    tag_redraw_all_nodeviews()


def callback_disable_all():
    global callback_dict
    temp_list = list(callback_dict.keys())
    for n_id in temp_list:
        if n_id:
            callback_disable(n_id)


def draw_callback_px(n_id, data):
    space = bpy.context.space_data
    ng_view = space.edit_tree
    if not ng_view:
        return

    ng_name = space.edit_tree.name
    if not (data['tree_name'] == ng_name):
        return
    if not isinstance(ng_view, node_tree.SverchCustomTree):
        return

    face_color = (0.2, 0.2, 0.2)
    scn = bpy.context.scene
    s = scn.sv_scale_unit
    image_name = scn.sv_available_image

    img = bpy.data.images.get(image_name)
    if img:
        img.gl_load(0, bgl.GL_NEAREST, bgl.GL_NEAREST)
        texture = img.bindcode
        w, h = img.size
        w2 = w / 2
        h2 = h / 2
        _w2 = w2 * s
        _h2 = h2 * s
    else:
        return

    glEnable(GL_BLEND)
    glBindTexture(GL_TEXTURE_2D, texture)
    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0 * _w2, -1.0 * _h2, 0.0)  # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0)
    glVertex3f(+1.0 * _w2, -1.0 * _h2, 0.0)  # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0)
    glVertex3f(+1.0 * _w2, +1.0 * _h2, 0.0)  # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0 * _w2, +1.0 * _h2, 0.0)  # Top Left Of The Texture and
    glEnd()
    glDisable(GL_TEXTURE_2D)

    # restore opengl defaults
    glLineWidth(1)
    glDisable(GL_BLEND)
    glColor4f(0.0, 0.0, 0.0, 1.0)


def get_items(self, context):
    images = bpy.data.images
    inames = [i.name for i in images]
    return [(i, i, 'image %s' % i) for i in inames]


class svImageShowOperator(bpy.types.Operator):
    bl_idname = "scene.operator_sv_show_image_bg"
    bl_label = "Image Show"
    bl_description = "Toggle the visibility of the background image"

    # _handle = None

    @classmethod
    def poll(cls, context):
        scn = context.scene
        if scn.sv_show_image and scn.sv_available_image:
            return True

    def modal(self, context, event):
        nt = context.space_data.node_tree
        if scn.sv_show_image and scn.sv_available_image:
            n_id = node_id(nt)
            callback_enable(n_id, nt)
        else:
            callback_disable_all()
            return {"CANCELLED"}

        return {"PASS_THROUGH"}

    def invoke(self, context, event):
        scn = context.scene
        nt = context.space_data.node_tree

        if scn.sv_show_image and scn.sv_available_image:
            n_id = node_id(nt)
            callback_enable(n_id, nt)
            return {'RUNNING_MODAL'}
        else:
            self.report({"WARNING"}, "View3D not found, can't run operator")
            return {"CANCELLED"}


class SverchokImageBG(bpy.types.Panel):
    bl_idname = "Sverchok_img_bf"
    bl_label = "SV BGIMAGE"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Sverchok'
    bl_options = {'DEFAULT_CLOSED'}
    use_pin = True

    @classmethod
    def poll(cls, context):
        try:
            return context.space_data.node_tree.bl_idname == 'SverchCustomTreeType'
        except:
            return False

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        ntree = context.space_data.node_tree
        c = layout.column()
        c.operator(svImageShowOperator.bl_idname, text="Show Image")
        c.prop(scn, 'sv_show_image')
        c.prop(scn, 'sv_available_image', text='pick image')
        c.prop(scn, 'sv_scale_unit')


def register():
    bpy.types.Scene.sv_show_image = bpy.props.BoolProperty()
    bpy.types.Scene.sv_available_image = bpy.props.EnumProperty(
        name="Images", items=get_items,
        description="Image paths")
    bpy.types.Scene.sv_scale_unit = bpy.props.FloatProperty(default=1.2)

    bpy.types.Scene.sv_custom_backdrop = bpy.props.StringProperty(default='')
    bpy.utils.register_class(svImageShowOperator)
    bpy.utils.register_class(SverchokImageBG)


def unregister():
    bpy.utils.unregister_class(SverchokImageBG)
    bpy.utils.unregister_class(svImageShowOperator)
    callback_disable_all()

    scn = bpy.types.Scene
    del scn.sv_custom_backdrop
    del scn.sv_show_image
    del scn.sv_available_image
    del scn.sv_scale_unit


if __name__ == '__main__':
    register()
