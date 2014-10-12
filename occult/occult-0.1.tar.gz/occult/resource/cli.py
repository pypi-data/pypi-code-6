# -*- coding: utf-8 -*-

import os
import shutil
import re
import subprocess

from PIL import Image
from PIL import ImageOps

from cliff.lister import Lister
from clint.textui import colored, puts
from ..libraries.mod_pbxproj import XcodeProject

IGNORE_DIR_SUFFIX = ('.framework', '.embeddedframework', '.bundle', '.xcodeproj')
IGNORE_DIR = ('Pods')

class Resource(Lister):
    def get_parser(self, prog_name):
        parser = super(Resource, self).get_parser(prog_name)
        subparsers = parser.add_subparsers()

        export_parser = subparsers.add_parser('export')
        export_parser.add_argument('command', nargs='?', default='export')
        export_parser.add_argument('-s','--source', type = str, help = 'the path of xcode project')
        export_parser.add_argument('-t','--target', type = str, default='./exports', help = 'the path of resource target directory')
        export_parser.add_argument('--flat', action = 'store_true', help = 'ignore the suffix name')

        import_parser = subparsers.add_parser('import')
        import_parser.add_argument('command', nargs='?', default='import')
        import_parser.add_argument('-s', '--source', type = str, help = 'the path of resource directory')
        import_parser.add_argument('-t', '--target', type = str, help = 'the path of xcode project')

        cleanup_parser = subparsers.add_parser('cleanup')
        cleanup_parser.add_argument('command', nargs='?', default='cleanup')
        cleanup_parser.add_argument('-p', '--project', type = str, help = 'the source to cleanup')

        scale_parser = subparsers.add_parser('scale')
        scale_parser.add_argument('command', nargs='?', default='scale')
        scale_parser.add_argument('-f', '--files', nargs='+', help='files to scale')
        scale_parser.add_argument('-s', '--size', nargs='+', help = 'the scaling size, 1,2,3 supported')
        scale_parser.add_argument('-r', '--recursive', action = 'store_true', help = 'recursive the directory')

        return parser

    def take_action(self, parsed_args):
        command = parsed_args.command
        if command == 'export':
            return self.export_resource(parsed_args)
        elif command == 'import':
            return self.import_resource(parsed_args)
        elif command == 'cleanup':
            return self.cleanup_resource(parsed_args)
        elif command == 'scale':
            return self.scale_resource(parsed_args)

    def export_resource(self, parsed_args):
        source = parsed_args.source
        target = parsed_args.target
        is_flat = parsed_args.flat
        result = []

        for root, subdirs, files in os.walk(source):
            for f in files:
                if re.match('.*\.(jpg|png|gif|jpeg)$',os.path.basename(f)):
                    if is_flat:
                        if not os.path.isdir(target) or not os.path.exists(target):
                            os.makedirs(target)

                        ofpath = os.path.join(root, os.path.basename(f))
                        tfpath = os.path.abspath(os.path.join(target, os.path.basename(f)))
                        try:
                            shutil.copy2(ofpath, tfpath)
                            result.append((f,'SUCCESS'))
                        except:
                            result.append((f,'FAILED'))
                    else:
                        rpath = os.path.relpath(root, source)
                        tpath = os.path.abspath(os.path.join(target, rpath))
                        ofpath = os.path.join(root, os.path.basename(f))
                        if not os.path.isdir(tpath) or not os.path.exists(tpath):
                            os.makedirs(tpath)
                        tfpath = os.path.join(tpath,os.path.basename(f))
                        try:
                            shutil.copy2(ofpath, tfpath)
                            result.append((f,'SUCCESS'))
                        except:
                            result.append((f,'FAILED'))


        return (('Name', 'Status'),
                (f for f in result)
            )

    def import_resource(self, parsed_args):
        source = parsed_args.source
        target = parsed_args.target
        result = []

        for root, subdirs, files in os.walk(source):
            for f in files:
                if re.match('.*\.(jpg|png|gif|jpeg)$',os.path.basename(f)):
                    rpath = os.path.relpath(root, source)
                    tpath = os.path.abspath(os.path.join(target, rpath))
                    ofpath = os.path.join(root, os.path.basename(f))
                    if not os.path.isdir(tpath) or not os.path.exists(tpath):
                        os.makedirs(tpath)
                    tfpath = os.path.join(tpath,os.path.basename(f))
                    try:
                        shutil.copy2(ofpath, tfpath)
                        result.append((f,'SUCCESS'))
                    except:
                        result.append((f,'FAILED'))

        return (('Name', 'Status'),
                (f for f in result)
            )

    def cleanup_resource(self, parsed_args):
        source = parsed_args.project
        resources = []
        resources_ext = {}
        resources_path_map = {}
        resources_in_file = []
        result = []
        flat_result = []
        resources_pbxproj_map = {}

        pbxproj = self.find_pbxproj(source)

        if not pbxproj:
            puts(colored.red('.xcodeproj not found.'))
            return

        #get all resource and create resource-path, resource-ext map
        for root, subdirs, files in os.walk(source):
            if self.is_in_ignore_dir(root, source):
                continue

            for f in files:
                if re.match('.*\.(jpg|png|gif|jpeg)$',os.path.basename(f)):
                    if self.is_igore_file(os.path.basename(f)):
                        continue

                    path = os.path.join(root, os.path.basename(f))
                    filename_with_scale = os.path.splitext(f)[0]
                    file_ext = os.path.splitext(f)[1]
                    filename = filename_with_scale.split('@')[0]

                    resources.append(filename)
                    paths = resources_path_map.get(filename, [])
                    paths.append(path)
                    resources_path_map[filename] = list(set(paths))

                    exts = resources_ext.get(filename,[])
                    exts.append(file_ext)
                    resources_ext[filename] = list(set(exts))

        resources = list(set(resources))
        resources.sort()

        #get all resource that in project file
        for m_root, m_subdirs, m_files in os.walk(source):
            if self.is_in_ignore_dir(m_root, source):
                continue

            for m_f in m_files:
                filematch = re.match('.*\.(m|plist|xib)$',os.path.basename(m_f))
                if filematch:
                    m_path = os.path.join(m_root, os.path.basename(m_f))
                    m_bf = open(m_path,'rb')
                    pattern = r'@"([a-zA-Z0-9_\-\/\.]+(\.jpg|\.png|\.gif|\.jpeg)?)"' if filematch.group(1) == 'm' else r'([a-zA-Z0-9_\-\/\.]+(\.jpg|\.png|\.gif|\.jpeg)?)'
                    matchs = re.finditer(pattern, m_bf.read())
                    for match in matchs:
                        resources_in_file.append(match.group(1))

        resources_in_file = list(set(resources_in_file))
        resources_in_file.sort()

        #return if not any resource in project
        if len(resources_in_file)==0:
            puts(colored.red('.m, .plist, .xib files not found.'))
            return

        for resource in resources:
            if resource not in resources_in_file:
                is_find = False
                exts = resources_ext.get(resource, [])
                for ext in exts:
                    name = resource+ext
                    if name in resources_in_file:
                        is_find = True
                        break

                if not is_find:
                    result.append(resource)


        #get the xcodeproj id of the resources in result
        for r in result:
            if r in resources_path_map:
                for path in resources_path_map[r]:
                    for id in pbxproj.get_ids():
                        obj = pbxproj.get_obj(id)
                        if os.path.basename(path) == obj.get('path', None):
                            resources_pbxproj_map[path] = id

        #modified the xcodeproj
        for r in result:
            if r in resources_path_map:
                for path in resources_path_map[r]:
                    try:
                        os.remove(path)
                        pbxproj_id = resources_pbxproj_map[path]
                        pbxproj.remove_file(pbxproj_id)
                        flat_result.append((os.path.basename(path), 'SUCCESS'))
                    except:
                        flat_result.append((os.path.basename(path), 'FAILED'))

        if pbxproj.modified:
            pbxproj.save()

        return (('Name', 'Status'),
                (f for f in flat_result)
        )

    def scale_resource(self, parser_args):
        files = parser_args.files
        sizes = [s for s in parser_args.size if s in ['1', '2', '3']]
        recursive = parser_args.recursive if len(files)==1 else False
        file_size_map = {}
        result = []

        sizes.sort()

        if recursive:
            source = os.path.dirname(files[0])
            files = []
            for root, subdirs, allfiles in os.walk(source):
                for f in allfiles:
                    if re.match('.*\.(jpg|png|gif|jpeg)$',os.path.basename(f)):
                        files.append(os.path.join(root, os.path.basename(f)))

        #create a file and size map
        for file in files:
            if os.path.exists(file) and os.path.isfile(file):
                if re.match('.*\.(jpg|png|gif|jpeg|svg)$',os.path.basename(file)):
                    filename_split = os.path.splitext(os.path.basename(file))
                    filename_with_scale = filename_split[0]
                    file_ext = filename_split[1]
                    filename_scale_split = filename_with_scale.split('@')
                    filename = filename_scale_split[0]
                    file_with_ext = filename+file_ext

                    filename_scale = filename_scale_split[1] if len(filename_scale_split) > 1  else '1x'
                    filename_scale = filename_scale if filename_scale else '1x'

                    filename_map_item = file_size_map.get(file_with_ext,{})

                    if file_ext == '.svg':
                        filename_map_item['svg'] = os.path.abspath(file)
                    else:
                        filename_map_item[filename_scale] = os.path.abspath(file)

                    file_size_map[file_with_ext] = filename_map_item

        puts(colored.yellow('Scaling %d files...' % len(file_size_map)))

        for fk, fv in file_size_map.iteritems():
            if not not fv.get('svg'):
                ret = self.scale_vector(fk, fv.get('svg'), sizes)
                result.append(ret)
            else:
                ret = self.scale_bitmap(fk, fv, sizes)
                result.append(ret)

        output_header = ['Name']
        for k in [s+'x' for s in sizes]:
            output_header.insert(len(output_header), k)

        if len(result)>0:
            return (output_header,
                    (r for r in result)
            )
        else:
            return 'Nothing Happened.'

    def scale_bitmap(self, skel_filename, file_and_size, sizes):
        sizes_with_suffix = [s+'x' for s in sizes]
        max_size = 1
        max_file = None
        need_scale_size = []
        ret = {}

        for fk, fv in file_and_size.iteritems():
            fk_int = int(fk.split('x')[0])
            if fk_int > max_size:
                if os.path.exists(fv):
                    max_size = fk_int
                    max_file = fv

        for size_with_suffix in sizes_with_suffix:
            if size_with_suffix not in file_and_size:
                need_scale_size.append(size_with_suffix)
                ret[size_with_suffix] = 'FAILED'
            else:
                ret[size_with_suffix] = 'EXIST'

        if max_file and len(need_scale_size)>0:
            for need_size in need_scale_size:
                need_size_float = float(need_size.split('x')[0])
                scaling = need_size_float/max_size

                if scaling > 1:
                    ret[need_size] = 'IGNORE'
                    continue

                scaling_file_dir = os.path.dirname(max_file)
                filename_split = os.path.splitext(skel_filename)
                need_size_format = '@'+need_size if need_size != '1x' else ''
                scaling_filename = '%s%s%s' % (filename_split[0], need_size_format, filename_split[1])
                scaling_path = os.path.join(scaling_file_dir, scaling_filename)

                try:
                    img = Image.open(max_file)
                    print img.mode
                    img.convert('RGB')
                    thumb = ImageOps.fit(img, (int(img.size[0]*scaling),int(img.size[1]*scaling)), Image.ANTIALIAS)
                    thumb.save(scaling_path)
                    ret[need_size] = 'SUCCESS'
                except:
                    pass

        result_list = [skel_filename]
        for size_with_suffix in sizes_with_suffix:
            result_list.insert(len(result_list), ret.get(size_with_suffix, 'UNKNOWN'))

        return result_list

    def scale_vector(self, skel_filename, file, sizes):
        filename = os.path.splitext(skel_filename)[0]
        scaling_file_dir = os.path.dirname(file)
        scaling_file_ext = '.png'
        sizes_with_suffix = [s+'x' for s in sizes]
        out = open(os.devnull, 'w')
        ret = {}

        has_rsvg = self.detect_rsvg()
        if not has_rsvg:
            return

        for size in sizes:
            scaling = int(size)
            scaling_format = '@%sx' % size if size != '1' else ''
            scaling_file = os.path.join(scaling_file_dir,filename+scaling_format+scaling_file_ext)
            cmd = 'rsvg-convert -z %d -o %s %s' % (scaling, scaling_file, file)
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=out)
            # p_status = p.wait()
            p_status = p.returncode
            ret[size+'x'] = 'SUCCESS' if p_status==0 else 'FAILED'

        out.close()

        result_list = [skel_filename]
        for size_with_suffix in sizes_with_suffix:
            result_list.insert(len(result_list), ret.get(size_with_suffix, 'UNKNOWN'))

        return result_list

    def is_in_ignore_dir(self, path, root):
        is_ignore = False

        while path != root and not is_ignore:
            ext = os.path.splitext(path)[1] if len(os.path.splitext(path)) > 1 else None

            if not ext:
                continue

            basename = os.path.basename(path)
            is_ignore = ext in IGNORE_DIR_SUFFIX or basename in IGNORE_DIR
            path = os.path.dirname(path)

        return is_ignore

    def is_igore_file(self, filename):
        pattern = r'^(Default|Icon)'
        return not not re.search(pattern, filename)

    def find_pbxproj(self, path):
        pbxproj = None
        for subdir in os.listdir(path):
            ext = os.path.splitext(subdir)
            if ext[1] == '.xcodeproj':
                pbxproj = os.path.join(path, subdir, 'project.pbxproj')

        return XcodeProject.Load(pbxproj) if pbxproj else None

    def detect_rsvg(self):
        out = open(os.devnull, 'w')
        p = subprocess.Popen('type rsvg-convert', shell=True, stdout=subprocess.PIPE, stderr=out)
        # (output, err) = p.communicate()
        # p_status = p.wait()
        p_status = p.returncode
        out.close()
        return p_status==0
