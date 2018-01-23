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
import bpy
from bpy.types import Panel

#
# RenderMan for Blender Imports
#
from . import icons
from .. import rfb
from .. import engine

from . RfB_PT_MIXIN_PanelIcon import RfB_PT_MIXIN_PanelIcon
from . RfB_MT_RENDER_Presets import RfB_MT_RENDER_Presets


class RfB_PT_VIEW3D_Toolshelf(RfB_PT_MIXIN_PanelIcon, Panel):
    bl_idname = "renderman_ui_panel"
    bl_label = "RenderMan"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = rfb.reg.get('BL_CATEGORY')

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return rd.engine == 'PRMAN_RENDER'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rm = scene.renderman
        if scene.render.engine != "PRMAN_RENDER":
            return

        flat_ui = not rfb.reg.get('RFB_FLAT_UI')

        # rootleyout, vertical arrangement
        rlv = layout.column()

        # ######################################################################
        # RENDER AND SPOOL LAYOUT (lay: current layout aka section)
        # ----------------------------------------------------------------------

        # [Render] Button with TRIA
        lay = rlv.column(align=True)
        row = lay.row(align=True)
        iid = icons.iconid("render")
        row.operator("render.render", text="Render Frame", icon_value=iid)
        icon = 'TRIA_DOWN' if scene.rm_render else 'TRIA_RIGHT'
        row.prop(scene, "rm_render", text="", icon=icon)

        if scene.rm_render:
            # Render UI (Smartcontrol)
            #
            # outer frame
            lay = lay.box()

            # inner frame
            box = lay.box()
            # ... and just switch to vertical arrangement
            box = box.column()

            # Render to | Denoise Post | Selected Only
            row = box.row()
            row.prop(rm, "render_into", text="")

            # Toggle: Denoise
            sub = row.row(align=True)
            iid = (icons.iconid("dnoise_on")
                   if rm.do_denoise
                   else icons.iconid("dnoise_off"))
            sub.prop(rm, "do_denoise", text="", icon_value=iid, emboss=flat_ui)

            # Toggle: selected objects only
            iid = (icons.iconid("selected_on")
                   if rm.render_selected_objects_only
                   else icons.iconid("selected_off"))
            sub.prop(rm, "render_selected_objects_only", text="", icon_value=iid, emboss=flat_ui)

            # -------------
            box.separator()
            # -------------

            # Render Presets
            row = box.row()
            row.menu("rfb_mt_render_presets", text=bpy.types.rfb_mt_render_presets.bl_label)

            sub = row.row(align=True)
            sub.label(text="", icon='BLANK1')
            sub.label(text="", icon='BLANK1')
            # sub.operator("rfb.render_add_preset", text="", icon='ZOOMIN')
            # sub.operator("rfb.render_add_preset", text="", icon='ZOOMOUT').remove_active = True

            # -------------
            box.separator()
            # -------------

            # Spool Action | External | Animation
            row = box.row()
            sub = row.row()
            op_label = "Spool Animation" if rm.external_animation else "Spool Frame"
            sub.enabled = rm.enable_external_rendering
            sub.operator("rfb.file_spool_render", text=op_label)

            # Toggle: External?
            subb = row.row(align=True)
            iid = (icons.iconid('spool_on')
                   if rm.enable_external_rendering
                   else icons.iconid('spool_off'))
            subb.prop(rm, "enable_external_rendering", icon_value=iid, icon_only=True, emboss=flat_ui)

            # Toggle: Animation?
            iid = (icons.iconid("animation_on")
                   if rm.external_animation
                   else icons.iconid("animation_off"))
            subbb = subb.row(align=True)
            subbb.enabled = rm.enable_external_rendering
            subbb.prop(rm, "external_animation", text="", icon_value=iid, emboss=flat_ui)

            # Display Driver | Denoise? | Selected only?
            row = box.row()
            row.enabled = rm.enable_external_rendering
            sub = row.row(align=True)
            sub.prop(rm, "display_driver", text="")

            # Denoise
            sub = row.row(align=True)
            sub.enabled = rm.enable_external_rendering
            iid = (icons.iconid("dnoise_on")
                   if rm.external_denoise
                   else icons.iconid("dnoise_off"))
            sub.prop(rm, "external_denoise", text="", icon_value=iid, emboss=flat_ui)

            # Selected only?
            # needs extra layout to enabale/disable explicitly
            subb = sub.row(align=True)
            iid = (icons.iconid("selected_on")
                   if rm.render_selected_objects_only
                   else icons.iconid("selected_off"))
            subb.prop(rm, "render_selected_objects_only", text="", icon_value=iid, emboss=flat_ui)

            row = box.row()
            row.enabled = rm.external_animation and rm.enable_external_rendering
            sub = row.row(align=True)
            # sub.enabled = rm.external_animation and rm.enable_external_rendering
            sub.prop(scene, "frame_start", text="Start")
            sub.prop(scene, "frame_end", text="End")

            subb = row.row(align=True)
            subb.enabled = rm.external_animation and rm.external_denoise
            iid = (icons.iconid("crossdn_on") if rm.crossframe_denoise else icons.iconid("crossdn_off"))
            subb.prop(rm, "crossframe_denoise", text="", icon_value=iid, emboss=flat_ui)
            subb.label(text="", icon='BLANK1')  # right indent

            # ui open - slightly more space on root layout
            rlv.separator()
            rlv.separator()

        # ######################################################################
        # IPR LAYOUT
        # ----------------------------------------------------------------------

        # next section layout
        lay = rlv.column(align=True)

        # Header (button with icon and label + open/close UI control)
        row = lay.row(align=True)

        # Icon for opened/closed UI
        icn = 'TRIA_DOWN' if scene.rm_ipr else 'TRIA_RIGHT'

        # Header: Stop IPR, it's running
        if engine.ipr:
            iid = icons.iconid("stop_ipr")
            row.operator('rfb.tool_ipr', text="Stop IPR", icon_value=iid)

            iid = icons.iconid("start_it")
            row.operator("rfb.tool_it", text="", icon_value=iid)
            row.prop(scene, "rm_ipr", text="", icon=icn)

        # Header: Start IPR isn't running
        else:
            iid = icons.iconid("start_ipr")
            row.operator('rfb.tool_ipr', text="Start IPR", icon_value=iid)

            iid = icons.iconid("start_it")
            row.operator("rfb.tool_it", text="", icon_value=iid)
            row.prop(scene, "rm_ipr", text="", icon=icn)

        # ui open?
        if scene.rm_ipr:
            # outer frame
            lay = lay.box()

            # inner frame
            box = lay.box()
            # ... and just switch to vertical arrangement
            box = box.column()

            # Interactive and Preview Sampling
            row = box.row(align=True)
            row.prop(rm, "preview_pixel_variance")

            row = box.row(align=True)
            row.prop(rm, "preview_min_samples", text="Min. Sampl.")
            row.prop(rm, "preview_max_samples", text="Max. Sampl.")

            row = box.row(align=True)
            row.prop(rm, "preview_max_specular_depth", text="Spec. Depth")
            row.prop(rm, "preview_max_diffuse_depth", text="Diff. Depth")

            # only when ui is open: slightly more space on root layout after
            # the frames
            rlv.separator()
            rlv.separator()

        # ######################################################################
        # CAMERA LAYOUT
        # ----------------------------------------------------------------------

        # next section layout
        lay = rlv.column(align=True)

        # Header (button with icon and label + open/close control)
        row = lay.row(align=True)
        iid = icons.iconid("camera")
        icn = 'TRIA_DOWN' if context.scene.prm_cam else 'TRIA_RIGHT'
        row.operator("rfb.object_add_camera", text="Add Camera", icon_value=iid)
        row.prop(context.scene, "prm_cam", text="", icon=icn)

        # ui open?
        if context.scene.prm_cam:
            ob = bpy.context.object
            lay = lay.box()
            box = lay.box()
            box = box.column()

            # camera list menu
            row = box.row()
            row.menu("rfb_mt_scene_cameras", text="Camera List", icon_value=iid)

            # a camera is selected, show camera controls
            if ob.type == 'CAMERA':
                row = box.row()
                # icn = 'LOCKED' if context.space_data.lock_camera else 'UNLOCKED'
                # sub = row.row(align=True)
                # sub.operator("view3d.object_as_camera", text="", icon='CURSOR')
                # sub.operator("view3d.viewnumpad", text="", icon='VISIBLE_IPO_ON').type = 'CAMERA'
                # sub.operator("wm.context_toggle", text="", icon=icn).data_path = "space_data.lock_camera"
                # sub.operator("view3d.camera_to_view", text="", icon='MAN_TRANS')

                # camera tools
                sub = row.row(align=True)
                sub.prop(ob, "name", text="", icon_value=iid)
                sub.prop(ob, "hide", text="")
                sub.prop(ob, "hide_render", icon='RESTRICT_RENDER_OFF', text="")
                sub.operator("rfb.object_delete_camera", text="", icon='PANEL_CLOSE')

                # depth of field
                row = box.row(align=True)
                row.prop(context.object.data, "dof_object", text="")
                row.prop(context.object.data.cycles, "aperture_type", text="")
                row.prop(context.object.data, "dof_distance", text="Dist.")
            else:
                box.label("")
                box.label("No Camera Selected")
            rlv.separator()
            rlv.separator()

        # ######################################################################
        # CREATE ENVIRONMENT LIGHT LAYOUT
        # ----------------------------------------------------------------------
        cl = layout.column(align=True)
        row = cl.row(align=True)
        iid = icons.iconid("envlight")
        row.operator("rfb.object_add_hemilight",
                     text="Add EnvLight",
                     icon_value=iid)

        lamps = [obj for obj in bpy.context.scene.objects if obj.type == "LAMP"]

        lamp_hemi = False
        lamp_area = False
        lamp_point = False
        lamp_spot = False
        lamp_sun = False

        if len(lamps):
            for lamp in lamps:
                if lamp.data.type == 'HEMI':
                    lamp_hemi = True

                if lamp.data.type == 'AREA':
                    lamp_area = True

                if lamp.data.type == 'POINT':
                    lamp_point = True

                if lamp.data.type == 'SPOT':
                    lamp_spot = True

                if lamp.data.type == 'SUN':
                    lamp_sun = True

        if lamp_hemi:

            row.prop(context.scene, "rm_env", text="",
                     icon='TRIA_DOWN' if context.scene.rm_env else 'TRIA_RIGHT')
            iid = icons.iconid('envlight')
            if context.scene.rm_env:
                ob = bpy.context.object
                box = cl.box()
                row = box.row(align=True)
                row.menu("rfb_mt_scene_hemilights",
                         text="EnvLight List", icon_value=iid)

                if ob.type == 'LAMP' and ob.data.type == 'HEMI':

                    row = box.row(align=True)
                    row.prop(ob, "name", text="", icon_value=iid)
                    row.prop(ob, "hide", text="")
                    row.prop(ob, "hide_render",
                             icon='RESTRICT_RENDER_OFF', text="")
                    row.operator("rfb.object_delete_light",
                                 text="", icon='PANEL_CLOSE')
                    row = box.row(align=True)
                    row.prop(ob, "rotation_euler", index=2, text="Rotation")

                else:
                    row = box.row()
                    row.label("")
                    row = box.row()
                    row.label("No EnvLight Selected")

        # ######################################################################
        # CREATE AREA LIGHT LAYOUT
        # ----------------------------------------------------------------------
        cl = layout.column(align=True)
        row = cl.row(align=True)
        iid = icons.iconid("arealight")
        row.operator("rfb.object_add_arealight", text="Add AreaLight",
                     icon_value=iid)

        lamps = [obj for obj in bpy.context.scene.objects if obj.type == "LAMP"]

        lamp_hemi = False
        lamp_area = False
        lamp_point = False
        lamp_spot = False
        lamp_sun = False

        if len(lamps):
            for lamp in lamps:
                if lamp.data.type == 'HEMI':
                    lamp_hemi = True

                if lamp.data.type == 'AREA':
                    lamp_area = True

                if lamp.data.type == 'POINT':
                    lamp_point = True

                if lamp.data.type == 'SPOT':
                    lamp_spot = True

                if lamp.data.type == 'SUN':
                    lamp_sun = True

        if lamp_area:

            row.prop(context.scene, "rm_area", text="",
                     icon='TRIA_DOWN' if context.scene.rm_area else 'TRIA_RIGHT')

            if context.scene.rm_area:
                ob = bpy.context.object
                box = cl.box()
                row = box.row(align=True)
                row.menu("rfb_mt_scene_arealights",
                         text="Area Light List", icon_value=iid)

                if ob and ob.type == 'LAMP' and ob.data.type == 'AREA':

                    row = box.row(align=True)
                    row.prop(ob, "name", text="", icon_value=iid)
                    row.prop(ob, "hide", text="")
                    row.prop(ob, "hide_render",
                             icon='RESTRICT_RENDER_OFF', text="")
                    row.operator("rfb.object_delete_light",
                                 text="", icon='PANEL_CLOSE')

                else:
                    row = box.row(align=True)
                    row.label("No AreaLight Selected")
        # ----------------------------------------------------------------------
        # CREATE AREA LIGHT LAYOUT END
        # ######################################################################

        # ######################################################################
        # CREATE DAYLIGHT LIGHT LAYOUT
        # ----------------------------------------------------------------------
        cl = layout.column(align=True)
        row = cl.row(align=True)
        iid = icons.iconid("sunlight")
        row.operator("rfb.object_add_daylight",
                     text="Add Daylight",
                     icon_value=iid)

        lamps = [obj for obj in bpy.context.scene.objects if obj.type == "LAMP"]

        lamp_hemi = False
        lamp_area = False
        lamp_point = False
        lamp_spot = False
        lamp_sun = False

        if len(lamps):
            for lamp in lamps:
                if lamp.data.type == 'SUN':
                    lamp_sun = True

                if lamp.data.type == 'HEMI':
                    lamp_hemi = True

                if lamp.data.type == 'AREA':
                    lamp_area = True

                if lamp.data.type == 'POINT':
                    lamp_point = True

                if lamp.data.type == 'SPOT':
                    lamp_spot = True

        if lamp_sun:

            row.prop(context.scene, "rm_daylight", text="",
                     icon='TRIA_DOWN' if context.scene.rm_daylight else 'TRIA_RIGHT')

            if context.scene.rm_daylight:
                ob = bpy.context.object
                box = layout.box()
                row = box.row(align=True)
                row.menu("rfb_mt_scene_daylights",
                         text="DayLight List", icon='LAMP_SUN')

                if ob.type == 'LAMP' and ob.data.type == 'SUN':

                    row = box.row(align=True)
                    row.prop(ob, "name", text="", icon='LAMP_SUN')
                    row.prop(ob, "hide", text="")
                    row.prop(ob, "hide_render",
                             icon='RESTRICT_RENDER_OFF', text="")
                    row.operator("rfb.object_delete_light",
                                 text="", icon='PANEL_CLOSE')

                else:
                    row = layout.row(align=True)
                    row.label("No DayLight Selected")

            # if layout is open creat more space
            layout.separator()
        # ----------------------------------------------------------------------
        # CREATE AREA LIGHT LAYOUT END
        # ######################################################################

        # ######################################################################
        # TODO: Dynamic Binding Editor
        # ######################################################################

        # ######################################################################
        # TODO: Create Holdout
        # ######################################################################

        # Open Linking Panel
        # row = layout.row(align=True)
        # row.operator("renderman.lighting_panel")

        # ######################################################################
        # SELECTED OBJECT LAYOUT
        # ----------------------------------------------------------------------
        #
        # Let's see if there are obejcts selected which this layout may
        # be usable for.
        #
        selected_objects = []
        if context.selected_objects:
            for obj in context.selected_objects:
                if obj.type not in ['CAMERA', 'LAMP', 'SPEAKER']:
                    selected_objects.append(obj)

        if selected_objects:
            #
            # Create a new 'current layout'
            #
            cl = layout.column(align=True)
            cl.label("Seleced Objects:")
            #
            # Create PxrLM Material
            #
            # iid = icons.iconid("pxrdisney")
            # custom icon in 'operator_menu_item' not possible
            cl.operator_menu_enum("rfb.material_add_bxdf",
                                  'bxdf_name',
                                  text="Add New Material",
                                  icon='MATERIAL')
            #
            # Make Selected Geo Emissive
            #
            iid = icons.iconid("make_emissive")
            cl.operator("rfb.object_make_emissive",
                        text="Make Emissive",
                        icon_value=iid)
            #
            # Add Subdiv Sheme
            #
            iid = icons.iconid("add_subdiv_sheme")
            cl.operator("rfb.object_enable_subdiv",
                        text="Make Subdiv",
                        icon_value=iid)
            #
            # Add/Create RIB Box. Create Archive node
            #
            iid = icons.iconid("archive_rib")
            cl.operator("rfb.object_export_rib",
                        icon_value=iid)

        # ----------------------------------------------------------------------
        # SELECTED OBJECT LAYOUT END
        # ######################################################################
        layout.separator()
        # ######################################################################
        #
        # TODO: Create Geo LightBlocker
        # TODO: Inspect RIB Selection
        # TODO: Shared Geometry Attribute
        # TODO: Add/Atach Coordsys
        # TODO: Open Tmake Window  ?? Run Tmake on everything.
        # TODO: Create OpenVDB Visualizer
        #
        # ######################################################################
        # layout.separator()
        # ######################################################################
        # SUPPORT LAYOUT
        # ----------------------------------------------------------------------
        cl = layout.column(align=True)
        #
        # RenderMan Doc (online)
        #
        iid = icons.iconid("web")  # used twice!

        href = "https://github.com/prman-pixar/RenderManForBlender/wiki/Documentation-Home"
        cl.operator("wm.url_open",
                    text="RenderMan Docs",
                    icon_value=iid).url = href
        #
        # RenderMan What's new (online)
        #
        href = "https://renderman.pixar.com/whats-new"
        cl.operator("wm.url_open",
                    text="About RenderMan",
                    icon_value=iid).url = href
        # ----------------------------------------------------------------------
        # SUPPORT LAYOUT END
        # ######################################################################
        layout.separator()
        # ######################################################################
        # RELOAD ADDON
        # ----------------------------------------------------------------------
        # # TODO: doesn't work!
        # #
        # # Reload the addon
        # #
        # # iid = icons.iconid("reload_plugin")
        # # cl.operator("rfb.restartaddon", icon_value=iid)
        #
        # Maybe this could work??
        #
        # row.operator(
        #         "wm.addon_disable" if is_enabled else "wm.addon_enable",
        #         icon='CHECKBOX_HLT' if is_enabled else 'CHECKBOX_DEHLT', text="",
        #         emboss=False,
        #         ).module = 'RMAN'
        # ----------------------------------------------------------------------
        # RELOAD ADDON END
        # ######################################################################
        # layout.separator()
        # ######################################################################
        # OPEN LAST RIB LAYOUT
        # ----------------------------------------------------------------------
        iid = icons.iconid("open_last_rib")
        layout.operator("rfb.file_open_last_rib",
                        text="Open Last RIB",
                        icon_value=iid)
        # ----------------------------------------------------------------------
        # OPEN LAST RIB END
        # ######################################################################

# EOF

# [CODE_ID_001]
# # Sampling
# row = box.row(align=True)
# row = box.row(align=True)
# col = row.column(align=True)
# col.prop(rm, "pixel_variance")
# row = col.row(align=True)
# row.prop(rm, "min_samples", text="Min Samples")
# row.prop(rm, "max_samples", text="Max Samples")
# row = col.row(align=True)
# row.prop(rm, "max_specular_depth", text="Specular Depth")
# row.prop(rm, "max_diffuse_depth", text="Diffuse Depth")

# # Resolution
# rd = scene.render
# row = box.row(align=True)
# sub = row.row(align=True)
# sub.prop(rd, "resolution_x", text="X")
# sub.prop(rd, "resolution_y", text="Y")
# sub.prop(rd, "resolution_percentage", text="")
