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
from . import icons


def draw_props(node, prop_names, layout):
    for prop_name in prop_names:
        prop_meta = node.prop_meta[prop_name]
        prop = getattr(node, prop_name)

        if prop_meta['renderman_type'] == 'page':
            ui_prop = prop_name + "_ui_open"
            ui_open = getattr(node, ui_prop)

            cond = bpy.context.scene.renderman.alf_options
            icn = 'panel_open' if cond else 'panel_closed'
            iid = icons.iconid(icn)
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
