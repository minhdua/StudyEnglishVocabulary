from src.query_paragraph import *
from src.query_sentence import *
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
# insert_paragraph("abc")
# id = get_last_id()[0]
#
# print(id)

import xlrd

# Give the location of the file



def import_excel(loc):
    wb = xlrd.open_workbook(loc)
    for sheet in wb.sheets():
        topic = sheet.cell_value(0,1)


        print("topic"," ===> ",topic)

        insert_paragraph(topic)
        id = get_last_id()[0]

        # id = get_last_id()[0]

        start = 2
        sentences_english = []
        sentences_vietnamese = []
        for i in range(start,sheet.nrows):
            e = sheet.row_values(i)

            paragraph_english = e[0]
            paragraph_vietnamese = e[1]

            sentence_english = sent_tokenize(paragraph_english)
            sentence_vietnamese = sent_tokenize(paragraph_vietnamese)
            #
            # print("english"," ===> ",paragraph_english)
            # print("vietnamese"," ===> ",paragraph_vietnamese)
            #
            # print("sentence english"," ===> ",sentence_english)
            # print("sentence vietnamese"," ===> ",sentence_vietnamese)
            #
            sentences_english.extend(sentence_english)
            sentences_vietnamese.extend(sentence_vietnamese)

        #     #word = new_word.NewWords(e[1],e[2],e[3],e[4],e[5],unit_code)
        #     update_or_insert_word(e[0],e[1],e[2],e[3],e[4],e[5],unit_code)
        if (len(sentences_english) == len(sentences_vietnamese)):
            for i in range(len(sentences_english)):
                insert_sentence(sentences_english[i],sentences_vietnamese[i],id,i)

        words = []
        for sentence in sentences_english:
            words.extend(word_tokenize(sentence))

        standard_words = []
        for word in words:
            standard_words.append(lemmatizer.lemmatize(word))
        print(words)
        print(standard_words)
loc = "C:\\Users\\ASUS\\Documents\\paragaphs.xlsx"
import_excel(loc)
