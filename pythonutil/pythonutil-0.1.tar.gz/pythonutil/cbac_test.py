import json
import requests
from OpenStackUtil import Keystone
from FileUtil import File
from JSONUtil import LoadJSON
	


USER="demo"
PASS="nova"
TENANT_NAME="demo"
#KEYSTONE_URL= "http://192.168.0.106:5000/v2.0"
#STORAGE_URL = "http://192.168.0.106:8080/v1/AUTH_4d6b4ade25754012a5cd22c255cffac8"


def _set_metadata(meta_name=None, container=None, object=None,meta_value=None, TOKEN=None):
	#policy should not be None

	Keystone.set_config(keystone_ip="192.168.0.106", username="demo",password="nova", tenant="demo")
	storage_url = Keystone.storage_url(tenant=TENANT_NAME)
	url = "{}/{}/{}".format(storage_url, container, object)
	print url
	res = requests.request("POST",url, headers={ \
				"X-Auth-Token":TOKEN,\
				"X-Object-Meta-"+meta_name[0]:meta_value[0],\
				"X-Object-Meta-"+meta_name[1]:meta_value[1],\
				"X-Object-Meta-"+meta_name[2]:meta_value[2],\
				"X-Object-Meta-"+meta_name[3]:meta_value[3]\
				}\
			)
	return res.text


'''
	set policy, set user_labels, object_labels metadata
'''
def set_metadata(policy_file=None,container=None, object=None):


	#name = name or "Jsonpolicy"
	Keystone.set_config(keystone_ip="192.168.0.106", username="demo",password="nova", tenant="demo")
	token = Keystone.get_token()
	print token
	container_name = container or "container1"
	object_name = object or "employee.json"
	return_status = ""
	if policy_file:
		
		try:
			# we strip new file from policy file, because Swift metadata does not support newline.
			filecontent = File(policy_file).read().replace("\n", " ")

			filecontent = ' '.join(filecontent.split())
			file_in_json = LoadJSON(str=filecontent).get_json()
			# replace consecutive space for space restriction of 256 chars.


			
			policy =  json.dumps(file_in_json['policy'],encoding='utf-8')
			user_labels = json.dumps(file_in_json['user_labels'], encoding='utf-8')
			object_labels = json.dumps(file_in_json['object_labels'], encoding='utf-8')
			labelling = json.dumps(file_in_json['labeling'], encoding='utf-8')
			# set JSONPolicy metadata
			return_status += _set_metadata(meta_name=["JSONPolicy", "UserLabels","ObjectLabels","JSONLabelling"], \
							container=container_name, object=object_name, \
							meta_value=[policy,user_labels,object_labels, labelling], TOKEN=token)
			return return_status
		except Exception as e:
			print "something gone HORRIBLE!! {}".format(e) 




if __name__ == "__main__":
	print set_metadata(policy_file="allpolicy.json", container="container1", object="employee.json")
	#test_labac("allpolicy.json")
