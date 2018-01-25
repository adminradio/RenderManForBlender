# ##### BEGIN MIT LICENSE BLOCK #####
#
# Copyright (c) 2015 - 2018 Pixar
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sb1license, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, sb1ject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or sb1stantial portions of the Software.
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

from . RfB_MT_RENDER_Presets import RfB_MT_RENDER_Presets
from . RfB_PT_MIXIN_PanelIcon import RfB_PT_MIXIN_PanelIcon


class RfB_PT_VIEW3D_Toolshelf(RfB_PT_MIXIN_PanelIcon, Panel):
    bl_idname = "renderman_ui_panel"
    bl_label = "Render Control"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = rfb.reg.get('RFB_TABNAME')

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

        # RENDER AND SPOOL LAYOUT (lay: current layout aka section)
        # ######################################################################
        col = layout.column(align=True)
        row = col.row(align=True)

        opr = "render.render"
        txt = "Render Animation" if rm.external_animation else "Render Frame"
        iid = icons.iconid("batch_render") if rm.external_animation else icons.iconid("render")
        ani = True if rm.external_animation else False
        sub = row.row(align=True)
        sub.enabled = True if bpy.context.scene.camera else False
        sub.operator(opr, text=txt, icon_value=iid).animation = ani

        prp = "rm_render"
        icn = 'TRIA_DOWN' if scene.rm_render else 'TRIA_RIGHT'
        row.prop(scene, prp, icon_only=True, icon=icn)

        # render ui open?
        if scene.rm_render:
            sub = col.box().box().column()

            row = sub.row()
            prp = "render_into"
            row.prop(rm, prp, text="")

            sb1 = row.row(align=True)
            prp = "do_denoise"
            iid = (icons.iconid("dnoise_on")
                   if rm.do_denoise
                   else icons.iconid("dnoise_off"))
            sb1.prop(rm, prp, icon_only=True, icon_value=iid)

            prp = "render_selected_objects_only"
            iid = (icons.iconid("selected_on")
                   if rm.render_selected_objects_only
                   else icons.iconid("selected_off"))
            sb1.prop(rm, prp, icon_only=True, icon_value=iid)
            sub.separator()

            # Render Presets
            row = sub.row()

            mnu = "rfb_mt_render_presets"
            txt = bpy.types.rfb_mt_render_presets.bl_label
            row.menu(mnu, text=txt)

            sb1 = row.row(align=True)
            sb1.label(text="", icon='BLANK1')
            sb1.label(text="", icon='BLANK1')
            sub.separator()

            # Spool Action | External | Animation
            row = sub.row()
            sb1 = row.row()
            sb1.enabled = rm.enable_external_rendering

            sb2 = sb1.row()
            sb2.enabled = True if bpy.context.scene.camera else False

            opr = "rfb.file_spool_render"
            txt = "Spool Animation" if rm.external_animation else "Spool Frame"
            sb2.operator(opr, text=txt)

            # Toggle: External?
            sb2 = row.row(align=True)
            prp = "enable_external_rendering"
            iid = icons.toggle('spool', rm.enable_external_rendering)
            sb2.prop(rm, prp, icon_only=True, icon_value=iid)

            # Toggle: Animation?
            sb3 = sb2.row(align=True)
            sb3.enabled = rm.enable_external_rendering
            prp = "external_animation"
            iid = icons.toggle("animation", rm.external_animation)
            sb3.prop(rm, prp, icon_only=True, icon_value=iid)

            # Dispsub.Driver | Denoise? | Selected only?
            row = sub.row()
            row.enabled = rm.enable_external_rendering

            sb1 = row.row(align=True)
            prp = "display_driver"
            sb1.prop(rm, prp, text="")

            # Denoise
            sb1 = row.row(align=True)
            sb1.enabled = rm.enable_external_rendering

            prp = "external_denoise"
            iid = icons.toggle("dnoise", rm.external_denoise)
            sb1.prop(rm, prp, icon_only=True, icon_value=iid)

            # Selected only?
            sb2 = sb1.row(align=True)
            prp = "render_selected_objects_only"
            iid = icons.toggle("selected", rm.render_selected_objects_only)
            sb2.prop(rm, prp, icon_only=True, icon_value=iid)

            row = sub.row()
            row.enabled = rm.external_animation and rm.enable_external_rendering
            sb1 = row.row(align=True)
            sb1.prop(scene, "frame_start", text="Start")
            sb1.prop(scene, "frame_end", text="End")

            sb2 = row.row(align=True)
            sb2.enabled = rm.external_animation and rm.external_denoise
            prp = "crossframe_denoise"
            iid = icons.toggle("crossdn", rm.crossframe_denoise)
            sb2.prop(rm, prp, icon_only=True, icon_value=iid)
            sb2.label(text="", icon='BLANK1')  # right indent

            # ui open - slightly more space on root layout
            layout.separator()

        # IPR LAYOUT
        # ######################################################################
        col = layout.column(align=True)
        row = col.row(align=True)
        icn = 'TRIA_DOWN' if scene.rm_ipr else 'TRIA_RIGHT'

        # Header: Stop IPR, it's running
        if engine.ipr:
            iid = icons.iconid("stop_ipr")
            row.operator('rfb.tool_ipr', text="Stop IPR", icon_value=iid)

            iid = icons.iconid("start_it")
            row.operator("rfb.tool_it", text="", icon_value=iid)
            row.prop(scene, "rm_ipr", icon_only=True, icon=icn)

        # Header: Start IPR isn't running
        else:
            iid = icons.iconid("start_ipr")
            sub = row.row(align=True)
            sub.enabled = True if bpy.context.scene.camera else False
            sub.operator('rfb.tool_ipr', text="Start IPR", icon_value=iid)

            iid = icons.iconid("start_it")
            row.operator("rfb.tool_it", text="", icon_value=iid)
            row.prop(scene, "rm_ipr", icon_only=True, icon=icn)

        # ui open?
        if scene.rm_ipr:
            sub = col.box().box().column()

            # Interactive and Preview Sampling
            row = sub.row(align=True)
            row.prop(rm, "preview_pixel_variance")

            row = sub.row(align=True)
            row.prop(rm, "preview_min_samples", text="Min. Sampl.")
            row.prop(rm, "preview_max_samples", text="Max. Sampl.")

            row = sub.row(align=True)
            row.prop(rm, "preview_max_specular_depth", text="Spec. Depth")
            row.prop(rm, "preview_max_diffuse_depth", text="Diff. Depth")

            # only when ui is open: slightly more space on root layout after
            # the frames
            layout.separator()

        # CAMERA LAYOUT
        # ######################################################################
        col = layout.column(align=True)
        row = col.row(align=True)

        opr = "rfb.object_add_camera"
        txt = "Add Camera"
        iid = icons.iconid("camera")
        row.operator(opr, text=txt, icon_value=iid)

        prp = "prm_cam"
        icn = 'TRIA_DOWN' if context.scene.prm_cam else 'TRIA_RIGHT'
        row.prop(context.scene, prp, text="", icon=icn)

        # ui open?
        if context.scene.prm_cam:
            sub = col.box().box().column()

            # camera list menu
            row = sub.row()
            mnu = "rfb_mt_scene_cameras"
            row.menu(mnu)

            obj = bpy.context.object
            if obj and obj.type == 'CAMERA':
                row = sub.row()

                # camera tools
                sb1 = row.row(align=True)

                opr = "rfb.object_delete_camera"
                icn = 'PANEL_CLOSE'
                sb1.operator(opr, text="", icon=icn)
                cam = bpy.data.scenes[scene.name].camera
                sb1.prop(cam, "name", text="", icon_value=iid)

                opr = "rfb.view_numpad0"
                view = context.space_data.region_3d.view_perspective
                if view == 'CAMERA':
                    sb1.operator(opr, text="", icon='VIEW3D')
                else:
                    iid = icons.iconid('camview_on')
                    sb1.operator(opr, text="", icon_value=iid)

                opr = "wm.context_toggle"
                iid = icons.toggle('camlock', context.space_data.lock_camera)
                pth = "space_data.lock_camera"
                sb1.operator(opr, text="", icon_value=iid).data_path = pth

                # depth of field
                row = sub.row(align=True)
                prp = "dof_object"
                row.prop(context.object.data, prp, icon_only=True)

                prp = "dof_distance"
                row.prop(context.object.data, prp, text="Dist.")
                #
                # TODO:   refactor aperture/radius to radio buttons
                # DATE:   2018-01-20
                # AUTHOR: Timm Wimmers
                # STATUS: assigned to self
                #
                opr = "rfb.camera_aperture_type"
                val = context.object.data.cycles.aperture_type
                iid = (
                    icons.iconid('shutter_off')
                    if val == 'FSTOP'
                    else icons.iconid('radius')
                )
                row.operator(opr, text="", icon_value=iid)
                # prp = "aperture_type"
                # row.prop(context.object.data.cycles, prp, text="")
            else:
                cams = [
                    obj for obj in bpy.context.scene.objects
                    if obj.type == "CAMERA"
                ]

                if cams:
                    active = ""
                    try:
                        active = bpy.data.scenes[scene.name].camera.name
                    except AttributeError:
                        bpy.data.scenes[scene.name].camera = cams[0]
                    txt = "Active camera: {}".format(cams[0].name)
                    sub.label(txt)
                    opr = "rfb.object_select_active_camera"
                    txt = "Select"
                    icn = 'RESTRICT_SELECT_OFF'
                    sub.operator(opr, text=txt, icon=icn)
                else:
                    sub.label("")
                    sub.label("Current scene contains no camera!")
            layout.separator()
            # layout.separator()

        # ######################################################################
        # CREATE ENVIRONMENT LIGHT LAYOUT
        #
        col = layout.column(align=True)
        row = col.row(align=True)

        opr = "rfb.object_add_light_hemi"
        txt = "Add EnvLight"
        iid = icons.iconid("envlight")  # used multiple times
        row.operator(opr, text=txt, icon_value=iid)

        prp = "rm_env"
        icn = 'TRIA_DOWN' if context.scene.rm_env else 'TRIA_RIGHT'
        row.prop(context.scene, prp, icon_only=True, icon=icn)

        lamps = [
            obj for obj in bpy.context.scene.objects
            if obj.type == "LAMP"
        ]

        lamp_hmi = lamp_rea = lamp_pnt = lamp_spt = lamp_sun = False

        for lamp in lamps:
            if lamp.data.type == 'HEMI':
                lamp_hmi = True
            if lamp.data.type == 'AREA':
                lamp_rea = True
            if lamp.data.type == 'POINT':
                lamp_pnt = True
            if lamp.data.type == 'SPOT':
                lamp_spt = True
            if lamp.data.type == 'SUN':
                lamp_sun = True

        if scene.rm_env:
            sub = col.box().box().column()
            row = sub.row(align=True)

            if lamp_hmi:
                txt = "EnvLight List"
                mnu = "rfb_mt_scene_lightshemi"
                row.menu(mnu, text=txt)
            else:
                row.label("")

            obj = bpy.context.object
            if obj and obj.type == 'LAMP' and obj.data.type == 'HEMI':
                row = sub.row(align=True)

                row.prop(obj, "name", text="", icon_value=iid)
                row.prop(obj, "hide", icon_only=True)

                prp = "hide_render"
                icn = 'RESTRICT_RENDER_OFF'
                row.prop(obj, prp, icon=icn, icon_only=True)

                opr = "rfb.object_delete_light"
                icn = 'PANEL_CLOSE'
                row.operator(opr, text="", icon=icn)

                row = sub.row(align=True)
                opr = "rotation_euler"
                txt = "Rotation"
                row.prop(obj, opr, index=2, text=txt)
            else:
                row = sub.row()
                row.label("")
                row = sub.row()
                txt = "No EnvLight Selected." if lamp_hmi else \
                      "Scene contains no EnvLight."
                row.label(txt)

            layout.separator()

        # ######################################################################
        # CREATE AREA LIGHT LAYOUT
        #
        col = layout.column(align=True)
        row = col.row(align=True)

        opr = "rfb.object_add_light_area"
        txt = "Add Area Light"
        iid = icons.iconid("arealight")
        row.operator(opr, text=txt, icon_value=iid)

        prp = "rm_area"
        icn = 'TRIA_DOWN' if scene.rm_area else 'TRIA_RIGHT'
        row.prop(context.scene, prp, icon_only=True, icon=icn)

        lamp_hmi = lamp_rea = lamp_pnt = lamp_spt = lamp_sun = False

        lamps = [
            obj for obj in bpy.context.scene.objects
            if obj.type == "LAMP"
        ]

        for lamp in lamps:
            if lamp.data.type == 'HEMI':
                lamp_hmi = True
            if lamp.data.type == 'AREA':
                lamp_rea = True
            if lamp.data.type == 'POINT':
                lamp_pnt = True
            if lamp.data.type == 'SPOT':
                lamp_spt = True
            if lamp.data.type == 'SUN':
                lamp_sun = True

        if scene.rm_area:
            sub = col.box().box().column()

            row = sub.row(align=True)

            if lamp_rea:
                mnu = "rfb_mt_scene_lightsarea"
                txt = "Area Light List"
                row.menu(mnu, text=txt)
            else:
                row.label("")

            obj = bpy.context.object
            if obj and obj.type == 'LAMP' and obj.data.type == 'AREA':
                row = sub.row(align=True)
                row.prop(obj, "name", text="", icon_value=iid)
                row.prop(obj, "hide", icon_only=True)
                icn = 'RESTRICT_RENDER_OFF'
                row.prop(obj, "hide_render", icon_only=True, icon=icn)
                icn = 'PANEL_CLOSE'
                row.operator("rfb.object_delete_light", text="", icon=icn)
            else:
                row = sub.row(align=True)
                txt = "No AreaLight Selected." if lamp_rea else \
                      "Scene contains no AreaLight."
                row.label(txt)
            # if layout is open create more space on root layout
            layout.separator()

        # ######################################################################
        # CREATE DAYLIGHT LIGHT LAYOUT
        #
        col = layout.column(align=True)
        row = col.row(align=True)
        opr = "rfb.object_add_light_day"
        txt = "Add Daylight"
        iid = icons.iconid("sunlight")
        row.operator(opr, text=txt, icon_value=iid)

        prp = "rm_daylight"
        icn = 'TRIA_DOWN' if scene.rm_daylight else 'TRIA_RIGHT'
        row.prop(context.scene, prp, icon_only=True, icon=icn)

        lamps = [
            obj for obj in bpy.context.scene.objects
            if obj.type == "LAMP"
        ]

        lamp_hmi = lamp_rea = lamp_pnt = lamp_spt = lamp_sun = False

        for lamp in lamps:
            if lamp.data.type == 'SUN':
                lamp_sun = True
            if lamp.data.type == 'HEMI':
                lamp_hmi = True
            if lamp.data.type == 'AREA':
                lamp_rea = True
            if lamp.data.type == 'POINT':
                lamp_pnt = True
            if lamp.data.type == 'SPOT':
                lamp_spt = True

        if scene.rm_daylight:
            sub = col.box().box().column()
            row = sub.row(align=True)

            if lamp_sun:
                mnu = "rfb_mt_scene_lightsday"
                txt = "DayLight List"
                icn = 'LAMP_SUN'
                row.menu(mnu, text=txt, icon=icn)
            else:
                row.label()

            obj = bpy.context.object
            if obj and obj.type == 'LAMP' and obj.data.type == 'SUN':
                row = sub.row(align=True)

                row.prop(obj, "name", text="", icon='LAMP_SUN')
                row.prop(obj, "hide", icon_only=True)

                prp = "hide_render"
                icn = 'RESTRICT_RENDER_OFF'
                row.prop(obj, prp, icon_only=True, icon=icn)

                opr = "rfb.object_delete_light"
                icn = 'PANEL_CLOSE'
                row.operator(opr, text="", icon=icn)
            else:
                row = sub.row(align=True)
                txt = "No DayLight selected." if lamp_sun else \
                      "Scene contains no DayLight."
                row.label(txt)
            # if layout is open create more space on root layout
            layout.separator()

        # ######################################################################
        # SELECTED OBJECTS - SUPPORT - OPEN LAST RIB
        #
        sln = []
        if context.selected_objects:
            for obj in bpy.context.selected_objects:
                if obj.type not in ['CAMERA', 'LAMP', 'SPEAKER']:
                    sln.append(obj)
        if sln:
            col = layout.column(align=True)

            # Create new material
            opr = "rfb.material_add_bxdf"
            txt = "Add New Material"
            icn = 'MATERIAL'
            col.operator_menu_enum(opr, 'bxdf_name', text=txt, icon=icn)

            # Make object emissive
            opr = "rfb.object_make_emissive"
            txt = "Make Emissive"
            iid = icons.iconid("make_emissive")
            col.operator(opr, text=txt, icon_value=iid)

            # Add sb1div scheme
            opr = "rfb.object_enable_subdiv"
            txt = "Make Subdiv"
            iid = icons.iconid("make_subdiv")
            col.operator(opr, text=txt, icon_value=iid)

            # Export object as RIB archive
            opr = "rfb.object_export_rib"
            txt = "Export RIB Archive"
            iid = icons.iconid("archive_rib")
            col.operator(opr, text=txt, icon_value=iid)

        col = layout.column(align=True)
        # iid used twice
        iid = icons.iconid("web")

        # RenderMan Doc (online)
        opr = "wm.url_open"
        txt = "RenderMan Docs"
        url = ("https://github.com/prman-pixar/"
               "RenderManForBlender/wiki/Documentation-Home")
        col.operator(opr, text=txt, icon_value=iid).url = url

        # RenderMan What's new (online)
        opr = "wm.url_open"
        txt = "About RenderMan"
        url = "https://renderman.pixar.com/whats-new"
        col.operator(opr, text=txt, icon_value=iid).url = url

        col = layout.column(align=True)

        opr = "rfb.file_open_last_rib"
        txt = "Open Last RIB"
        iid = icons.iconid("open_rib")
        col.operator(opr, text=txt, icon_value=iid)
