import cPickle
import gevent
import json
import logging
import os
import psutil
import subprocess
import shutil

try:
    from slugify import slugify
except:
    logging.error('Missing python-slugify module!')
    raise

import ajenti
from ajenti.api import *
from ajenti.api.http import HttpPlugin, url
from ajenti.plugins.main.api import SectionPlugin
from ajenti.plugins.services.api import ServiceMultiplexor
from ajenti.ui import on
from ajenti.ui.binder import Binder
from ajenti.plugins import manager
from ..usermgr import ElementsUserManager
from ..ipmap import ElementsIPMapper
from ..shaper.main import Shaper

from reconfigure.configs import SambaConfig, ExportsConfig, NetatalkConfig

import reconfigure.items.samba
import reconfigure.items.netatalk
import reconfigure.items.exports


try:
    FS_ROOT = os.readlink('/var/lib/elements/workspaces-root')
except:
    FS_ROOT = '/mnt/snfs1/'


IDENTIFICATION_COMMENT = 'Created by Elements Storage, do not edit'
ROOT = os.path.join(FS_ROOT, '.projects')
TEMPLATE_ROOT = '/var/lib/elements/templates'


# Detect components

snfs_present = os.path.exists('/usr/cvfs/bin/cvadmin')
if not snfs_present:
    logging.warn('SNFS support not present')

try:
    subprocess.check_call(['which', 'snquota'])
    subprocess.check_call(['snquota', '-L', '-Fsnfs1'])
    quotas_present = True
except:
    quotas_present = False
if not quotas_present:
    logging.warn('SNFS quota support not present')


class ElementsProject (object):
    def __init__(self):
        self.name = ''
        self.directory = ''
        self.permissions = []
        self.quota_size_usage = 0
        self.quota_size_current = 0
        self.verify()

    @classmethod
    def from_json(cls, json={}):
        self = cls()
        self.name = json.get('id', '')
        self.name = json.get('name', '')
        self.directory = json.get('directory', '')
        self.permissions = [ElementsProjectPermission.from_json(x) for x in json.get('permissions', [])]
        self.quota_size = json.get('quota_size_soft', 0)
        self.quota_size = json.get('quota_size_hard', 0)
        self.description = json.get('description', '')
        self.share_afp = json.get('share_afp', False)
        self.share_nfs = json.get('share_nfs', False)
        self.share_smb = json.get('share_smb', False)
        self.sharing_hidden = json.get('sharing_hidden', False)
        self.sharing_require_login = json.get('sharing_require_login', False)
        self.read_only = json.get('read_only', False)
        return self

    @property
    def path(self):
        if not hasattr(self, 'directory') or not self.directory:
            self.directory = slugify(self.name)
        return os.path.join(ROOT, self.directory)

    def verify(self):
        if not hasattr(self, 'directory') or not self.directory:
            self.directory = slugify(self.name)
        defaults = {
            'id': None,
            'description': '',
            'long_description': '',
            'emulate_avid': False,
            'share_nfs': False,
            'share_afp': False,
            'share_smb': False,
            'sharing_hidden': False,
            'sharing_require_login': False,
            'quota_size_hard': 0,
            'quota_size_soft': 0,
            'known_quota_size_hard': 0,
            'known_quota_size_soft': 0,
            'affinity': None,
            'read_only': False,
        }
        for k, v in defaults.iteritems():
            if not hasattr(self, k):
                setattr(self, k, v)

        if os.listdir(FS_ROOT):
            if self.directory and not os.path.exists(self.path):
                os.mkdir(self.path)

    def json(self):
        return {
            'name': self.name,
            'path': self.path,
            'directory': self.directory,
            'emulate_avid': self.emulate_avid,
            'read_only': self.read_only,
            'quota_size_usage': self.quota_size_usage,
            'quota_size_current': self.quota_size_current * 1024 * 1024 * 1024,
            'quota_size_hard': self.known_quota_size_hard * 1024 * 1024 * 1024,
        }

    def is_allowed_for(self, user):
        umgr = ElementsUserManager.get(manager.context)
        for p in self.permissions:
            if p.user == user or umgr.user_in_group(user, p.user):
                return True
        return False


class ElementsProjectPermission (object):
    def __init__(self):
        self.project = None
        self.user = 'root'

    @classmethod
    def from_json(cls, json={}):
        self = ElementsProjectPermission()
        self.user = json.get('user')
        self.read_only = json.get('read_only', False)
        return self


@plugin
@persistent
@rootcontext
class ElementsProjectManager (BasePlugin):
    default_classconfig = {'projects': ''}
    classconfig_root = True

    def init(self):
        self.smb_config = SambaConfig(path='/etc/samba/smb.conf')
        self.afp_config = NetatalkConfig(path='/etc/afp.conf')
        self.nfs_config = ExportsConfig(path='/etc/exports')

        self.umgr = ElementsUserManager.get()
        self.stripegroups = StripeGroups.get()

        if os.listdir(FS_ROOT):
            if not os.path.exists(ROOT):
                os.mkdir(ROOT)
            for subdir in ['.benchmark']:
                p = os.path.join(ROOT, subdir)
                if not os.path.exists(p):
                    os.mkdir(p)
        else:
            logging.error('SNFS root is empty: %s' % FS_ROOT)
            return

        try:
            pickle = str(self.classconfig['projects'])
            try:
                pickle = pickle.decode('base64')
            except:
                import traceback
                traceback.print_exc()
            self.projects = cPickle.loads(pickle)
        except Exception, e:
            import traceback
            traceback.print_exc()
            self.projects = []

        for p in self.projects:
            p.verify()

        self.active_users = {}

    def get_project(self, name):
        for p in self.projects:
            if p.name == name:
                return p
        return None

    def login(self, name, user):
        p = self.get_project(name)
        self.active_users.setdefault(user, set())
        if p:
            self.active_users[user].add(p)
        return True

    def logout(self, name, user):
        p = self.get_project(name)
        self.active_users.setdefault(user, set())
        if p:
            if p in self.active_users[user]:
                self.active_users[user].remove(p)
        else:
            del self.active_users[user]
        return False

    def __call_quota(self, p, args):
        d = subprocess.check_output(['snquota', '-F', 'snfs1', '-d', '.projects/' + p.directory] + args)
        return d

    def _parse_quotasize(self, s):
        sfx = s[-1]
        i = float(s[:-1])
        if sfx == 'K':
            i *= 1024
        if sfx == 'M':
            i *= 1024 ** 2
        if sfx == 'G':
            i *= 1024 ** 3
        if sfx == 'T':
            i *= 1024 ** 4
        return i / (1024 ** 3)

    def list_templates(self):
        return sorted(os.listdir(unicode(TEMPLATE_ROOT)))

    def create_project(self, p, template=None):
        self.projects.append(p)
        if template:
            if quotas_present:
                self.__call_quota(p, ['-D'])
            shutil.copytree(os.path.join(TEMPLATE_ROOT, template), p.path)
        p.verify()
        if quotas_present:
            self.__call_quota(p, ['-C'])
        self.save()
        subprocess.call(['chmod', '777', '-R', p.path])

    def delete_project(self, p):
        self.projects.remove(p)
        if quotas_present:
            self.__call_quota(p, ['-D'])

    def save(self, reload=True):
        self.projects = sorted(self.projects, key=lambda x: x.name)

        self.stripegroups.refresh()

        self.smb_config.load()
        self.nfs_config.load()
        self.afp_config.load()

        for share in self.smb_config.tree.shares:
            if share.comment == IDENTIFICATION_COMMENT:
                try:
                    self.smb_config.tree.shares.remove(share)
                except:
                    pass

        for share in self.nfs_config.tree.exports:
            if share.comment == IDENTIFICATION_COMMENT:
                self.nfs_config.tree.exports.remove(share)

        for share in self.afp_config.tree.shares:
            if share.comment == IDENTIFICATION_COMMENT:
                self.afp_config.tree.shares.remove(share)

        getattr(self.afp_config.tree, 'global').uam_list = 'uams_guest.so,uams_clrtxt.so,uams_dhx.so'

        for p in self.projects:
            if quotas_present:
                qh = p.quota_size_hard
                qs = p.quota_size_soft
                if not p.quota_size_hard:
                    qh = psutil.disk_usage(FS_ROOT).total / 1024 / 1024 / 1024
                    if p.affinity:
                        sg = self.stripegroups.get_group(p.affinity)
                        if sg:
                            qh = sg.total_b / 1024 / 1024 / 1024
                if qs == 0:
                    qs = qh
                self.__call_quota(p, ['-S', '-h', '%sg' % qh, '-s', '%sg' % qs, '-t', '1d'])
                p.known_quota_size_hard = qh
                p.known_quota_size_soft = qs

            s = reconfigure.items.samba.ShareData()
            s.name = p.name + '_'
            s.comment = IDENTIFICATION_COMMENT
            s.read_only = p.read_only
            s.browseable = not p.sharing_hidden
            s.guest_ok = not p.sharing_require_login
            s.path = os.path.join(ROOT, p.directory)
            s.create_mask = '0777'
            s.directory_mask = '0777'
            s.dfree_command = '/var/lib/ajenti/plugins/elements/bin/dfree %s' % p.path
            s.dfree_cache_time = '10'
            s.valid_users = ','.join(['root'] + [self.umgr.get_unix_username(x.user) for x in p.permissions])
            if not p.sharing_require_login:
                s.valid_users = ''
            if p.emulate_avid:
                s.fstype = 'AVIDFOS'
            self.smb_config.tree.shares.append(s)

            if p.share_nfs:
                s = reconfigure.items.exports.ExportData()
                s.name = os.path.join(ROOT, p.directory)
                c = reconfigure.items.exports.ClientData()
                c.name = '*'
                c.options = '%s,insecure,all_squash,async,no_subtree_check,anonuid=0,anongid=0' % ('ro' if p.read_only else 'rw')
                s.comment = IDENTIFICATION_COMMENT
                s.clients.append(c)
                self.nfs_config.tree.exports.append(s)

            if p.share_afp:
                s = reconfigure.items.netatalk.ShareData()
                s.name = p.name
                s.comment = IDENTIFICATION_COMMENT
                s.path = os.path.join(ROOT, p.directory)
                s.read_only = p.read_only
                s.valid_users = 'root,client'
                self.afp_config.tree.shares.append(s)

            if snfs_present:
                if p.affinity:
                    subprocess.call(['/usr/cvfs/bin/cvaffinity', '-s', p.affinity, p.path])

        self.smb_config.save()
        self.nfs_config.save()
        self.afp_config.save()

        if reload:
            ServiceMultiplexor.get().get_one('smb' if ajenti.platform == 'centos' else 'smbd').command('reload')
            subprocess.call(['exportfs', '-a'])
            #ServiceMultiplexor.get().get_one('nfs' if ajenti.platform == 'centos' else 'nfs-kernel-server').restart()
            #ServiceMultiplexor.get().get_one('netatalk').restart()
            subprocess.call(['pkill', '-HUP' 'afpd'])

        self.classconfig['projects'] = cPickle.dumps(self.projects).encode('base64')
        self.save_classconfig()

    def refresh(self):
        if quotas_present:
            # Read quota status
            q = json.loads(subprocess.check_output(['snquota', '-L', '-Fsnfs1', '-ojson']))
            q = q['directoryQuotas']
            for e in q:
                if e['type'] == 'dir':
                    for p in self.projects:
                        if e['name'] == '/.projects/' + p.directory:
                            p.quota_size_status = e['status']
                            try:
                                p.quota_size_current = self._parse_quotasize(e['curSize'])
                                p.quota_size_usage = p.quota_size_current / p.quota_size_hard
                            except:
                                p.quota_size_current = 0
                                p.quota_size_usage = 0


class StripeGroup (object):
    def __init__(self):
        self.name = self.usage = self.free = self.affinity = None
        self.total_b = 1


@persistent
@plugin
@rootcontext
class StripeGroups (BasePlugin):
    def init(self):
        self.groups = []

    def get_group(self, affinity):
        for g in self.groups:
            if g.affinity == affinity:
                return g

    def refresh(self):
        if subprocess.call(['which', 'cvadmin']) != 0:
            return
        self.groups = []
        ll = subprocess.check_output(['cvadmin', '-e', 'select snfs1; show long'])
        g = None
        for l in ll.splitlines():
            l = l.strip()
            if l.startswith('Stripe Group '):
                g = StripeGroup()
                g.name = l.split('[')[1].split(']')[0]
                self.groups.append(g)
            if l.startswith('Total Blocks:'):
                g.usage = 1.0 - float(l.split('(')[-1][:-2]) / 100
                g.free = l.split('(')[-2].split(')')[0]
                g.total_b = int(l.split()[1].split(':')[-1]) * 4096
            if l.startswith('Affinity Key:'):
                g.affinity = l.split(':')[1].strip()


ElementsProjectManager.get().save(reload=False)


@plugin
class ElementsProjects (SectionPlugin):
    def init(self):
        self.title = 'Workspaces'
        self.icon = 'suitcase'
        self.category = 'Elements'
        self.append(self.ui.inflate('elements:projects-main'))

        self.find('permissions').new_item = lambda c: ElementsProjectPermission()

        def post_project_bind(o, c, i, u):
            def on_set_affinity():
                i.affinity = u.find('affinity').value
                self.save()
            u.find('set-affinity').on('click', on_set_affinity)
            def on_rescan():
                self.context.launch('media-library:rescan', path=i.path)
            u.find('rescan').on('click', on_rescan)

        self.find('projects').post_item_bind = post_project_bind
        self.find('projects').delete_item = lambda i, c: self.delete_project(i)

        self.mgr = ElementsProjectManager.get()
        self.umgr = ElementsUserManager.get()
        self.stripegroups = StripeGroups.get()
        self.binder = Binder(self.mgr, self)
        self.sg_binder = Binder(self.stripegroups, self.find('stripegroups'))

        self.find('affinity-box').visible = snfs_present
        self.find('quotas-box').visible = quotas_present
        if not quotas_present:
            self.find('quotas-tab').delete()

    def on_page_load(self):
        self.refresh()

    def delete_project(self, p):
        self.mgr.delete_project(p)
        self.save()

    def refresh(self):
        self.stripegroups.refresh()
        self.sg_binder.populate()
        self.mgr.refresh()

        self.binder.unpopulate()
        self.find('affinity').labels = self.find('affinity').values = [x.affinity for x in self.stripegroups.groups if x.affinity]
        self.find('user-dropdown').labels = [x.name for x in ajenti.config.tree.users.values()] + ['"%s" group' % x.name for x in self.umgr.groups]
        self.find('user-dropdown').values = [x.name for x in ajenti.config.tree.users.values()] + [x.name for x in self.umgr.groups]
        self.binder.populate()

        self.find('new-project-template').labels = ['Without template'] + self.mgr.list_templates()
        self.find('new-project-template').values = [''] + self.mgr.list_templates()
        self.find('new-project-template').value = ''

    @on('new-project', 'click')
    def on_new_project(self):
        template = self.find('new-project-template').value
        self.save()
        p = ElementsProject()
        p.name = self.find('new-project-name').value
        if p.name:
            for project in self.mgr.projects:
                if project.name == p.name:
                    self.context.notify('error', 'There is already a project with this name')
                    return
            self.mgr.create_project(p, template=template)
            self.refresh()
            self.find('new-project-name').value = ''

    @on('save', 'click')
    def save(self):
        self.binder.update()
        self.mgr.save()
        self.refresh()


@plugin
class ElementsProjectServer (HttpPlugin):
    def init(self):
        self.mgr = ElementsProjectManager.get()
        self.ipmapper = ElementsIPMapper.get()

    @url('/elements/projects/(?P<endpoint>.+)')
    def get_page(self, context, endpoint):
        if context.session.identity is None:
            context.respond_forbidden()

        context.respond_ok()

        endpoint = endpoint.split('/')

        if endpoint[0] == 'test':
            return 'ok'

        if endpoint[0] == 'login':
            self.ipmapper.register(context.session.identity, context.env['REMOTE_ADDR'])
            Shaper.get(manager.context).refresh_ips()
            self.mgr.login(endpoint[1], context.session.identity)
            return 'ok'

        if endpoint[0] == 'logout':
            self.mgr.logout(endpoint[1], context.session.identity)
            return 'ok'

        if endpoint[0] == 'list-projects':
            self.mgr.refresh()
            return json.dumps([p.json() for p in self.mgr.projects if p.is_allowed_for(context.session.identity)])

        if endpoint[0] == 'stats':
            iostat = subprocess.Popen(['iostat', '-xd', '1', '2'], stdout=subprocess.PIPE)
            gevent.sleep(1)
            o, e = iostat.communicate()
            lines = o.splitlines()

            s = 0
            for l in lines[len(lines)/2:]:
                try:
                    s += float(l.split()[-1])
                except:
                    pass

            return str(int(s))
