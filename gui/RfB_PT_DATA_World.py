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

# <pep8 compliant>

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
from . RfB_PT_MIXIN_RIBInjection import RfB_PT_MIXIN_RIBInjection
from . RfB_PT_MIXIN_ShaderTypePolling import RfB_PT_MIXIN_ShaderTypePolling

from . import icons
from . utils import prop12   # |one third |     two thirds        |
from . utils import split12  # |one third |     two thirds        |
from . utils import draw_props


class RfB_PT_DATA_World(
        RfB_PT_MIXIN_RIBInjection,
        RfB_PT_MIXIN_ShaderTypePolling,
        Panel):
    bl_context = "world"
    bl_label = "World Lighting"
    shader_type = 'world'

    def draw(self, context):
        layout = self.layout
        layout = layout.column(align=True)
        world = context.scene.world

        if not world.renderman.use_renderman_node:
            layout.prop(world, "horizon_color")
            layout.operator('rfb.node_add_nodetree').idtype = 'world'
            return
        else:
            #
            # convinient access variables
            #
            __r = world.renderman
            __t = __r.renderman_type
            __n = __r.get_light_node()
            ctx = context.scene.renderman
            #
            # Type switcher (subheader of panel) aka TABs
            #
            row = layout.row(align=True)
            row.prop(__r, "renderman_type", expand=True)
            if __t == 'NONE':
                layout.separator()
                lay = layout.box()
                self.draw_rib_boxes(
                    lay, ['world_rib_box'], context.world
                )
                #
                # leave early, nothing more to draw!
                #
                return

            env = (__t == 'ENV')
            # ------------------------
            # ENV or SKY sublayout
            # ------------------------
            if __n:
                lay = layout.box().column(align=True)
                #
                # Visibility and Notes
                #
                iid = icons.toggle('cvisible', __r.light_primary_visibility)
                prp = 'light_primary_visibility'
                _s_ = lay.row(align=True)
                _s_.prop(__r, prp, text="", icon_value=iid)
                _s_.prop(__n, 'notes', text="")

                lay.separator()
                sub = lay.column(align=True)
                #
                # Basic light settings
                #
                icn = 'TRIA_DOWN' if __r.ui_open_basic else 'TRIA_RIGHT'
                prp = 'ui_open_basic'
                _s_ = sub.row(align=True)
                _s_.prop(__r, prp, text="", icon=icn)
                _s_.prop(__n, 'intensity', text="Int.")
                _s_.prop(__n, 'exposure', text="Exp.")
                if env:
                    _s_.prop(__n, 'lightColor', text="")
                else:
                    _s_.prop(__n, 'sunTint', text="")

                if __r.ui_open_basic:
                    sub = sub.box().column(align=True)
                    #
                    # This is an EnvLight, draw specifiv controls
                    #
                    if env:
                        lco, rco = split12(sub)
                        lco.label('Temperature:')
                        row = rco.row(align=True)
                        iid = icons.toggle('kelvin', __n.enableTemperature)
                        prp = 'enableTemperature'
                        row.prop(__n, prp, text="", icon_value=iid)
                        #
                        # need sublayout for active / inactive
                        #
                        _s_ = row.row(align=True)
                        _s_.active = __n.enableTemperature
                        _s_.prop(__n, 'temperature', text="Kelvin")

                        sub.separator()

                        lco, rco = split12(sub, align=True)
                        lco.label('Color Map:')
                        lco.label('Map Saturation:')
                        lco.label('Map Gamma:')
                        rco.prop(
                            __n, 'lightColorMap', text="")
                        rco.prop(
                            __n, 'colorMapSaturation', text="", slider=True)
                        row = rco.row(align=True)
                        row.prop(__n, 'colorMapGamma', text="")
                        #
                        # TODO:   Would be nice, if we could rotate the
                        #         EnvLight on z-axis. Research.
                        # DATE:   2018-02-08
                        # AUTHOR: Timm Wimmers
                        # STATUS: -unassigned-
                        #
                        # lco.label('Rotation:')
                        # rco.prop(__n, 'rotation_euler[2]', text='Z')
                        sub.separator()
                    #
                    # This is a sky light, draw additional controls
                    #
                    else:
                        lco, rco = split12(sub, align=True)
                        lco.label('Sun Size:')
                        rco.prop(__n, 'sunSize', text="")

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

                        sub.separator()

                        lco, rco = split12(sub, align=True)
                        prop12((lco, rco), __n, 'skyTint', 'Sky Tint:')
                        prop12((lco, rco), __n, 'haziness', 'Sky Haziness:')

                        sub.separator()

                        lco, rco = split12(sub)
                        lco.label('Ground Mode:')
                        if int(__n.groundMode) == 2:
                            _s_ = rco.row(align=True)
                            _s_.prop(__n, 'groundMode', text="")
                            _s_.prop(__n, 'groundColor', text="")
                        else:
                            rco.prop(__n, 'groundMode', text="")

                    sub.separator()

                    lco, rco = split12(sub)
                    lco.label('Light Group:')
                    rco.prop_search(__n, 'lightGroup',
                                    ctx, 'light_groups',
                                    text="")

                    sub.separator()

                    lco, rco = split12(sub, align=True)
                    lco.label("Specular Amount:")
                    lco.label("Diffuse Amount:")
                    rco.prop(__n, 'specular', slider=True)
                    rco.prop(__n, 'diffuse', slider=True)

                    sub.separator()

                    lco, rco = split12(sub, align=True)
                    lco.label('Light Samples:')
                    lco.label('Importance Factor:')
                    rco.prop(__n, 'fixedSampleCount', text="")
                    rco.prop(__n, 'importanceMultiplier', text="")

                layout.separator()

                icn = 'CHECKBOX_HLT'        \
                    if __n.traceLightPaths  \
                    else 'CHECKBOX_DEHLT'
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
                    lco.label("Falloff:")
                    lco.label("Gamma:")
                    rco.prop(__n, 'shadowDistance', text="")
                    rco.prop(__n, 'shadowFalloff', text="")
                    rco.prop(__n, 'shadowFalloffGamma', text="")

                    lco, rco = split12(lay, align=True)
                    lco.label("Trace:")
                    rco.prop_search(__n, 'shadowSubset',
                                    ctx, "object_groups", text="")
                    lco.label("Exclude:")
                    rco.prop_search(__n, 'shadowExcludeSubset',
                                    ctx, "object_groups", text="")

                layout.separator()
                lay = layout.box()
                self.draw_rib_boxes(lay, ['world_rib_box'], context.world)
