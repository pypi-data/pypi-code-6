import doctest
import locale
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import textwrap
import zipfile
from contextlib import closing
from io import BytesIO

try:
    import unittest2 as unittest    # Python 2.6
except ImportError:
    import unittest

try:
    from cStringIO import StringIO  # Python 2.x
except ImportError:
    from io import StringIO         # Python 3.x

import mock


def rmtree(path):
    """A version of rmtree that can remove read-only files on Windows.

    Needed because the stock shutil.rmtree() fails with an access error
    due to the files in .git/objects being read-only.
    """
    def onerror(func, path, exc_info):
        if func is os.remove or func is os.unlink:
            # Did you know what on Python 3.3 on Windows os.remove() and
            # os.unlink() are distinct functions?
            os.chmod(path, 0o644)
            func(path)
        else:
            raise
    shutil.rmtree(path, onerror=onerror)


class Tests(unittest.TestCase):

    def setUp(self):
        import check_manifest
        self.warnings = []
        self._real_warning = check_manifest.warning
        check_manifest.warning = self.warnings.append

    def tearDown(self):
        import check_manifest
        check_manifest.warning = self._real_warning

    def make_temp_dir(self):
        tmpdir = tempfile.mkdtemp(prefix='test-', suffix='-check-manifest')
        self.addCleanup(rmtree, tmpdir)
        return tmpdir

    def create_zip_file(self, filename, filenames):
        with closing(zipfile.ZipFile(filename, 'w')) as zf:
            for fn in filenames:
                zf.writestr(fn, '')

    def create_tar_file(self, filename, filenames):
        with closing(tarfile.TarFile(filename, 'w')) as tf:
            for fn in filenames:
                tf.addfile(tarfile.TarInfo(fn), BytesIO())

    def test_run_success(self):
        from check_manifest import run
        self.assertEqual(run(["true"]), "")

    def test_run_failure(self):
        from check_manifest import run, CommandFailed
        with self.assertRaises(CommandFailed) as cm:
            run(["false"])
        self.assertEqual(str(cm.exception),
                         "['false'] failed (status 1):\n")

    def test_run_no_such_program(self):
        from check_manifest import run, Failure
        with self.assertRaises(Failure) as cm:
            run(["there-is-really-no-such-program"])
        # Linux says "[Errno 2] No such file or directory"
        # Windows says "[Error 2] The system cannot find the file specified"
        # but on 3.x it's "[WinErr 2] The system cannot find the file specified"
        should_start_with = "could not run ['there-is-really-no-such-program']:"
        self.assertTrue(
            str(cm.exception).startswith(should_start_with),
            '\n%r does not start with\n%r' % (str(cm.exception),
                                              should_start_with))

    def test_copy_files(self):
        from check_manifest import copy_files
        actions = []
        n = os.path.normpath
        with mock.patch('os.path.isdir', lambda d: d in ('b', n('/dest/dir'))):
            with mock.patch('os.makedirs',
                            lambda d: actions.append('makedirs %s' % d)):
                with mock.patch('os.mkdir',
                                lambda d: actions.append('mkdir %s' % d)):
                    with mock.patch('shutil.copy2',
                                    lambda s, d: actions.append('cp %s %s' % (s, d))):
                        copy_files(['a', 'b', n('c/d/e')], n('/dest/dir'))
        self.assertEqual(
            actions,
            [
                'cp a %s' % n('/dest/dir/a'),
                'mkdir %s' % n('/dest/dir/b'),
                'makedirs %s' % n('/dest/dir/c/d'),
                'cp %s %s' % (n('c/d/e'), n('/dest/dir/c/d/e')),
            ])

    def test_get_one_file_in(self):
        from check_manifest import get_one_file_in
        with mock.patch('os.listdir', lambda dir: ['a']):
            self.assertEqual(get_one_file_in(os.path.normpath('/some/dir')),
                             os.path.normpath('/some/dir/a'))

    def test_get_one_file_in_empty_directory(self):
        from check_manifest import get_one_file_in, Failure
        with mock.patch('os.listdir', lambda dir: []):
            with self.assertRaises(Failure) as cm:
                get_one_file_in('/some/dir')
            self.assertEqual(str(cm.exception),
                             "No files found in /some/dir")

    def test_get_one_file_in_too_many(self):
        from check_manifest import get_one_file_in, Failure
        with mock.patch('os.listdir', lambda dir: ['b', 'a']):
            with self.assertRaises(Failure) as cm:
                get_one_file_in('/some/dir')
            self.assertEqual(str(cm.exception),
                             "More than one file exists in /some/dir:\na\nb")

    def test_unicodify(self):
        from check_manifest import unicodify
        nonascii = b'\xc3\xa9.txt'.decode('UTF-8') # because Py3.2 lacks u''
        self.assertEqual(unicodify(nonascii), nonascii)
        self.assertEqual(
            unicodify(nonascii.encode(locale.getpreferredencoding())),
            nonascii)

    def test_get_archive_file_list_unrecognized_archive(self):
        from check_manifest import get_archive_file_list, Failure
        with self.assertRaises(Failure) as cm:
            get_archive_file_list('archive.rar')
        self.assertEqual(str(cm.exception), 'Unrecognized archive type: .rar')

    def test_get_archive_file_list_zip(self):
        from check_manifest import get_archive_file_list
        filename = os.path.join(self.make_temp_dir(), 'archive.zip')
        self.create_zip_file(filename, ['a', 'b/c'])
        self.assertEqual(get_archive_file_list(filename),
                         ['a', 'b', 'b/c'])

    def test_get_archive_file_list_zip_nonascii(self):
        from check_manifest import get_archive_file_list
        filename = os.path.join(self.make_temp_dir(), 'archive.zip')
        nonascii = b'\xc3\xa9.txt'.decode('UTF-8') # because Py3.2 lacks u''
        self.create_zip_file(filename, [nonascii])
        self.assertEqual(get_archive_file_list(filename),
                         [nonascii])

    def test_get_archive_file_list_tar(self):
        from check_manifest import get_archive_file_list
        filename = os.path.join(self.make_temp_dir(), 'archive.tar')
        self.create_tar_file(filename, ['a', 'b/c'])
        self.assertEqual(get_archive_file_list(filename),
                         ['a', 'b', 'b/c'])

    def test_get_archive_file_list_tar_nonascii(self):
        from check_manifest import get_archive_file_list
        filename = os.path.join(self.make_temp_dir(), 'archive.tar')
        nonascii = b'\xc3\xa9.txt'.decode('UTF-8') # because Py3.2 lacks u''
        self.create_tar_file(filename, [nonascii])
        self.assertEqual(get_archive_file_list(filename),
                         [nonascii])

    def test_format_list(self):
        from check_manifest import format_list
        self.assertEqual(format_list([]), "")
        self.assertEqual(format_list(['a']), "  a")
        self.assertEqual(format_list(['a', 'b']), "  a\n  b")

    def test_format_missing(self):
        from check_manifest import format_missing
        self.assertEqual(
            format_missing(set(), set(), "1st", "2nd"),
            "")
        self.assertEqual(
            format_missing(set(["c"]), set(["a"]), "1st", "2nd"),
            "missing from 1st:\n"
            "  c\n"
            "missing from 2nd:\n"
            "  a")

    def test_strip_toplevel_name_empty_list(self):
        from check_manifest import strip_toplevel_name
        self.assertEqual(strip_toplevel_name([]), [])

    def test_strip_toplevel_name_no_common_prefix(self):
        from check_manifest import strip_toplevel_name, Failure
        self.assertRaises(Failure, strip_toplevel_name, ["a/b", "c/d"])

    def test_detect_vcs_no_vcs(self):
        from check_manifest import detect_vcs, Failure
        with mock.patch('check_manifest.VCS.detect', staticmethod(lambda *a: False)):
            with self.assertRaises(Failure) as cm:
                detect_vcs()
            self.assertEqual(str(cm.exception),
                             "Couldn't find version control data"
                             " (git/hg/bzr/svn supported)")

    def test_normalize_names(self):
        from check_manifest import normalize_names
        j = os.path.join
        self.assertEqual(normalize_names(["a", j("b", ""), j("c", "d"),
                                          j("e", "f", ""),
                                          j("g", "h", "..", "i")]),
                         ["a", "b", j("c", "d"), j("e", "f"), j("g", "i")])

    def test_add_directories(self):
        from check_manifest import add_directories
        j = os.path.join
        self.assertEqual(add_directories(['a', 'b', j('c', 'd'), j('e', 'f')]),
                         ['a', 'b', 'c', j('c', 'd'), 'e', j('e', 'f')])

    def test_file_matches(self):
        from check_manifest import file_matches
        # On Windows we might get the pattern list from setup.cfg using / as
        # the directory separator, but the filenames we're matching against
        # will use os.path.sep
        patterns = ['setup.cfg', '*.egg-info', '*.egg-info/*']
        j = os.path.join
        self.assertFalse(file_matches('setup.py', patterns))
        self.assertTrue(file_matches('setup.cfg', patterns))
        self.assertTrue(file_matches(j('src', 'zope.foo.egg-info'), patterns))
        self.assertTrue(
            file_matches(j('src', 'zope.foo.egg-info', 'SOURCES.txt'),
                         patterns))

    def test_strip_sdist_extras(self):
        from check_manifest import strip_sdist_extras
        filelist = list(map(os.path.normpath, [
            '.gitignore',
            'setup.py',
            'setup.cfg',
            'README.txt',
            'src',
            'src/zope',
            'src/zope/__init__.py',
            'src/zope/foo',
            'src/zope/foo/__init__.py',
            'src/zope/foo/language.po',
            'src/zope/foo/language.mo',
            'src/zope.foo.egg-info',
            'src/zope.foo.egg-info/SOURCES.txt',
        ]))
        expected = list(map(os.path.normpath, [
            'setup.py',
            'README.txt',
            'src',
            'src/zope',
            'src/zope/__init__.py',
            'src/zope/foo',
            'src/zope/foo/__init__.py',
            'src/zope/foo/language.po',
        ]))
        self.assertEqual(strip_sdist_extras(filelist), expected)

    def test_strip_sdist_extras_with_manifest(self):
        import check_manifest
        from check_manifest import strip_sdist_extras
        from check_manifest import _get_ignore_from_manifest as parse
        orig_ignore = check_manifest.IGNORE[:]
        orig_ignore_regexps = check_manifest.IGNORE_REGEXPS[:]
        manifest_in = textwrap.dedent("""
            graft src
            exclude *.cfg
            global-exclude *.mo
            prune src/dump
            recursive-exclude src/zope *.sh
        """)
        filelist = list(map(os.path.normpath, [
            '.gitignore',
            'setup.py',
            'setup.cfg',
            'MANIFEST.in',
            'README.txt',
            'src',
            'src/helper.sh',
            'src/dump',
            'src/dump/__init__.py',
            'src/zope',
            'src/zope/__init__.py',
            'src/zope/zopehelper.sh',
            'src/zope/foo',
            'src/zope/foo/__init__.py',
            'src/zope/foo/language.po',
            'src/zope/foo/language.mo',
            'src/zope/foo/config.cfg',
            'src/zope/foo/foohelper.sh',
            'src/zope.foo.egg-info',
            'src/zope.foo.egg-info/SOURCES.txt',
        ]))
        expected = list(map(os.path.normpath, [
            'setup.py',
            'MANIFEST.in',
            'README.txt',
            'src',
            'src/helper.sh',
            'src/zope',
            'src/zope/__init__.py',
            'src/zope/foo',
            'src/zope/foo/__init__.py',
            'src/zope/foo/language.po',
            'src/zope/foo/config.cfg',
        ]))

        # This will change the definitions.
        try:
            # This is normally done in read_manifest:
            ignore, ignore_regexps = parse(manifest_in)
            check_manifest.IGNORE.extend(ignore)
            check_manifest.IGNORE_REGEXPS.extend(ignore_regexps)
            # Filter the file list.
            result = strip_sdist_extras(filelist)
        finally:
            # Restore the original definitions
            check_manifest.IGNORE[:] = orig_ignore
            check_manifest.IGNORE_REGEXPS[:] = orig_ignore_regexps
        self.assertEqual(result, expected)

    def test_find_bad_ideas(self):
        from check_manifest import find_bad_ideas
        filelist = list(map(os.path.normpath, [
            '.gitignore',
            'setup.py',
            'setup.cfg',
            'README.txt',
            'src',
            'src/zope',
            'src/zope/__init__.py',
            'src/zope/foo',
            'src/zope/foo/__init__.py',
            'src/zope/foo/language.po',
            'src/zope/foo/language.mo',
            'src/zope.foo.egg-info',
            'src/zope.foo.egg-info/SOURCES.txt',
        ]))
        expected = list(map(os.path.normpath, [
            'src/zope/foo/language.mo',
            'src/zope.foo.egg-info',
        ]))
        self.assertEqual(find_bad_ideas(filelist), expected)

    def test_find_suggestions(self):
        from check_manifest import find_suggestions
        self.assertEqual(find_suggestions(['buildout.cfg']),
                         (['include buildout.cfg'], []))
        self.assertEqual(find_suggestions(['unknown.file~']),
                         ([], ['unknown.file~']))
        self.assertEqual(find_suggestions(['README.txt', 'CHANGES.txt']),
                         (['include *.txt'], []))
        filelist = list(map(os.path.normpath, [
            'docs/index.rst',
            'docs/image.png',
            'docs/Makefile',
            'docs/unknown-file',
        ]))
        expected_rules = [
            'recursive-include docs *.png',
            'recursive-include docs *.rst',
            'recursive-include docs Makefile',
        ]
        expected_unknowns = [os.path.normpath('docs/unknown-file')]
        self.assertEqual(find_suggestions(filelist),
                         (expected_rules, expected_unknowns))

    def test_find_suggestions_generic_fallback_rules(self):
        from check_manifest import find_suggestions
        n = os.path.normpath
        self.assertEqual(find_suggestions(['Changelog']),
                         (['include Changelog'], []))
        self.assertEqual(find_suggestions(['id-lang.map']),
                         (['include *.map'], []))
        self.assertEqual(find_suggestions([n('src/id-lang.map')]),
                         (['recursive-include src *.map'], []))

    def test_find_suggestions_ignores_directories(self):
        from check_manifest import find_suggestions
        with mock.patch('os.path.isdir', lambda d: True):
            self.assertEqual(find_suggestions(['SOMEDIR']),
                             ([], []))

    def test_is_package(self):
        from check_manifest import is_package
        j = os.path.join
        with mock.patch('os.path.exists', lambda fn: fn == j('a', 'setup.py')):
            self.assertTrue(is_package('a'))
            self.assertFalse(is_package('b'))

    def test_glob_to_regexp(self):
        from check_manifest import _glob_to_regexp as g2r
        sep = r'\\' if os.path.sep == '\\' else os.path.sep
        self.assertEqual(g2r('foo.py'), r'foo\.py\Z(?ms)')
        self.assertEqual(g2r('foo/bar.py'), r'foo\/bar\.py\Z(?ms)')
        self.assertEqual(g2r('foo*.py'), r'foo[^%s]*\.py\Z(?ms)' % sep)
        self.assertEqual(g2r('foo?.py'), r'foo[^%s]\.py\Z(?ms)' % sep)
        self.assertEqual(g2r('foo[123].py'), r'foo[123]\.py\Z(?ms)')
        self.assertEqual(g2r('foo[!123].py'), r'foo[^123]\.py\Z(?ms)')
        self.assertEqual(g2r('foo/*.py'), r'foo\/[^%s]*\.py\Z(?ms)' % sep)

    def test_get_ignore_from_manifest(self):
        from check_manifest import _get_ignore_from_manifest as parse
        from check_manifest import _glob_to_regexp as g2r
        j = os.path.join
        # The return value is a tuple with two lists:
        # ([<list of filename ignores>], [<list of regular expressions>])
        self.assertEqual(parse(''),
                         ([], []))
        self.assertEqual(parse('      \n        '),
                         ([], []))
        self.assertEqual(parse('exclude *.cfg'),
                         ([], [g2r('*.cfg')]))
        self.assertEqual(parse('#exclude *.cfg'),
                         ([], []))
        self.assertEqual(parse('exclude          *.cfg'),
                         ([], [g2r('*.cfg')]))
        self.assertEqual(parse('\texclude\t*.cfg foo.*   bar.txt'),
                         (['bar.txt'], [g2r('*.cfg'), g2r('foo.*')]))
        self.assertEqual(parse('exclude some/directory/*.cfg'),
                         ([], [g2r('some/directory/*.cfg')]))
        self.assertEqual(parse('include *.cfg'),
                         ([], []))
        self.assertEqual(parse('global-exclude *.pyc'),
                         (['*.pyc'], []))
        self.assertEqual(parse('global-exclude *.pyc *.sh'),
                         (['*.pyc', '*.sh'], []))
        self.assertEqual(parse('recursive-exclude dir *.pyc'),
                         ([j('dir', '*.pyc')], []))
        self.assertEqual(parse('recursive-exclude dir *.pyc foo*.sh'),
                         ([j('dir', '*.pyc'), j('dir', 'foo*.sh'),
                           j('dir', '*', 'foo*.sh')], []))
        self.assertEqual(parse('recursive-exclude dir nopattern.xml'),
                         ([j('dir', 'nopattern.xml'),
                           j('dir', '*', 'nopattern.xml')], []))
        # We should not fail when a recursive-exclude line is wrong:
        self.assertEqual(parse('recursive-exclude dirwithoutpattern'),
                         ([], []))
        self.assertEqual(parse('prune dir'),
                         (['dir', j('dir', '*')], []))
        # You should not add a slash at the end of a prune, but let's
        # not fail over it or end up with double slashes.
        self.assertEqual(parse('prune dir/'),
                         (['dir', j('dir', '*')], []))
        # And a mongo test case of everything at the end
        text = textwrap.dedent("""
            #exclude *.01
            exclude *.02
            exclude *.03 04.*   bar.txt
            exclude          *.05
            exclude some/directory/*.cfg
            global-exclude *.10 *.11
            global-exclude *.12
            include *.20
            prune 30
            recursive-exclude    40      *.41
            recursive-exclude 42 *.43 44.*
        """)
        self.assertEqual(
            parse(text),
            ([
                'bar.txt',
                '*.10',
                '*.11',
                '*.12',
                '30',
                j('30', '*'),
                j('40', '*.41'),
                j('42', '*.43'),
                j('42', '44.*'),
                j('42', '*', '44.*'),
            ], [
                g2r('*.02'),
                g2r('*.03'),
                g2r('04.*'),
                g2r('*.05'),
                g2r('some/directory/*.cfg'),
            ]))


class TestConfiguration(unittest.TestCase):

    def setUp(self):
        import check_manifest
        self.oldpwd = os.getcwd()
        self.tmpdir = tempfile.mkdtemp(prefix='test-', suffix='-check-manifest')
        os.chdir(self.tmpdir)
        self.OLD_IGNORE = check_manifest.IGNORE
        self.OLD_IGNORE_REGEXPS = check_manifest.IGNORE_REGEXPS
        check_manifest.IGNORE = ['default-ignore-rules']
        check_manifest.IGNORE_REGEXPS = ['default-ignore-regexps']

    def tearDown(self):
        import check_manifest
        check_manifest.IGNORE = self.OLD_IGNORE
        check_manifest.IGNORE_REGEXPS = self.OLD_IGNORE_REGEXPS
        os.chdir(self.oldpwd)
        shutil.rmtree(self.tmpdir)

    def test_read_config_no_config(self):
        import check_manifest
        check_manifest.read_config()
        self.assertEqual(check_manifest.IGNORE, ['default-ignore-rules'])

    def test_read_config_no_section(self):
        import check_manifest
        with open('setup.cfg', 'w') as f:
            f.write('[pep8]\nignore =\n')
        check_manifest.read_config()
        self.assertEqual(check_manifest.IGNORE, ['default-ignore-rules'])

    def test_read_config_no_option(self):
        import check_manifest
        with open('setup.cfg', 'w') as f:
            f.write('[check-manifest]\n')
        check_manifest.read_config()
        self.assertEqual(check_manifest.IGNORE, ['default-ignore-rules'])

    def test_read_config_extra_ignores(self):
        import check_manifest
        with open('setup.cfg', 'w') as f:
            f.write('[check-manifest]\nignore = foo\n  bar\n')
        check_manifest.read_config()
        self.assertEqual(check_manifest.IGNORE,
                         ['default-ignore-rules', 'foo', 'bar'])

    def test_read_config_override_ignores(self):
        import check_manifest
        with open('setup.cfg', 'w') as f:
            f.write('[check-manifest]\nignore = foo\n\n  bar\n')
            f.write('ignore-default-rules = yes\n')
        check_manifest.read_config()
        self.assertEqual(check_manifest.IGNORE,
                         ['foo', 'bar'])

    def test_read_manifest_no_manifest(self):
        import check_manifest
        check_manifest.read_manifest()
        self.assertEqual(check_manifest.IGNORE, ['default-ignore-rules'])

    def test_read_manifest(self):
        import check_manifest
        from check_manifest import _glob_to_regexp as g2r
        with open('MANIFEST.in', 'w') as f:
            f.write('exclude *.gif\n')
            f.write('global-exclude *.png\n')
        check_manifest.read_manifest()
        self.assertEqual(check_manifest.IGNORE,
                         ['default-ignore-rules', '*.png'])
        self.assertEqual(check_manifest.IGNORE_REGEXPS,
                         ['default-ignore-regexps', g2r('*.gif')])


class TestMain(unittest.TestCase):

    def setUp(self):
        import check_manifest
        self._cm_patcher = mock.patch('check_manifest.check_manifest')
        self._check_manifest = self._cm_patcher.start()
        self._se_patcher = mock.patch('sys.exit')
        self._sys_exit = self._se_patcher.start()
        self._error_patcher = mock.patch('check_manifest.error')
        self._error = self._error_patcher.start()
        self._orig_sys_argv = sys.argv
        sys.argv = ['check-manifest']
        self.OLD_IGNORE = check_manifest.IGNORE
        self.OLD_IGNORE_REGEXPS = check_manifest.IGNORE_REGEXPS
        check_manifest.IGNORE = ['default-ignore-rules']
        check_manifest.IGNORE_REGEXPS = ['default-ignore-regexps']

    def tearDown(self):
        import check_manifest
        check_manifest.IGNORE = self.OLD_IGNORE
        check_manifest.IGNORE_REGEXPS = self.OLD_IGNORE_REGEXPS
        sys.argv = self._orig_sys_argv
        self._se_patcher.stop()
        self._cm_patcher.stop()
        self._error_patcher.stop()

    def test(self):
        from check_manifest import main
        main()

    def test_exit_code_1_on_error(self):
        from check_manifest import main
        self._check_manifest.return_value = False
        main()
        self._sys_exit.assert_called_with(1)

    def test_exit_code_2_on_failure(self):
        from check_manifest import main, Failure
        self._check_manifest.side_effect = Failure('msg')
        main()
        self._error.assert_called_with('msg')
        self._sys_exit.assert_called_with(2)

    def test_extra_ignore_args(self):
        import check_manifest
        sys.argv.append('--ignore=x,y,z')
        check_manifest.main()
        self.assertEqual(check_manifest.IGNORE,
                         ['default-ignore-rules', 'x', 'y', 'z'])


class TestZestIntegration(unittest.TestCase):

    def setUp(self):
        sys.modules['zest'] = mock.Mock()
        sys.modules['zest.releaser'] = mock.Mock()
        sys.modules['zest.releaser.utils'] = mock.Mock()
        self.ask = sys.modules['zest.releaser.utils'].ask

    def tearDown(self):
        del sys.modules['zest.releaser.utils']
        del sys.modules['zest.releaser']
        del sys.modules['zest']

    @mock.patch('check_manifest.is_package', lambda d: False)
    @mock.patch('check_manifest.check_manifest')
    def test_zest_releaser_check_not_a_package(self, check_manifest):
        from check_manifest import zest_releaser_check
        zest_releaser_check(dict(workingdir='.'))
        check_manifest.assert_not_called()

    @mock.patch('check_manifest.is_package', lambda d: True)
    @mock.patch('check_manifest.check_manifest')
    def test_zest_releaser_check_user_disagrees(self, check_manifest):
        from check_manifest import zest_releaser_check
        self.ask.return_value = False
        zest_releaser_check(dict(workingdir='.'))
        check_manifest.assert_not_called()

    @mock.patch('check_manifest.is_package', lambda d: True)
    @mock.patch('sys.exit')
    @mock.patch('check_manifest.check_manifest')
    def test_zest_releaser_check_all_okay(self, check_manifest, sys_exit):
        from check_manifest import zest_releaser_check
        self.ask.return_value = True
        check_manifest.return_value = True
        zest_releaser_check(dict(workingdir='.'))
        sys_exit.assert_not_called()

    @mock.patch('check_manifest.is_package', lambda d: True)
    @mock.patch('check_manifest.error')
    @mock.patch('sys.exit')
    @mock.patch('check_manifest.check_manifest')
    def test_zest_releaser_check_error_user_aborts(self, check_manifest,
                                                   sys_exit, error):
        from check_manifest import zest_releaser_check
        self.ask.side_effect = [True, False]
        check_manifest.return_value = False
        zest_releaser_check(dict(workingdir='.'))
        sys_exit.assert_called_with(1)

    @mock.patch('check_manifest.is_package', lambda d: True)
    @mock.patch('check_manifest.error')
    @mock.patch('sys.exit')
    @mock.patch('check_manifest.check_manifest')
    def test_zest_releaser_check_error_user_plods_on(self, check_manifest,
                                                     sys_exit, error):
        from check_manifest import zest_releaser_check
        self.ask.side_effect = [True, True]
        check_manifest.return_value = False
        zest_releaser_check(dict(workingdir='.'))
        sys_exit.assert_not_called()

    @mock.patch('check_manifest.is_package', lambda d: True)
    @mock.patch('check_manifest.error')
    @mock.patch('sys.exit')
    @mock.patch('check_manifest.check_manifest')
    def test_zest_releaser_check_failure_user_aborts(self, check_manifest,
                                                     sys_exit, error):
        from check_manifest import zest_releaser_check, Failure
        self.ask.side_effect = [True, False]
        check_manifest.side_effect = Failure('msg')
        zest_releaser_check(dict(workingdir='.'))
        error.assert_called_with('msg')
        sys_exit.assert_called_with(2)

    @mock.patch('check_manifest.is_package', lambda d: True)
    @mock.patch('check_manifest.error')
    @mock.patch('sys.exit')
    @mock.patch('check_manifest.check_manifest')
    def test_zest_releaser_check_failure_user_plods_on(self, check_manifest,
                                                       sys_exit, error):
        from check_manifest import zest_releaser_check, Failure
        self.ask.side_effect = [True, True]
        check_manifest.side_effect = Failure('msg')
        zest_releaser_check(dict(workingdir='.'))
        error.assert_called_with('msg')
        sys_exit.assert_not_called()


class VCSHelper(object):

    def _run(self, *command):
        # Windows doesn't like Unicode arguments to subprocess.Popen(), on Py2:
        # https://github.com/mgedmin/check-manifest/issues/23#issuecomment-33933031
        if str is bytes:
            command = [s.encode(locale.getpreferredencoding()) for s in command]
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        stdout, stderr = p.communicate()
        rc = p.wait()
        if rc:
            print(' '.join(command))
            print(stdout)
            raise subprocess.CalledProcessError(rc, command[0], output=stdout)


class VCSMixin(object):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix='test-', suffix='-check-manifest')
        self.olddir = os.getcwd()
        os.chdir(self.tmpdir)

    def tearDown(self):
        os.chdir(self.olddir)
        rmtree(self.tmpdir)

    def _create_file(self, filename):
        assert not os.path.isabs(filename)
        basedir = os.path.dirname(filename)
        if basedir and not os.path.isdir(basedir):
            os.makedirs(basedir)
        open(filename, 'w').close()

    def _create_files(self, filenames):
        for filename in filenames:
            self._create_file(filename)

    def _init_vcs(self):
        self.vcs._init_vcs()

    def _add_to_vcs(self, filenames):
        self.vcs._add_to_vcs(filenames)

    def _commit(self):
        self.vcs._commit()

    def _create_and_add_to_vcs(self, filenames):
        self._create_files(filenames)
        self._add_to_vcs(filenames)

    def test_get_vcs_files(self):
        from check_manifest import get_vcs_files
        self._init_vcs()
        self._create_and_add_to_vcs(['a.txt', 'b/b.txt', 'b/c/d.txt'])
        self._commit()
        self._create_files(['b/x.txt', 'd/d.txt', 'i.txt'])
        j = os.path.join
        self.assertEqual(get_vcs_files(),
                         ['a.txt', 'b', j('b', 'b.txt'), j('b', 'c'),
                          j('b', 'c', 'd.txt')])

    def test_get_vcs_files_added_but_uncommitted(self):
        from check_manifest import get_vcs_files
        self._init_vcs()
        self._create_and_add_to_vcs(['a.txt', 'b/b.txt', 'b/c/d.txt'])
        self._create_files(['b/x.txt', 'd/d.txt', 'i.txt'])
        j = os.path.join
        self.assertEqual(get_vcs_files(),
                         ['a.txt', 'b', j('b', 'b.txt'), j('b', 'c'),
                          j('b', 'c', 'd.txt')])

    def test_get_vcs_files_in_a_subdir(self):
        from check_manifest import get_vcs_files
        self._init_vcs()
        self._create_and_add_to_vcs(['a.txt', 'b/b.txt', 'b/c/d.txt'])
        self._commit()
        self._create_files(['b/x.txt', 'd/d.txt', 'i.txt'])
        os.chdir('b')
        j = os.path.join
        self.assertEqual(get_vcs_files(), ['b.txt', 'c', j('c', 'd.txt')])

    def test_get_vcs_files_nonascii_filenames(self):
        # This test will fail if your locale is incapable of expressing
        # "eacute".  UTF-8 or Latin-1 should work.
        from check_manifest import get_vcs_files
        self._init_vcs()
        # A spelling of u"\xe9.txt" that works on Python 3.2 too
        filename = b'\xc3\xa9.txt'.decode('UTF-8')
        self._create_and_add_to_vcs([filename])
        self.assertEqual(get_vcs_files(), [filename])


class GitHelper(VCSHelper):

    def _init_vcs(self):
        self._run('git', 'init')
        self._run('git', 'config', 'user.name', 'Unit Test')
        self._run('git', 'config', 'user.email', 'test@example.com')

    def _add_to_vcs(self, filenames):
        self._run('git', 'add', '--', *filenames)

    def _commit(self):
        self._run('git', 'commit', '-m', 'Initial')


class TestGit(VCSMixin, unittest.TestCase):
    vcs = GitHelper()


class BzrHelper(VCSHelper):

    def _init_vcs(self):
        self._run('bzr', 'init')
        self._run('bzr', 'whoami', '--branch', 'Unit Test <test@example.com>')

    def _add_to_vcs(self, filenames):
        self._run('bzr', 'add', '--', *filenames)

    def _commit(self):
        self._run('bzr', 'commit', '-m', 'Initial')


class TestBzr(VCSMixin, unittest.TestCase):
    vcs = BzrHelper()


class HgHelper(VCSHelper):

    def _init_vcs(self):
        self._run('hg', 'init')
        with open('.hg/hgrc', 'a') as f:
            f.write('\n[ui]\nusername = Unit Test <test@example.com\n')

    def _add_to_vcs(self, filenames):
        self._run('hg', 'add', '--', *filenames)

    def _commit(self):
        self._run('hg', 'commit', '-m', 'Initial')


class TestHg(VCSMixin, unittest.TestCase):
    vcs = HgHelper()


class SvnHelper(VCSHelper):

    def _init_vcs(self):
        self._run('svnadmin', 'create', 'repo')
        self._run('svn', 'co', 'file:///' + os.path.abspath('repo').replace(os.path.sep, '/'), 'checkout')
        os.chdir('checkout')

    def _add_to_vcs(self, filenames):
        from check_manifest import add_directories
        self._run('svn', 'add', '-N', '--', *add_directories(filenames))

    def _commit(self):
        self._run('svn', 'commit', '-m', 'Initial')


class TestSvn(VCSMixin, unittest.TestCase):
    vcs = SvnHelper()


class TestUserInterface(unittest.TestCase):

    def setUp(self):
        self.real_stdout = sys.stdout
        self.real_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

    def tearDown(self):
        sys.stderr = self.real_stderr
        sys.stdout = self.real_stdout

    def test_info(self):
        from check_manifest import info
        info("Reticulating splines")
        self.assertEqual(sys.stdout.getvalue(),
                         "Reticulating splines\n")

    def test_info_begin_continue_end(self):
        from check_manifest import info_begin, info_continue, info_end
        info_begin("Reticulating splines...")
        info_continue(" nearly done...")
        info_continue(" almost done...")
        info_end(" done!")
        self.assertEqual(
            sys.stdout.getvalue(),
            "Reticulating splines... nearly done... almost done... done!\n")

    def test_info_emits_newline_when_needed(self):
        from check_manifest import info_begin, info
        info_begin("Computering...")
        info("Forgot to turn the gas off!")
        self.assertEqual(
            sys.stdout.getvalue(),
            "Computering...\n"
            "Forgot to turn the gas off!\n")

    def test_warning(self):
        from check_manifest import info_begin, warning
        info_begin("Computering...")
        warning("Forgot to turn the gas off!")
        self.assertEqual(
            sys.stdout.getvalue(),
            "Computering...\n")
        self.assertEqual(
            sys.stderr.getvalue(),
            "Forgot to turn the gas off!\n")

    def test_error(self):
        from check_manifest import info_begin, error
        info_begin("Computering...")
        error("Forgot to turn the gas off!")
        self.assertEqual(
            sys.stdout.getvalue(),
            "Computering...\n")
        self.assertEqual(
            sys.stderr.getvalue(),
            "Forgot to turn the gas off!\n")


class TestCheckManifest(unittest.TestCase):

    _vcs = GitHelper()

    def setUp(self):
        self.oldpwd = os.getcwd()
        self.tmpdir = tempfile.mkdtemp(prefix='test-', suffix='-check-manifest')
        os.chdir(self.tmpdir)
        self._stdout_patcher = mock.patch('sys.stdout', StringIO())
        self._stdout_patcher.start()
        self._stderr_patcher = mock.patch('sys.stderr', StringIO())
        self._stderr_patcher.start()

    def tearDown(self):
        self._stderr_patcher.stop()
        self._stdout_patcher.stop()
        os.chdir(self.oldpwd)
        rmtree(self.tmpdir)

    def _create_repo_with_code(self):
        self._vcs._init_vcs()
        with open('setup.py', 'w') as f:
            f.write("from setuptools import setup\n")
            f.write("setup(name='sample', py_modules=['sample'])\n")
        with open('sample.py', 'w') as f:
            f.write("# wow. such code. so amaze\n")
        self._vcs._add_to_vcs(['setup.py', 'sample.py'])

    def _add_to_vcs(self, filename, content=''):
        if os.path.sep in filename and not os.path.isdir(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, 'w') as f:
            f.write(content)
        self._vcs._add_to_vcs([filename])

    def test_not_python_project(self):
        from check_manifest import check_manifest, Failure
        with self.assertRaises(Failure) as cm:
            check_manifest()
        self.assertEqual(str(cm.exception),
                         "This is not a Python project (no setup.py).")

    def test_all_is_well(self):
        from check_manifest import check_manifest
        self._create_repo_with_code()
        self.assertTrue(check_manifest())

    def test_relative_pathname(self):
        from check_manifest import check_manifest
        os.mkdir('subdir')
        os.chdir('subdir')
        self._create_repo_with_code()
        os.chdir(os.pardir)
        self.assertTrue(check_manifest('subdir'))

    def test_suggestions(self):
        from check_manifest import check_manifest
        self._create_repo_with_code()
        self._add_to_vcs('unrelated.txt')
        self.assertFalse(check_manifest())
        self.assertIn("missing from sdist:\n  unrelated.txt",
                      sys.stderr.getvalue())
        self.assertIn("suggested MANIFEST.in rules:\n  include *.txt",
                      sys.stdout.getvalue())

    def test_suggestions_create(self):
        from check_manifest import check_manifest
        self._create_repo_with_code()
        self._add_to_vcs('unrelated.txt')
        self.assertFalse(check_manifest(create=True))
        self.assertIn("missing from sdist:\n  unrelated.txt",
                      sys.stderr.getvalue())
        self.assertIn("suggested MANIFEST.in rules:\n  include *.txt",
                      sys.stdout.getvalue())
        self.assertIn("creating MANIFEST.in",
                      sys.stdout.getvalue())
        with open('MANIFEST.in') as f:
            self.assertEqual(f.read(), "include *.txt\n")

    def test_suggestions_update(self):
        from check_manifest import check_manifest
        self._create_repo_with_code()
        self._add_to_vcs('unrelated.txt')
        self._add_to_vcs('MANIFEST.in', '#tbd')
        self.assertFalse(check_manifest(update=True))
        self.assertIn("missing from sdist:\n  unrelated.txt",
                      sys.stderr.getvalue())
        self.assertIn("suggested MANIFEST.in rules:\n  include *.txt",
                      sys.stdout.getvalue())
        self.assertIn("updating MANIFEST.in",
                      sys.stdout.getvalue())
        with open('MANIFEST.in') as f:
            self.assertEqual(
                f.read(),
                "#tbd\n# added by check_manifest.py\ninclude *.txt\n")

    def test_suggestions_all_unknown_patterns(self):
        from check_manifest import check_manifest
        self._create_repo_with_code()
        self._add_to_vcs('.dunno-what-to-do-with-this')
        self.assertFalse(check_manifest(update=True))
        self.assertIn("missing from sdist:\n  .dunno-what-to-do-with-this",
                      sys.stderr.getvalue())
        self.assertIn(
            "don't know how to come up with rules matching any of the files, sorry!",
            sys.stdout.getvalue())

    def test_suggestions_some_unknown_patterns(self):
        from check_manifest import check_manifest
        self._create_repo_with_code()
        self._add_to_vcs('.dunno-what-to-do-with-this')
        self._add_to_vcs('unrelated.txt')
        self.assertFalse(check_manifest(update=True))
        self.assertIn(
            "don't know how to come up with rules matching\n  .dunno-what-to-do-with-this",
            sys.stdout.getvalue())
        self.assertIn("creating MANIFEST.in",
                      sys.stdout.getvalue())
        with open('MANIFEST.in') as f:
            self.assertEqual(f.read(), "include *.txt\n")

    def test_MANIFEST_in_does_not_need_to_be_added_to_be_considered(self):
        from check_manifest import check_manifest
        self._create_repo_with_code()
        self._add_to_vcs('unrelated.txt')
        with open('MANIFEST.in', 'w') as f:
            f.write("include *.txt\n")
        self.assertFalse(check_manifest())
        self.assertIn("missing from VCS:\n  MANIFEST.in", sys.stderr.getvalue())
        self.assertNotIn("missing from sdist", sys.stderr.getvalue())

    def test_bad_ideas(self):
        from check_manifest import check_manifest
        self._create_repo_with_code()
        self._add_to_vcs('foo.egg-info')
        self._add_to_vcs('moo.mo')
        self.assertFalse(check_manifest())
        self.assertIn("you have foo.egg-info in source control!",
                      sys.stderr.getvalue())
        self.assertIn("this also applies to the following:\n  moo.mo",
                      sys.stderr.getvalue())


def test_suite():
    return unittest.TestSuite([
        unittest.defaultTestLoader.loadTestsFromName(__name__),
        doctest.DocTestSuite('check_manifest'),
    ])
