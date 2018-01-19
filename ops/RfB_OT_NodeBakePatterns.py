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
# ##### END MIT LICENSE BLOCK ####

#
# python imports
#
import os
import subprocess
import traceback

#
# blender imports
#
import bpy

#
# RenderMan for Blender imports
#
from .. import engine
from .. utils import find_local_queue
from .. utils import find_tractor_spool
from .. rfb import spool
from .. export import get_texture_list


class RfB_OT_NodeBakePatterns(bpy.types.Operator):
    bl_idname = "rfb.bake_pattern_nodes"
    bl_label = "Bake Pattern Nodes"
    bl_description = "Bake pattern nodes to texture."
    rpass = None
    is_running = False

    def gen_rib_frame(self, rpass):
        try:
            rpass.gen_rib(convert_textures=False)
        except Exception as err:
            self.report({'ERROR'}, 'Rib gen error: ' + traceback.format_exc())

    def execute(self, context):
        if engine.ipr:
            self.report(
                {"ERROR"}, 'Please stop IPR before baking')
            return {'FINISHED'}

        scene = context.scene
        rpass = engine.RPass(scene, external_render=True, bake=True)
        rm = scene.renderman
        rpass.display_driver = scene.renderman.display_driver

        if not os.path.exists(rpass.paths['texture_output']):
            os.mkdir(rpass.paths['texture_output'])

        self.report(
            {'INFO'}, 'RenderMan External Rendering generating rib for frame %d' % scene.frame_current)

        self.gen_rib_frame(rpass)

        rib_names = rpass.paths['rib_output']
        frame_tex_cmds = {scene.frame_current: get_texture_list(scene)}
        rm_version = rm.path_rmantree.split('-')[-1]
        rm_version = rm_version.strip('/\\')
        frame_begin = scene.frame_current
        frame_end = scene.frame_current
        to_render = True
        denoise_files = []
        denoise_aov_files = []
        job_tex_cmds = []
        denoise = False
        alf_file = spool.render(str(rm_version), to_render, [rib_names], denoise_files, denoise_aov_files, frame_begin, frame_end, denoise, context, job_texture_cmds=job_tex_cmds, frame_texture_cmds=frame_tex_cmds, rpass=rpass, bake=True)
        exe = find_tractor_spool() if rm.queuing_system == 'tractor' else find_local_queue()

        self.report(
            {'INFO'},
            'RenderMan Baking spooling to %s.' % rm.queuing_system)

        subprocess.Popen([exe, alf_file])

        rpass = None
        return {'FINISHED'}
