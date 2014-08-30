import pystache
import argparse
import sys
import os
import shutil
import pkg_resources

def compile_markdown_file(source_file):
  '''Compiles a single markdown file to a remark.js slideshow.'''
  template = pkg_resources.resource_string('md2remark.resources.templates', 'slideshow.mustache')

  renderer = pystache.Renderer(search_dirs='./templates')

  f = open(source_file, 'r')
  slideshow_md = f.read()
  f.close()
  slideshow_name = os.path.split(source_file)[1].split('.')[0]

  rendered_text = renderer.render(template, {'title': slideshow_name, 'slideshow': slideshow_md})  

  if not os.path.exists('md2remark_build'):
    os.makedirs('md2remark_build')
  
  f = open(os.path.join('md2remark_build', slideshow_name + '.html'), 'w')
  f.write(rendered_text)
  f.close()

def compile_slides(source):
  '''Compiles the source to a remark.js slideshow.'''
  # if it's a directory, do all md files.
  if os.path.isdir(source):
    for f in os.listdir(source):
      if f.lower().endswith('.md'):
        compile_markdown_file(os.path.join(source, f))
  else:
    compile_markdown_file(source)

def parse_cl_args(arg_vector):
  '''Parses the command line arguments'''
  parser = argparse.ArgumentParser(description='Compiles markdown files into html files for remark.js')
  parser.add_argument('source', metavar='source', help='the source to compile. If a directory is provided, all markdown files in that directory are compiled. Output is saved in the current working directory under a md2remark_build subdirectory.')

  return parser.parse_args(arg_vector)

def run():
  '''Compiles markdown files into html files for remark.js'''
  args = parse_cl_args(sys.argv[1:])
  compile_slides(args.source)