__author__ = 'AssadMahmood'
import requests
import json

from asposecloud import AsposeApp
from asposecloud import Product
from asposecloud.common import Utils

# ========================================================================
# DOCUMENT CLASS
# ========================================================================


class Document:

    def __init__(self, filename):
        self.filename = filename

        if not filename:
            raise ValueError("filename not specified")

        self.base_uri = Product.product_uri + 'words/' + self.filename

    def append_document(self, doc_list, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param doc_list:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/appendDocument'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        json_data = json.dumps(doc_list)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.post(signed_uri, json_data, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            return Utils.download_file(self.filename, self.filename, remote_folder, storage_type, storage_name)
        else:
            return validate_output

    def get_properties(self, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/documentProperties'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['DocumentProperties']['List']

    def get_document_info(self, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = Utils.append_storage(self.base_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['Document']

    def get_property(self, property_name, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param property_name:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/documentProperties/' + property_name
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['DocumentProperty']

    def set_property(self, property_name, property_value, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param property_name:
        :param property_value:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/documentProperties/' + property_name
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        json_data = json.dumps({'Value': property_value})

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.put(signed_uri, json_data, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['DocumentProperty']

    def delete_property(self, property_name, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param property_name:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/documentProperties/' + property_name
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.delete(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return True if response['Code'] == 200 else False

# ========================================================================
# EXTRACTOR CLASS
# ========================================================================


class Extractor:

    def __init__(self, filename):
        self.filename = filename

        if not filename:
            raise ValueError("filename not specified")

        self.base_uri = Product.product_uri + 'words/' + self.filename

    def get_text(self, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/textItems'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        output_text = ''
        for item in response['TextItems']['List']:
            output_text += item['Text']
        return output_text

    def get_drawing_object_list(self, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/drawingObjects'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['DrawingObjects']['List']

    def get_ole_data(self, ole_index, ole_format, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param ole_index:
        :param ole_format:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/drawingObjects/' + str(ole_index) + '/oleData'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            return Utils.save_file(response,
                                   AsposeApp.output_path + Utils.get_filename(self.filename)
                                   + '_' + str(ole_index) + '.' + ole_format)
        else:
            return validate_output

    def get_image_data(self, image_index, image_format, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param image_index:
        :param image_format:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/drawingObjects/' + str(image_index) + '/imagedata'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            return Utils.save_file(response,
                                   AsposeApp.output_path + Utils.get_filename(self.filename)
                                   + '_' + str(image_index) + '.' + image_format)
        else:
            return validate_output

    def convert_drawing_object(self, object_index, render_format,
                               remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param object_index:
        :param render_format:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/drawingObjects/' + str(object_index) + '?format=' + render_format
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            return Utils.save_file(response,
                                   AsposeApp.output_path + Utils.get_filename(self.filename)
                                   + '_' + str(object_index) + '.' + render_format)
        else:
            return validate_output

    @staticmethod
    def get_drawing_object(object_uri, output_path, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param object_uri:
        :param output_path:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        object_index = object_uri[-1:]

        str_uri = Product.product_uri + 'words/' + object_uri
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        object_info = response['DrawingObject']

        if not object_info['ImageDataLink'] is None:
            str_uri = Product.product_uri + 'words/' + object_uri + '/imageData'
            output_path = output_path + 'DrawingObject_' + str(object_index) + '.jpg'
        elif not object_info['OleDataLink'] is None:
            str_uri = Product.product_uri + 'words/' + object_uri + '/oleData'
            output_path = output_path + 'DrawingObject_' + str(object_index) + '.xlsx'
        else:
            str_uri = Product.product_uri + 'words/' + object_uri + '?format=jpg'
            output_path = output_path + 'DrawingObject_' + str(object_index) + '.jpg'

        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            return Utils.save_file(response, output_path)
        else:
            return validate_output

# ========================================================================
# MAIL MERGE CLASS
# ========================================================================


class MailMerge:

    def __init__(self, filename):
        self.filename = filename

        if not filename:
            raise ValueError("filename not specified")

        self.base_uri = Product.product_uri + 'words/' + self.filename

    def execute(self, str_xml, with_regions=False, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param str_xml:
        :param with_regions:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        if not str_xml:
            raise ValueError("str_xml not specified")

        str_uri = self.base_uri + '/executeMailMerge'
        str_uri = str_uri + '?withRegions=true' if with_regions else str_uri
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.post(signed_uri, str_xml, headers={
                'content-type': 'application/xml', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            return Utils.download_file(self.filename, self.filename, remote_folder, storage_type, storage_name)
        else:
            return validate_output

    def execute_template(self, str_xml, with_regions=False, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param str_xml:
        :param with_regions:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        if not str_xml:
            raise ValueError("str_xml not specified")

        str_uri = self.base_uri + '/executeTemplate'
        str_uri = str_uri + '?withRegions=true' if with_regions else str_uri
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.post(signed_uri, str_xml, headers={
                'content-type': 'application/xml', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            return Utils.download_file(self.filename, self.filename, remote_folder, storage_type, storage_name)
        else:
            return validate_output

# ========================================================================
# BUILDER CLASS
# ========================================================================


class Builder:

    def __init__(self, filename):
        self.filename = filename

        if not filename:
            raise ValueError("filename not specified")

        self.base_uri = Product.product_uri + 'words/' + self.filename

    def insert_watermark_image(self, image_file, angle, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param image_file:
        :param angle:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/insertWatermarkText'
        qry = {'imageFile': image_file, 'rotationAngle': angle}
        str_uri = Utils.build_uri(str_uri, qry)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.post(signed_uri, None, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            return Utils.download_file(self.filename, self.filename, remote_folder, storage_type, storage_name)
        else:
            return validate_output

    def insert_watermark_text(self, text, angle, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param text:
        :param angle:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/insertWatermarkText'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        json_data = json.dumps({'Text': text, 'RotationAngle': angle})

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.post(signed_uri, json_data, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            return Utils.download_file(self.filename, self.filename, remote_folder, storage_type, storage_name)
        else:
            return validate_output

    def replace_text(self, old_text, new_text, match_case=False, match_whole_word=False,
                     remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param old_text:
        :param new_text:
        :param match_case:
        :param match_whole_word:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/replaceText'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        json_data = json.dumps({'OldValue': old_text, 'NewValue': new_text,
                                'IsMatchCase': match_case, 'IsMatchWholeWord': match_whole_word})

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.post(signed_uri, json_data, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            return True
        else:
            return validate_output

# ========================================================================
# CONVERTER CLASS
# ========================================================================


class Converter:

    def __init__(self, filename):
        self.filename = filename

        if not filename:
            raise ValueError("filename not specified")

        self.base_uri = Product.product_uri + 'words/' + self.filename

    def convert(self, save_format, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param save_format:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        if not save_format:
            raise ValueError("save_format not specified")

        str_uri = self.base_uri + '?format=' + save_format
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            save_format = 'zip' if save_format == 'html' else save_format
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '.' + save_format
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    @staticmethod
    def convert_local_file(input_file, save_format):
        """

        :param input_file:
        :param save_format:
        :return:
        """
        if not input_file:
            raise ValueError("input_file not specified")

        if not save_format:
            raise ValueError("save_format not specified")

        str_uri = Product.product_uri + 'words/convert?format=' + save_format

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = Utils.upload_file_binary(input_file, signed_uri)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            save_format = 'zip' if save_format == 'html' else save_format
            output_path = AsposeApp.output_path + Utils.get_filename(input_file) + '.' + save_format
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output
