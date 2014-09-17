# Copyright (c) 2012-2013 gocept gmbh & co. kg
# See also LICENSE.txt

from paste.script.templates import var
import datetime
import os
import os.path
import paste.script.templates
import paste.util.template
import pkginfo
import shutil
import subprocess


class Skeleton(paste.script.templates.Template):

    template_renderer = staticmethod(
        paste.util.template.paste_script_template_renderer)

    def underline_double(self, text):
        return '=' * len(text)

    def pre(self, command, output_dir, vars):
        gocept_package = pkginfo.Installed('gocept.package')
        vars.update(
            year=datetime.date.today().year,
            underline_double=self.underline_double,
            gocept_package_version=gocept_package.version,
        )

    def post(self, command, output_dir, vars):
        os.rename(os.path.join(output_dir, 'hgignore'),
                  os.path.join(output_dir, '.hgignore'))
        subprocess.call(['hg', 'init', output_dir])
        shutil.move(os.path.join(output_dir, 'hgrc'),
                    os.path.join(output_dir, '.hg'))


class PackageSkeleton(Skeleton):

    summary = (
        'Python package with buildout, conforming to conventions at gocept')

    _template_dir = 'skeleton'

    vars = [
        var("description", "One-line description of the package"),
        var("keywords", "Space-separated keywords/tags"),
    ]

    def pre(self, command, output_dir, vars):
        super(PackageSkeleton, self).pre(command, output_dir, vars)
        namespace, package = vars['egg'].split('.')
        vars.update(
            namespace=namespace,
            package=package,
        )

    def post(self, command, output_dir, vars):
        super(PackageSkeleton, self).post(command, output_dir, vars)
        os.rename(os.path.join(output_dir, 'coveragerc'),
                  os.path.join(output_dir, '.coveragerc'))


class WebAppDeploymentSkeleton(Skeleton):

    summary = 'Batou deployment for a generic web app'

    _template_dir = 'webapp-deployment-skeleton'

    vars = [
        var("description", "One-line description of the project"),
    ]

    def post(self, command, output_dir, vars):
        super(WebAppDeploymentSkeleton, self).post(command, output_dir, vars)
        os.chmod(os.path.join(output_dir, 'batou'), 0775)
        for name in os.listdir(os.path.join(output_dir, 'bin')):
            os.chmod(os.path.join(output_dir, 'bin', name), 0775)
