import os
import bpy


class RfB_MT_RenderPresets(bpy.types.Menu):
    bl_label = "RenderMan Presets"
    bl_idname = "RfB_MT_render_presets"
    preset_subdir = os.path.join("renderman", "render")
    preset_operator = "script.execute_preset"
    draw = bpy.types.Menu.draw_preset
