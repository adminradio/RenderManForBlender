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
from . rfb.evt import handlers

bl_info = {
    "name": "RenderMan For Blender",
    "author": "Pixar",
    "version": (21, 6, 0),
    "blender": (2, 78, 0),
    "location": "Info Header, Render Engine Menu",
    "description": "RenderMan 21.6 Integration",
    "warning": "",
    "category": "Render",
}


class PRManRender(bpy.types.RenderEngine):
    bl_idname = 'PRMAN_RENDER'
    bl_label = "RenderMan Render"
    bl_use_preview = True
    bl_use_save_buffers = True
    bl_use_shading_nodes = True
    bl_use_shading_nodes_custom = False

    def __init__(self):
        self.render_pass = None

    def __del__(self):
        if hasattr(self, "render_pass"):
            if self.render_pass is not None:
                engine.free(self)  # noqa

    #
    # main scene render
    #
    def update(self, data, scene):
        if(engine.ipr):  # noqa
            return
        if self.is_preview:
            if not self.render_pass:
                engine.create(self, data, scene)  # noqa
        else:
            if not self.render_pass:
                engine.create(self, data, scene)  # noqa
            else:
                engine.reset(self, data, scene)  # noqa

        engine.update(self, data, scene)  # noqa

    def render(self, scene):
        if self.render_pass is not None:
            engine.render(self)  # noqa


def register():
    from . import preferences
    preferences.register()

    from . import gui
    from . import ops
    from . import nds
    from . import properties

    # # #### WIPs ####
    #
    # from . gui import RfB_HT_IMAGE_SmartControl  # noqa
    # from . gui import RfB_HT_NODE_SmartControl  # noqa
    # from . gui import RfB_HT_VIEW3D_SmartControl  # noqa
    #
    # # #### END WIPs ####
    #
    from . gui import RfB_HT_INFO_SmartControl  # noqa
    from . gui import RfB_MT_RENDER_Presets  # noqa
    from . gui import RfB_MT_SCENE_Cameras  # noqa
    from . gui import RfB_MT_SCENE_LightsArea  # noqa
    from . gui import RfB_MT_SCENE_LightsDay  # noqa
    from . gui import RfB_MT_SCENE_LightsHemi  # noqa
    from . gui import RfB_PT_DATA_Camera  # noqa
    from . gui import RfB_PT_DATA_Lamp  # noqa
    from . gui import RfB_PT_DATA_Light  # noqa
    from . gui import RfB_PT_DATA_LightFilters  # noqa
    from . gui import RfB_PT_DATA_World  # noqa
    from . gui import RfB_PT_LAYER_LayerOptions  # noqa
    from . gui import RfB_PT_LAYER_RenderPasses  # noqa
    from . gui import RfB_PT_MATERIAL_Displacement  # noqa
    from . gui import RfB_PT_MATERIAL_Preview  # noqa
    from . gui import RfB_PT_MATERIAL_ShaderLight  # noqa
    from . gui import RfB_PT_MATERIAL_ShaderSurface  # noqa
    from . gui import RfB_PT_MESH_PrimVars  # noqa
    from . gui import RfB_PT_MIXIN_Collection  # noqa
    from . gui import RfB_PT_OBJECT_Geometry  # noqa
    from . gui import RfB_PT_OBJECT_MatteID  # noqa
    from . gui import RfB_PT_OBJECT_Raytracing  # noqa
    from . gui import RfB_PT_OBJECT_RIBInjection  # noqa
    from . gui import RfB_PT_OBJECT_ShadingVisibility  # noqa
    from . gui import RfB_PT_PARTICLE_PrimVars  # noqa
    from . gui import RfB_PT_PARTICLE_Render  # noqa
    from . gui import RfB_PT_RENDER_Advanced  # noqa
    from . gui import RfB_PT_RENDER_Baking  # noqa
    from . gui import RfB_PT_RENDER_MotionBlur  # noqa
    from . gui import RfB_PT_RENDER_PreviewSampling  # noqa
    from . gui import RfB_PT_RENDER_Render  # noqa
    from . gui import RfB_PT_RENDER_Sampling  # noqa
    from . gui import RfB_PT_RENDER_Spooling  # noqa
    from . gui import RfB_PT_SCENE_DisplayFilters  # noqa
    from . gui import RfB_PT_SCENE_LightLinking  # noqa
    from . gui import RfB_PT_SCENE_LigthGroups  # noqa
    from . gui import RfB_PT_SCENE_ObjectGroups  # noqa
    from . gui import RfB_PT_SCENE_RIBInjection  # noqa
    from . gui import RfB_PT_SCENE_SampleFilters  # noqa
    from . gui import RfB_PT_WORLD_RIBInjection  # noqa
    from . gui import RfB_PT_VIEW3D_Toolshelf  # noqa

    from . ops import RfB_OT_COLL_TogglePath  # noqa
    from . ops import RfB_OT_FILE_OpenLastRIB  # noqa
    from . ops import RfB_OT_FILE_SpoolRender  # noqa
    from . ops import RfB_OT_FILE_ViewStats  # noqa
    from . ops import RfB_OT_ITEM_MovetoGroup  # noqa
    from . ops import RfB_OT_ITEM_RemoveGroup  # noqa
    from . ops import RfB_OT_ITEM_ToggleLightlink  # noqa
    from . ops import RfB_OT_LIST_AddMultilayer  # noqa
    from . ops import RfB_OT_MATERIAL_AddBXDF  # noqa
    from . ops import RfB_OT_MATERIAL_NewBXDF  # noqa
    from . ops import RfB_OT_NODE_AddNodetree  # noqa
    from . ops import RfB_OT_NODE_BakePatterns  # noqa
    from . ops import RfB_OT_NODE_CyclesConvertall  # noqa
    from . ops import RfB_OT_NODE_RefreshOSL  # noqa
    from . ops import RfB_OT_OBJECT_AddCamera  # noqa
    from . ops import RfB_OT_OBJECT_AddFilterLight  # noqa
    from . ops import RfB_OT_OBJECT_AddLightArea  # noqa
    from . ops import RfB_OT_OBJECT_AddLightDay  # noqa
    from . ops import RfB_OT_OBJECT_AddLightHemi  # noqa
    from . ops import RfB_OT_OBJECT_DeleteCamera  # noqa
    from . ops import RfB_OT_OBJECT_DeleteLight  # noqa
    from . ops import RfB_OT_OBJECT_EnableSubdiv  # noqa
    from . ops import RfB_OT_OBJECT_ExportRIB  # noqa
    from . ops import RfB_OT_OBJECT_MakeEmissive  # noqa
    from . ops import RfB_OT_OBJECT_SelectCamera  # noqa
    from . ops import RfB_OT_OBJECT_SelectActiveCamera  # noqa
    from . ops import RfB_OT_OBJECT_SelectLight  # noqa
    from . ops import RfB_OT_OUTPUT_ToggleChannel  # noqa
    from . ops import RfB_OT_RENDER_AddPreset  # noqa
    from . ops import RfB_OT_RPASS_AddRenderman  # noqa
    from . ops import RfB_OT_TOOL_Restart  # noqa
    from . ops import RfB_OT_TOOL_StartIPR  # noqa
    from . ops import RfB_OT_TOOL_StartIT  # noqa
    from . ops import RfB_OT_TOOL_StartLQ  # noqa
    from . ops import RfB_OT_VIEW3D_ViewNumpad0  # noqa
    from . ops import RfB_OT_VIEW3D_CameraApertureType  # noqa
    #
    # need this now rather than at beginning to make
    # sure preferences are loaded
    #
    from . import engine  # noqa
    properties.register()
    ops.register()
    gui.register()
    nds.register()
    from . import assets
    assets.register()
    handlers.register()
    bpy.utils.register_module(__name__)


def unregister():
    handlers.unregister()
    from . import assets
    assets.unregister()
    nds.unregister()  # noqa
    gui.unregister()  # noqa
    ops.unregister()  # noqa
    properties.unregister()  # noqa
    from . import preferences
    preferences.unregister()
    bpy.utils.unregister_module(__name__)
