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

# python imports
import os
import math

# blender imports
import bpy
import blf

from bpy.types import Panel

from bpy.props import PointerProperty
from bpy.props import StringProperty
from bpy.props import BoolProperty
from bpy.props import EnumProperty
from bpy.props import IntProperty
from bpy.props import FloatProperty
from bpy.props import FloatVectorProperty
from bpy.props import CollectionProperty

# global dictionaries
from bl_ui.properties_particle import ParticleButtonsPanel

narrowui = 180  # still used??

#
# RenderMan for Blender imports
#
from . import rt
from . import engine

from . nodes import NODE_LAYOUT_SPLIT
from . nodes import panel_node_draw
from . nodes import is_renderman_nodetree

# helper functions for parameters
from . nodes import draw_nodes_properties_ui
from . nodes import draw_node_properties_recursive


from . ops import RfB_OT_FileOpenLastRIB
from . ops import RfB_OT_FileViewStats
from . ops import RfB_OT_ItemToggleLightlink
from . ops import RfB_OT_NodeBakePatterns
from . ops import RfB_OT_ObjectExportRIB
from . ops import RfB_OT_ToolStartIPR
from . ops import RfB_OT_ToolStartIT

from . gui import icons
from . gui import draw_props

# RenderControls in header area
from . gui import RfB_HT_RenderUiImage
from . gui import RfB_HT_RenderUiInfo
from . gui import RfB_HT_RenderUiNode
from . gui import RfB_HT_RenderUiView3D

# populating menus
from . gui import RfB_MT_RenderPresets
from . gui import RfB_MT_SceneAreaLights
from . gui import RfB_MT_SceneCameras
from . gui import RfB_MT_SceneDaylights
from . gui import RfB_MT_SceneHemiLights

# layout utils
from . gui.utils import split_lr  # |:left---|---right:|
from . gui.utils import split_ll  # |:left---|:left----|

# Panels
from . gui.RfB_PT_RootPanel import RfB_PT_RootPanel
from . gui.RfB_PT_RootPanelIcon import RfB_PT_RootPanelIcon
from . gui.RfB_PT_PropsRenderRender import RfB_PT_PropsRenderRender
from . gui.RfB_PT_PropsRenderBaking import RfB_PT_PropsRenderBaking
from . gui.RfB_PT_Collection import RfB_PT_Collection
from . gui.RfB_PT_PropsRenderExternal import RfB_PT_PropsRenderExternal
from . gui.RfB_PT_ViewportToolshelf import RfB_PT_ViewportToolshelf
from . gui.RfB_PT_PropsRenderSampling import RfB_PT_PropsRenderSampling
from . gui.RfB_PT_PropsRenderMotionBlur import RfB_PT_PropsRenderMotionBlur
from . gui.RfB_PT_PropsRenderSamplingPreview import RfB_PT_PropsRenderSamplingPreview
from . gui.RfB_PT_PropsRenderAdvanced import RfB_PT_PropsRenderAdvanced
from . gui.RfB_PT_PropsMeshPrimvars import RfB_PT_PropsMeshPrimvars
from . gui.RfB_PT_PropsMaterialPreview import RfB_PT_PropsMaterialPreview
from . gui.RfB_PT_PropsObjectGeometry import RfB_PT_PropsObjectGeometry
from . gui.RfB_PT_PropsLayerRenderPasses import RfB_PT_PropsLayerRenderPasses
from . gui.RfB_PT_PropsSceneLigthGroups import RfB_PT_PropsSceneLigthGroups
from . gui.RfB_PT_PropsSceneLightLinking import RfB_PT_PropsSceneLightLinking
from . gui.RfB_PT_PropsSceneObjectGroups import RfB_PT_PropsSceneObjectGroups
from . gui.RfB_PT_PropsParticleRender import RfB_PT_PropsParticleRender
from . gui.RfB_PT_PropsObjectRaytracing import RfB_PT_PropsObjectRaytracing
from . gui.RfB_PT_PropsObjectShadingVisibility import RfB_PT_PropsObjectShadingVisibility
from . gui.RfB_UL_LightLinkingObjects import RfB_UL_LightLinkingObjects
from . gui.RfB_UL_LightLinkingLights import RfB_UL_LightLinkingLights
from . gui.RfB_UL_ObjectGroup import RfB_UL_ObjectGroup
from . gui.RfB_PT_PropsLayerOptions import RfB_PT_PropsLayerOptions


class ShaderNodePanel(RfB_PT_RootPanelIcon):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_label = 'Node Panel'

    bl_context = ""
    COMPAT_ENGINES = {'PRMAN_RENDER'}

    @classmethod
    def poll(cls, context):
        if context.scene.render.engine not in cls.COMPAT_ENGINES:
            return False
        if cls.bl_context == 'material':
            if context.material and context.material.node_tree != '':
                return True
        if cls.bl_context == 'data':
            if not context.lamp:
                return False
            if context.lamp.renderman.use_renderman_node:
                return True
        return False


class ShaderPanel(RfB_PT_RootPanel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    COMPAT_ENGINES = {'PRMAN_RENDER'}

    shader_type = 'surface'
    param_exclude = {}

    @classmethod
    def poll(cls, context):
        rd = context.scene.render

        if cls.bl_context == 'data' and cls.shader_type == 'light':
            return (hasattr(context, "lamp") and context.lamp is not None and rd.engine in {'PRMAN_RENDER'})
        elif cls.bl_context == 'world':
            return (hasattr(context, "world") and context.world is not None and
                    rd.engine in {'PRMAN_RENDER'})
        elif cls.bl_context == 'material':
            return (hasattr(context, "material") and context.material is not None and
                    rd.engine in {'PRMAN_RENDER'})


class MATERIAL_PT_renderman_shader_surface(ShaderPanel, Panel):
    bl_context = "material"
    bl_label = "Bxdf"
    shader_type = 'Bxdf'

    def draw(self, context):
        mat = context.material
        layout = self.layout
        if context.material.renderman and context.material.node_tree:
            nt = context.material.node_tree

            if is_renderman_nodetree(mat):
                panel_node_draw(layout, context, mat,
                                'RendermanOutputNode', 'Bxdf')
                # draw_nodes_properties_ui(
                #    self.layout, context, nt, input_name=self.shader_type)
            else:
                if not panel_node_draw(layout, context, mat, 'ShaderNodeOutputMaterial', 'Surface'):
                    layout.prop(mat, "diffuse_color")
            layout.separator()

        else:
            # if no nodetree we use pxrdisney
            mat = context.material
            rm = mat.renderman

            row = layout.row()
            row.prop(mat, "diffuse_color")

            layout.separator()
        if mat and not is_renderman_nodetree(mat):
            layout.operator(
                'rfb.node_add_nodetree').idtype = "material"
            layout.operator('rfb.node_cycles_convertall')
        # self._draw_shader_menu_params(layout, context, rm)


class MATERIAL_PT_renderman_shader_light(ShaderPanel, Panel):
    bl_context = "material"
    bl_label = "Light Emission"
    shader_type = 'Light'

    def draw(self, context):
        if context.material.node_tree:
            nt = context.material.node_tree
            draw_nodes_properties_ui(
                self.layout, context, nt, input_name=self.shader_type)


class MATERIAL_PT_renderman_shader_displacement(ShaderPanel, Panel):
    bl_context = "material"
    bl_label = "Displacement"
    shader_type = 'Displacement'

    def draw(self, context):
        if context.material.node_tree:
            nt = context.material.node_tree
            draw_nodes_properties_ui(
                self.layout, context, nt, input_name=self.shader_type)
            # BBM addition begin
        row = self.layout.row()
        row.prop(context.material.renderman, "displacementbound")
        # BBM addition end
        # self._draw_shader_menu_params(layout, context, rm)


class DATA_PT_renderman_camera(ShaderPanel, Panel):
    bl_context = "data"
    bl_label = "RenderMan Camera"

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        if not context.camera:
            return False
        return rd.engine == 'PRMAN_RENDER'

    def draw(self, context):
        layout = self.layout
        cam = context.camera
        scene = context.scene
        dof_options = cam.gpu_dof

        row = layout.row()
        row.prop(scene.renderman, "depth_of_field")
        sub = row.row()
        sub.enabled = scene.renderman.depth_of_field
        sub.prop(cam.renderman, "fstop")

        split = layout.split()

        col = split.column()

        col.label(text="Focus:")
        col.prop(cam, "dof_object", text="")
        sub = col.column()
        sub.active = (cam.dof_object is None)
        sub.prop(cam, "dof_distance", text="Distance")

        col = split.column()
        sub = col.column(align=True)
        sub.label("Aperture Controls:")
        sub.prop(cam.renderman, "dof_aspect", text="Aspect")
        sub.prop(cam.renderman, "aperture_sides", text="Sides")
        sub.prop(cam.renderman, "aperture_angle", text="Angle")
        sub.prop(cam.renderman, "aperture_roundness", text="Roundness")
        sub.prop(cam.renderman, "aperture_density", text="Density")

        layout.prop(cam.renderman, "projection_type")
        if cam.renderman.projection_type != 'none':
            projection_node = cam.renderman.get_projection_node()
            draw_props(projection_node, projection_node.prop_names, layout)


class DATA_PT_renderman_world(ShaderPanel, Panel):
    bl_context = "world"
    bl_label = "World"
    shader_type = 'world'

    def draw(self, context):
        layout = self.layout
        world = context.scene.world

        if not world.renderman.use_renderman_node:
            layout.prop(world, "horizon_color")
            layout.operator('rfb.node_add_nodetree').idtype = 'world'
            return
        else:
            layout.prop(world.renderman, "renderman_type", expand=True)
            if world.renderman.renderman_type == 'NONE':
                return
            layout.prop(world.renderman, 'light_primary_visibility')
            lamp_node = world.renderman.get_light_node()
            if lamp_node:
                draw_props(lamp_node, lamp_node.prop_names, layout)


class DATA_PT_renderman_lamp(ShaderPanel, Panel):
    bl_context = "data"
    bl_label = "Lamp"
    shader_type = 'light'

    def draw(self, context):
        layout = self.layout

        lamp = context.lamp
        ipr_running = engine.ipr != None
        if not lamp.renderman.use_renderman_node:
            layout.prop(lamp, "type", expand=True)
            layout.operator('rfb.node_add_nodetree').idtype = 'lamp'
            layout.operator('rfb.node_cycles_convertall')
            return
        else:
            if ipr_running:
                layout.label(
                    "Note: Some items cannot be edited while IPR running.")
            row = layout.row()
            row.enabled = not ipr_running
            row.prop(lamp.renderman, "renderman_type", expand=True)
            if lamp.renderman.renderman_type == 'FILTER':
                row = layout.row()
                row.enabled = not ipr_running
                row.prop(lamp.renderman, "filter_type", expand=True)
            if lamp.renderman.renderman_type == "AREA":
                row = layout.row()
                row.enabled = not ipr_running
                row.prop(lamp.renderman, "area_shape", expand=True)
                row = layout.row()
                if lamp.renderman.area_shape == "rect":
                    row.prop(lamp, 'size', text="Size X")
                    row.prop(lamp, 'size_y')
                else:
                    row.prop(lamp, 'size', text="Diameter")
            # layout.prop(lamp.renderman, "shadingrate")

        # layout.prop_search(lamp.renderman, "nodetree", bpy.data, "node_groups")
        row = layout.row()
        row.enabled = not ipr_running
        row.prop(lamp.renderman, 'illuminates_by_default')


class DATA_PT_renderman_node_shader_lamp(ShaderNodePanel, Panel):
    bl_label = "Light Shader"
    bl_context = 'data'

    def draw(self, context):
        layout = self.layout
        lamp = context.lamp

        lamp_node = lamp.renderman.get_light_node()
        if lamp_node:
            if lamp.renderman.renderman_type != 'FILTER':
                layout.prop(lamp.renderman, 'light_primary_visibility')
            draw_props(lamp_node, lamp_node.prop_names, layout)


class DATA_PT_renderman_display_filters(RfB_PT_Collection, Panel):
    bl_label = "Display Filters"
    bl_context = 'scene'

    def draw_item(self, layout, context, item):
        layout.prop(item, 'filter_type')
        layout.separator()
        filter_node = item.get_filter_node()
        draw_props(filter_node, filter_node.prop_names, layout)

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return rd.engine == 'PRMAN_RENDER'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rm = scene.renderman

        self._draw_collection(context, layout, rm, "Display Filters:",
                              "rfb.collection_toggle_path", "scene", "display_filters",
                              "display_filters_index")


class DATA_PT_renderman_Sample_filters(RfB_PT_Collection, Panel):
    bl_label = "Sample Filters"
    bl_context = 'scene'

    def draw_item(self, layout, context, item):
        layout.prop(item, 'filter_type')
        layout.separator()
        filter_node = item.get_filter_node()
        draw_props(filter_node, filter_node.prop_names, layout)

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return rd.engine == 'PRMAN_RENDER'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rm = scene.renderman

        self._draw_collection(context, layout, rm, "Sample Filters:",
                              "rfb.collection_toggle_path", "scene", "sample_filters",
                              "sample_filters_index")


class DATA_PT_renderman_node_filters_lamp(RfB_PT_Collection, Panel):
    bl_label = "Light Filters"
    bl_context = 'data'

    def draw_item(self, layout, context, item):
        layout.prop(item, 'filter_name')

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return rd.engine == 'PRMAN_RENDER' and hasattr(context, "lamp") \
            and context.lamp is not None and hasattr(context.lamp, 'renderman') \
            and context.lamp.renderman.renderman_type != 'FILTER'

    def draw(self, context):
        layout = self.layout
        lamp = context.lamp

        self._draw_collection(context, layout, lamp.renderman, "",
                              "rfb.collection_toggle_path", "lamp", "light_filters",
                              "light_filters_index")


class RendermanRibBoxPanel(RfB_PT_RootPanel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_label = "RIB Box"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return (rd.engine in {'PRMAN_RENDER'})

    def draw_rib_boxes(self, layout, rib_box_names, item):
        rm = item.renderman
        for rib_box in rib_box_names:
            row = layout.row()
            row.prop_search(rm, rib_box, bpy.data, "texts")
            if getattr(item.renderman, rib_box) != '':
                text_name = getattr(item.renderman, rib_box)
                rib_box_string = bpy.data.texts.get(text_name)
                for line in rib_box_string.lines:
                    row = layout.row()
                    row.label(text=line.body)


class OBJECT_PT_renderman_rib_box(RendermanRibBoxPanel, Panel):
    bl_context = "object"
    bl_label = "Object RIB boxes"

    def draw(self, context):
        self.draw_rib_boxes(self.layout, ['pre_object_rib_box', 'post_object_rib_box'],
                            context.object)


class WORLD_PT_renderman_rib_box(RendermanRibBoxPanel, Panel):
    bl_context = "world"
    bl_label = "World RIB box"

    def draw(self, context):
        self.draw_rib_boxes(self.layout, ['world_rib_box'],
                            context.world)


class SCENE_PT_renderman_rib_box(RendermanRibBoxPanel, Panel):
    bl_context = "scene"
    bl_label = "Scene RIB box"

    def draw(self, context):
        self.draw_rib_boxes(self.layout, ['frame_rib_box'],
                            context.scene)


class OBJECT_PT_renderman_object_matteid(Panel, RfB_PT_RootPanel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_label = "Matte ID"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return (context.object and rd.engine in {'PRMAN_RENDER'})

    def draw(self, context):
        layout = self.layout.column(align=True)
        ob = context.object
        rm = ob.renderman

        row = layout.row(align=True)
        row.prop(rm, 'MatteID0', text='')
        row.prop(rm, 'MatteID1', text='')
        row.prop(rm, 'MatteID2', text='')
        row.prop(rm, 'MatteID3', text='')

        row = layout.row(align=True)
        row.prop(rm, 'MatteID4', text='')
        row.prop(rm, 'MatteID5', text='')
        row.prop(rm, 'MatteID6', text='')
        row.prop(rm, 'MatteID7', text='')


class PARTICLE_PT_renderman_prim_vars(RfB_PT_Collection, Panel):
    bl_context = "particle"
    bl_label = "Primitive Variables"

    def draw_item(self, layout, context, item):
        ob = context.object
        layout.prop(item, "name")

        row = layout.row()
        row.prop(item, "data_source", text="Source")

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        if not context.particle_system:
            return False
        return rd.engine == 'PRMAN_RENDER'

    def draw(self, context):
        layout = self.layout
        psys = context.particle_system
        rm = psys.settings.renderman

        self._draw_collection(context, layout, rm, "Primitive Variables:",
                              "rfb.collection_toggle_path",
                              "particle_system.settings",
                              "prim_vars", "prim_vars_index")

        layout.prop(rm, "export_default_size")


def PRMan_menu_func(self, context):
    if context.scene.render.engine != "PRMAN_RENDER":
        return
    self.layout.separator()
    if engine.ipr:
        self.layout.operator('rfb.tool_ipr',
                             text="RenderMan Stop Interactive Rendering")
    else:
        self.layout.operator('rfb.tool_ipr',
                             text="RenderMan Start Interactive Rendering")


def get_panels():
    exclude_panels = {
        'DATA_PT_area',
        'DATA_PT_camera_dof',
        'DATA_PT_falloff_curve',
        'DATA_PT_lamp',
        'DATA_PT_preview',
        'DATA_PT_shadow',
        # 'DATA_PT_spot',
        'DATA_PT_sunsky',
        # 'MATERIAL_PT_context_material',
        'MATERIAL_PT_diffuse',
        'MATERIAL_PT_flare',
        'MATERIAL_PT_halo',
        'MATERIAL_PT_mirror',
        'MATERIAL_PT_options',
        'MATERIAL_PT_pipeline',
        'MATERIAL_PT_preview',
        'MATERIAL_PT_shading',
        'MATERIAL_PT_shadow',
        'MATERIAL_PT_specular',
        'MATERIAL_PT_sss',
        'MATERIAL_PT_strand',
        'MATERIAL_PT_transp',
        'MATERIAL_PT_volume_density',
        'MATERIAL_PT_volume_integration',
        'MATERIAL_PT_volume_lighting',
        'MATERIAL_PT_volume_options',
        'MATERIAL_PT_volume_shading',
        'MATERIAL_PT_volume_transp',
        'RENDERLAYER_PT_layer_options',
        'RENDERLAYER_PT_layer_passes',
        'RENDERLAYER_PT_views',
        'RENDER_PT_antialiasing',
        'RENDER_PT_bake',
        'RENDER_PT_motion_blur',
        'RENDER_PT_performance',
        'RENDER_PT_freestyle',
        # 'RENDER_PT_post_processing',
        'RENDER_PT_shading',
        'RENDER_PT_render',
        'RENDER_PT_stamp',
        'SCENE_PT_simplify',
        'TEXTURE_PT_context_texture',
        'WORLD_PT_ambient_occlusion',
        'WORLD_PT_environment_lighting',
        'WORLD_PT_gather',
        'WORLD_PT_indirect_lighting',
        'WORLD_PT_mist',
        'WORLD_PT_preview',
        'WORLD_PT_world',
    }

    panels = []
    for t in bpy.types.Panel.__subclasses__():
        if hasattr(t, 'COMPAT_ENGINES') and 'BLENDER_RENDER' in t.COMPAT_ENGINES:
            if t.__name__ not in exclude_panels:
                panels.append(t)

    return panels


def register():
    bpy.utils.register_class(RfB_UL_ObjectGroup)
    bpy.utils.register_class(RfB_UL_LightLinkingLights)
    bpy.utils.register_class(RfB_UL_LightLinkingObjects)
    bpy.types.INFO_MT_render.append(PRMan_menu_func)

    for panel in get_panels():
        panel.COMPAT_ENGINES.add('PRMAN_RENDER')


def unregister():
    bpy.utils.unregister_class(RfB_UL_ObjectGroup)
    bpy.utils.unregister_class(RfB_UL_LightLinkingLights)
    bpy.utils.unregister_class(RfB_UL_LightLinkingObjects)
    bpy.types.INFO_MT_render.remove(PRMan_menu_func)

    for panel in get_panels():
        panel.COMPAT_ENGINES.add('PRMAN_RENDER')
