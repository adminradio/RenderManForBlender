# ##### BEGIN MIT LICENSE BLOCK #####
#
# Copyright (c) 2015 - 2017 Pixar
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

#
# RenderMan for Blender Imports
#
from .. import icons
from ... import engine


def split_ll(layout, alignment=True):
    """Split a layout into two colums. Both are left aligned."""
    row = layout.row()

    # left column, left aligned
    lc = row.row(align=alignment)
    lc.alignment = "LEFT"

    # right column, left aligned
    rc = row.row(align=alignment)
    rc.alignment = "LEFT"
    return lc, rc


def split_lr(layout, alignment=True):
    """Split a layout into two colums. First is left, second is right aligned."""
    row = layout.row()

    # left column, left aligned
    lc = row.row(align=alignment)
    lc.alignment = "LEFT"

    # right column, right aligned
    rc = row.row(align=alignment)
    rc.alignment = "RIGHT"
    return lc, rc


def bbox_h(layout):
    """Draw a bordered box with horizontal arrangement."""
    box = layout.box()
    return box.row()


def bbox_v(layout):
    """Draw a bordered box with vertical arrangement."""
    box = layout.box()
    return box.column()


def draw_props(node, prop_names, layout):
    for prop_name in prop_names:
        prop_meta = node.prop_meta[prop_name]
        prop = getattr(node, prop_name)

        if prop_meta['renderman_type'] == 'page':
            ui_prop = prop_name + "_ui_open"
            ui_open = getattr(node, ui_prop)
            iid = icons.toggle('panel', ui_open)
            cl = layout.box()
            cl.prop(
                node,
                ui_prop,
                icon_value=iid,
                text=prop_name.split('.')[-1],
                icon_only=True,
                emboss=False)

            if ui_open:
                draw_props(node, prop, cl)

        else:
            if ('widget' in prop_meta and prop_meta['widget'] == 'null'
                    or 'hidden' in prop_meta and prop_meta['hidden']
                    or prop_name == 'combineMode'):
                continue

            cl = layout.row()
            if "Subset" in prop_name and prop_meta['type'] == 'string':
                cl.prop_search(
                    node,
                    prop_name,
                    bpy.data.scenes[0].renderman,
                    "object_groups")
            else:
                if 'widget' in prop_meta and prop_meta['widget'] == 'floatRamp':
                    rm = bpy.context.lamp.renderman
                    nt = bpy.context.lamp.node_tree
                    float_node = nt.nodes[rm.float_ramp_node]
                    layout.template_curve_mapping(float_node, 'mapping')
                elif 'widget' in prop_meta and prop_meta['widget'] == 'colorRamp':
                    rm = bpy.context.lamp.renderman
                    nt = bpy.context.lamp.node_tree
                    ramp_node = nt.nodes[rm.color_ramp_node]
                    layout.template_color_ramp(ramp_node, 'color_ramp')
                else:
                    cl.prop(node, prop_name)


def rfb_menu_func(self, context):
    if context.scene.render.engine != "PRMAN_RENDER":
        return
    self.layout.separator()
    if engine.ipr:
        self.layout.operator('rfb.tool_ipr',
                             text="RenderMan Stop Interactive Rendering")
    else:
        self.layout.operator('rfb.tool_ipr',
                             text="RenderMan Start Interactive Rendering")


def rfb_panels():
    rfb_panels_true = []
    rfb_panels_false = {
        'DATA_PT_area',
        'DATA_PT_camera_dof',
        'DATA_PT_falloff_curve',
        'DATA_PT_lamp',
        'DATA_PT_preview',
        'DATA_PT_shadow',
        # 'DATA_PT_spot',
        'DATA_PT_sunsky',
        # 'MATERIAL_PT_context_material',
        'MATERIAL_PT_diffuse',
        'MATERIAL_PT_flare',
        'MATERIAL_PT_halo',
        'MATERIAL_PT_mirror',
        'MATERIAL_PT_options',
        'MATERIAL_PT_pipeline',
        'MATERIAL_PT_preview',
        'MATERIAL_PT_shading',
        'MATERIAL_PT_shadow',
        'MATERIAL_PT_specular',
        'MATERIAL_PT_sss',
        'MATERIAL_PT_strand',
        'MATERIAL_PT_transp',
        'MATERIAL_PT_volume_density',
        'MATERIAL_PT_volume_integration',
        'MATERIAL_PT_volume_lighting',
        'MATERIAL_PT_volume_options',
        'MATERIAL_PT_volume_shading',
        'MATERIAL_PT_volume_transp',
        'RENDERLAYER_PT_layer_options',
        'RENDERLAYER_PT_layer_passes',
        'RENDERLAYER_PT_views',
        'RENDER_PT_antialiasing',
        'RENDER_PT_bake',
        'RENDER_PT_motion_blur',
        'RENDER_PT_performance',
        'RENDER_PT_freestyle',
        # 'RENDER_PT_post_processing',
        'RENDER_PT_shading',
        'RENDER_PT_render',
        'RENDER_PT_stamp',
        'SCENE_PT_simplify',
        'TEXTURE_PT_context_texture',
        'WORLD_PT_ambient_occlusion',
        'WORLD_PT_environment_lighting',
        'WORLD_PT_gather',
        'WORLD_PT_indirect_lighting',
        'WORLD_PT_mist',
        'WORLD_PT_preview',
        'WORLD_PT_world',
    }

    for t in bpy.types.Panel.__subclasses__():
        if hasattr(t, 'COMPAT_ENGINES') and 'BLENDER_RENDER' in t.COMPAT_ENGINES:
            if t.__name__ not in rfb_panels_false:
                rfb_panels_true.append(t)

    return rfb_panels_true
