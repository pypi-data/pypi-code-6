class Request(object):

    def __init__(self, application, requester, cookie, comment, *args,
                 **kwargs):
        self.application = application
        self.requester = requester
        self.cookie = cookie
        self.comment = comment

    def serialize_to_dict(self):
        return {
            'Application': self.application,
            'Requester': self.requester,
            'AuthCookie': self.cookie,
            'Comment': self.comment
        }


class GenerateCertificateRequest(Request):

    def __init__(self, application, requester, cookie, comment, ou, owner,
                 identifier, duration, mask, privilege=0, profile=0,
                 number=1, *args, **kwargs):

        super(GenerateCertificateRequest, self).__init__(application,
                                                         requester, cookie,
                                                         comment, *args,
                                                         **kwargs)
        self.ou = ou
        self.owner = owner
        self.identifier = identifier
        self._duration = duration
        self.mask = mask
        self.privilege = privilege
        self.profile = profile
        self.number = number

    @property
    def duration(self):
        if self._duration < 1 or self._duration > 1095:
            raise Exception("The duration must be less than 1095 and greater"
                            " than 0.")

        return self._duration

    def serialize_to_dict(self):
        parent = super(GenerateCertificateRequest, self).serialize_to_dict()
        parent.update({
            'OrganizationUnit': self.ou,
            'Owner': self.owner,
            'Identifier': self.identifier,
            'Privilege': self.privilege,
            'Profile': self.profile,
            'Duration': self.duration,
            'AuthenticationMask': self.mask,
            'Number': self.number
        })
        return parent


class RevokeCertificateRequest(Request):

    def __init__(self, application, requester, cookie, comment, ou, owner,
                 index, *args, **kwargs):
        super(RevokeCertificateRequest, self).__init__(application, requester,
                                                       cookie, comment)
        self.ou = ou
        self.owner = owner
        self.index = index

    def serialize_to_dict(self):
        parent = super(RevokeCertificateRequest, self).serialize_to_dict()
        parent.update({
            'OrganizationUnit': self.ou,
            'Owner': self.owner,
            'Index': self.index
        })
        return parent


class GetCertificateRequest(Request):

    def __init__(self, application, requester, cookie, owner_filter,
                 ou_filter, index_filter, requester_filter):
        super(GetCertificateRequest, self).__init__(application, requester,
                                                    cookie, '')
        self.owner_filter = owner_filter
        self.ou_filter = ou_filter
        self.index_filter = index_filter
        self.requester_filter = requester_filter

    def serialize_to_dict(self):
        parent = super(GetCertificateRequest, self).serialize_to_dict()
        del parent['Comment']
        parent.update({
            'OwnerFilter': self.owner_filter,
            'OrganizationUnitFilter': self.ou_filter,
            'IndexFilter': self.index_filter,
            'RequesterFilter': self.requester_filter
        })
        return parent
