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
from . utils import prop12   # one third // two thirds
from . utils import split12  # one third // two thirds


class RfB_PT_DATA_World(
        RfB_PT_MIXIN_RIBInjection,
        RfB_PT_MIXIN_ShaderTypePolling,
        Panel):
    bl_context = "world"
    bl_label = "World Setup"
    shader_type = 'world'

    def draw(self, context):
        layout = self.layout
        world = context.scene.world

        layout = layout.column(align=True)

        if not world.renderman.use_renderman_node:
            layout.prop(world, "horizon_color")
            layout.operator('rfb.node_add_nodetree').idtype = 'world'
            return
        else:
            #
            # convinient access variables
            #
            wrm = world.renderman
            wrt = world.renderman.renderman_type
            #
            # Type switcher (subheader of panel) aka TABs
            #
            row = layout.row(align=True)
            row.prop(wrm, "renderman_type", expand=True)
            if wrt == 'NONE':
                layout.separator()
                lay = layout.box()
                self.draw_rib_boxes(
                    lay, ['world_rib_box'], context.world
                )
                #
                # leave early, nothing more to draw!
                #
                return

            env = (wrt == 'ENV')
            # ------------------------
            # ENV or SKY sublayout
            # ------------------------
            wln = wrm.get_light_node()  # W_orld L_ight N_ode
            if wln:
                lay = layout.box().column(align=True)
                #
                # Visibility and Notes
                #
                iid = icons.toggle('cvisible', wrm.light_primary_visibility)
                prp = 'light_primary_visibility'
                _s_ = lay.row(align=True)
                _s_.prop(wrm, prp, text="", icon_value=iid)
                _s_.prop(wln, 'notes', text="")

                lay.separator()
                sub = lay.column(align=True)
                #
                # Basic light settings
                #
                icn = 'TRIA_DOWN' if wrm.ui_open_basic else 'TRIA_RIGHT'
                prp = 'ui_open_basic'
                _s_ = sub.row(align=True)
                _s_.prop(wrm, prp, text="", icon=icn)
                _s_.prop(wln, 'intensity', text="Int.")
                _s_.prop(wln, 'exposure', text="Exp.")
                if env:
                    _s_.prop(wln, 'lightColor', text="")
                else:
                    _s_.prop(wln, 'sunTint', text="")

                if wrm.ui_open_basic:
                    sub = sub.box().column(align=True)
                    #
                    # This is an EnvLight, draw specifiv controls
                    #
                    if env:
                        lco, rco = split12(sub)
                        lco.label('Temperature:')
                        row = rco.row(align=True)
                        iid = icons.toggle('kelvin', wln.enableTemperature)
                        prp = 'enableTemperature'
                        row.prop(wln, prp, text="", icon_value=iid)
                        #
                        # need sublayout for active / inactive
                        #
                        _s_ = row.row(align=True)
                        _s_.active = wln.enableTemperature
                        _s_.prop(wln, 'temperature', text="Kelvin")

                        sub.separator()

                        prop12(
                            sub, wln,
                            'lightColorMap', 'Color Map:'
                        )
                        prop12(
                            sub, wln,
                            'colorMapSaturation', 'Map Saturation:'
                        )
                        lco, rco = split12(sub)
                        lco.label('Map Gamma:')
                        _s_ = rco.row()
                        _s_.prop(wln, 'colorMapGamma', text="")
                        #
                        # TODO:   Would be nice, if we could rotate the
                        #         EnvLight. Research.
                        # DATE:   2018-02-08
                        # AUTHOR: Timm Wimmers
                        # STATUS: -unassigned-
                        #
                        # lco.label('Rotation:')
                        # rco.prop(wln, 'rotation_euler[2]', text='Z')
                        sub.separator()
                    #
                    # This is a sky light, draw additional controls
                    #
                    else:
                        lco, rco = split12(sub)
                        prop12((lco, rco), wln, 'sunSize', 'Sun Size:')

                        lco.label('Sun Mode:')
                        if int(wln.month) > 0:
                            _s_ = rco.row(align=True)
                            _s_.prop(wln, 'month', text="")
                            _s_.prop(wln, 'day', text="")
                            _s_.prop(wln, 'year', text="")

                            lco.label('Hour / TZ:')
                            _s_ = rco.row(align=True)
                            _s_.prop(wln, 'hour', text="")
                            _s_.prop(wln, 'zone', text="")

                            lco.label('Lat. / Long.:')
                            _s_ = rco.row(align=True)
                            _s_.prop(wln, 'latitude', text="")
                            _s_.prop(wln, 'longitude', text="")
                        else:
                            rco.prop(wln, 'month', text="")
                            lco.label("Sun Direction:")
                            _s_ = rco.row(align=True)
                            _s_.prop(wln, 'sunDirection', text="")

                        sub.separator()

                        lco, rco = split12(sub, align=True)
                        prop12((lco, rco), wln, 'skyTint', 'Sky Tint:')
                        prop12((lco, rco), wln, 'haziness', 'Sky Haziness:')

                        sub.separator()

                        lco, rco = split12(sub)
                        lco.label('Ground Mode:')
                        if int(wln.groundMode) == 2:
                            _s_ = rco.row(align=True)
                            _s_.prop(wln, 'groundMode', text="")
                            _s_.prop(wln, 'groundColor', text="")
                        else:
                            rco.prop(wln, 'groundMode', text="")

                        sub.separator()

                    lco, rco = split12(sub, align=True)
                    prop12((lco, rco), wln, 'specular', 'Specular:')
                    prop12((lco, rco), wln, 'diffuse', 'Diffuse:')
                #
                # Advanced (Shadows / Trace Light Paths)
                #
                lay.separator()
                row = lay.row(align=True)
                icn = 'TRIA_DOWN' if wrm.ui_open_advanced else 'TRIA_RIGHT'
                row.prop(wrm, 'ui_open_advanced', text="", icon=icn)
                row.prop(wrm, 'rfb_light_advanced', expand=True)

                if wrm.ui_open_advanced:
                    sub = lay.column(align=True).box().column(align=True)
                    les = wln.enableShadows
                    ctx = context.scene.renderman
                    if les:
                        sub.separator()

                        lco, rco = split12(sub)
                        lco.prop(wln, 'thinShadow')
                        rco.prop(wln, 'shadowColor', text="")
                        sub.separator()

                        lco, rco = split12(sub, align=True)
                        prop12(
                            (lco, rco), wln,
                            'shadowDistance', 'Max Distance:'
                        )
                        prop12(
                            (lco, rco), wln,
                            'shadowFalloff', 'Falloff:'
                        )
                        prop12(
                            (lco, rco), wln,
                            'shadowFalloffGamma', 'Gamma:'
                        )

                        sub.separator()

                        lco, rco = split12(sub, align=True)
                        lco.label('Trace Subset:')
                        rco.prop_search(
                            wln, 'shadowSubset',
                            ctx, "object_groups",
                            text=""
                        )
                        lco.label('Exclude Subset:')
                        rco.prop_search(
                            wln, 'shadowExcludeSubset',
                            ctx, "object_groups",
                            text=""
                        )
                        sub.separator()

                    lco, rco = split12(sub)
                    lco.label('Light Group:')
                    rco.prop_search(wln, 'lightGroup',
                                    ctx, 'light_groups',
                                    text="")

                    sub.separator()

                    lco, rco = split12(sub, align=True)
                    prop12(
                        (lco, rco), wln,
                        'fixedSampleCount', 'Light Samples:'
                    )
                    prop12(
                        (lco, rco), wln,
                        'importanceMultiplier', 'Importance Factor:'
                    )
                layout.separator()
                lay = layout.box()
                self.draw_rib_boxes(lay, ['world_rib_box'], context.world )
