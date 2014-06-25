#!/usr/bin/env python

"""
MySearch
Copyright (C) 2013   Tuxicoman

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Twisted imports
from twisted.internet import protocol, ssl
from twisted.web import client
from twisted.internet.endpoints import TCP4ClientEndpoint, SSL4ClientEndpoint
from twisted.web.error import SchemeNotSupported

#Import external libs
import os, sys
ext_libs_path = os.path.join(os.getcwd(), "ext_libs")
sys.path.append(ext_libs_path)
import ext_libs.service_identity as service_identity

from utils import outputlog
import backends

relay_port = 60062 #Should be the same between all Mysearch relays to communicate between them. Do not change.

def get_relay_address():
  #Relays knows the last relay IP (your personal IP for the 1st relay so) and the final destination machine but are NOT aware of the content if the request uses SSL encryption (most backends use SSL)
  
  #For now hardcode it to a known relay
  return "search.jesuislibre.net", relay_port

class Proxy(protocol.Protocol):
    peer = None

    def setPeer(self, peer):
        self.peer = peer

    def connectionLost(self, reason):
        if self.peer is not None:
            self.peer.transport.loseConnection()
            self.peer = None
        else :
            print("Unable to connect to peer: %s" % (reason,))

    def dataReceived(self, data):
        if self.peer is not None: 
          self.peer.transport.write(data)
          
          
        
        
## Client

class RelayClient(Proxy):
    def connectionMade(self):
        self.peer.setPeer(self)

        # Wire this and the peer transport together to enable
        # flow control (this stops connections from filling
        # this proxy memory when one side produces data at a
        # higher rate than the other can consume).
        self.transport.registerProducer(self.peer.transport, True)
        self.peer.transport.registerProducer(self.transport, True)

        # We're connected, everybody can read to their hearts content.
        self.peer.transport.resumeProducing()
        self.peer.dataReceived(self.peer.first_data)
        pass#print "Out connection made"
        
    def connectionLost(self, reason):
      pass#print "Out connection close"
        
    def dataReceived(self, data):
        #print "client", len(data)
        Proxy.dataReceived(self, data)
        

class RelayClientFactory(protocol.ClientFactory):

    protocol = RelayClient

    def setServer(self, server):
        self.server = server

    def buildProtocol(self, *args, **kw):
        prot = protocol.ClientFactory.buildProtocol(self, *args, **kw)
        prot.setPeer(self.server)
        return prot

    def clientConnectionFailed(self, connector, reason):
        self.server.transport.loseConnection()



## Server

class RelayServer(Proxy):

    clientProtocolFactory = RelayClientFactory
    reactor = None
    connected_to_end = False
    data_received_count = 0
    first_data = ""
    
    def connectionMade(self):
        pass#print "Relay connection made"
        
    def check_autorized_host(self, hostname):
      for backend in backends.available_backends :
        if hostname in backend().get_destination_domains():
          return True
      return False
      
    def dataReceived(self, data):
        if self.connected_to_end == False:
          #print data
          host = ""
          if data[0:2] == "##":
            host_start = 2
            host_end = host_start + data[host_start:].find("##")
            headers = data[host_start:host_end].split(',')
            final_host = headers[0]
            if self.check_autorized_host(final_host) == True:
              final_port = int(headers[1])
              desired_hops = int(headers[2]) -1
              data = data[host_end+2:]
              if desired_hops == 0 :
                host = final_host
                port = final_port
              else :
                header = "##%s,%i,%i##" % (final_host, final_port, desired_hops)
                data = header + data
                host, port = get_relay_address()
            else:
              outputlog("%s is not an autorized host" % final_host, "error")
              self.transport.loseConnection()
              return
              

          if host != "":
            outputlog("Relay to destination %s:%i with %i hop remaining" %( host, port, desired_hops), "info") 
            # Don't read anything from the connecting client until we have
            # somewhere to send it to.
            self.transport.pauseProducing()

            client = self.clientProtocolFactory()
            client.setServer(self)

            if self.reactor is None:
                from twisted.internet import reactor
                self.reactor = reactor
            self.reactor.connectTCP(host, port, client)
            self.first_data += data
            self.connected_to_end = True
          else:
            print "Error, invalid destination host defined"
            self.transport.loseConnection()
            
          data = ""

        Proxy.dataReceived(self, data)
        self.data_received_count +=1
        
    def connectionLost(self, reason):
      Proxy.connectionLost(self, reason)
      self.data_received_count = 0
      self.first_data = ""
      self.connection_made = False
      #print "Relay connection close"



class RelayServerFactory(protocol.Factory):

    protocol = RelayServer
    
    
    
#Local wrapper: Use to add routing information to original datastream.
#As datastream can (and should be encrypted by SSL), it's not possible to know to which endpoint the relay should forward the datastream just looking at its content. Thus we add a destination header in datastream : "##final_host,final_port,desired_hop##ssl_content....." 
    
class RequestWrapperServer(Proxy):
    clientProtocolFactory = RelayClientFactory
    first_data = ""
    data_received_count = 0
    
    def connectionMade(self):
        self.transport.pauseProducing()

        client = self.clientProtocolFactory()
        client.setServer(self)
        
        if self.factory.use_relay:
          self.factory.reactor.connectTCP(self.factory.hop_host, self.factory.hop_port, client)
        else:
          self.factory.reactor.connectTCP(self.factory.final_host, self.factory.final_port, client)
        #print "Wrapper connection made"

    def dataReceived(self, data):
        if self.data_received_count == 0 and self.factory.use_relay:
          self.first_data += data
          desired_hops = 1
          data = "##%s,%i,%i##" % (self.factory.final_host, self.factory.final_port, desired_hops)

        Proxy.dataReceived(self, data)
        self.data_received_count +=1
          
    def connectionLost(self, reason):
      #print "Wrapper connection close"
      Proxy.connectionLost(self, reason)
      self.transport.loseConnection()
    
class RequestWrapperFactory(protocol.Factory):

    protocol = RequestWrapperServer
      
    def __init__(self, reactor, final_host, final_port, use_relay=True ):
      self.reactor = reactor
      self.final_host, self.final_port = final_host, final_port
      self.use_relay = use_relay
      if self.use_relay == True:
        self.hop_host, self.hop_port = get_relay_address()
  
class SSLClientContextFactory(ssl.CertificateOptions):
        def getContext(self, hostname, port):
          
            ctx = ssl.CertificateOptions.getContext(self)
            
            
            #verify hostname in trusted certificates
            def verifyHostname(conn, cert, errno, depth, preverify_ok):
              if preverify_ok and depth == 0 :
                outputlog("Checking SSL cert for '%s' : %s" % (hostname, cert.get_subject().commonName), "info") 
                valid_entries = service_identity.verify_service_identity( service_identity.pyopenssl.extract_ids(cert),[service_identity.DNS_ID(u"%s" % hostname)])
                if len(valid_entries) == 0:
                  return False
              return preverify_ok
              
            from OpenSSL import SSL
            ctx.set_verify(SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT, verifyHostname)
            
            
            return ctx

class OnionAgent(client.Agent):
  wrapper_host = "localhost"
  
  def __init__(self, reactor, contextFactory=client.WebClientContextFactory(), connectTimeout=None, bindAddress=None, pool=None, use_relay=True):
    self.use_relay = use_relay
    
    #Get trusted CA autorities
    import os, glob
    from OpenSSL.crypto import load_certificate, FILETYPE_PEM
    certificateAuthorityMap = {}
    for certFileName in glob.glob("/etc/ssl/certs/*.pem"):
        # There might be some dead symlinks in there, so let's make sure it's real.
        if os.path.exists(certFileName):
            data = open(certFileName).read()
            x509 = load_certificate(FILETYPE_PEM, data)
            digest = x509.digest('sha1')
            # Now, de-duplicate in case the same cert has multiple names.
            certificateAuthorityMap[digest] = x509
    
    #Force SSL verification
    contextFactory = SSLClientContextFactory(verify=True, caCerts=certificateAuthorityMap.values())
    
    
    client.Agent.__init__(self, reactor, contextFactory, connectTimeout, bindAddress, pool)
    
  def request(self, method, uri, headers=None, bodyProducer=None):
      
        parsedURI = client._URI.fromBytes(uri)
        
        #Change endpoint to use onion route
        p = self._reactor.listenTCP(0, RequestWrapperFactory(self._reactor, parsedURI.host, parsedURI.port, use_relay=self.use_relay), interface=self.wrapper_host)
        listening_port = p.getHost().port
        def stop_tunnel_wrapper(request, connection):
          connection.stopListening()
          return request
          
        try:
            endpoint = self._getEndpoint(parsedURI.scheme, self.wrapper_host, listening_port, parsedURI.host)
        except SchemeNotSupported:
            stop_tunnel_wrapper(None, p)
            return defer.fail(Failure())
        key = (parsedURI.scheme, parsedURI.host, parsedURI.port)
        d = self._requestWithEndpoint(key, endpoint, method, parsedURI, headers, bodyProducer, parsedURI.originForm)
        
        #Close onion route
        d.addCallback(stop_tunnel_wrapper, p)
        
        return d
            
  def _getEndpoint(self, scheme, host, port, destination_host):
    #same as _getEndpoint but with ContextFactory pointing to the destination_host rather than the proxy_host. Thus SSL verification will done againt destination_host
    kwargs = {}
    if self._connectTimeout is not None:
        kwargs['timeout'] = self._connectTimeout
    kwargs['bindAddress'] = self._bindAddress
    if scheme == 'http':
        return TCP4ClientEndpoint(self._reactor, host, port, **kwargs)
    elif scheme == 'https':
        return SSL4ClientEndpoint(self._reactor, host, port,
                                  self._wrapContextFactory(destination_host, port),
                                  **kwargs)
    else:
        raise SchemeNotSupported("Unsupported scheme: %r" % (scheme,))
    
