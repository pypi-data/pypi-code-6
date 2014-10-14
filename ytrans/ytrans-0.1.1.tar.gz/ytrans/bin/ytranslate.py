#!/usr/bin/env python
# coding: utf-8
from ytrans import YTranslator
from ytrans import read_key
from ytrans.utils import to_str


def get_args_parser():
    import argparse
    parser = argparse.ArgumentParser(description="Yandex translator")
    parser.add_argument(
        "--lang", '-l', dest='lang', default='none', help='Translation direction')
    parser.add_argument(
        "--available-languages", "-a", dest='available',
        action='store_true', help="Show available languages")

    parser.add_argument("text", nargs='*', metavar='text', help='Text for translation')
    return parser


def main():
    key = read_key()
    translator = YTranslator(key)
    parser = get_args_parser()
    args = parser.parse_args()
    show_available_languages = args.available
    if show_available_languages:
        print("Languages available : {0}".format(
            ", ".join(translator.get_translation_directions())))
        exit()

    lang = args.lang
    text = " ".join(args.text)

    if not text:
        print("Text is required!")
        parser.print_help()
        exit()

    if lang == "none":
        text_lang = translator.detect(text=text[:100])
        if text_lang != "ru":
            lang = "ru"
        else:
            lang = "en"

    print(to_str(translator.translate(lang=lang, text=text)))


if __name__ == '__main__':
    main()
