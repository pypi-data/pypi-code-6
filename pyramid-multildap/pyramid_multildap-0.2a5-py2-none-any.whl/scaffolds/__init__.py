from pyramid.scaffolds import PyramidTemplate

class LdapAuthTemplate(PyramidTemplate):
    _template_dir = 'ldapauth'
    summary = 'Pyramid ldap auth example/starter project'

