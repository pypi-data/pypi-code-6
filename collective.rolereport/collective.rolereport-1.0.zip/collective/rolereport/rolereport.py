from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.PluggableAuthService.interfaces.plugins import IRoleEnumerationPlugin, IUserEnumerationPlugin

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


class RoleReportHTML(BrowserView):
    
    def __call__(self):
        roles, users, role_users = user_report(self.context)

        result = '<html><head><title>Role report</title><head><body>\n<h1>Role report</h1>\n'
        for role in roles:
            role_title = role['title'] or role['id']
            result += '<h2>%s</h2>\n' % role_title
            
            for userid in role_users[role['id']]:
                user = users[userid]
                result += '<p>%s, %s, %s</p>\n' % (user['id'], user['fullname'], user['email'])
                
        return result

