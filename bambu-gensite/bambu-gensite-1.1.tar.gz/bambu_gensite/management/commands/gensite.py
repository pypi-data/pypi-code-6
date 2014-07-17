from django.db import transaction
from django.db.models import Model, get_model, get_app
from django.db.models.query import QuerySet
from django.db.models import OneToOneField, ForeignKey, ManyToManyField, FileField
from django.contrib.webdesign.lorem_ipsum import paragraph, words
from django.utils.importlib import import_module
from django.contrib.sites.models import Site
from django.template import Template, Context
from django.template.loader import add_to_builtins
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from tempfile import mkstemp
from mimetypes import guess_extension
from os import write, close, path
from yaml import safe_load
from collections import defaultdict
import compiler, requests, re

LIPSUM_PARAGRAPH = re.compile(r'^lipsum\.paragraph(?:\((\d+)\))?$')
LIPSUM_WORDS = re.compile(r'^lipsum\.words(?:\((\d+)\))?$')

class Command(BaseCommand):
    help = u'Generate a site\'s data from a YAML file'
    generators = {
        'auth.user': 'bambu_gensite.generators.auth.user'
    }

    def __init__(self, *args, **kwargs):
        self._indent = 0
        super(Command, self).__init__(*args, **kwargs)

    def _log(self, t, i = 0):
        line = []
        co = False

        line.append(
            '\033[0m'
        )

        for c in t:
            if c == '*':
                if not co:
                    # Start priting in 'bold'
                    co = True
                    line.append(
                        '\033[94m'
                    )
                else:
                    # Stop printing in 'bold'
                    co = False
                    line.append(
                        '\033[0m'
                    )

            else:
                line.append(c)

        if co:
            line.append(
                '\033[0m'
            )

        self.stdout.write('  ' * (i + self._indent) + ''.join(line))

    def add_arguments(self, parser):
        parser.add_argument('file', nargs = 1, type = 'str')

    def get_generator(self, name):
        generator = self.generators.get(name)
        if not generator:
            return

        try:
            module, dot, function = generator.rpartition('.')
        except:
            return

        try:
            module = import_module(module)
        except ImportError:
            return

        try:
            return getattr(module, function)
        except:
            pass

    def query(self, model, count = None, context = None, **kwargs):
        if not context:
            context = {}

        q = model.objects.all()
        if 'where' in kwargs:
            q = q.filter(
                **dict(
                    (
                        k,
                        self.render(v, context)
                    ) for (k, v) in kwargs['where'].items()
                )
            )

        if 'exclude' in kwargs:
            q = q.exclude(
                **dict(
                    (
                        k,
                        self.render(v, context)
                    ) for (k, v) in kwargs['exclude'].items()
                )
            )

        if 'from' in kwargs:
            if count:
                q = q[
                    kwargs['from']:count
                ]
            else:
                q = q[
                    kwargs['from']:
                ]
        elif 'at' in kwargs:
            if kwargs['at'] == 'random':
                q = q.order_by('?')
                if count:
                    q = q[:count]
            else:
                raise CommandError(
                    'Unrecognised value for \'at\' (%s)' % kwargs['at']
                )

        return q

    def render(self, value, context):
        return Template(
            value
        ).render(
            Context(
                context
            )
        )

    def make_generator(self, model, data, context):
        fields = {}
        m2ms = defaultdict(list)

        if data:
            for key, value in data.items():
                if isinstance(value, (str, unicode)):
                    if '{{' in value:
                        v = self.render(value, context)
                    else:
                        v = value

                    if v.startswith("'") and v.endswith("'"):
                        v = unicode(v[1:-1])
                    else:
                        match = LIPSUM_PARAGRAPH.match(v)
                        if match:
                            groups = match.groups()
                            if groups[0]:
                                v = paragraph(int(groups[0]))
                            else:
                                v = paragraph()
                        else:
                            match = LIPSUM_WORDS.match(v)
                            if match:
                                groups = match.groups()
                                if groups[0]:
                                    v = words(int(groups[0]), False).capitalize()
                                else:
                                    v = words(1, False).capitalize()
                else:
                    if isinstance(value, dict):
                        ff = model._meta.get_field_by_name(key)
                        if isinstance(ff[0], ManyToManyField):
                            c = value.get('count', 1)
                            o = ff[0].rel.to

                            if 'fields' in value:
                                self._indent += 1

                                gg = self.make_generator(o, value['fields'],
                                    {
                                        'parent': context
                                    }
                                )

                                for ag in gg(o, c, self._log):
                                    m2ms[key].append(ag)

                                self._indent -= 1
                            elif 'from' in value or 'at' in value or 'where' in value or 'exclude' in value:
                                m2ms[key] = self.query(
                                    o,
                                    context = context,
                                    **value
                                )
                            else:
                                raise CommandError(
                                    'No data specified for many-to-many relationship between %s and %s' % (
                                        unicode(model._meta.verbose_name),
                                        unicode(o._meta.verbose_name)
                                    )
                                )

                            continue

                        if isinstance(ff[0], (OneToOneField, ForeignKey)):
                            o = ff[0].rel.to
                            if 'fields' in value:
                                self._indent += 1

                                gg = self.make_generator(o, value['fields'],
                                    {
                                        'parent': context
                                    }
                                )

                                for ag in gg(o, 1, self._log):
                                    v = ag

                                self._indent -= 1
                            elif 'at' in value or 'where' in value or 'exclude' in value:
                                try:
                                    v = self.query(
                                        o,
                                        count = 1,
                                        context = context,
                                        **value
                                    )[0]
                                except IndexError:
                                    raise CommandError(
                                        'No %s found to add' % (
                                            unicode(o._meta.verbose_name_plural)
                                        )
                                    )
                            else:
                                raise CommandError(
                                    'No data specified for foreign key relationship between %s and %s' % (
                                        unicode(model._meta.verbose_name),
                                        unicode(o._meta.verbose_name)
                                    )
                                )
                    else:
                        v = value

                fields[key] = v

        obj = context.get('object')
        if isinstance(obj, Model):
            for field in model._meta.get_all_field_names():
                af = model._meta.get_field_by_name(field)
                if isinstance(af[0], (OneToOneField, ForeignKey)):
                    if not field in fields:
                        if issubclass(af[0].rel.to, type(obj)):
                            fields[field] = obj
                elif isinstance(af[0], FileField):
                    filename = fields.get(field)
                    if filename:
                        if filename.startswith('http:') or filename.startswith('https:'):
                            fields[field] = self.download(filename)
                        else:
                            if not filename.startswith('/'):
                                filename = path.join(
                                    path.dirname(
                                        get_app(model._meta.app_label).__file__
                                    ),
                                    filename
                                )

                            if not path.exists(filename):
                                raise CommandError('Cannot find file %s' % filename)

                            fields[field] = File(
                                open(filename, 'r')
                            )

        def g(model, count, log, **kwargs):
            for x in range(0, count):
                obj = model(**fields)

                if 'password' in fields:
                    obj.set_password(
                        fields.pop('password')
                    )

                try:
                    obj.full_clean()
                except ValidationError, ex:
                    raise CommandError(
                        u'Error creating %s' % (
                            model._meta.verbose_name
                        ),
                        ex
                    )

                obj.save()
                yield obj

                for m, i in m2ms.items():
                    field = getattr(obj, m)
                    field.add(*i)

                    c = len(i)
                    if isinstance(i, QuerySet):
                        self._log(
                            'Added %d %s' % (
                                c,
                                c != 1 and unicode(
                                    i.model._meta.verbose_name_plural
                                ) or unicode(
                                    i.model._meta.verbose_name
                                )
                            ),
                            1
                        )
                    else:
                        self._log(
                            'Created %d %s' % (
                                c,
                                c != 1 and unicode(
                                    i[0]._meta.verbose_name_plural
                                ) or unicode(
                                    i[0]._meta.verbose_name
                                )
                            ),
                            1
                        )

        return g

    def download(self, url):
        self._log('Downloading *%s*' % url)
        response = requests.get(url)
        t = response.headers.get('content-type', '').split(';')
        extension = guess_extension(t[0])

        handle, filename = mkstemp(extension or '')
        write(handle, response.content)
        close(handle)

        return File(
            open(filename, 'rb')
        )

    def load_json(self, json, root = None, **kwargs):
        try:
            data = requests.get(json).json()
        except:
            raise CommandError('Error getting JSON data from %s' % json)

        self._log('Generating data from JSON source at *%s*' % json)
        if root:
            data = data.get(root)
            if not data:
                raise CommandError(
                    'Root item %s not found in JSON resource' % root
                )

        return data

    def load_model(self, model, count = None, **kwargs):
        try:
            model = get_model(*model.lower().split('.'))
        except:
            raise CommandError('Cannot find model %s' % model)

        self._log('Generating data from *%s*' % unicode(model._meta.verbose_name_plural))
        return self.query(
            model,
            count,
            **kwargs
        )

    @transaction.commit_on_success()
    def handle(self, filename, **options):
        add_to_builtins(
            'bambu_gensite.templatetags'
        )

        yaml = safe_load(
            open(filename, 'r')
        )

        def gen(model, count = 1, foreach = None, context = None, fields = None, **kwargs):
            if not context:
                context = {}

            iif = kwargs.get('if', '')
            if iif:
                expr = compiler.compile(iif, '<string>', 'eval')
                result = eval(expr, context or {})
                if not result:
                    return

            if not count:
                raise CommandError('Model %s must create 1 or more objects' % model)

            mnl = model.lower()

            try:
                o = get_model(*mnl.split('.'))
            except:
                raise CommandError('Cannot find model %s' % model)

            g = not fields and self.get_generator(mnl) or None
            if not g:
                g = self.make_generator(o, fields, context)

            v = o._meta.verbose_name
            alt = False

            for obj in g(o, count, lambda t: self._log(t, 1)):
                self._log(
                    u'Created %s *%s*' % (
                        unicode(v),
                        unicode(obj)
                    )
                )

                for pf in kwargs.get('print', []):
                    try:
                        self._log(
                            '%s: *%s*' % (
                                pf,
                                self.render(fields[pf], context)
                            ),
                            1
                        )
                    except KeyError:
                        self._log(
                            '%s: *%s*' % (
                                pf,
                                self.render(
                                    getattr(obj, pf),
                                    context
                                )
                            ),
                            1
                        )

                if foreach:
                    self._indent += 1
                    for f in foreach:
                        models = f.get('create', [])
                        for m in models:
                            gen(
                                context = {
                                    'object': obj,
                                    'alt': alt,
                                    'parent': context
                                },
                                **m
                            )

                        alt = not alt
                    self._indent -= 1

        site_id = 1
        for s in yaml:
            if Site.objects.filter(pk = site_id).exists():
                Site.objects.filter(
                    pk = site_id
                ).update(
                    domain = s.get('domain', 'example.com'),
                    name = s.get('name', s.get('domain', 'example.com'))
                )

                site = Site.objects.get(pk = 1)
            else:
                site = Site.objects.create(
                    domain = s.get('domain', 'example.com'),
                    name = s.get('name', s.get('domain', 'example.com'))
                )

            site_id += 1
            for source in s.get('sources', []):
                alt = False
                if source.get('json'):
                    data = self.load_json(**source)
                elif source.get('model'):
                    data = self.load_model(**source)
                else:
                    raise CommandError(
                        'Unrecognised source (must be either \'model\' or \'json\')'
                    )

                for e, item in enumerate(data):
                    self._indent += 1
                    for f in source.get('foreach', []):
                        for m in f.get('create', []):
                            gen(
                                context = {
                                    'alt': alt,
                                    'object': item,
                                    'forloop': {
                                        'counter': e + 1,
                                        'first': e == 0,
                                        'last': e == len(data) - 1
                                    }
                                },
                                **m
                            )

                    alt = not alt
                    self._indent -= 1

            for m in s.get('create', []):
                gen(**m)
