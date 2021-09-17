import urllib.request

import eng_to_ipa
from bs4 import BeautifulSoup
from nltk.corpus.reader.wordnet import ADJ, ADV, NOUN, VERB

from src.constant import Color
from src.dto import ExtendInfo, RelationInfo
import re


def get_or_default(this,that):
    if(not this):
        return that
    return this

def cover_slash(word):
    return '/'+word + '/'

def high_light(word,color,color_default=Color.DEFAULT):
        return color + str(word) + color_default
        
def get_notation(word):
        if(word.capitalize().startswith('Adjective')):
            return ADJ
        elif(word.capitalize().startswith('Adverb')):
            return ADV
        elif(word.capitalize().startswith('Verb')):
            return VERB
        else:
            return NOUN
            
def get_list_input(args):
    list_input = []
    if(args):
        list_input = re.split(';\s*',' '.join(args))
    return list_input
    
class Browser:
    def pronounce(self):
        try:
            pronounce = self.soup.select_one('.pronounce').string
        except:
            pronounce = cover_slash(eng_to_ipa.convert(self.word))
        return pronounce

    def description_list1(self,r):
        if(r.select_one('li b')):
                    tag = str(r.select_one('li b').string)
                    if (tag != 'None'):
                            return '-'+tag +'\n ' 
        return ''

    def description_list2(self,r):
        ul = r.select('.list2 li')
        if(len(ul) > 0):
            for li in ul:
                description = '>>>'+ li.select_one('.example-original').string +'\n '
                return description+ '('+li.contents[2] +')\n '
        return ''

    def description(self):
        result = self.soup.select('.phanloai, .list1, .list2')
        description = ''
        for r in result:
            if(r.has_attr('class')and r['class'][0] == 'phanloai'):
                description = description + '\n'+ r.string + ': \n'
            elif(r.has_attr('class')and r['class'][0] == 'list1'):
                description = description + self.description_list1(r)
            elif(r.has_attr('class')and r['class'][0] == 'list2'):
                description = description + self.description_list2(r)
        return  str(description).replace('"','\\"')

    def relation_word(self):
        
        synonymous    = ''
        antonym = ''
        related_word = self.soup.select('.relatedWord .list1 li')
        # #print(len(related_word))
        for rr in related_word:
            strong = rr.select_one('strong')
            title = strong.contents[0].string
            if(str(title).startswith('Từ đồng nghĩa')):
                words = rr.select('a')
                for w in words:
                    ##print(word.string)
                    synonymous = synonymous + w.string + '; '
            if(str(title).startswith('Từ trái nghĩa')):
                words = rr.select('a')
                for w in words:
                    ##print(word.string)
                    antonym = antonym + w.string + '; '
                    # #print('w = ',w,'\n>>type w =',type(w))
        return RelationInfo(synonymous,antonym)

    def __init__(self,word):
        self.word = word
        word = word.replace(' ','+')
        url = 'https://vdict.com/word?word={word}&select-dictionary=1'.format(word = word)
        response = urllib.request.urlopen(url)
        html = response.read()
        self.soup = BeautifulSoup(html, "html.parser")

    def search(self):
        return ExtendInfo(self.pronounce(),self.description(),self.relation_word())

def translate(english):
    english = english.replace(' ','+')
    url = 'https://vdict.com/word?word={}&select-dictionary=1'.format(english.capitalize())
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    tag1 = soup.select('#result-contents > ul > li > b')
    vietnamese=get_tag_notblank(tag1)
    tag = soup.select('#result-contents > div')
    type_word = get_tag_notblank(tag)
    return (vietnamese,type_word)

def get_tag_notblank(tag):
    s = ''
    if(tag):
        for e in tag:
            if(e and e.string!=None and e.string.strip() !=''):
                s = e.string
                break
    return s
