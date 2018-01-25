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

import bpy.utils
from bpy.props import *
from bpy.types import PropertyGroup

from . import assets
from .. import rfb
from .. rfb import utils

# This file holds the properties for the asset browser.
# They will be parsed from the json file

# get the enum items

# an actual asset


class RendermanAsset(PropertyGroup):
    bl_label = "RenderMan Asset Group"
    bl_idname = 'RendermanAsset'

    # def get_enum_items(self, context):
    #    return assets.enum_items

    @classmethod
    def get_from_path(cls, lib_path):
        if not lib_path:
            return
        group_path, asset = os.path.split(lib_path)

        group = RendermanAssetGroup.get_from_path(group_path)
        return group.assets[asset] if asset in group.assets.keys() else None

    name = StringProperty(default='')
    label = StringProperty(default='')
    #thumbnail = EnumProperty(items=get_enum_items)
    thumb_path = StringProperty(subtype='FILE_PATH')
    path = StringProperty(subtype='FILE_PATH')
    json_path = StringProperty(subtype='FILE_PATH')


# forward define asset group
class RendermanAssetGroup(PropertyGroup):
    bl_label = "RenderMan Asset Group"
    bl_idname = 'RendermanAssetGroup'
    pass

# A property group holds assets and sub groups


class RendermanAssetGroup(PropertyGroup):
    bl_label = "RenderMan Asset Group"
    bl_idname = 'RendermanAssetGroup'

    @classmethod
    def get_from_path(cls, lib_path):
        ''' get from abs lib_path '''
        head = rfb.reg.prefs().assets_library
        lib_path = os.path.relpath(lib_path, head.path)
        active = head
        for sub_path in lib_path.split(os.sep):
            if sub_path in active.sub_groups.keys():
                active = active.sub_groups[sub_path]
        return active

    # get the active library from the addon pref
    @classmethod
    def get_active_library(cls):
        active_path = rfb.reg.prefs().active_assets_path
        if active_path != '':
            return cls.get_from_path(active_path)
        else:
            return None

    name = StringProperty(default='')
    ui_open = BoolProperty(default=True)

    def generate_previews(self, context):
        return assets.load_previews(self)

    path = StringProperty(default='')
    assets = CollectionProperty(type=RendermanAsset)
    current_asset = EnumProperty(items=generate_previews, name='Current Asset')

    # gets the assets and all from children
    def get_assets(self):
        all_assets = self.assets[:]
        for group in self.sub_groups:
            all_assets += group.get_assets()
        return all_assets

    def is_active(self):
        return self.path == rfb.reg.prefs().active_assets_path


def register():
    try:
        bpy.utils.register_class(RendermanAsset)
        bpy.utils.register_class(RendermanAssetGroup)

        # set sub groups type we have to do this after registered
        sub_groups = CollectionProperty(type=RendermanAssetGroup)
        setattr(RendermanAssetGroup, 'sub_groups', sub_groups)

    except:
        pass  # allready registered


def unregister():
    bpy.utils.unregister_class(RendermanAssetGroup)
    bpy.utils.unregister_class(RendermanAsset)
