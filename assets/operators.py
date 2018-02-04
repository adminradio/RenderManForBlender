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

import os
import json
import shutil

import bpy

from bpy.props import EnumProperty
from bpy.props import BoolProperty
from bpy.props import StringProperty

from . properties import RendermanAsset
from . properties import RendermanAssetGroup

from .. rfb.lib import guess_rmantree

from .. rfb.lib.prfs import pref
from .. rfb.lib.prfs import prefs


#
# update the tree structure from disk file
#
def refresh_assets_libraries(disk_lib, asset_library):
    dirs = os.listdir(disk_lib)
    for dir in dirs:
        cdir = os.path.join(disk_lib, dir)
        # skip if not a dir
        if not os.path.isdir(cdir):
            continue

        is_asset = '.rma' in dir
        path = os.path.join(disk_lib, dir)

        if is_asset:
            asset = asset_library.assets.get(dir, None)
            if not asset:
                asset = asset_library.assets.add()

            asset.name = dir
            json_path = os.path.join(path, 'asset.json')
            data = json.load(open(json_path))
            asset.label = data['RenderManAsset']['label']
            asset.path = path
            asset.json_path = os.path.join(path, 'asset.json')

        else:
            sub_group = asset_library.sub_groups.get(dir, None)
            if not sub_group:
                sub_group = asset_library.sub_groups.add()
            sub_group.name = dir
            sub_group.path = path

            refresh_assets_libraries(cdir, sub_group)

    for i, sub_group in enumerate(asset_library.sub_groups):
        if sub_group.name not in dirs:
            asset_library.sub_groups.remove(i)
    for i, asset in enumerate(asset_library.assets):
        if asset.name not in dirs:
            asset_library.assets.remove(i)


# if the library isn't present copy it from rmantree to the path in addon prefs
class init_asset_library(bpy.types.Operator):
    bl_idname = "rfb.init_asset_library"
    bl_label = "Init RenderMan Asset Library"
    bl_description = "Copies the Asset Library from RMANTREE to the library path if not present\n Or refreshes if changed on disk."

    def invoke(self, context, event):
        assets_library = pref('assets_library')
        assets_path = pref('assets_path')
        if not os.path.exists(assets_path):
            rmantree_lib_path = os.path.join(guess_rmantree(), 'lib', 'RenderManAssetLibrary')
            shutil.copytree(rmantree_lib_path, assets_path)

        assets_library.name = 'Library'
        assets_library.path = assets_path
        refresh_assets_libraries(assets_path, assets_library)
        bpy.ops.wm.save_userpref()
        return {'FINISHED'}


class load_asset_to_scene(bpy.types.Operator):
    bl_idname = "rfb.asset_load_to_scene"
    bl_label = "Load Asset to Scene"
    bl_description = "Load the Asset to scene"

    asset_path = StringProperty(default='')
    assign = BoolProperty(default=False)

    def invoke(self, context, event):
        asset = RendermanAsset.get_from_path(self.properties.asset_path)
        from . import rmanAssetsBlender
        mat = rmanAssetsBlender.importAsset(asset.json_path)
        if self.properties.assign and mat and type(mat) == bpy.types.Material:
            for ob in context.selected_objects:
                ob.active_material = mat

        return {'FINISHED'}


# save the current material to the library
class save_asset_to_lib(bpy.types.Operator):
    bl_idname = "rfb.asset_save_to_library"
    bl_label = "Save Asset to Library"
    bl_description = "Save Asset to Library"

    lib_path = StringProperty(default='')

    def invoke(self, context, event):
        assets_path = pref('assets_library').path
        path = os.path.relpath(self.properties.lib_path, assets_path)
        library = RendermanAssetGroup.get_from_path(self.properties.lib_path)
        ob = context.active_object
        mat = ob.active_material
        nt = mat.node_tree
        if nt:
            from . import rmanAssetsBlender
            os.environ['RMAN_ASSET_LIBRARY'] = assets_path
            rmanAssetsBlender.exportAsset(nt, 'nodeGraph',
                                          {'label': mat.name,
                                           'author': '',
                                           'version': ''},
                                          path
                                          )
        refresh_assets_libraries(library.path, library)
        bpy.ops.wm.save_userpref()
        return {'FINISHED'}


# if the library isn't present copy it from rmantree to the path in addon prefs
class set_active_asset_library(bpy.types.Operator):
    bl_idname = "rfb.assets_set_active_library"
    bl_label = "Set active RenderMan Asset Library"
    bl_description = "Sets the clicked library active"

    lib_path = StringProperty(default='')

    def execute(self, context):
        lib_path = self.properties.lib_path
        if lib_path:
            prefs().active_assets_path = lib_path
        return {'FINISHED'}

# if the library isn't present copy it from rmantree to the path in addon prefs


class add_asset_library(bpy.types.Operator):
    bl_idname = "rfb.assets_library_add"
    bl_label = "Add RenderMan Asset Library"
    bl_description = "Adds a new library"

    new_name = StringProperty(default="")

    def execute(self, context):
        active = RendermanAssetGroup.get_active_library()
        lib_path = active.path
        new_folder = self.properties.new_name
        if lib_path and new_folder:
            path = os.path.join(lib_path, new_folder)
            os.mkdir(path)
            sub_group = active.sub_groups.add()
            sub_group.name = new_folder
            sub_group.path = path
            prefs().active_assets_path = path
        bpy.ops.wm.save_userpref()
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        row = self.layout
        row.prop(self, "new_name", text="New Folder Name:")


class remove_asset_library(bpy.types.Operator):
    bl_idname = "rfb.assets_library_remove"
    bl_label = "Remove RenderMan Asset Library"
    bl_description = "Remove a library"

    def execute(self, context):
        active = RendermanAssetGroup.get_active_library()
        lib_path = active.path
        if lib_path:
            parent_path = os.path.split(active.path)[0]
            parent = RendermanAssetGroup.get_from_path(parent_path)
            prefs().active_assets_path = parent_path

            shutil.rmtree(active.path)

            refresh_assets_libraries(parent.path, parent)
        bpy.ops.wm.save_userpref()
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class remove_asset(bpy.types.Operator):
    bl_idname = "rfb.asset_remove"
    bl_label = "Remove RenderMan Asset"
    bl_description = "Remove an Asset"

    asset_path = StringProperty()

    def execute(self, context):
        asset_path = self.properties.asset_path
        active = RendermanAsset.get_from_path(asset_path)
        if active:
            parent_path = os.path.split(asset_path)[0]
            parent = RendermanAssetGroup.get_from_path(parent_path)

            shutil.rmtree(active.path)

            refresh_assets_libraries(parent.path, parent)
        bpy.ops.wm.save_userpref()
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class move_asset(bpy.types.Operator):
    bl_idname = "rfb.asset_move"
    bl_label = "Move RenderMan Asset"
    bl_description = "Move an Asset"

    def get_libraries(self, context):
        def get_libs(parent_lib):
            enum = [(parent_lib.path, parent_lib.name, '')]
            for lib in parent_lib.sub_groups:
                enum.extend(get_libs(lib))
            return enum
        return get_libs(pref('assets_library'))

    asset_path = StringProperty(default='')
    new_library = EnumProperty(items=get_libraries, description='New Library', name="New Library")

    def execute(self, context):
        new_parent_path = self.properties.new_library
        active = RendermanAsset.get_from_path(self.properties.asset_path)
        if active:
            old_parent_path = os.path.split(active.path)[0]
            old_parent = RendermanAssetGroup.get_from_path(old_parent_path)
            new_parent = RendermanAssetGroup.get_from_path(new_parent_path)

            shutil.move(active.path, new_parent_path)

            refresh_assets_libraries(old_parent.path, old_parent)
            refresh_assets_libraries(new_parent.path, new_parent)
        bpy.ops.wm.save_userpref()
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        row = self.layout
        row.prop(self, "new_library", text="New Library")


class move_asset_library(bpy.types.Operator):
    bl_idname = "rfb.assets_library_move"
    bl_label = "Move RenderMan Asset Group"
    bl_description = "Move an Asset Group"

    def get_libraries(self, context):
        def get_libs(parent_lib):
            enum = [(parent_lib.path, parent_lib.name, '')]
            for lib in parent_lib.sub_groups:
                enum.extend(get_libs(lib))
            return enum

        return get_libs(pref('assets_library'))

    lib_path = StringProperty(default='')
    new_library = EnumProperty(items=get_libraries, description='New Library', name="New Library")

    def execute(self, context):
        new_parent_path = self.properties.new_library
        active = RendermanAssetGroup.get_from_path(self.properties.lib_path)
        if active:
            old_parent_path = os.path.split(active.path)[0]
            old_parent = RendermanAssetGroup.get_from_path(old_parent_path)
            new_parent = RendermanAssetGroup.get_from_path(new_parent_path)

            shutil.move(active.path, new_parent_path)

            refresh_assets_libraries(old_parent.path, old_parent)
            refresh_assets_libraries(new_parent.path, new_parent)
        bpy.ops.wm.save_userpref()
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        row = self.layout
        row.prop(self, "new_library", text="New Parent")


def register():
    try:
        bpy.utils.register_class(init_asset_library)
        bpy.utils.register_class(set_active_asset_library)
        bpy.utils.register_class(load_asset_to_scene)
        bpy.utils.register_class(save_asset_to_lib)
        bpy.utils.register_class(add_asset_library)
        bpy.utils.register_class(remove_asset_library)
        bpy.utils.register_class(move_asset_library)
        bpy.utils.register_class(move_asset)
        bpy.utils.register_class(remove_asset)
    except:
        pass  # allready registered


def unregister():
    bpy.utils.unregister_class(init_asset_library)
    bpy.utils.unregister_class(set_active_asset_library)
    bpy.utils.unregister_class(load_asset_to_scene)
    bpy.utils.unregister_class(save_asset_to_lib)
    bpy.utils.unregister_class(add_asset_library)
    bpy.utils.unregister_class(remove_asset_library)
    bpy.utils.unregister_class(move_asset_library)
    bpy.utils.unregister_class(move_asset)
    bpy.utils.unregister_class(remove_asset)
