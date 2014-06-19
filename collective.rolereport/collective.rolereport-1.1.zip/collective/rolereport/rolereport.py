from App import config
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.PluggableAuthService.interfaces.plugins import IRoleEnumerationPlugin, IUserEnumerationPlugin
from datetime import date
import os


def report_dir():
    # XXX This needs to be configurable.
    clientdir = config.getConfiguration().clienthome
    vardir = os.path.realpath(os.path.join(clientdir, os.path.pardir))
    fbdir = os.path.join(vardir, 'reports')
    if not os.path.exists(fbdir):
        os.mkdir(fbdir)
    return fbdir

def user_report(context):
    acl = getToolByName(context, 'acl_users')
    plugins = acl._getOb('plugins')
    role_plugins = plugins.listPlugins(IRoleEnumerationPlugin)

    roles = []
    role_users = {}
    users = {}
    for id_, plugin in role_plugins:
        for role in plugin.enumerateRoles():
            roleid = role['id']
            if roleid in ('Authenticated', 'Member'):
                # Skip the roles all users have.
                continue
            roles.append(role)
            role_users[roleid] = set()
    
    user_plugins = plugins.listPlugins(IUserEnumerationPlugin)
    for id_, plugin in user_plugins:
        for user in plugin.enumerateUsers():
            user = acl.getUser(user['id'])
            if user is None:
                # Why does this happen? Weird.
                continue
            user_info = {'id': user.getId(), 
                         'fullname': user.getProperty('fullname'), 
                         'email': user.getProperty('email')}
            for user_role in user.getRoles():
                if user_role in ('Authenticated', 'Member'):
                    # Skip the roles all users have.
                    continue
                role_users[user_role].add(user_info['id'])
                if user_info['id'] not in users:
                    users[user_info['id']] = user_info
                
    return roles, users, role_users

def create_report(site, outfile):
    roles, users, role_users = user_report(site)

    result = '<html><head><title>Role report</title><head><body>\n<h1>Role report</h1>\n'
    for role in roles:
        role_title = role['title'] or role['id']
        result += '<h2>%s</h2>\n' % role_title
        
        for userid in role_users[role['id']]:
            user = users[userid]
            result += '<p>%s, %s, %s</p>\n' % (user['id'], user['fullname'], user['email'])
    
    # You were lucky to have context managers! There were a hundred and fifty
    # of us living in t' try/except clause in t' middle o' road!
    open(outfile, 'wb').write(result)


class RoleReportHTML(BrowserView):
    
    def run(self):
        output_folder = report_dir()
        
        filename = date.today().strftime('role-report-%Y-%m-%d.html')
        outfile = os.path.join(output_folder, filename)
        self.output_file = outfile

        count = 0
        while os.path.exists(outfile):
            if len(open(outfile, 'rb').read()) == 0:
                # Report in progress (or failed)
                return 'already'
            count += 1
            filename = date.today().strftime('role-report-%Y-%m-%d.%%s.html') % count            
            outfile = os.path.join(output_folder, filename)
            self.output_file = outfile
        
        # Create the file
        out = open(outfile, 'wb')
        out.close()

        create_report(self.context, outfile)
        return ''
