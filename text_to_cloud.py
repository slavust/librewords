#!/usr/bin/python3
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from collections import OrderedDict
import wordcloud
import matplotlib.pyplot as plt
import sys
import argparse
import numpy as np
import cld3
import translate

__MAX_WORDS_OUTPUT = 1000

def __get_words_sorted_by_freq(text):
    split = nltk.word_tokenize(text)
    words_to_exclude = set(stopwords.words('english')) | set(wordcloud.STOPWORDS)
    split = list(filter(lambda word : word not in words_to_exclude, split))


    sorted_lemmas = []

    words_by_lemmas = OrderedDict()
    for word in split:
        synsets = wn.synsets(word)
        word_lemmas = list()
        for synset in synsets:
            for lemma in synset.lemmas():
                if lemma in word_lemmas:
                    continue
                word_lemmas.append(lemma)
        for lemma in word_lemmas:
            words_by_lemmas.setdefault(lemma, list()).append(word)
    words_by_lemmas = [[lemma, words] for lemma, words in zip(words_by_lemmas.keys(), words_by_lemmas.values())]
    while len(sorted_lemmas) < __MAX_WORDS_OUTPUT:
        lemma, words = max(words_by_lemmas, key=lambda x: len(x[1]))
        if len(words) == 0:
            break
        sorted_lemmas.append([words[0], len(words)])
        words_to_delete = set(words)
        # remove selected words usages from other lemmas
        words_by_lemmas = [[lemma, list(filter(lambda w: w not in words_to_delete, words))] for lemma, words in words_by_lemmas]
    return sorted_lemmas

def render_cloud_from_text(text, output_img_path, remove_most_frequent):
    language = cld3.get_language(text).language
    print('Language:', language)
    if language != 'en':
        print('Translating...')
        text = translate.translate(text, language, 'en')
    
    print('Counting words stats...')
    word_and_count = __get_words_sorted_by_freq(text)
    if remove_most_frequent:
        word_and_count = word_and_count[int(len(word_and_count)*0.25):]
        
    print('Generating image...')
    # show
    frequencies = dict()
    for word, count in word_and_count:
        frequencies.setdefault(word, 0)
        frequencies[word] += count
    print(len(frequencies.keys()))
    wc = wordcloud.WordCloud(width=1024, height=1024, background_color='white').generate_from_frequencies(frequencies)
    wc.to_file(output_img_path)
    print('done')

if __name__ == '__main__':
    # parse command-line
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--text', help='input text file path', required=True)
    parser.add_argument('-o', '--output', help='output image path', required=True)
    parser.add_argument('-ro', 
                        '--remove-obvious', 
                        help='exclude 15 percents of most frequent words',
                         required=False, 
                         default=False)
    parser.set_defaults(remove_obvious=False)
    args = parser.parse_args()

    text_file_path = args.text
    output_picture_path = args.output

    #read input file
    try:
        with open(text_file_path, 'r') as text_file:
            text = text_file.read()
    except IOError as e:
        print('Unable to read ' + text_file_path, file=sys.stderr)
        exit(1)
    
    render_cloud_from_text(text, output_picture_path, args.remove_obvious)

    

    
    
                    