# ##### BEGIN MIT LICENSE BLOCK #####
#
# Copyright (c) 2015 Brian Savery
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
import os.path
import bpy
import time
import traceback
import subprocess
import asyncio

from ..util.util import get_addon_prefs, init_env, user_path, get_path_list_converted, find_it_path
from .dspy_server import DisplayServer

PRMAN_INITED = False


def init_prman():
    ''' import prman and mark it as inited.  This is important to make sure we are not
    making calls from multiple threads to ri '''
    global prman
    import prman
    global PRMAN_INITED
    PRMAN_INITED = True


class RenderManager(object):
    """ RenderManager takes care of all the actual work for rib gen,
    and has hooks to launch processes"""

    def __init__(self, scene, engine=None, is_interactive=False, external_render=False):
        ''' Instantiate the Render Manager and set the variables needed for it '''
        self.scene = scene
        self.engine = engine
        # set the display driver
        if external_render:
            self.display_driver = scene.renderman.display_driver
        elif engine and engine.is_preview:
            self.display_driver = 'openexr'
        else:
            self.display_driver = scene.renderman.render_into

        # pass addon prefs to init_envs
        init_env()

        self.is_preview = self.engine.is_preview if engine else False
        self.scene_rm = scene.renderman
        self.initialize_paths(scene)
        self.external_render = external_render
        self.is_interactive = is_interactive
        self.is_interactive_ready = False
        self.options = []
        # check if prman is imported
        if not PRMAN_INITED:
            init_prman()
        self.ri = None

    def __del__(self):
        ''' Delete and cleanup prman if it's inited.  This is so there isn't threading issues.'''
        if self.is_interactive and self.is_prman_running():
            self.ri.EditWorldEnd()
            self.ri.End()
        if PRMAN_INITED:
            prman.Cleanup()

    def reset(self, scene):
        ''' Reset prman and reinstantiate it.'''
        if PRMAN_INITED:
            prman.Cleanup()
        self.scene = scene

    def write_rib(self):
        ''' set up ri context and Write out scene rib '''
        try:
            prman.Init()
            self.ri = prman.Ri()

            if self.is_preview:
                self.gen_preview_rib()
            else:
                self.gen_rib()
            del self.ri
            prman.Cleanup()

        except Exception as err:
            self.ri = None
            prman.Cleanup()
            self.engine.report(
                {'ERROR'}, 'Rib gen error: ' + traceback.format_exc())

    def initialize_paths(self, scene):
        ''' Expands all the output paths for this pass and makes dirs for outputs '''
        rm = self.scene_rm
        addon_prefs = get_addon_prefs()

        self.paths = {}
        out = user_path(addon_prefs.out, scene=scene)
        self.paths['scene_output_dir'] = out

        self.paths['frame_rib'] = user_path(
            addon_prefs.path_rib_output, scene=scene, out=out)
        self.paths['texture_output'] = user_path(addon_prefs.path_texture_output, scene=scene,
                                                 out=out)

        if not os.path.exists(self.paths['scene_output_dir']):
            os.makedirs(self.paths['scene_output_dir'])

        self.paths['main_image'] = user_path(addon_prefs.path_main_image, out=out,
                                             scene=scene, display_driver=self.display_driver)
        self.paths['aov_image_templ'] = user_path(addon_prefs.path_aov_image, scene=scene,
                                                  display_driver=self.display_driver, out=out)
        self.paths['shader'] = [out] + get_path_list_converted(rm, 'shader')
        self.paths['texture'] = [self.paths['texture_output']]

        if self.is_preview:
            previewdir = os.path.join(
                self.paths['scene_output_dir'], "preview")
            self.paths['frame_rib'] = os.path.join(previewdir, "preview.rib")
            self.paths['main_image'] = os.path.join(previewdir, "preview.tif")
            self.paths['scene_output_dir'] = os.path.dirname(
                self.paths['frame_rib'])
            if not os.path.exists(previewdir):
                os.mkdir(previewdir)

        static_archive_dir = os.path.dirname(user_path(addon_prefs.path_object_archive_static,
                                                       scene=scene, out=out))
        frame_archive_dir = os.path.dirname(user_path(addon_prefs.path_object_archive_animated,
                                                      scene=scene, out=out))

        self.paths['static_archives'] = static_archive_dir
        self.paths['frame_archives'] = frame_archive_dir

        if not os.path.exists(self.paths['static_archives']):
            os.makedirs(self.paths['static_archives'])
        if not os.path.exists(self.paths['frame_archives']):
            os.makedirs(self.paths['frame_archives'])
        self.paths['archive'] = os.path.dirname(static_archive_dir)
        self.paths['output_files'] = []
        self.paths['aovs_to_denoise'] = []

    def update_frame_num(self, num):
        ''' When rendering an animation we may need to use the same rpass to output multiple
            frames.  This will reset the frame number and reset paths'''
        self.scene.frame_set(num)
        self.initialize_paths(self.scene)

    def preview_render(self, engine):
        ''' For preview renders, simply render and load exr to blender swatch '''
        pass

    def render(self):
        ''' Start the PRMan render process, and if rendering to Blender, setup display driver server 
            Also reports status
        '''
        base_dir = self.paths['scene_output_dir']
        loop = asyncio.new_event_loop()

        if self.display_driver == 'it':
            it_path = find_it_path()
            if not it_path:
                self.engine.report({"ERROR"},
                                   "Could not find 'it'. Check your RenderMan installation.")
            else:
                environ = os.environ.copy()
                subprocess.Popen([it_path], env=environ, shell=True)
        elif self.display_driver == 'socket':
            driver_socket_port = 55557
            render = self.scene.render
            os.environ['DSPYSOCKET_PORT'] = str(driver_socket_port)
            server = DisplayServer(self.engine, driver_socket_port, prman)
            server.start(loop)

        async def check_status():
            started = False
            pct = 0
            # loop while rendering has started and pct returned to 0
            while True:
                await asyncio.sleep(.01)
                if started and pct == 0:
                    break
                self.engine.update_progress(pct / 100)
                if self.engine.test_break():
                    self.ri.ArchiveRecord(
                        "structure", self.ri.STREAMMARKER + "END")
                    prman.RicFlush("END", 0, self.ri.SUSPENDRENDERING)
                    loop.stop()
                    break
                pct = prman.RicGetProgress()
                if not started and pct > 0:
                    started = True

            if self.display_driver == 'it':
                loop.stop()

        try:
            prman.Init()
            self.ri = prman.Ri()

            if self.is_interactive:

                self.ri.Begin(
                    "launch:prman? -ctrl $ctrlin $ctrlout -t:-1 -dspyserver it")

                self.ri.ArchiveBegin("frame_rib")
                self.frame_rib()
                self.ri.ArchiveEnd()

                # record archive of frame
                self.interactive_initial_rib()
                self.is_interactive_ready = True

            else:
                self.ri.Begin("launch:prman? -ctrl $ctrlin $ctrlout -t:-1")
                self.frame_rib()

                asyncio.set_event_loop(loop)
                asyncio.Task(check_status())
                loop.run_forever()
                self.engine.update_progress(1)

                if self.display_driver == 'socket':
                    server.stop(loop)

                self.ri.End()
                del self.ri
                prman.Cleanup()

        except Exception as err:
            if self.display_driver == 'socket':
                server.stop(loop)
            self.ri = None
            prman.Cleanup()
            self.engine.report(
                {'ERROR'}, 'Rib gen error: ' + traceback.format_exc())

    def is_prman_running(self):
        ''' Uses Rix interfaces to get progress on running IPR or render '''
        return prman.RicGetProgress() < 100

    def gen_rib(self):
        ''' sets up for rib generation
        '''
        time_start = time.time()
        rib_options = {"string format": "ascii",
                       "string asciistyle": "indented,wide"}
        self.ri.Option("rib", rib_options)
        self.cache_archives()
        # self.frame_rib()
        if self.engine:
            self.engine.report({"INFO"}, "RIB generation took %s" %
                               str(time.time() - time_start))

    def cache_archives(self, clear_motion=False):
        ''' Does all the caching nescessary for generating a render rib, first caches motion blur 
            items, then outputs geometry caches,
        '''
        # cache motion first and write out data archives
        self.scene_rm.cache_motion(self.ri, self)
        for ob in self.scene.objects:
            items = ob.renderman.get_data_items()
            if items:
                for data in items:
                    data_rm = data.renderman
                    try:
                        archive_filename = data_rm.get_archive_filename(
                            paths=self.paths, ob=ob)
                        if archive_filename:
                            self.ri.Begin(archive_filename)
                            data_rm.to_rib(self.ri, ob=ob, scene=self.scene)
                            self.ri.End()
                    except:
                        self.engine.report({'ERROR'},
                                           'Rib gen error object %s data %s: ' % (ob.name, data.name) +
                                           traceback.format_exc())

        if clear_motion:
            self.scene_rm.clear_motion()

    def frame_rib(self):
        ''' Do the Frame_rib '''
        self.scene_rm.to_rib(self.ri, paths=self.paths,
                             display_driver=self.display_driver)
        self.scene_rm.clear_motion()

    def gen_preview_rib(self):
        ''' generates a preview rib file '''
        self.ri.Begin(self.paths['frame_rib'])
        self.scene_rm.to_rib(self.ri, preview=True)
        self.ri.End()

    def ipr_update(self):
        ''' Issue any needed ipr updates for the given scene.  If nescessary rebuild the scene
            rib and get that ready to restart '''
        scene = self.scene
        # these are the updates we can do
        to_update = {}

        # check if scene is updated
        to_update['scene'] = scene if scene.is_updated else None

        # check for material updates and issue them
        to_update['materials'] = [
            mat for mat in bpy.data.materials if mat.is_updated]

        # check if world is updated
        to_update['world'] = scene.world if scene.world.is_updated else None

        # get the lamp shaders, these don't need restart
        to_update['lamp_shaders'] = [ob.data for ob in scene.objects if ob.type == 'LAMP'
                                     and ob.is_updated_data]

        # get the lamps
        to_update['lamps'] = [
            ob for ob in scene.objects if ob.type == 'LAMP' and ob.is_updated]

        # get the camera if updated
        to_update['camera'] = scene.camera if scene.camera.is_updated else None

        # get all data items updated
        to_update['data'] = [data for ob in scene.objects if ob.type not in ['LAMP', 'CAMERA']
                             for data in ob.renderman.get_updated_data_items()]

        # get all updated objects
        to_update['objects'] = [ob for ob in scene.objects if ob.is_updated]
        if len(to_update['objects']):
            self.ri.ArchiveBegin("frame_rib")
            self.frame_rib()
            self.ri.ArchiveEnd()

            self.ri.EditWorldEnd()
            self.ri.EditWorldBegin(
                "frame_rib", {"string rerenderer": "raytrace"})
            self.ri.Option('rerender', {'int[2] lodrange': [0, 3]})
            # self.ri.ReadArchive("frame_rib")

            self.ri.ArchiveRecord(
                "structure", self.ri.STREAMMARKER + "_initial")
            prman.RicFlush("_initial", 0, self.ri.FINISHRENDERING)

            self.ri.EditBegin('null', {})
            self.ri.EditEnd()

    def interactive_initial_rib(self):
        self.ri.Display('rerender', 'it', 'rgba')
        self.ri.Hider('raytrace', {
            'int maxsamples': 0,
            'int minsamples': 128,
            'int incremental': 1
        })

        self.ri.EditWorldBegin("frame_rib", {"string rerenderer": "raytrace"})
        self.ri.Option('rerender', {'int[2] lodrange': [0, 3]})
        # self.ri.ReadArchive("frame_rib")

        self.ri.ArchiveRecord("structure", self.ri.STREAMMARKER + "_initial")
        prman.RicFlush("_initial", 0, self.ri.FINISHRENDERING)

        self.ri.EditBegin('null', {})
        self.ri.EditEnd()
