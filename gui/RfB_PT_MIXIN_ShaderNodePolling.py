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
# RenderManForBlender Imports
#
from . RfB_PT_MIXIN_PanelIcon import RfB_PT_MIXIN_PanelIcon


class RfB_PT_MIXIN_ShaderNodePolling(RfB_PT_MIXIN_PanelIcon):
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
