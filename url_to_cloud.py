#!/usr/bin/python3
import urllib
import sys
from bs4 import BeautifulSoup
import text_to_cloud
import argparse

def get_text_from_url(url):
    try:
        with urllib.request.urlopen(url) as page:
            encoding = page.headers.get_content_charset()
            html = page.read().decode(encoding if encoding else 'utf-8')
    except RuntimeError as e:
        print('Unable to load ' + url)
        return ''
    except urllib.error.HTTPError:
        print('Unable to load ' + url)
        return ''
    except urllib.error.URLError:
        print('Unable to load ' + url)
        return ''
        
    soup = BeautifulSoup(html, features='html.parser')

    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    return soup.get_text()

def render_cloud_from_url(url, output_image_path, remove_most_frequent_words):
    text = get_text_from_url(url)
    text_to_cloud.render_cloud_from_text(text, output_image_path, remove_most_frequent_words)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='input url', required=True)
    parser.add_argument('-o', '--output', help='output image path', required=True)
    parser.add_argument('-ro', 
                        '--remove-obvious', 
                        help='exclude 15 percents of most frequent words',
                        required=False, 
                        dest='remove_obvious',
                        action='store_true')
    parser.set_defaults(remove_obvious=False)
    args = parser.parse_args()
    render_cloud_from_url(args.url, args.output, args.remove_obvious)
    