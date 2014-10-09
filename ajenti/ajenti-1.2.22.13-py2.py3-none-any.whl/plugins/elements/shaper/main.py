import logging
import subprocess

from ajenti.api import BasePlugin, plugin
from ajenti.plugins.main.api import SectionPlugin
from ajenti.ui import on
from ajenti.ui.binder import Binder
from ajenti.plugins import manager

from ..ipmap import ElementsIPMapper


class ShaperRule (object):
    def __init__(self, json):
        self.username = None
        self.rate = '1024'
        self.ceil = '1024'
        self.__dict__.update(json)

    def save(self):
        return {
            'username': self.username,
            'ip': self.ip,
            'rate': self.rate,
            'ceil': self.ceil,
        }


@plugin
class Shaper (BasePlugin):
    default_classconfig = {'rules': []}
    classconfig_root = True

    def init(self):
        self.rules = [ShaperRule(x) for x in self.classconfig['rules']]

    def refresh_ips(self):
        ipmapper = ElementsIPMapper.get(manager.context)
        for rule in self.rules:
            if rule.username:
                ip = ipmapper.get_ip(rule.username)
                if ip:
                    rule.ip = ip
        self.save()

    def save(self):
        self.classconfig['rules'] = [x.save() for x in self.rules]
        self.save_classconfig()


        clsname = lambda r: "elements_user_%s_rule_%s" % (r.username, id(r))

        code = "egress {"
        for r in self.rules:
            code += "class ( <$out_%s> ) if ip_dst == %s ; \n" % (clsname(r), r.ip)
        code += "htb {\n"
        for r in self.rules:
            code += "$out_%s = class ( rate %sMbps, ceil %sMbps ) { sfq; } ;\n" % (clsname(r), r.rate, r.ceil)
        code += "}}"

        logging.debug('TCNG script:\n' + code)

        ifaces = [l.strip().split()[0].split(':')[0] for l in open('/proc/net/dev') if ':' in l]

        for iface in ifaces:
            tcng = subprocess.Popen(['tcng', '-q', '-r', '-w', '-i', iface], stdout=subprocess.PIPE)
            o, e = tcng.communicate(code)

            tc_script = o.replace('\n', ';\n')
            logging.debug(tc_script)

            tc = subprocess.Popen(['sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            o, e = tc.communicate(tc_script)

            if tc.returncode:
                raise Exception(e)


@plugin
class ElementsShaperPlugin (SectionPlugin):
    def init(self):
        self.title = 'Shaping'
        self.icon = 'exchange'
        self.category = 'Elements'
        self.append(self.ui.inflate('elements:shaper-main'))

        self.shaper = Shaper.get(manager.context)
        self.ipmapper = ElementsIPMapper.get(manager.context)

        self.binder = Binder(self.shaper, self)

    def on_page_load(self):
        self.refresh()

    def refresh(self):
        self.binder.unpopulate()

        self.find('users').labels = self.find('users').values = [x.username for x in self.ipmapper.list()]

        self.binder.populate()

    @on('add-user', 'click')
    def on_add_user(self):
        user = self.find('users').value
        self.add(ShaperRule({'ip': self.ipmapper.get_ip(user), 'username': user}))

    @on('add-ip', 'click')
    def on_add_ip(self):
        ip = self.find('ip').value
        self.add(ShaperRule({'ip': ip}))

    def add(self, rule):
        self.binder.unpopulate()
        self.shaper.rules.append(rule)
        self.binder.populate()
        self.save()

    @on('save', 'click')
    def save(self):
        self.binder.update()

        try:
            self.shaper.save()
        except Exception, e:
            self.context.notify('error', str(e))
        self.refresh()
        self.context.notify('info', 'Saved')
