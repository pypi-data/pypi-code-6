from suds import WebFault
from suds.client import Client

from django_idshost.certificate.request import (GenerateCertificateRequest,
                                                RevokeCertificateRequest,
                                                GetCertificateRequest)


class ClientPki(object):

    wsdl = 'http://api.idshost.priv/pki.wsdl'

    def __init__(self, *args, **kwargs):
        super(ClientPki, self).__init__(*args, **kwargs)
        self.client = Client(ClientPki.wsdl)

    def _send_request(self, service, request, *args, **kwargs):
        try:
            return service(request.serialize_to_dict())
        except WebFault, e:
            raise e

    def generate_certificate(self, request, *args, **kwargs):
        if not isinstance(request, GenerateCertificateRequest):
            raise Exception("To send a generate request your request argument"
                            " have to be an instance of"
                            " GenerateCertificateRequest.")

        service = self.client.service.CertRequest
        return self._send_request(service, request, *args, **kwargs)

    def revoke_certificate(self, request, *args, **kwargs):
        if not isinstance(request, RevokeCertificateRequest):
            raise Exception("To send a revoke request your request argument"
                            " have to be an instance of"
                            " RevokeCertificateRequest.")
        service = self.client.service.CertRevocate
        return self._send_request(service, request, *args, **kwargs)

    def get_certificate(self, request, *args, **kwargs):
        if not isinstance(request, GetCertificateRequest):
            raise Exception("To send a get request your request argument"
                            " have to be an instance of"
                            " RevokeCertificateRequest.")
        service = self.client.service.GetCertificateRetrievalStatus
        return self._send_request(service, request, *args, **kwargs)
