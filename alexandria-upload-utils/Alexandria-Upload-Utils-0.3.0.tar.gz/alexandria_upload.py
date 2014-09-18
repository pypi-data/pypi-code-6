import requests, os, json, hashlib


class AlexandriaException(Exception):
    pass


class AlexandriaUploader():
    
    def __init__(self, api_key, archive_url):
        self.api_key = api_key
        self.headers = {"Authorization": "Token " + api_key, 
                        "content-type": "application/json"}
        self.archive_url = archive_url


    def make_request(self, uri, verb, content):
        url = os.path.join(self.archive_url, uri)
        if verb == "GET":
            return requests.get(url, data=json.dumps(content), headers=self.headers)
        elif verb == "POST":
            return requests.post(url, data=json.dumps(content), headers=self.headers)
        elif verb == "PUT":
            return requests.put(url, data=json.dumps(content), headers=self.headers)
        elif verb == "PATCH":
            return requests.patch(url, data=json.dumps(content), headers=self.headers)
        elif verb == "DELETE":
            return requests.delete(url, data=json.dumps(content), headers=self.headers)


    """ 
    Takes a build name, a dictionary of metadata, and a list of tags, and creates a
    build on the archive.

    Returns the id of the created build, or throws an exception.
    """
    def create_build(self, name, metadata, tags=[]):
        build_bundle = {"name": name, "metadata": metadata, "tags": tags}
        r = self.make_request("api/build/", "POST", build_bundle)
        try:
            data = r.json()
        except:
            raise AlexandriaException("Archive did not return valid json: " +
                                        r.content)

        if "pk" in data:
            return data["pk"]
        elif "id" in data:
            return data["id"]

        raise AlexandriaException("Unexpected data returned while posting \
                                    build: " + r.content)


    """
    Takes a build id, an artifact category (in slug form), and the local filename of
    an artifact to be uploaded.  Calculates the size of the artifact, and an md5
    checksum, and notifies the archive of a new artifact.
    
    Returns the temporary PUTable upload URL returned by the archive.
    """
    def notify_new_artifact(self, build_id, artifact_category, filename): 
        try:
            file_size = os.path.getsize(filename)
            md5 = hashlib.md5(open(filename, 'rb').read()).hexdigest()
        except:
            raise AlexandriaException("Error calculating file metadata. Did you\
                                        provide a proper filename?")
        
        artifact_bundle = {"category": artifact_category, "build": build_id,
                            "size": file_size, "checksum": md5}

        r = self.make_request("api/artifact/", "PUT", artifact_bundle)

        try:
            data = r.json()
        except:
            raise AlexandriaException("Archive did not return valid json: " +
                                        r.content)

        if "url" in data:
            return data['url']
        else:
            raise AlexandriaException("Archive did not return upload url! \
                                        Response: " + r.content)

    
    """
    Takes a filename and an upload URL and uploads the file.
    """
    def do_upload(self, filename, upload_url):
        curl_cmd = "curl --request PUT --upload-file %s '%s'" % (filename, upload_url)
        out = os.system(curl_cmd)
        if out != 0:
            raise AlexandriaException("Uploading returned non-zero retval!")
    
    
    """
    Takes a build id and an artifact category (in slug form) and notifies the
    archive that the appropriate upload is complete.
    """
    def verify_new_artifact(self, build_id, artifact_category):
        patch_bundle = {"category": artifact_category, "build": build_id}
        r = self.make_request("api/artifact/", "PATCH", patch_bundle)

        try:
            data = r.json()
        except:
            raise AlexandriaException("Archive did not return valid json: " +
                                        r.content)

        if "error" in data:
            raise AlexandriaException("Archive returned error: " + r.content)

    
"""
The whole shebang
"""
def create_build_and_upload_artifacts(name, metadata, tags, artifacts, 
                                     api_key, archive_url):

    uploader = AlexandriaUploader(api_key, archive_url)
    build_id = uploader.create_build(name, metadata, tags)
    for category, filename in artifacts.iteritems():
        url = uploader.notify_new_artifact(build_id, category, filename)
        uploader.do_upload(filename, url)

    for category, filename in artifacts.iteritems():
        uploader.verify_new_artifact(build_id, category)



def create_and_upload_from_build_manifest(manifest_name, api_key, archive_url):
    manifest_data = json.load(open(manifest_name))
    create_build_and_upload_artifacts(  
                                        manifest_data["name"],
                                        manifest_data["metadata"],
                                        manifest_data.get("tags", []),
                                        manifest_data["artifacts"],
                                        api_key,
                                        archive_url
                                    )
