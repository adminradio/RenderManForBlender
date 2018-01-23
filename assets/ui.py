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
from bpy.types import Panel
from bpy.props import StringProperty

from .. import utils

from . properties import RendermanAssetGroup
from . properties import RendermanAsset

from . import assets
from .. gui import icons
from .. import rfb
from .. gui.RfB_PT_MIXIN_PanelIcon import RfB_PT_MIXIN_PanelIcon


# panel for the toolbar of node editor


class Renderman_Assets_UI_Panel(RfB_PT_MIXIN_PanelIcon, Panel):
    bl_idname = "rfb.assets_ui_panel"
    bl_label = "RenderMan Assets"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = rfb.reg.get('BL_CATEGORY')

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return rd.engine == 'PRMAN_RENDER'

    # def draw_header(self, context):
    #     if rfb.reg.prefs().draw_panel_icon:
    #         iid = icons.iconid("renderman")
    #         self.layout.label(text="", icon_value=iid)
    #     else:
    #         pass

    # draws the panel
    def draw(self, context):
        scene = context.scene
        rm = scene.renderman
        layout = self.layout

        if context.scene.render.engine != "PRMAN_RENDER":
            return

        assets_library = rfb.reg.prefs().assets_library

        if assets_library.name == '':
            layout.operator("rfb.init_asset_library", text="Set up Library")
        else:
            layout = self.layout

            row = layout.row(align=True)
            row.context_pointer_set('renderman_asset', rfb.reg.prefs().assets_library)
            row.menu('renderman_assets_menu', text="Select Library")
            row.operator("rfb.init_asset_library", text="", icon="FILE_REFRESH")
            active = RendermanAssetGroup.get_active_library()

            if active:
                row = layout.row(align=True)
                # row.prop(active, 'name', text='Library')
                row.prop(active, 'name', text='')
                row.operator('rfb.assets_library_add', text='', icon='ZOOMIN')
                row.operator('rfb.assets_library_move', text='', icon='MAN_TRANS').lib_path = active.path
                row.operator('rfb.assets_library_remove', text='', icon='X')
                current_asset = RendermanAsset.get_from_path(active.current_asset)

                if current_asset:
                    row = layout.row()
                    #row.label("Current Asset:")
                    row.prop(active, 'current_asset', text='')
                    layout.template_icon_view(active, "current_asset")
                    # row of controls for asset
                    row = layout.row(align=True)
                    row.prop(current_asset, 'label', text="")
                    row.operator('rfb.asset_move', icon='MAN_TRANS', text="").asset_path = current_asset.path
                    row.operator('rfb.asset_remove', icon='X', text="").asset_path = current_asset.path

                    # add to scene
                    row = layout.row(align=True)
                    row.operator("rfb.asset_load_to_scene", text="Load to Scene", ).asset_path = current_asset.path
                    assign = row.operator("rfb.asset_load_to_scene", text="Assign to selected", )
                    assign.asset_path = current_asset.path
                    assign.assign = True

                # get from scene
                layout.separator()
                layout.operator("rfb.asset_save_to_library", text="Save Material to Library").lib_path = active.path


class Renderman_Assets_Menu(bpy.types.Menu):
    bl_idname = "renderman_assets_menu"
    bl_label = "RenderMan Assets Menu"

    path = StringProperty(default="")

    def draw(self, context):
        lib = context.renderman_asset
        prefix = "* " if lib.is_active() else ''
        self.layout.operator('rfb.assets_set_active_library', text=prefix + lib.name).lib_path = lib.path
        if len(lib.sub_groups) > 0:
            for key in sorted(lib.sub_groups.keys(), key=lambda k: k.lower()):
                sub = lib.sub_groups[key]
                self.layout.context_pointer_set('renderman_asset', sub)
                prefix = "* " if sub.is_active() else ''
                if len(sub.sub_groups):
                    self.layout.menu('renderman_assets_menu', text=prefix + sub.name)
                else:
                    prefix = "* " if sub.is_active() else ''
                    self.layout.operator('rfb.assets_set_active_library', text=prefix + sub.name).lib_path = sub.path


def register():
    try:
        bpy.utils.register_class(Renderman_Assets_Menu)
        bpy.utils.register_class(Renderman_Assets_UI_Panel)
    except:
        pass  # allready registered


def unregister():
    bpy.utils.unregister_class(Renderman_Assets_Menu)
    bpy.utils.unregister_class(Renderman_Assets_UI_Panel)
