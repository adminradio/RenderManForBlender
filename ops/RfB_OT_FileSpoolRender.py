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
# Python Imports
#
import os
import traceback
import subprocess


#
# Blender Imports
#
import bpy


#
# RenderMan for Blender Imports
#
from .. import engine

from .. utils import user_path
from .. utils import find_local_queue
from .. utils import find_tractor_spool

from .. import rfb

from .. import spool   # import spool_render
from .. export import get_texture_list


class RfB_OT_FileSpoolRender(bpy.types.Operator):
    bl_idname = "rfb.file_spool_render"
    bl_label = "External Render"
    bl_description = "Launch and external render outside Blender"
    rpass = None
    is_running = False

    def gen_rib_frame(self, rpass, do_objects):
        try:
            rpass.gen_rib(do_objects, convert_textures=False)
        except Exception as err:
            self.report(
                {'ERROR'},
                'RIB generation error: ' + traceback.format_exc())

    def gen_denoise_aov_name(self, scene, rpass):
        addon_prefs = rfb.reg.prefs()
        files = []
        rm = scene.renderman
        for layer in scene.render.layers:
            # custom aovs
            rm_rl = None
            for render_layer_settings in rm.render_layers:
                if layer.name == render_layer_settings.render_layer:
                    rm_rl = render_layer_settings
            if rm_rl:
                layer_name = layer.name.replace(' ', '')
                if rm_rl.denoise_aov:
                    if rm_rl.export_multilayer:
                        dspy_name = user_path(
                            addon_prefs.path_aov_image,
                            scene=scene,
                            display_driver=rpass.display_driver,
                            layer_name=layer_name,
                            pass_name='multilayer')

                        files.append(dspy_name)
                    else:
                        for aov in rm_rl.custom_aovs:
                            aov_name = aov.name.replace(' ', '')
                            dspy_name = user_path(
                                addon_prefs.path_aov_image, scene=scene, display_driver=rpass.display_driver,
                                layer_name=layer_name, pass_name=aov_name)
                            files.append(dspy_name)
        return files

    def execute(self, context):
        if engine.ipr:
            self.report(
                {"ERROR"}, 'Please stop IPR before rendering externally')
            return {'FINISHED'}
        scene = context.scene
        rpass = engine.RPass(scene, external_render=True)
        rm = scene.renderman
        render_output = rpass.paths['render_output']
        images_dir = os.path.split(render_output)[0]
        aov_output = rpass.paths['aov_output']
        aov_dir = os.path.split(aov_output)[0]
        do_rib = rm.generate_rib
        do_objects = rm.generate_object_rib
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        if not os.path.exists(aov_dir):
            os.makedirs(aov_dir)
        if not os.path.exists(rpass.paths['texture_output']):
            os.mkdir(rpass.paths['texture_output'])

        # rib gen each frame
        rpass.display_driver = scene.renderman.display_driver
        rib_names = []
        denoise_files = []
        denoise_aov_files = []
        job_tex_cmds = []
        frame_tex_cmds = {}
        if rm.external_animation:
            rpass.update_frame_num(scene.frame_end + 1)
            rpass.update_frame_num(scene.frame_start)
            if rm.convert_textures:
                tmp_tex_cmds = get_texture_list(rpass.scene)
                tmp2_cmds = get_texture_list(rpass.scene)
                job_tex_cmds = [
                    cmd for cmd in tmp_tex_cmds if cmd in tmp2_cmds]

            for frame in range(scene.frame_start, scene.frame_end + 1):
                rpass.update_frame_num(frame)
                if do_rib:
                    self.report(
                        {'INFO'}, 'RenderMan External Rendering generating rib for frame %d' % scene.frame_current)
                    self.gen_rib_frame(rpass, do_objects)
                rib_names.append(rpass.paths['rib_output'])
                if rm.convert_textures:
                    frame_tex_cmds[frame] = [cmd for cmd in get_texture_list(
                        rpass.scene) if cmd not in job_tex_cmds]
                if rm.external_denoise:
                    denoise_files.append(rpass.get_denoise_names())
                    if rm.spool_denoise_aov:
                        denoise_aov_files.append(
                            self.gen_denoise_aov_name(scene, rpass))

        else:
            if do_rib:
                self.report(
                    {'INFO'}, 'RenderMan External Rendering generating rib for frame %d' % scene.frame_current)
                self.gen_rib_frame(rpass, do_objects)
            rib_names.append(rpass.paths['rib_output'])
            if rm.convert_textures:
                frame_tex_cmds = {scene.frame_current: get_texture_list(scene)}
            if rm.external_denoise:
                denoise_files.append(rpass.get_denoise_names())
                if rm.spool_denoise_aov:
                    denoise_aov_files.append(
                        self.gen_denoise_aov_name(scene, rpass))

        # gen spool job
        if rm.generate_alf:
            denoise = rm.external_denoise
            to_render = rm.generate_render
            rm_version = rm.path_rmantree.split('-')[-1]
            rm_version = rm_version.strip('/\\')
            if denoise:
                denoise = 'crossframe' if rm.crossframe_denoise and scene.frame_start != scene.frame_end and rm.external_animation else 'frame'
            frame_begin = scene.frame_start if rm.external_animation else scene.frame_current
            frame_end = scene.frame_end if rm.external_animation else scene.frame_current
            alf_file = spool.render(
                str(rm_version), to_render, rib_names, denoise_files, denoise_aov_files, frame_begin, frame_end, denoise, context, job_texture_cmds=job_tex_cmds, frame_texture_cmds=frame_tex_cmds, rpass=rpass)

            # if spooling send job to queuing
            if rm.do_render:
                exe = find_tractor_spool() if rm.queuing_system == 'tractor' else find_local_queue()
                self.report(
                    {'INFO'}, 'RenderMan External Rendering spooling to %s.' % rm.queuing_system)
                subprocess.Popen([exe, alf_file])

        rpass = None
        return {'FINISHED'}
