# coding: utf-8
"""
Unoficial client to translate.yandex.com

API Documentation:
http://api.yandex.com/translate/doc/dg/concepts/About.xml
"""
import re
import json
import collections

from ytrans.exceptions import APIException, throw
from ytrans.settings import KEY_ENVIRON_VARIABLE, read_key
from ytrans import utils


__all__ = ["YTranslator", "APIException", "PLAIN", "HTML",
           "read_key", "KEY_ENVIRON_VARIABLE"]


PLAIN = 'plain'
HTML = 'html'

OK = 200

reSpaceCompile = re.compile('\s', re.UNICODE)


class YTranslator(object):
    def __init__(self, api_key):
        self.__API_KEY = api_key
        self.__invalid_langs_map = {}
        self.__valid_langs_map = collections.defaultdict(list)

    def is_valid_lang(self, lang_str):
        if not isinstance(lang_str, str):
            return False

        lang_str = lang_str.lower()

        if lang_str in self.__invalid_langs_map:
            return False

        if lang_str in self.__valid_langs_map:  # Cache hit
            return True

        # Refresh, since after all this could be a compulsory miss
        self.__valid_langs_map = self.__get_supported_langs_map()
        if lang_str not in self.__valid_langs_map: # Black list it
            self.__invalid_langs_map[lang_str] = True
            return False

        return True

    def get_supported_translations(self, lang_str):
        if not self.is_valid_lang(lang_str):
            return []

        lower_lang_str = lang_str
         # No tampering with internal data
        return self.__valid_langs_map[lower_lang_str][:]

    def get_supported_primaries(self):
        if not self.__valid_langs_map:
            self.__valid_langs_map = self.__get_supported_langs_map()

        return list(self.__valid_langs_map.keys())

    def __get_supported_langs_map(self):
        lang_list = self.get_translation_directions()
        lang_map = collections.defaultdict(list)

        for from_to_str in lang_list:
            primary, rest = from_to_str.split('-')
            lang_map[primary].append(rest)

        return lang_map

    def detect(self, text):
        """
        Text language detection

        :param str text: Text for language detection
        :return: text written language code
        """
        response = self.__call_api("detect", text=text)
        return response["lang"]

    def __call_api(self, method, text_collection=None, **kwargs):
        """
        API method call

        :param str method: API method name
        :return: JSON response
        """
        assert self.__API_KEY, "API key wasn't read"

        kwargs['key'] = self.__API_KEY
        joined_per_line = ''

        text_collection = text_collection or []
        if text_collection:
            kwargs.pop('text', '')
            mapped_to_text = map(
                lambda e: 'text=%s' % (reSpaceCompile.sub('+', e)),
                text_collection)
            joined_per_line = utils.to_str('&'.join(mapped_to_text))

        data = utils.urlencode(
            utils.encoded_dict(kwargs)
        ).encode(settings.ENCODING)

        if joined_per_line:
            data += utils.bytes('&' + joined_per_line)

        response = utils.request(method, data=data)
        response = json.loads(response.read().decode(settings.ENCODING))
        if response.get("code", OK) != OK:
            throw(response["code"])

        return response

    def translate(self, lang, text='', text_collection=None, format=PLAIN):
        """
        Translates the text.

        :param str text: The text to be translated.
        :param collections.Iterable text_collection:
         collection containing lines of the text
        :param str lang: Translation direction (for example, "en-ru" or "ru").
         Format:
            * A pair of language codes separated by a dash.
            For example, "en-ru" specifies to translate from English to Russian.
            *Single language code. For example, "ru" specifies to translate to Russian.
            In this case, the language of the original text is detected automatically.
        :param str format: Text format.
            Possible values
            * plain - Text without markup (default value).
            * html - Text in HTML format.
        ** note: you should provide only one of them: text or text_collection
        :return: Translated text

        """
        assert not (text and text_collection),\
            "both, text and text_collection is not supported!"

        return_list = text_collection is not None
        text_collection = text_collection or []
        response = self.__call_api("translate", text=text,
                                   text_collection=text_collection,
                                   lang=lang, format=format)
        result = response["text"]

        if not return_list:
            return " ".join(utils.to_unicode(line) for line in result)

        return result

    def translate_file(self, lang, file_path):
        utils.check_existance_and_permissions(file_path)
        with open(file_path) as f:
            results = self.translate(lang=lang, text_collection=f.readlines())
        return results

    def get_translation_directions(self):
        """
        Returns a list of translation directions supported by the service.

        :return: list of translation directions
        :rtype: list
        """
        response = self.__call_api('getLangs')
        return response["dirs"]

    def get_langs(self, ui):
        """
        Returns a dict with languages, like:
            {language code: language_name}

        :param str ui: language_name language
        """
        return self.__call_api('getLangs', ui=ui)['langs']
