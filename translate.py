#!/usr/bin/python3
import sys
import argostranslate.package, argostranslate.translate, argostranslate.argospm
import argparse
import os
import cld3
import re

def __is_translation_installed(src_lang, dest_lang):
    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = list(filter(
            lambda x: x.code == src_lang,
            installed_languages))
    to_lang = list(filter(
            lambda x: x.code == dest_lang,
            installed_languages))
    return len(from_lang) > 0 and len(to_lang) > 0

def __is_translation_downloadable(src_lang, dest_lang):
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    available_package = list(
        filter(lambda x: x.from_code == src_lang and x.to_code == dest_lang, available_packages))
    return len(available_packages) > 0

def __install_translation(src_lang, dest_lang):
    argostranslate.package.update_package_index()
    argostranslate.argospm.install_all_packages()
    #available_packages = argostranslate.package.get_available_packages()
    #available_packages = list(
    #    filter(
    #        lambda x: x.from_code == src_lang and x.to_code == dest_lang, available_packages
    #    ))
    #assert len(available_packages) > 0
    #download_path = available_packages[0].download()
    #argostranslate.package.install_from_path(download_path)

class NoAvailableTranslation(RuntimeError):
    def __init__(self):
        RuntimeError(self, 'No available translation packages for specified languages')

def batch_translate(lines, src_lang, dest_lang):
    if not __is_translation_installed(src_lang, dest_lang):
        if not __is_translation_downloadable(src_lang, dest_lang):
            raise NoAvailableTranslation()
        __install_translation(src_lang, dest_lang)

    assert __is_translation_installed(src_lang, dest_lang)

    installed_languages = argostranslate.translate.get_installed_languages()
    from_translator = list(filter(
            lambda x: x.code == src_lang,
            installed_languages))[0]
    to_translator = list(filter(
            lambda x: x.code == dest_lang,
            installed_languages))[0]
    translation = from_translator.get_translation(to_translator)
    translated_lines = [translation.translate(line) for line in lines]
    return translated_lines
    

def translate(text, src_lang, dest_lang):
    #if not __is_translation_installed(src_lang, dest_lang):
    #    if not __is_translation_downloadable(src_lang, dest_lang):
    #        raise NoAvailableTranslation()
    #    __install_translation(src_lang, dest_lang)
    if 'MAX_WORDS_TO_TRANSLATE' in os.environ:
        words = re.split(' |\t|\r|\n', text)
        print('num words:', len(words))
        if len(words) > int(os.environ['MAX_WORDS_TO_TRANSLATE']):
            print('Warning: max number of words reached, will cut', file=sys.stderr)
            text = ' '.join(words[:int(os.environ['MAX_WORDS_TO_TRANSLATE'])])

    installed_languages = argostranslate.translate.get_installed_languages()
    from_translators = list(filter(
            lambda x: x.code == src_lang,
            installed_languages))
    to_translators = list(filter(
            lambda x: x.code == dest_lang,
            installed_languages))
    translator = None
    for from_tr in from_translators:
        for to_tr in to_translators:
            translator = from_tr.get_translation(to_tr)
            if translator:
                break
    assert translator is not None
    translated_text = translator.translate(text)
    return translated_text

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source-lang', help='Language to translate from', required=False, default='auto')
    parser.add_argument('-d', '--dest-lang', help='language to translate to', required=True)
    args = parser.parse_args()

    text = sys.stdin.read()
    try:
        src_lang = args.source_lang
        if src_lang == 'auto':
            src_lang = cld3.get_language(text).language
        translated_text = translate(text, src_lang, args.dest_lang)
    except NoAvailableTranslation:
        print('No available translation packages for specified languages', file=sys.stderr)
    
    print(translated_text)
