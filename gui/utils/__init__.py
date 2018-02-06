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

from ... rfb.lib.prfs import pref


#
# FIXME:  split_ll() and split_lr() return rows() instead of column()
#         This is wrong - have to be fixed everywhere!
# DATE:   2018-02-04
# AUTHOR: Timm Wimmers
# STATUS: -unassigned-
#
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
    nst = pref('rfb_nesting')
    #
    # if the user enables boxed nesting, we can compress space vertically a
    # little bit, because boxing adds also space by itself inside
    #
    align = True if nst else False
    layout = layout.column(align=align)

    for prop_name in prop_names:
        prop_meta = node.prop_meta[prop_name]
        prop = getattr(node, prop_name)

        if prop_meta['renderman_type'] == 'page':
            ui_prop = prop_name + "_ui_open"
            ui_open = getattr(node, ui_prop)

            txt = prop_name.split('.')[-1]
            if nst:
                icn = 'panel_open' if ui_open else 'panel_closed'
                iid = icons.iconid(icn)
                lay = layout.box()
                lay.prop(node, ui_prop, icon_value=iid, text=txt, emboss=False)
            else:
                icn = 'TRIA_DOWN' if ui_open else 'TRIA_RIGHT'
                lay = layout
                lay.prop(node, ui_prop, icon=icn, text=txt, emboss=False)

            if ui_open:
                draw_props(node, prop, lay)

        else:
            if ('widget'
                    in prop_meta
                    and prop_meta['widget'] == 'null'
                    or 'hidden' in prop_meta and prop_meta['hidden']
                    or prop_name == 'combineMode'):
                continue
            sub = layout.column()
            lay = sub.row()
            if "Subset" in prop_name and prop_meta['type'] == 'string':
                rm = bpy.data.scenes[0].renderman
                #
                # FIXME:  bpy.data.scenes[0] is the first scene
                #         in file, this should be 'active scene'!
                # DATE:   2018-02-06
                # AUTHOR: Timm Wimmers
                # STATUS: -unassigned-
                #
                lay.prop_search(node, prop_name, rm, "object_groups")
            else:
                if ('widget'
                        in prop_meta
                        and prop_meta['widget'] == 'floatRamp'):
                    rm = bpy.context.lamp.renderman
                    nt = bpy.context.lamp.node_tree
                    float_node = nt.nodes[rm.float_ramp_node]
                    layout.template_curve_mapping(float_node, 'mapping')

                elif ('widget'
                        in prop_meta
                        and prop_meta['widget'] == 'colorRamp'):
                    rm = bpy.context.lamp.renderman
                    nt = bpy.context.lamp.node_tree
                    ramp_node = nt.nodes[rm.color_ramp_node]
                    layout.template_color_ramp(ramp_node, 'color_ramp')
                else:
                    lay.prop(node, prop_name)
                    if nst:
                        #
                        # disable compressed layout inside box()
                        # workaround, lay.column(align=False) doesn't work!
                        #
                        sub.separator()


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
