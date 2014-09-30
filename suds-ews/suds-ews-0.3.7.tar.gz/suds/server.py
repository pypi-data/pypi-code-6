
class Server(object):
    def __init__(self, client, binding=None):
        self.wsdl = client.wsdl
        self.factory = client.factory

        def get_binding(obj):
            return self.wsdl.bindings_def['%s/literal' % obj.soap.style] # assume literal use

        if binding:
            for (name, ns), binding_obj in self.wsdl.bindings.iteritems():
                if name == binding:
                    self.binding  = get_binding(binding_obj)
                    break
            else:
                raise ValueError('Binding `%s` not found' % binding)
        else:
            if len(self.wsdl.bindings) == 1:
                self.binding = get_binding(self.wsdl.bindings.values()[0])
            else:
                raise ValueError('Binding name required')

    def handle_request(self, content):
        replyroot = self.binding.parser.parse(string=content)

        soapenv = replyroot.getChild('Envelope')
        soapenv.promotePrefixes()

        soapbody = soapenv.getChild('Body')
        soapbody = self.binding.multiref.process(soapbody)

        nodes = soapbody.getChildren()

        unmarshaller = self.binding.unmarshaller()
        result = [unmarshaller.process(node, None) for node in nodes]
        return len(result) == 1 and result[0] or result

    def handle_response(self, *content):
        message = self.binding.get_message(*content)
        return str(message)
