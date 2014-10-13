import requests

try:
	import simplejson as json
except ImportError:
	import json

'''
    Retrieve Token for working with OpenStack Services.
'''
class Keystone:
    host_ip="192.168.0.101"   
    username="demo"
    password="nova"
    tenant_name="demo"
    
    @staticmethod
    def set_config(keystone_ip=None, username=None, password=None, tenant=None):
        if keystone_ip != None:
            Keystone.host_ip = keystone_ip
        if username:
            Keystone.username = username
        if password:
            Keystone.password = password
	if tenant:
	    Keystone.tenant = tenant
    

    '''
	return a scoped token for the given tenant.
    '''
    @staticmethod
    def get_token():
        '''change USERNAME, PASSWORD from the following credential'''
        pass_cred = '{ "auth":{ \
			    "tenantName":"%s",\
                            "passwordCredentials": { \
                                "username": "%s",\
                                "password": "%s" \
                            }\
                         } \
                     }'%(Keystone.tenant_name,Keystone.username, Keystone.password)
        headers={"Content-Type":"application/json"}
        endpoint="http://{}:5000/v2.0".format(Keystone.host_ip)
        url = "{}/{}".format(endpoint,"tokens")
        response =  URL.submit(URL=url, HEADERS=headers, METHOD="POST", DATA=pass_cred)
        return response()['access']['token']['id']
        
        
    '''	
	given a tenant name, it returns id of the tenant.
    '''
    @staticmethod
    def get_tenant_id(name=None):
        endpoint="http://{}:5000/v2.0".format(Keystone.host_ip)
        api_endpoint = "tenants"
        tenant_name= name or "demo"
        token= Keystone.get_token()   
        url= "{}/{}".format(endpoint, api_endpoint)
        headers = {'X-Auth-Token':token, 'name':tenant_name}    
        response =  URL.submit(URL=url, METHOD="GET", HEADERS=headers)
        return [ tenant['id'] for tenant in response()['tenants'] if tenant['name']==tenant_name ][0]
    
    '''
	return the endpoint for swift. It assumes swift API version 1.0
    '''
    @staticmethod
    def storage_url(tenant=None):
        swift_endpoint="http://{}:8080/v1/AUTH_".format(Keystone.host_ip)
	tenant_name = tenant or "demo"
        tenant_id = Keystone.get_tenant_id(tenant_name)
        return swift_endpoint + tenant_id

def test_get_token():
    print Keystone.get_token()
def test_get_tenant_id():
    print Keystone.get_tenant_id(name="demo")
def test_storage_url():
    print Keystone.storage_url(tenant="demo")

'''submit a request to a remote url and get response from it'''
class URL:
    @staticmethod
    def submit( URL=None, HEADERS=None, METHOD=None, DATA=None):
        if URL and HEADERS and METHOD and DATA:
            response = requests.request(METHOD, URL, headers=HEADERS, data=DATA) 
        elif URL and HEADERS and METHOD:
            response = requests.request(METHOD, URL, headers=HEADERS)  
        if response:          
            return response.json            
        else:
            return None
       
if __name__ == '__main__':
    Keystone.set_config(keystone_ip="192.168.0.106", username="demo",password="nova")
    test_get_token()
    test_get_tenant_id()
    test_storage_url()
