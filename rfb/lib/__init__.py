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
# TODO:   Refactor functions by type into separate modules, i.e:
#         clamp() -> math.clamp()
#         get_path_list() -> path.dir()
#         readOSO() -> file.read_oso()
#         etc.
#
#         And everything related to env, prefs, cli tools, paths, etc.
#         should be refactored into root module 'rfb'
#
#  DATE:  2018-01-17
# AUTHOR: Timm Wimmers
# STATUS: -unassigned-
#

#
# Python imports
#
import re
import os
import sys
import fnmatch
import platform
import mathutils
import subprocess
from pathlib import Path


#
# Blender Imports
#
import bpy


#
# RenderMan for Blender Imports
#
from . prfs import pref
from . math import clamp
from . echo import debug

from . import rman
from . import tmpl

#
# Developer options are candidates for user prefs!
#
DEBUG = pref('rfb_debug')
INFOS = pref('rfb_info')


def getattr_recursive(ptr, attrstring):
    for attr in attrstring.split("."):
        ptr = getattr(ptr, attr)

    return ptr


def get_real_path(path):
    p = str(Path(path).resolve())
    # p = os.path.realpath(efutil.filesystem_path(path))
    print("get_real_path(): " + p)
    return p


#
# return a list of meta tuples
#
def get_osl_line_meta(line):
    if "%%meta" not in line:
        return {}
    meta = {}
    for m in re.finditer('meta{', line):
        sub_str = line[m.start(), line.find('}', beg=m.start())]
        item_type, item_name, item_value = sub_str.split(',', 2)
        val = item_value
        if item_type == 'string':
            val = val[1:-1]
        elif item_type == 'int':
            val = int(val)
        elif item_type == 'float':
            val = float(val)

        meta[item_name] = val
    return meta


def locate_openVDB_cache(frameNum):
    if not bpy.data.is_saved:
        return None
    filename = os.path.splitext(os.path.split(bpy.data.filepath)[1])[0]
    cacheDir = os.path.join(bpy.path.abspath("//"), 'blendcache_%s' % filename)
    if not os.path.exists(cacheDir):
        return None
    for f in os.listdir(os.path.join(bpy.path.abspath("//"), cacheDir)):
        if '.vdb' in f and "%06d" % frameNum in f:
            return os.path.join(bpy.path.abspath("//"), cacheDir, f)

    return None


def readOSO(filePath):
    line_number = 0
    shader_meta = {}
    prop_names = []
    shader_meta["shader"] = os.path.splitext(os.path.basename(filePath))[0]
    with open(filePath, encoding='utf-8') as osofile:
        for line in osofile:
            # if line.startswith("surface") or line.startswith("shader"):
            #    line_number += 1
            #    listLine = line.split()
            #    shader_meta["shader"] = listLine[1]
            if line.startswith("param"):
                line_number += 1
                listLine = line.split()
                name = listLine[2]
                type = listLine[1]
                if type == "point" or type == "vector" or type == "normal" or \
                        type == "color":
                    defaultString = []
                    defaultString.append(listLine[3])
                    defaultString.append(listLine[4])
                    defaultString.append(listLine[5])
                    default = []
                    for element in defaultString:
                        default.append(float(element))
                elif type == "matrix":
                    default = []
                    x = 3
                    while x <= 18:
                        default.append(float(listLine[x]))
                        x += 1
                elif type == "closure":
                    debug('error', "Closure types are not supported")
                    # type = "void"
                    # name = listLine[3]
                else:
                    default = listLine[3]

                prop_names.append(name)
                prop_meta = {"type": type, "default": default, "IO": "in"}
                for tup in listLine:
                    if tup == '%meta{int,lockgeom,0}':
                        prop_meta['lockgeom'] = 0
                        break
                prop_meta.update(get_osl_line_meta(line))
                shader_meta[name] = prop_meta
            elif line.startswith("oparam"):
                line_number += 1
                listLine = line.split()
                name = listLine[2]
                type = listLine[1]
                if type == "point" or type == "vector" or type == "normal" or \
                        type == "color":
                    default = []
                    default.append(listLine[3])
                    default.append(listLine[4])
                    default.append(listLine[5])
                elif type == "matrix":
                    default = []
                    x = 3
                    while x <= 18:
                        default.append(listLine[x])
                        x += 1
                elif type == "closure":
                    debug('error', "Closure types are not supported")
                    type = "void"
                    name = listLine[3]
                else:
                    default = listLine[3]
                prop_names.append(name)
                prop_meta = {"type": type, "default": default, "IO": "out"}
                prop_meta.update(get_osl_line_meta(line))
                shader_meta[name] = prop_meta
            else:
                line_number += 1
    return prop_names, shader_meta


def get_Selected_Objects(scene):
    objectNames = []
    for obj in scene.objects:
        if obj.select:
            objectNames.append(obj.name)
    return objectNames


# -------------------- Path Handling -----------------------------
#
# convert multiple path delimiters from : to ;
# converts both windows style paths (x:C:\blah -> x;C:\blah)
# and unix style (x:/home/blah -> x;/home/blah)
#
def path_delimit_to_semicolons(winpath):
    return re.sub(r'(:)(?=[A-Za-z]|\/)', r';', winpath)


def args_files_in_path(prefs, idblock, shader_type='', threaded=True):
    init_env(prefs)
    args = {}

    path_list = get_path_list_converted(prefs, 'args')
    for path in path_list:
        #
        # TODO:   Refactor path handling
        #         https://github.com/adminradio/RenderManForBlender/issues/3
        # DATE:   2018-01-22
        # AUTHOR: Timm Wimmers
        # STATUS: assigned to self
        #
        # QUICKFIX: because of moving this from 'utils.py' to 'rfb/lib'
        if platform.system() == 'Windows':
            path = path.replace("\\rfb\\lib", "")
        else:
            path = path.replace("/rfb/lib", "")
        # QUICKFIX end
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.args'):
                args[filename.split('.')[0]] = os.path.join(root, filename)
    return args


def get_path_list(rm, type):
    paths = []
    if rm.use_default_paths:
        #
        # here for getting args
        #
        if type == 'args':
            rmantree = guess_rmantree()
            paths.append(os.path.join(rmantree, 'lib', 'plugins'))
            paths.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      'data', 'args'))
        if type == 'shader':
            paths.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      'data', 'shaders'))
            paths.append(os.path.join(bpy.utils.resource_path('LOCAL'), 'scripts',
                                      'addons', 'cycles', 'shader'))
            paths.append(os.path.join('${RMANTREE}', 'lib', 'shaders'))
        paths.append('@')

    if rm.use_builtin_paths:
        paths.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  "%ss" % type))

    if hasattr(rm, "%s_paths" % type):
        for p in getattr(rm, "%s_paths" % type):
            paths.append(bpy.path.abspath(p.name))

    return paths


#
# Convert env variables to full paths.
#
def path_list_convert(path_list, to_unix=False):
    paths = []

    for p in path_list:
        p = os.path.expanduser(p)

        if p.find('$') != -1:
            # path contains environment variables
            # p = p.replace('@', os.path.expandvars('$DL_SHADERS_PATH'))
            # convert path separators from : to ;
            p = path_delimit_to_semicolons(p)

            if to_unix:
                p = path_win_to_unixy(p)

            envpath = ''.join(p).split(';')
            paths.extend(envpath)
        else:
            if to_unix:
                p = path_win_to_unixy(p)
            paths.append(p)

    return paths


def get_path_list_converted(rm, type, to_unix=False):
    return path_list_convert(get_path_list(rm, type), to_unix)


#
# TODO:   Oh man, please comment your additions/deletions!
#         IS THIS A STUB OR CAN THIS BE REFACTORED OUT?
#
# DATE:   2018-02-05
# AUTHOR: Timm Wimmers
# STATUS: -unassigned-
#
def path_win_to_unixy(winpath, escape_slashes=False):
    # if escape_slashes:
    #    p = winpath.replace('\\', '\\\\')
    # else:
    #    # convert pattern C:\\blah to //C/blah so 3delight can understand
    #    p = re.sub(r'([A-Za-z]):\\', r'//\1/', winpath)
    #    p = p.replace('\\', '/')
    return winpath


def get_sequence_path(path, blender_frame, anim):
    if not anim.animated_sequence:
        return path

    frame = blender_frame - anim.blender_start + anim.sequence_in

    # hold
    frame = clamp(frame, anim.sequence_in, anim.sequence_out)
    return tmpl.hashnum(path, frame)


def rib_path(path, escape_slashes=False):
    _p_ = path_win_to_unixy(
        bpy.path.abspath(path), escape_slashes=escape_slashes
    )
    print("RFB-DBG - rib_path() -> In:  {}".format(path))
    print("RFB-DBG - rib_path() -> Out: {}".format(_p_))
    return _p_


#
# return a list of properties set on this group
#
def get_properties(prop_group):
    props = []
    for (key, prop) in prop_group.bl_rna.properties.items():
        # This is somewhat ugly, but works best!!
        if key not in ['rna_type', 'name']:
            props.append(prop)
    return props


def rmantree_from_env():
    RMANTREE = ''

    if 'RMANTREE' in os.environ.keys():
        RMANTREE = os.environ['RMANTREE']
    return RMANTREE


def set_pythonpath(path):
    sys.path.append(path)


def set_rmantree(rmantree):
    os.environ['RMANTREE'] = rmantree


def set_path(paths):
    for path in paths:
        if path is not None:
            os.environ['PATH'] = path + os.pathsep + os.environ['PATH']


def check_valid_rmantree(rmantree):
    prman = 'prman.exe' if platform.system() == 'Windows' else 'prman'

    if os.path.exists(rmantree) and \
       os.path.exists(os.path.join(rmantree, 'bin')) and \
       os.path.exists(os.path.join(rmantree, 'bin', prman)):
        return True
    return False


def get_rman_version(rmantree):
    try:
        prman = 'prman.exe' if platform.system() == 'Windows' else 'prman'
        exe = os.path.join(rmantree, 'bin', prman)
        desc = subprocess.check_output(
            [exe, "-version"], stderr=subprocess.STDOUT)
        vstr = str(desc, 'ascii').split('\n')[0].split()[-1]
        major_vers, minor_vers = vstr.split('.')
        vers_modifier = ''
        for v in ['b', 'rc']:
            if v in minor_vers:
                i = minor_vers.find(v)
                vers_modifier = minor_vers[i:]
                minor_vers = minor_vers[:i]
                break
        return int(major_vers), int(minor_vers), vers_modifier
    except:
        return 0, 0, ''


def guess_rmantree():
    rmantree_method = rman.prefs().rmantree_method
    choice = rman.prefs().rmantree_choice

    if rmantree_method == 'MANUAL':
        rmantree = rman.prefs().path_rmantree
    elif rmantree_method == 'ENV' or choice == 'NEWEST':
        rmantree = rmantree_from_env()
    else:
        rmantree = choice
    version = get_rman_version(rmantree)  # major, minor, mod

    if choice == 'NEWEST':

        # get from detected installs (at default installation path)
        try:
            base = {'Windows': r'C:\Program Files\Pixar',
                    'Darwin': '/Applications/Pixar',
                    'Linux': '/opt/pixar'}[platform.system()]
            for d in os.listdir(base):
                if "RenderManProServer" in d:
                    d_rmantree = os.path.join(base, d)
                    d_version = get_rman_version(d_rmantree)
                    if d_version > version:
                        rmantree = d_rmantree
                        version = d_version
        except:
            pass

    # check rmantree valid
    if version[0] == 0:
        msg = (
            "Error loading addon.  RMANTREE {} is not valid. Correct "
            "RMANTREE setting in addon preferences.".format(rmantree)
        )
        raise ImportError(msg)
        return None

    # check that it's >= 21
    if version[0] < 21:
        msg = (
            "Error loading addon using RMANTREE={}. RMANTREE must be "
            "version 21.0 or greater.  Correct RMANTREE setting in addon "
            "preferences.".format(rmantree)
        )
        raise ImportError(msg)
        return None

    return rmantree


def get_installed_rendermans():
    base = ""
    if platform.system() == 'Windows':
        # default installation path
        # or base = 'C:/Program Files/Pixar'
        base = r'C:\Program Files\Pixar'

    elif platform.system() == 'Darwin':
        base = '/Applications/Pixar'

    elif platform.system() == 'Linux':
        base = '/opt/pixar'

    rendermans = []
    try:
        for d in os.listdir(base):
            if "RenderManProServer" in d:
                try:
                    vstr = d.split('-')[1]
                    rendermans.append((vstr, os.path.join(base, d)))
                except:
                    pass
    except:
        pass

    return rendermans


def check_if_archive_dirty(update_time, archive_filename):
    if update_time > 0 and os.path.exists(archive_filename) \
            and os.path.getmtime(archive_filename) >= update_time:
        return False
    else:
        return True


def find_it_path():
    rmantree = guess_rmantree()

    if not rmantree:
        return None
    else:
        rmantree = os.path.join(rmantree, 'bin')
        if platform.system() == 'Windows':
            it_path = os.path.join(rmantree, 'it.exe')
        elif platform.system() == 'Darwin':
            it_path = os.path.join(
                rmantree, 'it.app', 'Contents', 'MacOS', 'it')
        elif platform.system() == 'Linux':
            it_path = os.path.join(rmantree, 'it')
        if os.path.exists(it_path):
            return it_path
        else:
            return None


def find_local_queue():
    rmantree = guess_rmantree()

    if not rmantree:
        return None
    else:
        rmantree = os.path.join(rmantree, 'bin')
        if platform.system() == 'Windows':
            lq = os.path.join(rmantree, 'LocalQueue.exe')
        elif platform.system() == 'Darwin':
            lq = os.path.join(
                rmantree, 'LocalQueue.app', 'Contents', 'MacOS', 'LocalQueue')
        elif platform.system() == 'Linux':
            lq = os.path.join(rmantree, 'LocalQueue')
        if os.path.exists(lq):
            return lq
        else:
            return None


def find_tractor_spool():
    base = ""
    if platform.system() == 'Windows':
        # default installation path
        base = r'C:\Program Files\Pixar'

    elif platform.system() == 'Darwin':
        base = '/Applications/Pixar'

    elif platform.system() == 'Linux':
        base = '/opt/pixar'

    latestver = 0.0
    guess = ''
    for d in os.listdir(base):
        if "Tractor" in d:
            vstr = d.split('-')[1]
            vf = float(vstr)
            if vf >= latestver:
                latestver = vf
                guess = os.path.join(base, d)
    tractor_dir = guess

    if not tractor_dir:
        return None
    else:
        spool_name = os.path.join(tractor_dir, 'bin', 'tractor-spool')
        if os.path.exists(spool_name):
            return spool_name
        else:
            return None


def init_exporter_env(prefs):
    if 'OUT' not in os.environ.keys():
        os.environ['OUT'] = prefs.env_vars.out

    # if 'SHD' not in os.environ.keys():
    #     os.environ['SHD'] = rm.env_vars.shd
    # if 'PTC' not in os.environ.keys():
    #     os.environ['PTC'] = rm.env_vars.ptc
    if 'ARC' not in os.environ.keys():
        os.environ['ARC'] = prefs.env_vars.arc


def init_env(rm):
    # init_exporter_env(scene.renderman)
    # try user set (or guessed) path
    RMANTREE = guess_rmantree()
    os.environ['RMANTREE'] = RMANTREE
    RMANTREE_BIN = os.path.join(RMANTREE, 'bin')
    if RMANTREE_BIN not in sys.path:
        sys.path.append(RMANTREE_BIN)
    pathsep = os.pathsep
    if 'PATH' in os.environ.keys():
        os.environ['PATH'] += pathsep + os.path.join(RMANTREE, "bin")
    else:
        os.environ['PATH'] = os.path.join(RMANTREE, "bin")
