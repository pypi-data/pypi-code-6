import json
import logging
import os
import subprocess
import psutil
import shutil

import ajenti
from ajenti.api import *
from ajenti.ipc import IPCHandler
from ajenti.plugins.services.api import ServiceMultiplexor

from reconfigure.configs import SambaConfig, ExportsConfig, NetatalkConfig
import reconfigure.items.samba
import reconfigure.items.netatalk
import reconfigure.items.exports

from ..usermgr import ElementsUserManager



IDENTIFICATION_COMMENT = 'Created by Elements Storage, do not edit'
TEMPLATE_ROOT = '/data/%s/.elements/templates'


class ElementsWorkspace (object):
    @classmethod
    def from_json(cls, j={}):
        self = cls()
        self.id = j.get('id', '')
        self.name = j.get('name', '')
        self.project_name = j.get('project_name', '')
        self.volume_name = j.get('volume_name', '')
        self.directory = j.get('directory', '')
        self.mac_protocol = j.get('mac_protocol', '')
        self.rw_access_group = j['rw_access_group']
        self.ro_access_group = j['ro_access_group']
        self.quota_size_soft = j.get('quota_size_soft', 0)
        self.quota_size_hard = j.get('quota_size_hard', 0)
        self.description = j.get('description', '')
        self.share_afp = j.get('share_afp', False)
        self.share_nfs = j.get('share_nfs', False)
        self.sharing_hidden = j.get('sharing_hidden', False)
        self.sharing_require_login = j.get('sharing_require_login', False)
        self.read_only = j.get('read_only', False)
        self.emulate_avid = j.get('emulate_avid', False)
        self.affinity = j.get('affinity', None)
        return self

    @property
    def path(self):
        return os.path.join('/data', self.volume_name, '.projects', self.directory)


@plugin
@persistent
@rootcontext
class ElementsWorkspaceManager (BasePlugin):
    def init(self):
        self.supports_snfs = os.path.exists('/usr/cvfs/bin/cvadmin')
        if not self.supports_snfs:
            logging.warn('SNFS support not present')

        self.supports_afp = os.path.exists('/etc/afp.conf')
        if not self.supports_afp:
            logging.warn('AFP support not present')

        try:
            subprocess.check_call(['which', 'snquota'])
            subprocess.check_call(['snquota', '-L', '-Fsnfs1'])
            self.supports_quotas = True
        except:
            self.supports_quotas = False
        if not self.supports_quotas:
            logging.warn('SNFS quota support not present')

        self.smb_config = SambaConfig(path='/etc/samba/smb.conf')
        if self.supports_afp:
            self.afp_config = NetatalkConfig(path='/etc/afp.conf')
        self.nfs_config = ExportsConfig(path='/etc/exports')

        self.stripegroups = StripeGroups.get()
        self.umgr = ElementsUserManager.get()

    def __call_quota(self, workspace, args):
        return subprocess.check_output(['snquota', '-F', 'snfs1', '-d', '.projects/' + workspace.directory] + args)

    def _parse_quotasize(self, s):
        if type(s) in [int, long, float]:
            return s
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
        return i

    def create(self, workspace, template=None):
        if template:
            if self.supports_quotas:
                self.__call_quota(workspace, ['-D'])
            shutil.copytree(os.path.join(TEMPLATE_ROOT % workspace.volume_name, template), workspace.path)
        if not os.path.exists(workspace.path):
            os.makedirs(workspace.path)

        if self.supports_quotas:
            self.__call_quota(workspace, ['-C'])

        subprocess.call(['chmod', '777', '-R', workspace.path])

    def delete(self, workspace):
        if self.supports_quotas:
            self.__call_quota(workspace, ['-D'])

    def configure(self, workspaces):
        self.smb_config.load()
        self.nfs_config.load()
        if self.supports_afp:
            self.afp_config.load()

        self.stripegroups.refresh()

        for share in self.smb_config.tree.shares:
            if share.comment == IDENTIFICATION_COMMENT:
                try:
                    self.smb_config.tree.shares.remove(share)
                except:
                    pass

        for share in self.nfs_config.tree.exports:
            if share.comment == IDENTIFICATION_COMMENT:
                self.nfs_config.tree.exports.remove(share)

        if self.supports_afp:
            getattr(self.afp_config.tree, 'global').uam_list = 'uams_guest.so,uams_clrtxt.so,uams_dhx.so'
            for share in self.afp_config.tree.shares:
                if share.comment == IDENTIFICATION_COMMENT:
                    self.afp_config.tree.shares.remove(share)

        for workspace in workspaces:
            if self.supports_quotas:
                qh = workspace.quota_size_hard
                qs = workspace.quota_size_soft
                if not workspace.quota_size_hard:
                    if workspace.affinity:
                        qh = self.stripegroups.get(workspace.affinity).total_b / 1024 / 1024 / 1024
                    else:
                        qh = psutil.disk_usage(workspace.path).total / 1024 / 1024 / 1024
                if qs == 0:
                    qs = qh
                self.__call_quota(workspace, ['-S', '-h', '%sg' % qh, '-s', '%sg' % qs, '-t', '1d'])
                workspace.known_quota_size_hard = qh
                workspace.known_quota_size_soft = qs

            s = reconfigure.items.samba.ShareData()
            s.name = workspace.project_name + ' ' + workspace.name + '_'
            s.comment = IDENTIFICATION_COMMENT
            s.read_only = workspace.read_only
            s.browseable = not workspace.sharing_hidden
            s.guest_ok = not workspace.sharing_require_login
            s.path = workspace.path
            s.create_mask = '0775'
            s.directory_mask = '0775'
            s.dfree_command = '/var/lib/ajenti/plugins/elements/bin/dfree %s' % workspace.path
            s.dfree_cache_time = '10'
            
            s.valid_users = 'root'
            s.read_list = 'nobody'

            if workspace.rw_access_group:
                s.force_group = self.umgr.get_unix_groupname(workspace.rw_access_group['name'])
                for member in workspace.rw_access_group['members']:
                    s.valid_users += ',' + self.umgr.get_unix_username(member['username'])

            if workspace.ro_access_group:
                for member in workspace.ro_access_group['members']:
                    s.valid_users += ',' + self.umgr.get_unix_username(member['username'])
                    s.read_list += ',' + self.umgr.get_unix_username(member['username'])

            if not workspace.sharing_require_login:
                s.valid_users = ''
            if workspace.emulate_avid:
                s.fstype = 'AVIDFOS'
            self.smb_config.tree.shares.append(s)

            if workspace.mac_protocol == 'nfs':
                if workspace.share_nfs:
                    s = reconfigure.items.exports.ExportData()
                    s.name = workspace.path
                    c = reconfigure.items.exports.ClientData()
                    c.name = '*'
                    c.options = '%s,insecure,all_squash,async,no_subtree_check,anonuid=0,anongid=0' % ('ro' if workspace.read_only else 'rw')
                    s.comment = IDENTIFICATION_COMMENT
                    s.clients.append(c)
                    self.nfs_config.tree.exports.append(s)

            if workspace.mac_protocol == 'afp' or workspace.share_afp:
                if self.supports_afp:
                    s = reconfigure.items.netatalk.ShareData()
                    s.name = workspace.project_name + ' ' + workspace.name + '_'
                    s.comment = IDENTIFICATION_COMMENT
                    s.path = workspace.path
                    s.read_only = workspace.read_only
                    if not workspace.sharing_require_login:
                        s.valid_users = ''
                    else:
                        s.valid_users = 'root,client'
                    self.afp_config.tree.shares.append(s)

            if self.supports_snfs:
                if workspace.affinity:
                    subprocess.call(['/usr/cvfs/bin/cvaffinity', '-s', workspace.affinity, workspace.path])

        self.smb_config.save()
        self.nfs_config.save()
        if self.supports_afp:
            self.afp_config.save()

        if reload:
            ServiceMultiplexor.get().get_one('smb' if ajenti.platform == 'centos' else 'smbd').command('reload')
            subprocess.call(['exportfs', '-a'])
            subprocess.call(['pkill', '-HUP' 'afpd'])

    def get_quotas(self):
        res = {}
        if self.supports_quotas:
            # Read quota status
            q = json.loads(subprocess.check_output(['snquota', '-L', '-Fsnfs1', '-ojson']))
            q = q['directoryQuotas']
            for e in q:
                if e['type'] == 'dir':
                    #for p in self.projects:
                    #    if e['name'] == '/.projects/' + p.directory:
                    quota_size_status = e['status']
                    try:
                        quota_size_current = self._parse_quotasize(e['curSize'])
                        quota_size_soft = self._parse_quotasize(e['softLimit'])
                        quota_size_hard = self._parse_quotasize(e['hardLimit'])
                        if quota_size_hard > 0:
                            quota_size_usage = quota_size_current / quota_size_hard
                        else:
                            quota_size_usage = 0
                    except:
                        import traceback; traceback.print_exc();
                        quota_size_current = 0
                        quota_size_soft = 0
                        quota_size_hard = 0
                        quota_size_usage = 0
                    res[e['name']] = {
                        'current': quota_size_current,
                        'hard': quota_size_hard,
                        'soft': quota_size_soft,
                        'usage': quota_size_usage,
                    }
        return res


class StripeGroup (object):
    def __init__(self):
        self.name = self.usage = self.free = self.affinity = self.status = None
        self.total_b = 1

    def to_json(self):
        return {
            'name': self.name,
            'free': self.free_b,
            'total': self.total_b,
            'used': self.used_b,
            'affinity': self.affinity,
            'status': self.status,
        }


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
            return []
        self.groups = []
        ll = subprocess.check_output(['cvadmin', '-F', 'snfs1', '-e', 'show long'])
        g = None
        for l in ll.splitlines():
            l = l.strip()
            if l.startswith('Stripe Group '):
                g = StripeGroup()
                g.name = l.split('[')[1].split(']')[0]
                g.status = l.split(':')[-1].strip().split(',')
                self.groups.append(g)
            if l.startswith('Total Blocks:'):
                g.usage = 1.0 - float(l.split('(')[-1][:-2]) / 100
                g.total_b = int(l.split()[1].split(':')[-1]) * 4096
                g.used_b = int(g.total_b * g.usage)
                g.free_b = g.total_b - g.used_b
            if l.startswith('Affinity Key:'):
                g.affinity = l.split(':')[1].strip()


@plugin
class WorkspacesIPC (IPCHandler):
    def init(self):
        self.mgr = ElementsWorkspaceManager.get()

    def get_name(self):
        return 'elements:workspaces'

    def handle(self, args):
        command = args[0]

        if command == 'create':
            cfg = json.loads(args[1])
            ElementsWorkspaceManager.get().create(ElementsWorkspace.from_json(cfg), template=cfg.get('template', None))
            return 'OK'

        if command == 'delete':
            cfg = json.loads(args[1])
            ElementsWorkspaceManager.get().delete(ElementsWorkspace.from_json(cfg))
            return 'OK'

        if command == 'configure':
            cfg = json.load(open(args[1]))
            workspaces = [ElementsWorkspace.from_json(x) for x in cfg]
            ElementsWorkspaceManager.get().configure(workspaces)
            return 'OK'

        return 'Unknown command ' + command
