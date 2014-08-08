__author__ = 'AssadMahmood'
import requests
import json

from asposecloud import AsposeApp
from asposecloud import Product
from asposecloud.common import Utils


class Document:
    """
    Wrapper class for Aspose.PDF API Document Resource.
    The Aspose.PDF API let's you manipulate PDF files.
    """

    def __init__(self, filename):
        self.filename = filename

        if not filename:
            raise ValueError("filename not specified")

        self.base_uri = Product.product_uri + 'pdf/' + self.filename

    def get_page_count(self, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Get count of pages in pdf file

        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/pages'
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

        return len(response['Pages']['List']) if response['Pages']['List'] else 0

    def append_documents(self, append_file, start_page=None, end_page=None,
                         remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Append a pdf file to base pdf

        :param append_file:
        :param start_page:
        :param end_page:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/appendDocument'
        qry = {'appendFile': append_file}
        if start_page:
            qry['startPage'] = start_page
        if end_page:
            qry['endPage'] = end_page
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
        if validate_output:
            return validate_output
        else:
            return True

    @staticmethod
    def merge_documents(merged_filename, source_files, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Merge multiple pdf files

        :param merged_filename:
        :param source_files:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """

        json_data = json.dumps({'List': source_files})

        str_uri = Product.product_uri + 'pdf/' + merged_filename + '/merge'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

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

        return True if response['Status'] == 'OK' else False


class TextEditor:
    """
    Wrapper class for Aspose.PDF API for Text Editing features.
    The Aspose.PDF API let's you manipulate PDF files.
    """

    def __init__(self, filename):
        self.filename = filename

        if not filename:
            raise ValueError("filename not specified")

        self.base_uri = Product.product_uri + 'pdf/' + self.filename

    def get_fragment_count(self, page_number, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Count fragments in a pdf file on given page number

        :param page_number:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/pages/' + str(page_number) + '/fragments'
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

        return len(response['TextItems']['List']) if response['TextItems']['List'] else 0

    def get_text(self, page_number, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Get text from give page number

        :param page_number:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/pages/' + str(page_number) + '/textitems'
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

    def get_text_items(self, page_number, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Get text items from given page number

        :param page_number:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/pages/' + str(page_number) + '/textitems'
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

        return response['TextItems']['List'] if response['TextItems']['List'] else False

    def replace_text(self, page_number, old_text, new_text, is_reg=False,
                     remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Replace text on any given page

        :param page_number:
        :param old_text:
        :param new_text:
        :param is_reg:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/pages/' + str(page_number) + '/replaceText'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        json_data = json.dumps({'OldValue': old_text, 'NewValue': new_text, 'Regex': is_reg})

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


class Extractor:
    """
    Wrapper class for Aspose.PDF API Extraction features.
    The Aspose.PDF API let's you manipulate PDF files.
    """
    def __init__(self, filename):
        self.filename = filename

        if not filename:
            raise ValueError("filename not specified")

        self.base_uri = Product.product_uri + 'pdf/' + self.filename

    def get_image(self, page_number, image_index, save_format, width=None, height=None,
                  remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Get image from given page

        :param page_number:
        :param image_index:
        :param save_format:
        :param width:
        :param height:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        if not save_format:
            raise ValueError("save_format not specified")

        if not page_number:
            raise ValueError("page_number not specified")

        str_uri = self.base_uri + '/pages/' + str(page_number) + '/images/' + str(image_index)
        qry = {'format': save_format}
        if width and height:
            qry['width'] = width
            qry['height'] = height
        str_uri = Utils.build_uri(str_uri, qry)
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
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_' + str(page_number) \
                + '_' + str(image_index) + '.' + save_format
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    def get_image_count(self, page_number, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Count images on a given page

        :param page_number:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        if not page_number:
            raise ValueError("page_number not specified")

        str_uri = self.base_uri + '/pages/' + str(page_number) + '/images'
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
        return len(response['Images']['List']) if response['Images']['List'] else 0


class Converter:
    """
    Wrapper class for Aspose.PDF API.
    The Aspose.PDF API let's you manipulate PDF files.
    """

    def __init__(self, filename):
        self.filename = filename

        if not filename:
            raise ValueError("filename not specified")

        self.base_uri = Product.product_uri + 'pdf/' + self.filename

    def convert_to_image(self, page_number, save_format, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Convert a page to image

        :param page_number:
        :param save_format:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        if not save_format:
            raise ValueError("save_format not specified")

        if not page_number:
            raise ValueError("page_number not specified")

        str_uri = self.base_uri + '/pages/' + str(page_number)
        qry = {'format': save_format}
        str_uri = Utils.build_uri(str_uri, qry)
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
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_' + str(page_number) + '.' + \
                save_format
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    def convert(self, save_format, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Convert a pdf file to any supported format

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

        save_format = 'zip' if save_format == 'html' else save_format
        output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '.' + save_format
        Utils.save_file(response, output_path)
        return output_path

    @staticmethod
    def convert_local_file(input_file, save_format):
        """
        Convert a local pdf file to any supported format

        :param input_file:
        :param save_format:
        :return:
        """
        if not input_file:
            raise ValueError("input_file not specified")

        if not save_format:
            raise ValueError("save_format not specified")

        str_uri = Product.product_uri + 'pdf/convert?format=' + save_format

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = Utils.upload_file_binary(input_file, signed_uri)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        save_format = 'zip' if save_format == 'html' else save_format
        output_path = AsposeApp.output_path + Utils.get_filename(input_file) + '.' + save_format
        Utils.save_file(response, output_path)
        return output_path
