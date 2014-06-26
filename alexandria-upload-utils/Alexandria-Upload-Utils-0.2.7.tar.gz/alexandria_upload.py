import requests
import boto
import json
import uuid
import os


class AlexandriaUploadException(Exception):
	pass


def get_api_auth(user_name, api_key):
	return "ApiKey %s:%s" % (user_name, api_key)


def create_build(build_name, metadata, extradata, archive_url, upload_user, api_key):
	metadata_list = []
	for k, v in metadata.iteritems():
		metadata_list.append({'category': k, 'value': v})

	extradata_list = []
	for k, v in extradata.iteritems():
		extradata_list.append({'ed_type': k, 'value': v})
		
	build_post_data = {	'name': build_name, 
				'metadata': metadata_list,
				'extra_data': extradata_list,
				'artifacts':[]}

	build_post_url = "%s/api/v0/build/?username=%s&api_key=%s" % (archive_url, upload_user, api_key)
	auth_header = get_api_auth(upload_user, api_key)

	r = requests.post(	build_post_url,
				data=json.dumps(build_post_data), 
				headers={"Authorization": auth_header, 'content-type': 'application/json'})

	try:
		build_id = r.json()["id"]
	except:
		raise AlexandriaUploadException("Build creation was unsuccessful: %s" %(r.text))

	return build_id


def upload_to_s3_and_post(filename, build_id, artifact_type, archive_url, upload_user, api_key):
	key_name = str(uuid.uuid4())
	s3 = boto.connect_s3(os.getenv("AWS_ACCESS_KEY"), os.getenv("AWS_ACCESS_SECRET"))
	bucket = s3.lookup(os.getenv("S3_BUCKET"))
	key = bucket.new_key(key_name)
	print "Posting to S3..."
	key.set_contents_from_file(open(filename, 'rb'))

	print "Notifying archive of upload..."
	post_data = {'type': artifact_type, 'build': build_id, 'secure_uuid': key_name}
	post_url = archive_url + "/api/v0/artifact/"
	auth_header = get_api_auth(upload_user, api_key)
	r = requests.post(	post_url,
				data=json.dumps(post_data),
				headers={'Authorization': auth_header, 'content-type': 'application/json'})

	if r.status_code > 300:
		raise AlexandriaUploadException("Error uploading %s: %s" % (artifact_type, r.text))


def upload_file(filename, build_id, artifact_type, archive_url, upload_user, api_key):
	post_data = {'type': artifact_type, 'build_id': build_id}
	post_url = archive_url + "/upload/"
	
	try:
		payload_data = open(filename, 'rb')
	except:
		raise AlexandriaUploadException("Error opening file: %s" % filename)

	auth_header = get_api_auth(upload_user, api_key)
	print "Uploading " + filename
	r = requests.post(	post_url,
				stream=True,
				data=post_data, 
				headers={'Authorization': auth_header},
				files={'payload': open(filename, 'rb')})

	for line in r.iter_lines():
		if line:
			print line
	
	if r.status_code > 300:
		raise AlexandriaUploadException("Error uploading %s: %s" % (artifact_type, r.text))


def create_build_and_upload(name, metadata, extradata, artifacts, archive_url, upload_user, api_key, post_to_s3=False):
	build_id = create_build(name, metadata, extradata, archive_url, upload_user, api_key)
	
	for k, v in artifacts.iteritems():
		if post_to_s3:	
			upload_to_s3_and_post(v, build_id, k, archive_url, upload_user, api_key)
		else:
			upload_file(v, build_id, k, archive_url, upload_user, api_key)


def upload_with_build_file(filename, archive_url, upload_user, api_key):
	build_data = json.load(open(filename))
	create_build_and_upload(build_data["name"], build_data["metadata"], build_data["extradata"], build_data["artifacts"], archive_url, upload_user, api_key)

