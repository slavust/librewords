#!/usr/bin/python3
import textract
import text_to_cloud
import argparse

def render_wordcloud_from_document(doc_path, output_image_path, exclude_obvious):
    text = textract.process(doc_path, output_encoding='utf-8').decode('utf-8')
    print(text)
    text_to_cloud.render_cloud_from_text(text, output_image_path, exclude_obvious)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--document', help='input document path', required=True)
    parser.add_argument('-o', '--output', help='output image path', required=True)
    parser.add_argument('-ro', 
                        '--remove-obvious', 
                        help='exclude 15 percents of most frequent words',
                        required=False, 
                        dest='remove_obvious',
                        action='store_true')
    parser.set_defaults(remove_obvious=True)
    args = parser.parse_args()
    render_wordcloud_from_document(args.document, args.output, args.remove_obvious)