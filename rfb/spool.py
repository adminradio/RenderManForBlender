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
import os
import time

#
# Blender Imports
#
import bpy

#
# RenderManForBlender Imports
#
from . prf import pref
from . lib.file import quote
from . lib.path import expand


def end_block(f, lvl):
    f.write("%s}\n" % ('\t' * lvl))


def w_parents(f, title, serial_subtasks, lvl):
    i = '\t' * lvl
    s = int(serial_subtasks)
    f.write("%sTask {%s} -serialsubtasks %d -subtasks {\n" % (i, title, s))


def w_commands(f, title, cmds, lvl):
    j = " "  # joiner

    #
    # open level
    #
    i = '\t' * lvl  # current indent
    f.write("%sTask {%s} -cmds {\n" % (i, title))

    #
    # write sublevel(s)
    #
    ii = '\t' * (lvl + 1)  # next indent
    for k, v in cmds:
        f.write("%sRemoteCmd -service {%s} {%s}\n" % (ii, k, j.join(v)))

    #
    # close level
    #
    f.write("%s}\n" % (i))


def txmake_task(f, title, ifn, ofn, options, lvl):
    cmd = ['txmake'] + options + ['-newer'] + [ifn, ofn]
    w_commands(f, title, [('PixarRender', cmd)], lvl)


def render(rman_version_short,
           to_render,
           rib_files,
           denoise_files,
           denoise_aov_files,
           frame_begin,
           frame_end=None,
           denoise=None,
           context=None,
           job_texture_cmds=[],
           frame_texture_cmds={},
           rpass=None,
           bake=False):

    frb = frame_begin
    fre = frame_end
    odr = pref('env_vars').out
    cdr = expand(odr)
    scn = context.scene
    rmn = scn.renderman

    _t_ = time.strftime("%m%d%y%H%M%S")
    alf_file = os.path.join(cdr, 'bake_%s.alf' % _t_) \
        if bake \
        else os.path.join(cdr, rmn.custom_alfname + '_%s.alf' % _t_)

    f_dnoise = denoise == 'frame'
    x_dnoise = denoise == 'crossframe'

    # open file
    f = open(alf_file, 'w')

    # write header
    f.write('##AlfredToDo 3.0\n')

    # job line
    job_title = os.path.splitext(os.path.split(bpy.data.filepath)[1])[0] \
        if bpy.data.filepath else 'untitled'

    job_title += " frames %d-%d" % (frb, fre) if fre else " frame %d" % frb

    if f_dnoise:
        job_title += ' per-frame denoise'

    elif x_dnoise:
        job_title += ' crossframe_denoise'

    job_params = {
        'title': job_title,
        'serialsubtasks': 1,
        'envkey': 'prman-%s' % rman_version_short,
        'comment': 'Created by RenderMan for Blender'
    }

    jstr = 'Job'
    for k, v in job_params.items():
        if k == 'serialsubtasks':
            jstr += " -%s %s" % (k, str(v))
        else:
            jstr += " -%s {%s}" % (k, str(v))

    f.write(jstr + ' -subtasks {' + '\n')

    #
    # collect textures find frame specific and job specific
    #
    if job_texture_cmds:
        w_parents(f, 'Job Textures', False, 1)

    #
    # do job txmake texture(s)
    #
    for ifn, ofn, options in job_texture_cmds:
        ifn = bpy.path.abspath(ifn)
        ofn = os.path.join(rpass.paths['texture_output'], ofn)
        txmake_task(
            f, "TxMake %s" % os.path.split(ifn)[-1],
            quote(ifn), quote(ofn), options, 2
        )

    if job_texture_cmds:
        end_block(f, 1)

    w_parents(f, 'Frame Renders', False, 1)

    #
    # do txmake for frame(s)
    #
    if fre is None:
        fre = frb

    for frn in range(frb, fre + 1):
        if frn in frame_texture_cmds or denoise:
            w_parents(f, 'Frame %d' % frn, True, 2)

        #
        # do frame specific txmake
        #
        if frn in frame_texture_cmds:
            w_parents(f, 'Frame %d textures' % frn, False, 3)

            for ifn, ofn, options in frame_texture_cmds[frn]:
                ifn = bpy.path.abspath(ifn)
                ofn = os.path.join(rpass.paths['texture_output'], ofn)
                txmake_task(
                    f, "TxMake %s" % os.path.split(ifn)[-1],
                    quote(ifn), quote(ofn), options, 4
                )
            end_block(f, 3)

        #
        # render frame
        #
        if to_render:
            threads = rmn.threads \
                if not rmn.override_threads \
                else rmn.external_threads

            cmd_str = [
                'prman',
                '-Progress',
                '-cwd',
                quote(cdr),
                '-t:%d' % threads,
                quote(rib_files[frn - frb])
            ]

            if rmn.enable_checkpoint:
                if rmn.render_limit == 0:
                    a = rmn.checkpoint_interval
                    b = rmn.checkpoint_type
                    cmd_str.insert(5, '-checkpoint %d%s' % (a, b))
                else:
                    a = rmn.checkpoint_interval
                    b = rmn.checkpoint_type
                    c = rmn.render_limit
                    d = rmn.checkpoint_type
                    cmd_str.insert(5, '-checkpoint %d%s,%d%s' % (a, b, c, d))

            if rmn.recover:
                cmd_str.insert(5, '-recover 1')

            if rmn.custom_cmd != '':
                cmd_str.insert(5, rmn.custom_cmd)

            w_commands(
                f, 'Render frame %d' % frn, [('PixarRender', cmd_str)], 3
            )

        #
        # denoise single frame
        #
        if f_dnoise:
            j = " "
            dafs = denoise_aov_files
            denoise_options = []
            if rmn.denoise_cmd != '':
                denoise_options.append(rmn.denoise_cmd)
            if rmn.spool_denoise_aov and dafs != []:
                denoise_options.insert(0, '--filtervariance 1')

                cmd_str = (
                    ['denoise']
                    + denoise_options
                    + [quote(denoise_files[frn - frb][0])]
                    + [j.join([quote(file) for file in dafs[frn - frb]])]
                )
            else:
                if rmn.denoise_gpu:
                    denoise_options.append('--override gpuIndex 0 --')

                cmd_str = (
                    ['denoise']
                    + denoise_options
                    + [quote(denoise_files[frn - frb][0])]
                )

            w_commands(
                f, 'Denoise frame %d' % frn, [('PixarRender', cmd_str)], 3
            )

        #
        # cross frame denoise
        #
        elif x_dnoise:
            denoise_options = ['--crossframe -v variance', '-F 1', '-L 1']

            if rmn.spool_denoise_aov and denoise_aov_files != []:
                denoise_options.append('--filtervariance 1')

            if rmn.denoise_cmd != '':
                denoise_options.append(rmn.denoise_cmd)

            if rmn.denoise_gpu and not rmn.spool_denoise_aov:
                denoise_options.append('--override gpuIndex 0 --')

            if frn - frb < 1:
                pass

            elif frn - frb == 1:
                denoise_options.remove('-F 1')
                cmd_str = (
                    ['denoise']
                    + denoise_options
                    + [quote(f[0]) for f in denoise_files[0:2]]
                )

                if rmn.spool_denoise_aov and denoise_aov_files != []:
                    files = [
                        quote(item)
                        for sublist in denoise_aov_files[0:2]
                        for item in sublist
                    ]

                    cmd_str = (
                        ['denoise']
                        + denoise_options
                        + [quote(f[0]) for f in denoise_files[0:2]] + files
                    )
                w_commands(
                    f, 'Denoise frame %d' % (frn - 1),
                    [('PixarRender', cmd_str)], 3
                )

            else:
                cmd_str = (
                    ['denoise']
                    + denoise_options
                    + [
                        quote(f[0])
                        for f in
                        denoise_files[frn - frb - 2:frn - frb + 1]
                    ]
                )

                if rmn.spool_denoise_aov and denoise_aov_files != []:
                    files = [
                        quote(item)
                        for sublist in
                        denoise_aov_files[frn - frb - 2:frn - frb + 1]
                        for item in sublist
                    ]

                    cmd_str = (
                        ['denoise']
                        + denoise_options
                        + [
                            quote(f[0])
                            for f in
                            denoise_files[frn - frb - 2:frn - frb + 1]
                        ]
                        + files
                    )

                w_commands(
                    f, 'Denoise frame %d' % (frn - 1),
                    [('PixarRender', cmd_str)], 3
                )

            if frn == fre:
                denoise_options.remove('-L 1')

                cmd_str = (
                    ['denoise']
                    + denoise_options
                    + [
                        quote(f[0])
                        for f in denoise_files[frn - frb - 1:frn - frb + 1]
                    ]
                )

                if rmn.spool_denoise_aov and denoise_aov_files != []:
                    files = [
                        quote(item)
                        for sublist in
                        denoise_aov_files[frn - frb - 1:frn - frb + 1]
                        for item in sublist
                    ]

                    cmd_str = (
                        ['denoise']
                        + denoise_options
                        + [
                            quote(f[0])
                            for f in
                            denoise_files[frn - frb - 1:frn - frb + 1]
                        ]
                        + files)

                w_commands(
                    f, 'Denoise frame %d' % frn,
                    [('PixarRender', cmd_str)], 3
                )

        if denoise or frn in frame_texture_cmds:
            end_block(f, 2)

    end_block(f, 1)

    # end job
    f.write("}\n")
    f.close()
    return alf_file
