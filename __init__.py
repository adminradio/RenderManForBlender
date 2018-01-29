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

import bpy
import sys

#
# Event Handlers
#
from . rfb.evt import events
from . rfb.evt import handlers


bl_info = {
    "name": "RenderMan For Blender",
    "author": "Pixar",
    "version": (21, 5, 0),
    "blender": (2, 78, 0),
    "location": "Info Header, Render Engine Menu",
    "description": "RenderMan 21.5 Integration",
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
                engine.free(self)

    # main scene render
    def update(self, data, scene):
        if(engine.ipr):
            return
        if self.is_preview:
            if not self.render_pass:
                engine.create(self, data, scene)
        else:
            if not self.render_pass:
                engine.create(self, data, scene)
            else:
                engine.reset(self, data, scene)

        engine.update(self, data, scene)

    def render(self, scene):
        if self.render_pass is not None:
            engine.render(self)


# # these handlers are for marking files as dirty for ribgen
def add_handlers(scene):
    if (engine.update_timestamp
            not in bpy.app.handlers.scene_update_post):

        bpy.app.handlers.scene_update_post.append(engine.update_timestamp)

    if (properties.initial_groups
            not in bpy.app.handlers.scene_update_post):

        bpy.app.handlers.load_post.append(properties.initial_groups)


def remove_handlers():
    if (properties.initial_groups
            in bpy.app.handlers.scene_update_post):

        bpy.app.handlers.scene_update_post.remove(properties.initial_groups)

    if (engine.update_timestamp
            in bpy.app.handlers.scene_update_post):

        bpy.app.handlers.scene_update_post.remove(engine.update_timestamp)


def load_addon():
    # if rmantree is ok load the stuff
    from . rfb.lib import guess_rmantree
    from . rfb.lib import throw_error
    from . import preferences

    #
    # TODO:   Refactor guess_rmantree() to RfB Registry
    # DATE:   2018-01-17
    # AUTHOR: Timm Wimmers
    # STATUS: -unassigned-
    #
    if guess_rmantree():
        #
        # else display an error, tell user to correct
        # and don't load anything else
        #
        from . import gui
        from . import ops
        from . import nds
        from . import properties

        from . gui import RfB_HT_IMAGE_SmartControl
        from . gui import RfB_HT_INFO_SmartControl
        from . gui import RfB_HT_NODE_SmartControl
        from . gui import RfB_HT_VIEW3D_SmartControl
        from . gui import RfB_MT_RENDER_Presets
        from . gui import RfB_MT_SCENE_Cameras
        from . gui import RfB_MT_SCENE_LightsArea
        from . gui import RfB_MT_SCENE_LightsDay
        from . gui import RfB_MT_SCENE_LightsHemi
        from . gui import RfB_PT_DATA_Camera
        from . gui import RfB_PT_DATA_Lamp
        from . gui import RfB_PT_DATA_Light
        from . gui import RfB_PT_DATA_LightFilters
        from . gui import RfB_PT_DATA_World
        from . gui import RfB_PT_LAYER_LayerOptions
        from . gui import RfB_PT_LAYER_RenderPasses
        from . gui import RfB_PT_MATERIAL_Displacement
        from . gui import RfB_PT_MATERIAL_Preview
        from . gui import RfB_PT_MATERIAL_ShaderLight
        from . gui import RfB_PT_MATERIAL_ShaderSurface
        from . gui import RfB_PT_MESH_PrimVars
        from . gui import RfB_PT_MIXIN_Collection
        from . gui import RfB_PT_OBJECT_Geometry
        from . gui import RfB_PT_OBJECT_MatteID
        from . gui import RfB_PT_OBJECT_Raytracing
        from . gui import RfB_PT_OBJECT_RIBInjection
        from . gui import RfB_PT_OBJECT_ShadingVisibility
        from . gui import RfB_PT_PARTICLE_PrimVars
        from . gui import RfB_PT_PARTICLE_Render
        from . gui import RfB_PT_RENDER_Advanced
        from . gui import RfB_PT_RENDER_Baking
        from . gui import RfB_PT_RENDER_MotionBlur
        from . gui import RfB_PT_RENDER_PreviewSampling
        from . gui import RfB_PT_RENDER_Render
        from . gui import RfB_PT_RENDER_Sampling
        from . gui import RfB_PT_RENDER_Spooling
        from . gui import RfB_PT_SCENE_DisplayFilters
        from . gui import RfB_PT_SCENE_LightLinking
        from . gui import RfB_PT_SCENE_LigthGroups
        from . gui import RfB_PT_SCENE_ObjectGroups
        from . gui import RfB_PT_SCENE_RIBInjection
        from . gui import RfB_PT_SCENE_SampleFilters
        from . gui import RfB_PT_VIEW3D_Toolshelf

        from . ops import RfB_OT_COLL_TogglePath
        from . ops import RfB_OT_FILE_OpenLastRIB
        from . ops import RfB_OT_FILE_SpoolRender
        from . ops import RfB_OT_FILE_ViewStats
        from . ops import RfB_OT_ITEM_MovetoGroup
        from . ops import RfB_OT_ITEM_RemoveGroup
        from . ops import RfB_OT_ITEM_ToggleLightlink
        from . ops import RfB_OT_LIST_AddMultilayer
        from . ops import RfB_OT_MATERIAL_AddBXDF
        from . ops import RfB_OT_MATERIAL_NewBXDF
        from . ops import RfB_OT_NODE_AddNodetree
        from . ops import RfB_OT_NODE_BakePatterns
        from . ops import RfB_OT_NODE_CyclesConvertall
        from . ops import RfB_OT_NODE_RefreshOSL
        from . ops import RfB_OT_OBJECT_AddCamera
        from . ops import RfB_OT_OBJECT_AddFilterLight
        from . ops import RfB_OT_OBJECT_AddLightArea
        from . ops import RfB_OT_OBJECT_AddLightDay
        from . ops import RfB_OT_OBJECT_AddLightHemi
        from . ops import RfB_OT_OBJECT_DeleteCamera
        from . ops import RfB_OT_OBJECT_DeleteLight
        from . ops import RfB_OT_OBJECT_EnableSubdiv
        from . ops import RfB_OT_OBJECT_ExportRIB
        from . ops import RfB_OT_OBJECT_MakeEmissive
        from . ops import RfB_OT_OBJECT_SelectCamera
        from . ops import RfB_OT_OBJECT_SelectActiveCamera
        from . ops import RfB_OT_OBJECT_SelectLight
        from . ops import RfB_OT_OUTPUT_ToggleChannel
        from . ops import RfB_OT_RENDER_AddPreset
        from . ops import RfB_OT_RPASS_AddRenderman
        from . ops import RfB_OT_TOOL_Restart
        from . ops import RfB_OT_TOOL_StartIPR
        from . ops import RfB_OT_TOOL_StartIT
        from . ops import RfB_OT_TOOL_StartLQ
        from . ops import RfB_OT_VIEW3D_ViewNumpad0
        from . ops import RfB_OT_VIEW3D_CameraApertureType

        #
        # need this now rather than at beginning to make
        # sure preferences are loaded
        #
        from . import engine
        properties.register()
        ops.register()
        gui.register()
        add_handlers(None)
        nds.register()
    else:
        #
        # display loading error
        #
        throw_error(
            "Error loading addon.  Correct RMANTREE setting in addon preferences.")


def register():
    from . import rfb
    from . import preferences
    preferences.register()
    load_addon()
    from . import assets
    assets.register()
    handlers.register()
    bpy.utils.register_module(__name__)


def unregister():
    from . import preferences
    remove_handlers()
    handlers.unregister()
    properties.unregister()
    ops.unregister()
    gui.unregister()
    nds.unregister()
    preferences.unregister()
    from . import assets
    assets.unregister()
    bpy.utils.unregister_module(__name__)
