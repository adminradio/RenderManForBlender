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
# RenderManForBlender Imports
#
from . RM_ShaderNodeBase import RM_ShaderNodeBase


class RM_OutputNode(RM_ShaderNodeBase):
    bl_label = 'RenderMan Material'
    renderman_node_type = 'output'
    bl_icon = 'MATERIAL'
    node_tree = None

    def init(self, context):
        input = self.inputs.new('RendermanShaderSocket', 'Bxdf')
        input.type = 'SHADER'
        input.hide_value = True
        input = self.inputs.new('RendermanShaderSocket', 'Light')
        input.hide_value = True
        input = self.inputs.new('RendermanShaderSocket', 'Displacement')
        input.hide_value = True

    def draw_buttons(self, context, layout):
        return

    def draw_buttons_ext(self, context, layout):
        return

    # when a connection is made or removed see if we're in IPR mode and issue
    # updates
    def update(self):
        from .. import engine
        if engine.is_ipr_running():
            engine.ipr.last_edit_mat = None
            engine.ipr.issue_shader_edits(nt=self.id_data)
