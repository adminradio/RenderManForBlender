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
# RenderManForBlender Imports
#
from .. import icons
from ... import engine

from ... rfb.prf import pref


#
# FIXME:  splitll() and splitlr() return rows() instead of column()
#         This is NOT wrong´, but have to be parameterized for ROW and COL!
# DATE:   2018-02-04
# AUTHOR: Timm Wimmers
# STATUS: -unassigned-
#
def splitll(_l_, align=False):
    row = _l_.row()

    __l = row.row(align=align)
    __l.alignment = "LEFT"

    __r = row.row(align=align)
    __r.alignment = "LEFT"

    return __l, __r


def splitlr(_l_, align=False):
    row = _l_.row()

    __l = row.row(align=align)
    __l.alignment = "LEFT"

    __r = row.row(align=align)
    __r.alignment = "RIGHT"

    return __l, __r

#
# split percentage
#


def splitpc(_l_, _p_, align=False):
    spl = _l_.row().split(percentage=_p_)
    __l = spl.column(align=align)
    spl = spl.split()
    __r = spl.column(align=align)
    return __l, __r


#
# read them like:
#   - split one one
#   - split one two
#   - split two one etc.
#
#   i.e: 'split12' or spoken as 'split one two' is:
#       - one fraction left    (one third)
#       - two fractions right  (two thirds)
#       - you get the idea ...
#
def split11(_l_, align=False):
    return splitpc(_l_, 1 / 2, align=align)


def split12(_l_, align=False):
    return splitpc(_l_, 1 / 3, align=align)


def split21(_l_, align=False):
    return splitpc(_l_, 2 / 3, align=align)


def split13(_l_, align=False):
    return splitpc(_l_, 1 / 4, align=align)


def split31(_l_, align=False):
    return splitpc(_l_, 3 / 4, align=align)


def split14(_l_, align=False):
    return splitpc(_l_, 1 / 5, align=align)


def split41(_l_, align=False):
    return splitpc(_l_, 4 / 5, align=align)


def prop12(_l_, dta, prp, lbl):
    """
    Draw a property left labeled with 1/3 - 2/3 distribution.

    If you already have a distributed layout, you can pass in a tuple with
    two layout references (aka left and right); if not simply pass in a parent
    layout we will draw your property in a row with 1/3 distribution.

    This function doesn't append any colons, if you want one, append one to
    your label string (lbl).
    """
    #
    # TODO:   if lbl is none take from property name.
    # DATE:   2018-02-08
    # AUTHOR: Timm Wimmers
    # STATUS: -unassigned-
    #
    if type(_l_) == tuple:
        _ll = _l_[0]
        _rl = _l_[1]
    else:
        _ll, _rl = split12(_l_.row())
    _ll.label(lbl)
    _rl.prop(dta, prp, text="")
    return


def boxh(_l_):
    """Draw a bordered box with horizontal arrangement."""
    return _l_.box().row()


def boxv(_l_):
    """Draw a bordered box with vertical arrangement."""
    #
    # vertical alignmnet is default
    #
    return _l_.box()


def draw_props(node, prop_names, layout):
    nst = pref('rfb_nesting')
    #
    # if the user enables boxed nesting, we can compress space vertically a
    # little bit, because boxing adds a bit of padding by itself
    #
    align = True if nst else False
    layout = layout.column(align=align)

    for prop_name in prop_names:
        prop_meta = node.prop_meta[prop_name]
        prop = getattr(node, prop_name)
        #
        # skip 'Notes', already drawn on root layout
        #
        if prop_name in ['Notes', 'notes']:
            continue
        #
        # -------------------------------------------------------------------
        # 'pages' are the headers of subpanels
        # -------------------------------------------------------------------
        #
        if prop_meta['renderman_type'] == 'page':
            #
            # we add a little bit space in FRONT of the sublayout
            # this is nicer as behind, because of recursion that would add
            # also space behind sub sub layouts, which looks ugly.
            #
            layout.separator()

            ui_prop = prop_name + "_ui_open"
            ui_open = getattr(node, ui_prop)

            txt = prop_name.split('.')[-1]
            if nst:
                icn = 'TRIA_DOWN' if ui_open else 'TRIA_RIGHT'
                lay = layout
                lay.prop(node, ui_prop, icon=icn, text=txt, emboss=True)
            else:
                icn = 'TRIA_DOWN' if ui_open else 'TRIA_RIGHT'
                lay = layout
                lay.prop(node, ui_prop, icon=icn, text=txt, emboss=False)

            if ui_open:
                lay = lay.box()
                draw_props(node, prop, lay)
        #
        # -------------------------------------------------------------------
        # this is a property of a page
        # -------------------------------------------------------------------
        #
        else:
            if ('widget'
                    in prop_meta
                    and prop_meta['widget'] == 'null'
                    or 'hidden' in prop_meta and prop_meta['hidden']
                    or prop_name == 'combineMode'):
                continue
            lay = layout.column(align=True)
            if "Subset" in prop_name and prop_meta['type'] == 'string':
                #
                # FIXME:  bpy.data.scenes[0] is the first scene
                #         in file, this should be 'active scene'!
                # DATE:   2018-02-06
                # AUTHOR: Timm Wimmers
                # STATUS: -unassigned-
                #
                rm = bpy.data.scenes[0].renderman
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
                #
                # properties where we don't want a label
                #
                elif prop_name in ['map', 'fillColor', 'tint']:
                    lay.prop(node, prop_name, text="")

                elif prop_name in ['directional', 'useLightDirection']:
                    iid = icons.iconid(prop_name)
                    if prop_name == 'directional':
                        row = lay.row(align=True)
                        row.prop(node, prop_name, icon_value=iid, emboss=True)
                    else:
                        row.prop(node, prop_name, icon_value=iid, emboss=True)

                elif prop_name in ['density', 'invert']:
                    #
                    # tricky swap of rows
                    #
                    if prop_name == 'density':
                        one = lay.column(align=True)
                        two = lay.column(align=True)
                        two.prop(node, prop_name)
                    else:
                        iid = icons.toggle('invert', getattr(node, prop_name))
                        try:
                            one.prop(node, prop_name, icon_value=iid)
                        except UnboundLocalError:
                            #
                            # Yuck! I want this row at first place but, that
                            # seems not be possible.
                            #
                            # Different 'invert' property, there was no
                            # 'density' before! A bit ugly! Maybe this can be
                            # done with some reorderung of args-xml while
                            # parsing it?
                            #
                            # TW: 2018-02-14
                            #
                            lay.separator()
                            lay.prop(node, prop_name, icon_value=iid)
                            lay.separator()

                elif prop_name in ['tileMode', 'invertU', 'invertV']:
                    iid = icons.toggle('invert', getattr(node, prop_name))
                    if prop_name == 'tileMode':
                        row = lay.row(align=True)
                        lay.prop(node, prop_name, text="")  # yes, not row!
                    else:
                        row.prop(node, prop_name, icon_value=iid)

                #
                # no special handling, draw simply the property
                #
                else:
                    lay.prop(node, prop_name)
                #
                # props which requires some space behind
                #
                if prop_name in ['edge', 'rampType', 'tileMode',
                                 'preBarn', ]:
                    lay.separator()
    # -------------------------------------------------------------
    # end for
    # -------------------------------------------------------------


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
