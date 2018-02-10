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
# import os

#
# Blender Imports
#
import bpy

#
# RenderManForBlender Imports
#
from .. rfb.lib.echo import stdmsg
from .. rfb.lib.echo import stdadd
from .. rfb.lib.file import rfb_examples


class RfB_OT_STUB_DevelOperator(bpy.types.Operator):
    bl_idname = 'rfb.stub_devel_operator'
    bl_label = "Stub Operator (Developer)"
    bl_description = "A developer operator for drafting OPS."

    def invoke(self, context, event=None):
        scn = context.scene  # noqa
        rmn = context.scene.renderman  # noqa

        print()
        stdmsg('DEVOP: Found RenderMan For Blender Examples:')
        for item in rfb_examples():
            stdadd(item)
        print()

        cancelled = False
        return {'CANCELLED'} if cancelled else {'FINISHED'}
