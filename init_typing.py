from src.query_typing import *
from src.query_word import *
from src.search import search
words = get_all_word()
for word in words:
    typing = get_type_by_english(word.english)
    if(typing == None):
        try:
            result = search(word.english)
            #print(result)
            vocabs = get_word_by_english(word.english)
            units_contain = ''
            if(len(vocabs) != 0):
                for word in vocabs:
                    #print(word)
                    units_contain = units_contain + word.unit_code + '; '
            typing = Typing(word.english,word.right_times,word.wrong_times,result[0],result[1],result[2],result[3],units_contain)
            insert_type(typing)
            print('>>> : ', typing.english)
        except:
            print('error: ', word.english,ex)