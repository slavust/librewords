#!/usr/bin/python3
import text_to_cloud
import url_to_cloud
import argparse
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    internal_urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)

        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            continue
        internal_urls.add(href)
    return internal_urls


def render_cloud_from_website(url, output_image_path, exclude_obvious):
    urls = get_all_website_links(url)
    texts = [url_to_cloud.get_text_from_url(url) for url in urls]
    whole_thing = '\n.\n'.join(texts)
    text_to_cloud.render_cloud_from_text(whole_thing, output_image_path, exclude_obvious)
    
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
    render_cloud_from_website(args.url, args.output, args.remove_obvious)
