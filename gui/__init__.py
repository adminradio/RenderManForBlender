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
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY",
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM",
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
# ##### END MIT LICENSE BLOCK #####

__all__ = [
    "RfB_HT_IMAGE_SmartControl",
    "RfB_HT_INFO_SmartControl",
    "RfB_HT_NODE_SmartControl",
    "RfB_HT_VIEW3D_SmartControl",
    "RfB_MT_ExampleFiles",
    "RfB_MT_RENDER_Presets",
    "RfB_MT_SCENE_LightsArea",
    "RfB_MT_SCENE_Cameras",
    "RfB_MT_SCENE_LightsDay",
    "RfB_MT_SCENE_LightsHemi"
    "RfB_PT_DATA_Camera",
    "RfB_PT_DATA_Lamp",
    "RfB_PT_DATA_Light",
    "RfB_PT_DATA_LightFilters",
    "RfB_PT_DATA_World",
    "RfB_PT_LAYER_LayerOptions",
    "RfB_PT_LAYER_RenderPasses",
    "RfB_PT_MATERIAL_Displacement",
    "RfB_PT_MATERIAL_Preview",
    "RfB_PT_MATERIAL_ShaderLight",
    "RfB_PT_MATERIAL_ShaderSurface",
    "RfB_PT_MESH_PrimVars",
    "RfB_PT_OBJECT_Geometry",
    "RfB_PT_OBJECT_MatteID",
    "RfB_PT_OBJECT_Raytracing",
    "RfB_PT_OBJECT_RIBInjection",
    "RfB_PT_OBJECT_ShadingVisibility",
    "RfB_PT_PARTICLE_PrimVars",
    "RfB_PT_PARTICLE_Render",
    "RfB_PT_RENDER_Advanced",
    "RfB_PT_RENDER_Baking",
    "RfB_PT_RENDER_MotionBlur",
    "RfB_PT_RENDER_PreviewSampling",
    "RfB_PT_RENDER_Render",
    "RfB_PT_RENDER_Sampling",
    "RfB_PT_RENDER_Spooling",
    "RfB_PT_SCENE_DisplayFilters",
    "RfB_PT_SCENE_LightLinking",
    "RfB_PT_SCENE_LigthGroups",
    "RfB_PT_SCENE_ObjectGroups",
    "RfB_PT_SCENE_RIBInjection",
    "RfB_PT_SCENE_SampleFilters",
    "RfB_PT_VIEW3D_Toolshelf",
    "RfB_UL_LIGHTS_Linking",
    "RfB_UL_LIGHTS_LinkingObjects",
    "RfB_UL_ObjectGroup",
]

#
# Blender Imports
#
import bpy

#
# RenderMan for Blender Imports
#
from . utils import rfb_menu_func

from . RfB_UL_ObjectGroup import RfB_UL_ObjectGroup
from . RfB_UL_LIGHTS_Linking import RfB_UL_LIGHTS_Linking
from . RfB_UL_LIGHTS_LinkingObjects import RfB_UL_LIGHTS_LinkingObjects


def rfb_panels():
    rfb_panels_true = []
    rfb_panels_false = {
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

    for t in bpy.types.Panel.__subclasses__():
        if hasattr(t, 'COMPAT_ENGINES') and 'BLENDER_RENDER' in t.COMPAT_ENGINES:
            if t.__name__ not in rfb_panels_false:
                rfb_panels_true.append(t)

    return rfb_panels_true


def register():
    bpy.utils.register_class(RfB_UL_ObjectGroup)
    bpy.utils.register_class(RfB_UL_LIGHTS_Linking)
    bpy.utils.register_class(RfB_UL_LIGHTS_LinkingObjects)
    bpy.types.INFO_MT_render.append(rfb_menu_func)

    for panel in rfb_panels():
        panel.COMPAT_ENGINES.add('PRMAN_RENDER')


def unregister():
    bpy.utils.unregister_class(RfB_UL_ObjectGroup)
    bpy.utils.unregister_class(RfB_UL_LIGHTS_Linking)
    bpy.utils.unregister_class(RfB_UL_LIGHTS_LinkingObjects)
    bpy.types.INFO_MT_render.remove(rfb_menu_func)

    for panel in rfb_panels():
        panel.COMPAT_ENGINES.remove('PRMAN_RENDER')
