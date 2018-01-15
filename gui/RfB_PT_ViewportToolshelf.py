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
from .. import rt
from .. import engine

from . RfB_PT_RootPanelIcon import RfB_PT_RootPanelIcon
from . RfB_MT_RenderPresets import RfB_MT_RenderPresets


class RfB_PT_ViewportToolshelf(RfB_PT_RootPanelIcon, Panel):
    # class Renderman_UI_Panel(bpy.types.Panel, RfB_PT_RootPanelIcon):
    bl_idname = "renderman_ui_panel"
    bl_label = "RenderMan"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = rt.reg.get('BL_CATEGORY')

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return rd.engine == 'PRMAN_RENDER'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rm = scene.renderman

        # #
        # # [Save Scene] Button
        # #
        # layout.operator("wm.save_mainfile", text="Save Scene", icon='FILE_TICK')

        # layout.separator()
        # layout.separator()

        if scene.render.engine != "PRMAN_RENDER":
            return

        # ######################################################################
        # RENDER LAYOUT
        # ----------------------------------------------------------------------
        cl = layout.column(align=True)

        #
        # [Render] Button with TRIA
        #
        row = cl.row(align=True)

        iid = icons.iconid("render")
        row.operator("render.render", text="Render", icon_value=iid)

        icon = 'TRIA_DOWN' if context.scene.rm_render else 'TRIA_RIGHT'
        row.prop(context.scene, "rm_render", text="", icon=icon)

        if scene.rm_render:
            #
            # [Render] - Sublayout is open.
            #
            box = cl.box()
            # box.separator()  # slightly more space
            #
            # [Render Animation]
            #
            iid = icons.iconid("batch_render")
            row = box.row(align=True)
            row.operator("render.render", text="Render Animation",
                         icon_value=iid).animation = True

            #
            # [Display Driver] [Denoise] [Selected]
            #
            row = box.row(align=True)
            row.prop(rm, "render_into", text="")

            iid = (icons.iconid("dnoise_on")
                   if rm.do_denoise
                   else icons.iconid("dnoise_off"))
            row.prop(rm, "do_denoise",
                     text="",
                     icon_value=iid)

            iid = (icons.iconid("selected_on")
                   if rm.render_selected_objects_only
                   else icons.iconid("selected_off"))
            row.prop(rm, "render_selected_objects_only",
                     text="",
                     icon_value=iid)

            #
            # [RenderMan Presets]
            #
            row = box.row(align=True)
            row.menu("RfB_MT_render_presets")

            row.operator("rfb.render_add_preset", text="",
                         icon='ZOOMIN')

            row.operator("rfb.render_add_preset", text="",
                         icon='ZOOMOUT').remove_active = True
            # ### Renderman Presets ####

            # rd = scene.render ### ???? ####
            # #Resolution
            # row = box.row(align=True)
            # sub = row.column(align=True)
            # sub.label(text="Resolution:")
            # sub.prop(rd, "resolution_x", text="X")
            # sub.prop(rd, "resolution_y", text="Y")
            # sub.prop(rd, "resolution_percentage", text="")

            # # layout.prop(rm, "display_driver")
            # #Sampling
            # row = box.row(align=True)
            # row.label(text="Sampling:")
            # row = box.row(align=True)
            # col = row.column()
            # col.prop(rm, "pixel_variance")
            # row = col.row(align=True)
            # row.prop(rm, "min_samples", text="Min Samples")
            # row.prop(rm, "max_samples", text="Max Samples")
            # row = col.row(align=True)
            # row.prop(rm, "max_specular_depth", text="Specular Depth")
            # row.prop(rm, "max_diffuse_depth", text="Diffuse Depth")
            #
        # ----------------------------------------------------------------------
        # END RENDER LAYOUT
        # ######################################################################

        # ######################################################################
        # EXTERNAL RENDER LAYOUT
        # ----------------------------------------------------------------------
        cl = layout.column(align=True)
        row = cl.row(align=True)

        # if scene.renderman.enable_external_rendering:
        iid = icons.iconid("render_spool")
        row.operator("rfb.file_spool_render",
                     text="External Render",
                     icon_value=iid)

        icon = 'TRIA_DOWN' if scene.rm_render_external else 'TRIA_RIGHT'
        row.prop(context.scene,
                 "rm_render_external", text="",
                 icon=icon)

        if scene.rm_render_external:
            #
            # Layout is open
            #
            box = cl.box()
            # box.separator()  # slightly more space

            row = box.row(align=True)

            #
            # [Display Driver] [Denoise] [Crossframe] [Selected only]
            #

            row.prop(rm, "display_driver", text="")

            #
            # Denoise (simple)
            #
            iid = (icons.iconid("dnoise_on")
                   if rm.external_denoise
                   else icons.iconid("dnoise_off"))
            row.prop(rm, "external_denoise",
                     text="",
                     icon_value=iid)
            #
            # Cross Denoise
            #
            sub = row.row(align=True)
            sub.enabled = rm.external_denoise and rm.external_animation
            iid = (icons.iconid("crossdn_on")
                   if rm.crossframe_denoise
                   else icons.iconid("crossdn_off"))
            sub.prop(rm, "crossframe_denoise",
                     text="",
                     icon_value=iid)
            #
            # Selected Objects only
            #
            iid = (icons.iconid("selected_on")
                   if rm.render_selected_objects_only
                   else icons.iconid("selected_off"))
            row.prop(rm, "render_selected_objects_only",
                     text="",
                     icon_value=iid)
            #
            # Animation
            #
            iid = (icons.iconid("animation_on")
                   if rm.external_animation
                   else icons.iconid("animation_on"))

            row = box.row(align=True)

            sub = row.row(align=True)
            sub.enabled = rm.external_animation
            sub.prop(scene, "frame_start", text="Start")
            sub.prop(scene, "frame_end", text="End")

            row.prop(rm, "external_animation",
                     text="",
                     icon_value=iid)
            #
            # Presets Menu
            #
            row = box.row(align=True)
            row.menu("RfB_MT_render_presets", text=bpy.types.RfB_MT_render_presets.bl_label)

            #
            # spool render
            #
            # FIXME: property not found
            # row = box.row(align=True)
            # row.prop(rm, "external_action", text='')
            # col = row.column()
            # col.enabled = rm.external_action == 'spool'
            # col.prop(rm, "queuing_system", text='')
        # ----------------------------------------------------------------------
        # EXTERNAL RENDER LAYOUT END
        # ######################################################################

        # ######################################################################
        # IPR LAYOUT
        # ----------------------------------------------------------------------
        cl = layout.column(align=True)

        if engine.ipr:
            #
            # [Stop IPR} it's running
            #
            row = cl.row(align=True)
            iid = icons.iconid("stop_ipr")
            row.operator('rfb.tool_ipr',
                         text="Stop IPR", icon_value=iid)
            row.prop(context.scene, "rm_ipr", text="",
                     icon='TRIA_DOWN' if context.scene.rm_ipr else 'TRIA_RIGHT')

            if scene.rm_ipr:

                # scene = context.scene
                # rm = scene.renderman

                box = cl.box()
                row = box.row(align=True)

                col = row.column()
                col.prop(rm, "preview_pixel_variance")
                row = col.row(align=True)
                row.prop(rm, "preview_min_samples", text="Min Samples")
                row.prop(rm, "preview_max_samples", text="Max Samples")
                row = col.row(align=True)
                row.prop(rm, "preview_max_specular_depth",
                         text="Specular Depth")
                row.prop(rm, "preview_max_diffuse_depth", text="Diffuse Depth")
                row = col.row(align=True)

        else:
            #
            # [Start IPR] it's not running
            #
            row = cl.row(align=True)
            iid = icons.iconid("start_ipr")
            row.operator('rfb.tool_ipr', text="Start IPR",
                         icon_value=iid)

            row.prop(context.scene, "rm_ipr", text="",
                     icon='TRIA_DOWN' if context.scene.rm_ipr else 'TRIA_RIGHT')

            if scene.rm_ipr:
                #
                # [Start IT] (in sublayout)
                #
                box = cl.box()
                iid = icons.iconid("start_it")
                # box.separator()  # slightly more space

                box.operator("rfb.tool_it",
                             text="Start · Focus IT",
                             icon_value=iid)
                #
                # Interactive and Preview Sampling
                #
                row = box.row(align=True)
                col = row.column()
                col.prop(rm, "preview_pixel_variance")

                row = col.row(align=True)
                row.prop(rm, "preview_min_samples", text="Min. Samples")
                row.prop(rm, "preview_max_samples", text="Max. Samples")

                row = col.row(align=True)
                row.prop(rm, "preview_max_specular_depth",
                         text="Specular Depth")

                row.prop(rm, "preview_max_diffuse_depth", text="Diffuse Depth")
        # ----------------------------------------------------------------------
        # END IPR LAYOUT
        # ######################################################################

        # ######################################################################
        # CREATE CAMERA LAYOUT
        # ----------------------------------------------------------------------
        cl = layout.column(align=True)
        row = cl.row(align=True)
        iid = icons.iconid("camera")
        row.operator("rfb.object_add_camera",
                     text="Add Camera", icon_value=iid)

        row.prop(context.scene, "prm_cam", text="",
                 icon='TRIA_DOWN' if context.scene.prm_cam else 'TRIA_RIGHT')

        if context.scene.prm_cam:
            ob = bpy.context.object
            box = cl.box()
            row = box.row(align=True)
            row.menu("RfB_MT_scene_cameras",
                     text="Camera List", icon_value=iid)

            if ob.type == 'CAMERA':

                row = box.row(align=True)
                row.prop(ob, "name", text="", icon_value=iid)
                row.prop(ob, "hide", text="")
                row.prop(ob, "hide_render",
                         icon='RESTRICT_RENDER_OFF', text="")
                row.operator("rfb.object_delete_camera",
                             text="", icon='PANEL_CLOSE')

                row = box.row(align=True)
                row.scale_x = 2
                row.operator("view3d.object_as_camera", text="", icon='CURSOR')

                row.scale_x = 2
                row.operator("view3d.viewnumpad", text="",
                             icon='VISIBLE_IPO_ON').type = 'CAMERA'

                if not context.space_data.lock_camera:
                    row.scale_x = 2
                    row.operator("wm.context_toggle", text="",
                                 icon='UNLOCKED').data_path = "space_data.lock_camera"
                elif context.space_data.lock_camera:
                    row.scale_x = 2
                    row.operator("wm.context_toggle", text="",
                                 icon='LOCKED').data_path = "space_data.lock_camera"

                row.scale_x = 2
                row.operator("view3d.camera_to_view",
                             text="", icon='MAN_TRANS')

                row = box.row(align=True)
                row.label("Depth Of Field :")

                row = box.row(align=True)
                row.prop(context.object.data, "dof_object", text="")
                row.prop(context.object.data.cycles, "aperture_type", text="")

                row = box.row(align=True)
                row.prop(context.object.data, "dof_distance", text="Distance")

            else:
                box.label("No Camera Selected")
        # ----------------------------------------------------------------------
        # CREATE CAMERA LAYOUT END
        # ######################################################################

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
                row.menu("RfB_MT_scene_hemilights",
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
                    row.label("No EnvLight Selected")

        # ----------------------------------------------------------------------
        # CREATE ENVIRONMENT LIGHT LAYOUT END
        # ######################################################################

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
                row.menu("RfB_MT_scene_arealights",
                         text="Area Light List", icon_value=iid)

                if ob.type == 'LAMP' and ob.data.type == 'AREA':

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
                row.menu("RfB_MT_scene_daylights",
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
