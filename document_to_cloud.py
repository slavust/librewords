#!/usr/bin/python3
import textract
import text_to_cloud
import argparse
import os
import os.path
import language_codes


def get_text_from_document(doc_path, language):
    # added as submodule
    tessdata_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tessdata')
    os.environ['TESSDATA_PREFIX'] = tessdata_path

    if language in language_codes.LANG_CODES.keys():
        language = lang_codes[language]

    text = textract.process(doc_path, output_encoding='utf-8', language=language).decode('utf-8')
    return text

def render_wordcloud_from_document(doc_path, output_image_path, exclude_obvious, language):
    text = get_text_from_document(doc_path, language)
    text_to_cloud.render_cloud_from_text(text, output_image_path, exclude_obvious)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--document', help='input document path', required=True)
    parser.add_argument('-o', '--output', help='output image path', required=True)
    parser.add_argument('-l', '--lang', help='image language', default='en', required=False)
    parser.add_argument('-ro', 
                        '--remove-obvious', 
                        help='exclude 15 percents of most frequent words',
                        required=False, 
                        dest='remove_obvious',
                        action='store_true')
    parser.set_defaults(remove_obvious=False)
    args = parser.parse_args()
    render_wordcloud_from_document(args.document, args.output, args.remove_obvious, args.lang)