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

# <pep8-80 compliant>

#
# Python Imports
#

#
# Blender Imports
#
import bpy
from bpy.types import Panel

#
# RenderManForBlender Imports
#
from . import icons
from .. import engine
from .. rfb.lib.prfs import pref

from . RfB_MT_RENDER_Presets import RfB_MT_RENDER_Presets  # noqa
from . RfB_PT_MIXIN_PanelIcon import RfB_PT_MIXIN_PanelIcon


class RfB_PT_VIEW3D_Toolshelf(RfB_PT_MIXIN_PanelIcon, Panel):
    bl_idname = "rfb_pt_view3d_toolshelf"
    bl_label = "Main Control"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = pref('rfb_tabname')

    def __init__(self):
        self.eid = icons.iconid('empty')
        self.cid = icons.iconid('camera')
        self.wid = icons.iconid("web")

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return rd.engine == 'PRMAN_RENDER'

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        rmn = scn.renderman
        if scn.render.engine != "PRMAN_RENDER":
            return

        #
        # selected renderable objects (no cameras, no lamps, no speaker)
        # used for button "Selected Objects Only" and later on for
        # object specific operators near the end of toolshelf
        #
        _sro_ = []  # selected renderable objects
        if context.selected_objects:
            for obj in bpy.context.selected_objects:
                if obj.type not in ['CAMERA', 'LAMP', 'SPEAKER']:
                    _sro_.append(obj)

        # RENDER AND SPOOL LAYOUT
        # #####################################################################
        col = layout.column(align=True)
        row = col.row(align=True)

        opr = "render.render"
        txt = "Render"
        iid = icons.iconid("render")
        sub = row.row(align=True)
        sub.enabled = True if bpy.context.scene.camera else False
        sub.operator(opr, text=txt, icon_value=iid)
        iid = icons.iconid("batch_render")
        row.operator("render.render", text="", icon_value=iid).animation = True

        prp = "rm_render"
        icn = 'TRIA_DOWN' if scn.rm_render else 'TRIA_RIGHT'
        row.prop(scn, prp, icon_only=True, icon=icn)

        # render ui open?
        if scn.rm_render:
            box = col.box().box()

            row = box.row()
            prp = "render_into"
            row.prop(rmn, prp, text="")

            sub = row.row(align=True)
            sub.scale_x = 2.0
            iid = icons.toggle("dnoise", rmn.do_denoise)
            sub.prop(rmn, "do_denoise", text="", icon_value=iid)

            # box.separator()

            # Render Presets
            row = box.row()
            #
            # TODO:   Add naming the menu to the selected preset
            #         be aware of changes and name to 'unnamed' then!
            # DATE:   2018-02-09
            # AUTHOR: Timm Wimmers
            # STATUS: -unassigned-
            #
            txt = bpy.types.rfb_mt_render_presets.bl_label
            row.menu("rfb_mt_render_presets", text=txt)

            sub = row.row(align=True)
            #
            # renderable objects selected?
            #
            sub.active = True if _sro_ else False
            sub.scale_x = 2.0
            prp = "render_selected_objects_only"
            iid = icons.toggle("selected", rmn.render_selected_objects_only)
            sub.prop(rmn, prp, icon_only=True, icon_value=iid)
            #
            # Spool Action | External | Animation
            # A bit more complicated sublayouts 'cause of complex states
            #
            row = box.row()
            sb1 = row.row()
            sb1.enabled = rmn.enable_external_rendering

            sb2 = sb1.row()
            sb2.enabled = True if bpy.context.scene.camera else False

            opr = "rfb.file_spool_render"
            txt = "Spool Animation" if rmn.external_animation else "Spool Frame"
            sb2.operator(opr, text=txt)

            # Toggle: External?
            sb2 = row.row(align=True)
            prp = "enable_external_rendering"
            iid = icons.toggle('spool', rmn.enable_external_rendering)
            sb2.prop(rmn, prp, icon_only=True, icon_value=iid)

            # Toggle: Animation?
            sb3 = sb2.row(align=True)
            sb3.active = rmn.enable_external_rendering
            prp = "external_animation"
            iid = icons.toggle("animation", rmn.external_animation)
            sb3.prop(rmn, prp, icon_only=True, icon_value=iid)

            # DisplayDriver | Denoise? | Selected only?
            row = box.row()
            row.active = rmn.enable_external_rendering

            sb1 = row.row(align=True)
            prp = "display_driver"
            sb1.prop(rmn, prp, text="")

            # Denoise
            sb1 = row.row(align=True)
            sb1.active = rmn.enable_external_rendering

            prp = "external_denoise"
            iid = icons.toggle("dnoise", rmn.external_denoise)
            sb1.prop(rmn, prp, icon_only=True, icon_value=iid)

            sb2 = sb1.row(align=True)
            sb2.active = rmn.external_animation and rmn.external_denoise
            prp = "crossframe_denoise"
            iid = icons.toggle("crossdn", rmn.crossframe_denoise)
            sb2.prop(rmn, prp, icon_only=True, icon_value=iid)

            _a_ = rmn.external_animation
            _b_ = rmn.enable_external_rendering
            row = box.row()
            row.active = _a_ and _b_

            sub = row.row(align=True)
            sub.prop(scn, "frame_start", text="Start")
            sub.prop(scn, "frame_end", text="End")

            sub = row.row(align=True)
            sub.scale_x = 2.0
            sub.label(text="", icon='BLANK1')
            #
            # ui open - slightly more space on root layout
            #
            layout.separator()

        # IPR LAYOUT
        # #####################################################################
        col = layout.column(align=True)
        row = col.row(align=True)
        icn = 'TRIA_DOWN' if scn.rm_ipr else 'TRIA_RIGHT'

        # Header: Stop IPR, it's running
        if engine.ipr:
            iid = icons.iconid("stop_ipr")
            row.operator('rfb.tool_ipr', text="Stop IPR", icon_value=iid)

            iid = icons.iconid("start_it")
            row.operator("rfb.tool_it", text="", icon_value=iid)
            row.prop(scn, "rm_ipr", icon_only=True, icon=icn)

        # Header: Start IPR isn't running
        else:
            iid = icons.iconid("start_ipr")
            sub = row.row(align=True)
            sub.enabled = True if bpy.context.scene.camera else False
            sub.operator('rfb.tool_ipr', text="Start IPR", icon_value=iid)

            iid = icons.iconid("start_it")
            row.operator("rfb.tool_it", text="", icon_value=iid)
            row.prop(scn, "rm_ipr", icon_only=True, icon=icn)

        # ui open?
        if scn.rm_ipr:
            sub = col.box().box()

            # Interactive and Preview Sampling
            row = sub.row(align=True)
            row.prop(rmn, "preview_pixel_variance")

            row = sub.row(align=True)
            row.prop(rmn, "preview_min_samples", text="Min. Sampl.")
            row.prop(rmn, "preview_max_samples", text="Max. Sampl.")

            row = sub.row(align=True)
            row.prop(rmn, "preview_max_specular_depth", text="Spec. Depth")
            row.prop(rmn, "preview_max_diffuse_depth", text="Diff. Depth")

            # only when ui is open: slightly more space on root layout after
            # the frames
            layout.separator()

        # CAMERA LAYOUT
        # #####################################################################
        layout.separator()
        col = layout.column(align=True)
        row = col.row(align=True)

        _c_ = False
        try:
            txt = bpy.data.scenes[scn.name].camera.name
            _c_ = True
        except AttributeError:
            txt = "No camera!"
        if _c_:
            row.menu("rfb_mt_scene_cameras", text=txt, icon_value=self.cid)
        else:
            row.menu("rfb_mt_scene_cameras", text=txt, icon_value=self.eid)

        row.operator("rfb.object_add_camera", text="", icon='ZOOMIN')
        icn = 'TRIA_DOWN' if scn.prm_cam else 'TRIA_RIGHT'
        row.prop(scn, "prm_cam", text="", icon=icn)

        # ui open?
        if scn.prm_cam:
            sub = col.box().box()

            obj = bpy.context.object
            if obj and obj.type == 'CAMERA':
                row = sub.row()

                #
                # camera tools
                #
                sb1 = row.row(align=True)
                sb2 = sb1.row(align=True)
                sb2.enabled = obj.is_visible(scn)

                opr = "rfb.object_delete_camera"
                sb2.operator(opr, text="", icon='ZOOMOUT')
                cam = bpy.data.scenes[scn.name].camera
                sb1.prop(cam, "name", text="")

                opr = "rfb.view_numpad0"
                view = context.space_data.region_3d.view_perspective
                if view == 'CAMERA':
                    sb1.operator(opr, text="", icon='VIEW3D')
                else:
                    iid = icons.iconid('camview_on')
                    sb1.operator(opr, text="", icon_value=iid)

                view = context.space_data
                iid = icons.toggle('camlock', view.lock_camera)
                sb1.prop(view, "lock_camera", text="", icon_value=iid)

                #
                # depth of field
                #
                row = sub.row(align=True)
                opr = "rfb.camera_aperture_type"
                val = context.object.data.cycles.aperture_type
                iid = icons.iconid('shutter_off') \
                    if val == 'FSTOP' \
                    else icons.iconid('radius')
                row.operator(opr, text="", icon_value=iid)

                prp = "dof_object"
                row.prop(context.object.data, prp, icon_only=True)

                if not context.object.data.dof_object:
                    prp = "dof_distance"
                    row.prop(context.object.data, prp, text="Dist.")
            else:
                objs = bpy.context.scene.objects
                cams = [obj for obj in objs if obj.type == "CAMERA"]
                if cams:
                    #
                    # if an active camera was deleted before make [0] active
                    #
                    if not hasattr(bpy.data.scenes[scn.name].camera, "name"):
                        bpy.data.scenes[scn.name].camera = cams[0]

                    sub.label("")  # keep opened ui same size (no juming)
                    opr = "rfb.object_select_active_camera"
                    icn = "RESTRICT_SELECT_OFF"
                    txt = "Select"
                    sub.operator(opr, text=txt, icon=icn)
                else:
                    #
                    # Scene contains no camera!
                    #
                    sub.label("Render globally disabled!", icon='ERROR')
                    sub.label("")  # keep opened ui same size (no juming)

        # #####################################################################
        # CREATE ENVIRONMENT LIGHT LAYOUT
        #
        iid = icons.iconid('envlight')
        col = layout.column(align=True)
        row = col.row(align=True)

        hemi = False
        objs = bpy.context.scene.objects
        for lamp in [obj for obj in objs if obj.type == "LAMP"]:
            if lamp.data.type == 'HEMI':
                hemi = True
                break  # leave early, scene contains at least one area light
        if hemi:
            row.menu("rfb_mt_scene_lightshemi", icon_value=iid)
        else:
            txt = "No EnvLight"
            row.menu("rfb_mt_scene_lightshemi", text=txt, icon_value=iid)

        row.operator("rfb.object_add_light_hemi", text="", icon='ZOOMIN')

        icn = 'TRIA_DOWN' if scn.rm_env else 'TRIA_RIGHT'
        row.prop(scn, "rm_env", icon_only=True, icon=icn)

        #
        # UI open?
        #
        if scn.rm_env:
            sub = col.box().box()
            row = sub.row(align=True)

            obj = bpy.context.object
            if obj and obj.type == 'LAMP' and obj.data.type == 'HEMI':

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
                row.label("No EnvLight Selected.", icon='INFO')
                sub.label("")  # keep opened ui same size (no juming)

        # CREATE AREA LIGHT LAYOUT
        # #####################################################################
        iid = icons.iconid("arealight")
        col = layout.column(align=True)
        row = col.row(align=True)

        area = False
        objs = bpy.context.scene.objects
        for lamp in [obj for obj in objs if obj.type == "LAMP"]:
            if lamp.data.type == 'AREA':
                area = True
                break  # leave early, scene contains at least one area light
        if area:
            row.menu("rfb_mt_scene_lightsarea", icon_value=iid)
        else:
            txt = "No AreaLight"
            row.menu("rfb_mt_scene_lightsarea", text=txt, icon_value=iid)

        opr = "rfb.object_add_light_area"
        row.operator(opr, text="", icon="ZOOMIN")

        icn = 'TRIA_DOWN' if scn.rm_area else 'TRIA_RIGHT'
        row.prop(scn, "rm_area", icon_only=True, icon=icn)

        #
        # UI open?
        #
        if scn.rm_area:
            sub = col.box().box()
            row = sub.row(align=True)

            obj = bpy.context.object
            if obj and obj.type == 'LAMP' and obj.data.type == 'AREA':
                row.prop(obj, "name", text="", icon_value=iid)
                row.prop(obj, "hide", icon_only=True)
                icn = 'RESTRICT_RENDER_OFF'
                row.prop(obj, "hide_render", icon_only=True, icon=icn)
                icn = 'PANEL_CLOSE'
                row.operator("rfb.object_delete_light", text="", icon=icn)
            else:
                row.label("No AreaLight Selected.", icon='INFO')
                # sub.separator()  # keep opened ui same size (no juming ui)

        # CREATE DAYLIGHT LIGHT LAYOUT
        # #####################################################################
        iid = icons.iconid('sunlight')
        col = layout.column(align=True)
        row = col.row(align=True)

        sun = False
        objs = bpy.context.scene.objects
        for lamp in [obj for obj in objs if obj.type == "LAMP"]:
            if lamp.data.type == 'SUN':
                sun = True
                break  # leave early, scene contains at least one area light

        if sun:
            row.menu("rfb_mt_scene_lightsday", icon_value=iid)
        else:
            txt = "No Sun"
            row.menu("rfb_mt_scene_lightsday", text=txt, icon_value=iid)

        opr = "rfb.object_add_light_day"
        row.operator(opr, text="", icon='ZOOMIN')

        icn = 'TRIA_DOWN' if scn.rm_daylight else 'TRIA_RIGHT'
        row.prop(scn, "rm_daylight", icon_only=True, icon=icn)

        if scn.rm_daylight:
            sub = col.box().box()
            row = sub.row(align=True)

            obj = bpy.context.object
            if obj and obj.type == 'LAMP' and obj.data.type == 'SUN':

                row.prop(obj, "name", text="", icon_value=iid)
                row.prop(obj, "hide", icon_only=True)

                prp = "hide_render"
                icn = 'RESTRICT_RENDER_OFF'
                row.prop(obj, prp, icon_only=True, icon=icn)

                opr = "rfb.object_delete_light"
                icn = 'PANEL_CLOSE'
                row.operator(opr, text="", icon=icn)
            else:
                row.label("No DayLight selected.", icon='INFO')
                # sub.separator()  # keep opened ui same size (no juming ui)

        # SELECTED OBJECTS - SUPPORT - OPEN LAST RIB
        # #####################################################################
        #
        # selected renderable objects
        #
        if _sro_:
            layout.separator()
            col = layout.column(align=True)

            #
            # Create new material
            #
            opr = "rfb.material_add_bxdf"
            txt = "Add New Material"
            icn = 'MATERIAL'
            col.operator_menu_enum(opr, 'bxdf_name', text=txt, icon=icn)

            #
            # Make object emissive
            #
            opr = "rfb.object_make_emissive"
            txt = "Make Emissive"
            iid = icons.iconid("make_emissive")
            col.operator(opr, text=txt, icon_value=iid)

            #
            # Add sb1div scheme
            #
            opr = "rfb.object_enable_subdiv"
            txt = "Make Subdiv"
            iid = icons.iconid("make_subdiv")
            col.operator(opr, text=txt, icon_value=iid)

            #
            # Export object as RIB archive
            #
            opr = "rfb.object_export_rib"
            txt = "Export RIB Archive"
            iid = icons.iconid("archive_rib")
            col.operator(opr, text=txt, icon_value=iid)

        #
        # support
        #
        layout.separator()
        col = layout.column(align=True)
        iid = icons.iconid("web")  # used twice

        #
        # RenderMan Doc (online)
        #
        opr = "wm.url_open"
        txt = "RenderMan Docs"
        url = ("https://github.com/prman-pixar/"
               "RenderManForBlender/wiki/Documentation-Home")
        col.operator(opr, text=txt, icon_value=iid).url = url

        #
        # RenderMan What's new (online)
        #
        opr = "wm.url_open"
        txt = "About RenderMan"
        url = "https://renderman.pixar.com/whats-new"
        col.operator(opr, text=txt, icon_value=iid).url = url

        #
        # Open last RIB // Developer Stub Operator (if enabled)
        #
        layout.separator()
        col = layout.column(align=True)
        #
        # FIXME:  lost "examples" by accident, will fix this later
        # DATE:   2018-02-06
        # AUTHOR: Timm Wimmers
        # STATUS: assidned to self, 2018-02-06
        #
        # iid = icons.iconid("prman")
        # layout.menu("rfb_mt_example_files", icon_value=iid)

        #
        # open last rib, only enabled if not binary
        # (like ASCII and not compressed file format)
        #
        if rmn.rib_format == 'ascii'and rmn.rib_compression == 'none':
            opr = "rfb.file_open_last_rib"
            iid = icons.iconid("open_rib")
            col.operator(opr, icon_value=iid)

        if pref('rfb_stub_operator'):
            opr = 'rfb.stub_devel_operator'
            iid = icons.iconid("open_rib")
            col.operator(opr, icon_value=iid)
