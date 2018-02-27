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
from bpy.types import Panel

#
# RenderManForBlender Imports
#
from . RfB_PT_MIXIN_ShaderNodePolling import RfB_PT_MIXIN_ShaderNodePolling
from . utils import draw_props

from . icons import toggle
from . utils import split12


class RfB_PT_DATA_Light(RfB_PT_MIXIN_ShaderNodePolling, Panel):
    bl_label = "Light Shader"
    bl_context = 'data'

    def draw(self, context):
        layout = self.layout
        layout = layout.column(align=True)
        __l = context.lamp
        __n = __l.renderman.get_light_node()
        __c = context.scene.renderman
        __r = __l.renderman
        __t = __r.renderman_type

        if not __n:
            #
            # This is not a RenderMan light node, leave early!
            #
            return

        #
        # Camera Visibility (if not filter) and notes
        #
        row = layout.row(align=True)
        if __t != 'FILTER':
            iid = toggle('cvisible', __r.light_primary_visibility)
            row.prop(__r, 'light_primary_visibility', text="", icon_value=iid)
            row.prop(__n, 'notes', text="")
            layout.separator()
        #
        # Basic Settings
        #
        lay = layout.column(align=True)
        row = lay.row(align=True)
        if hasattr(__n, 'Basic_ui_open') and __t != 'SKY':
            icn = 'TRIA_DOWN' if __n.Basic_ui_open else 'TRIA_RIGHT'
            row.prop(__n, 'Basic_ui_open', text="", icon=icn)
            row.prop(__n, 'intensity', text="Int.")
            row.prop(__n, 'exposure', text="Exp.")
            row.prop(__n, 'lightColor', text="")

            if __n.Basic_ui_open:
                lay = lay.box()
                lco, rco = split12(lay.row(), align=True)
                lco.label("Temperature:")
                row = rco.row(align=True)
                iid = toggle('kelvin', __n.enableTemperature)
                row.prop(__n, 'enableTemperature', text="", icon_value=iid)
                ##
                # TODO:   implement menu for common kelvin values i.e.
                #         cie illuminants
                # DATE:   2018-02-13
                # AUTHOR: Timm Wimmers
                # STATUS: -unassigned-
                #
                sub = row.row(align=True)
                sub.active = __n.enableTemperature
                sub.prop(__n, 'temperature', text="Kelvin")

                if hasattr(__n, 'lightColorMap'):
                    lco, rco = split12(lay.column(), align=True)
                    lco.label("Color Map:")
                    lco.label("Map Saturation:")
                    lco.label("Map Gamma:")
                    rco.prop(__n, 'lightColorMap', text="")
                    rco.prop(__n, 'colorMapSaturation', text="", slider=True)
                    row = rco.row(align=True)
                    row.prop(__n, 'colorMapGamma', text="")

                if hasattr(__n, 'iesProfile'):
                    lco, rco = split12(lay.column(), align=True)
                    lco.label('IES Profile:')

                    split = rco.split(percentage=1 / 3, align=True)
                    row = split.row(align=True)
                    row.prop(__n, 'iesProfileScale', text="", slider=True)
                    row = split.row(align=True)
                    row.row(align=True).prop(__n, 'iesProfile', text="")

                if hasattr(__n, 'lightGroup'):
                    lco, rco = split12(lay.column(), align=True)
                    lco.label('Light Group:')
                    rco.prop_search(
                        __n, 'lightGroup', __c, 'light_groups', text="")

                if hasattr(__n, 'specular'):
                    lco, rco = split12(lay.column(), align=True)
                    lco.label('Specular Amount:')
                    lco.label('Diffuse Amount:')
                    rco.prop(__n, 'specular', text="", slider=True)
                    rco.prop(__n, 'diffuse', text="", slider=True)

                if hasattr(__n, 'emissionFocus'):
                    lco, rco = split12(lay.column(), align=True)
                    lco.label('Emission Focus:')
                    row = rco.row(align=True)
                    row.prop(__n, 'emissionFocus', text="")
                    row.prop(__n, 'emissionFocusTint', text="")

                if hasattr(__n, 'intensityNearDist'):
                    lco, rco = split12(lay.column(), align=True)
                    lco.label('Intensity Near Dist:')
                    rco.prop(__n, 'intensityNearDist', text="")

                if hasattr(__n, 'coneAngle'):
                    lco, rco = split12(lay.column(), align=True)
                    lco.label('Cone Angle:')
                    lco.label('Cone Softness:')
                    rco.prop(__n, 'coneAngle', text="")
                    rco.prop(__n, 'coneSoftness', text="")

                if hasattr(__n, 'fixedSampleCount'):
                    lco, rco = split12(lay.column(), align=True)
                    lco.label('Light Samples:')
                    rco.prop(__n, 'fixedSampleCount', text="")
                    lco.label('Importance Multiplier:')
                    rco.prop(__n, 'importanceMultiplier', text="")

                if hasattr(__n, 'areaNormalize'):
                    lco, rco = split12(lay.column(), align=True)
                    lco.label('Light Scaling:')
                    rco.prop(__n, 'areaNormalize')

            layout.separator()

            icn = 'CHECKBOX_HLT'if __n.traceLightPaths else 'CHECKBOX_DEHLT'
            layout.prop(__n, 'traceLightPaths', icon=icn, emboss=True)

            lay = layout.column(align=True)
            lay.enabled = not __n.traceLightPaths
            icn = 'CHECKBOX_HLT'            \
                if __n.enableShadows        \
                and not __n.traceLightPaths \
                else 'CHECKBOX_DEHLT'
            lay.prop(__n, 'enableShadows', icon=icn)
            if __n.enableShadows and not __n.traceLightPaths:
                lay = lay.box()

                lco, rco = split12(lay, align=True)
                lco.prop(__n, 'thinShadow', text="Thin Shadows")
                rco.prop(__n, 'shadowColor', text="")

                lco, rco = split12(lay, align=True)
                lco.label("Max Distance:")
                rco.prop(__n, 'shadowDistance', text="")
                lco.label("Falloff:")
                rco.prop(__n, 'shadowFalloff', text="")
                lco.label("Gamma:")
                rco.prop(__n, 'shadowFalloffGamma', text="")

                lco, rco = split12(lay, align=True)
                lco.label("Trace:")
                rco.prop_search(__n, 'shadowSubset',
                                __c, "object_groups", text="")
                lco.label("Exclude:")
                rco.prop_search(__n, 'shadowExcludeSubset',
                                __c, "object_groups", text="")

        elif __t == 'SKY':
            #
            # we use refine as lamps with __t = 'SKY' do not yet have an
            # attribut basic_ui_open (refine is otherwise unused after
            # refactoring)
            #
            icn = 'TRIA_DOWN' if __n.Refine_ui_open else 'TRIA_RIGHT'
            row.prop(__n, 'Refine_ui_open', text="", icon=icn)
            row.prop(__n, 'intensity')
            row.prop(__n, 'exposure')
            row.prop(__n, 'sunTint', text="")
            if __n.Refine_ui_open:
                lay = lay.box()
                lco, rco = split12(lay.row())
                lco.label('Sun Size:')
                rco.prop(__n, 'sunSize', text="")

                lco, rco = split12(lay.row(), align=True)
                lco.label('Sun Mode:')
                if int(__n.month) > 0:
                    _s_ = rco.row(align=True)
                    _s_.prop(__n, 'month', text="")
                    _s_.prop(__n, 'day', text="")
                    _s_.prop(__n, 'year', text="")

                    lco.label('Hour / TZ:')
                    _s_ = rco.row(align=True)
                    _s_.prop(__n, 'hour', text="")
                    _s_.prop(__n, 'zone', text="")

                    lco.label('Lat. / Long.:')
                    _s_ = rco.row(align=True)
                    _s_.prop(__n, 'latitude', text="")
                    _s_.prop(__n, 'longitude', text="")
                else:
                    rco.prop(__n, 'month', text="")
                    lco.label("Sun Direction:")
                    _s_ = rco.row(align=True)
                    _s_.prop(__n, 'sunDirection', text="")

                lco, rco = split12(lay.column(), align=True)
                lco.label("Sky Tint:")
                lco.label("Sky Haziness:")
                rco.prop(__n, 'skyTint', text="")
                rco.prop(__n, 'haziness', text="")

                lco, rco = split12(lay)
                lco.label('Ground Mode:')
                if int(__n.groundMode) == 2:
                    _s_ = rco.row(align=True)
                    _s_.prop(__n, 'groundMode', text="")
                    _s_.prop(__n, 'groundColor', text="")
                else:
                    rco.prop(__n, 'groundMode', text="")

                lco, rco = split12(lay.column(), align=True)
                lco.label("Specular:")
                lco.label("Diffuse:")
                rco.prop(__n, 'specular', text="", slider=True)
                rco.prop(__n, 'diffuse', text="", slider=True)

                if hasattr(__n, 'fixedSampleCount'):
                    lco, rco = split12(lay.column(), align=True)
                    lco.label('Light Samples:')
                    rco.prop(__n, 'fixedSampleCount', text="")
                    lco.label('Importance Multiplier:')
                    rco.prop(__n, 'importanceMultiplier', text="")

            layout.separator()

            icn = 'CHECKBOX_HLT'if __n.traceLightPaths else 'CHECKBOX_DEHLT'
            layout.prop(__n, 'traceLightPaths', icon=icn, emboss=True)

            layout.separator()

            lay = layout.column(align=True)
            lay.enabled = not __n.traceLightPaths
            icn = 'CHECKBOX_HLT'            \
                if __n.enableShadows        \
                and not __n.traceLightPaths \
                else 'CHECKBOX_DEHLT'
            lay.prop(__n, 'enableShadows', icon=icn)
            if __n.enableShadows and not __n.traceLightPaths:
                lay = lay.box()

                lco, rco = split12(lay, align=True)
                lco.prop(__n, 'thinShadow', text="Thin Shadows")
                rco.prop(__n, 'shadowColor', text="")

                lco, rco = split12(lay, align=True)
                lco.label("Max Distance:")
                rco.prop(__n, 'shadowDistance', text="")
                lco.label("Falloff:")
                rco.prop(__n, 'shadowFalloff', text="")
                lco.label("Gamma:")
                rco.prop(__n, 'shadowFalloffGamma', text="")

                lco, rco = split12(lay, align=True)
                lco.label("Trace:")
                rco.prop_search(__n, 'shadowSubset',
                                __c, "object_groups", text="")
                lco.label("Exclude:")
                rco.prop_search(__n, 'shadowExcludeSubset',
                                __c, "object_groups", text="")
        elif __t == 'FILTER':
            lay = layout.column(align=True)
            lay.prop(__n, 'notes', text="")
            layout.separator()
            draw_props(__n, __n.prop_names, layout)
