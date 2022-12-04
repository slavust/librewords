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

__MAX_WORDS_OUTPUT = 300 # already a bit slow

def __get_words_sorted_by_freq(text):
    split = nltk.word_tokenize(text)
    words_to_exclude = set(stopwords.words('english')) | set(wordcloud.STOPWORDS)
    split = list(filter(lambda word : word not in words_to_exclude, split))

    #if len(split) > 5000:
    #    split = list(np.random.choice(split, __MAX_WORDS, replace=False))

    sorted_lemmas = []
    while len(sorted_lemmas) < __MAX_WORDS_OUTPUT:
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
        any_lemma_found = len(words_by_lemmas.keys()) > 0
        if not any_lemma_found:
            break
        words_by_lemmas = [(words[0], words) for lemma, words in zip(words_by_lemmas.keys(), words_by_lemmas.values())]
        max_priority = max(words_by_lemmas, key=lambda lemma: len(lemma[1]))
        sorted_lemmas.append((max_priority[0], len(max_priority[1])))
        words_to_delete = set(max_priority[1])
        split = list(filter(lambda word: word not in words_to_delete, split))
    return sorted_lemmas

def render_cloud_from_text(text, output_img_path, remove_most_frequent):
    language = cld3.get_language(text).language
    print('Language:', language)
    if language != 'en':
        text = translate.translate(text, language, 'en')
    
    word_and_count = __get_words_sorted_by_freq(text)
    if remove_most_frequent:
        word_and_count = word_and_count[int(len(word_and_count)*0.15):]
        
    if language != 'en':
        words_en = [word for word, _ in word_and_count]
        words_translated = translate.batch_translate(words_en, 'en', language)
        word_and_count = [(wt, en_with_count[1]) for wt, en_with_count in zip(words_translated, word_and_count)]

    # show
    frequencies = {word : count for word, count in word_and_count}
    wc = wordcloud.WordCloud(width=2048, height=2048, background_color='white', max_words=__MAX_WORDS_OUTPUT).generate_from_frequencies(frequencies)
    wc.to_file(output_img_path)

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

    

    
    
                    