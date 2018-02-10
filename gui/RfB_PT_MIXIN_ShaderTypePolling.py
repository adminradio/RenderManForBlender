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


#
# RenderManForBlender Imports
#
# from . import icons

from . RfB_PT_MIXIN_Panel import RfB_PT_MIXIN_Panel


class RfB_PT_MIXIN_ShaderTypePolling(RfB_PT_MIXIN_Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    COMPAT_ENGINES = {'PRMAN_RENDER'}

    shader_type = 'surface'
    param_exclude = {}

    @classmethod
    def poll(cls, context):
        rd = context.scene.render

        if cls.bl_context == 'data' and cls.shader_type == 'light':
            return (hasattr(context, "lamp")
                    and context.lamp is not None
                    and rd.engine in {'PRMAN_RENDER'}
                    )
        elif cls.bl_context == 'world':
            return (hasattr(context, "world")
                    and context.world is not None
                    and rd.engine in {'PRMAN_RENDER'}
                    )
        elif cls.bl_context == 'material':
            return (hasattr(context, "material")
                    and context.material is not None
                    and rd.engine in {'PRMAN_RENDER'}
                    )
