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
# Python Imports
#

#
# Blender Imports
#
import bpy

#
# RenderManForBlender Imports
#
from .. rfb.prf import pref


class RfB_OT_MIXIN_AddLight(bpy.types.Operator):
    bl_idname = "rfb.object_mixin_addlight"
    bl_label = "DUMMY MIXIN LABEL"
    bl_options = {"REGISTER", "UNDO"}

    #
    # TODO:   Is this really the right way to do as a mixin?
    #         This operator mixin gets even registered under bpy.ops.rfb
    #         but shouldn't distribute to the user or executed by itself.
    #         Or should we create a simple utility function instead without
    #         wrapping it into a class?
    # DATE:   2018-02-10
    # AUTHOR: Timm Wimmers
    # STATUS: -unassigned-
    #
    def addlight(self, context, typ):
        if pref('add_lights_pos') == 'CURSOR':
            bpy.ops.object.lamp_add(
                type=typ
            )
        elif pref('add_lights_pos') == 'WORLDCENTER':
            bpy.ops.object.lamp_add(
                type=typ, location=(0, 0, 0)
            )
        elif pref('add_lights_pos') == 'POSITION':
            bpy.ops.object.lamp_add(
                type=typ, location=pref('add_lights_coord')
            )
        lgt = bpy.context.active_object  # remember light
        if pref('add_lights_rigged'):
            _n_ = pref('add_lights_rigname')
            rig = None  # fd
            aex = True  # fd already existing rig (dead mans switch)

            try:
                rig = bpy.data.objects[_n_]
            except KeyError:
                # there is no rig
                aex = False

            if not aex:
                rig = bpy.data.objects.new(_n_, None)
                bpy.context.scene.objects.link(rig)
                #
                # TODO:   Add pref for size of empty/rig
                #         IMHO the default of 1.0 is always to small!
                # DATE:   2018-02-09
                # AUTHOR: Timm Wimmers
                # STATUS: -unassigned-
                #
                rig.empty_draw_size = 3.0
                rig.empty_draw_type = 'PLAIN_AXES'
                rig.name = _n_
            lgt.parent = rig
        bpy.ops.object.select_all(action='DESELECT')
        tmpl = pref('add_lights_naming')
        if tmpl:
            _l_ = {
                'HEMI': 'EnvLight', 'SUN': 'DayLight', 'AREA': 'AreaLight'
            }
            _t_ = {
                'HEMI': 'ENV', 'SUN': 'DAY', 'AREA': 'AREA'
            }
            _s_ = {
                'HEMI': 'E', 'SUN': 'D', 'AREA': 'A'
            }
            tmpl = tmpl.replace("{LONG}", _l_[typ])
            tmpl = tmpl.replace("{TYPE}", _t_[typ])
            tmpl = tmpl.replace("{SHORT}", _s_[typ])
            lgt.name = tmpl
            lgt.data.name = tmpl

        bpy.context.scene.objects.active = lgt
        lgt.select = True
        bpy.ops.rfb.node_add_nodetree(
            {'material': None, 'lamp': bpy.context.active_object.data},
            idtype='lamp'
        )
        return
