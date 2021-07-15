from .connector import *
from .words_paragraph import *
import eng_to_ipa as ipa

def insert_words_paragraph(english,vietnamese,paragraph_id,number_of):

    mycursor = mydb.cursor()
    sql = "insert into \
            words_paragraph(english,vietnamese,paragraph_id,number_of) \
            values(%s,%s,%s,%s)"
    val = (english,vietnamese,paragraph_id,number_of)
    mycursor.execute(sql, val)
    mydb.commit()

def update_words_paragraph(id,english,vietnamese,paragraph_id,number_of):
    mycursor = mydb.cursor()
    sql ="UPDATE words_paragraph SET \
          english= %s,\
          vietnamese= %s,\
          paragraph_id= %s,\
          number_of = %s\
          WHERE id = %s"
    val =  (english,vietnamese,paragraph_id,number_of,id)
    mycursor.execute(sql,val)
    mydb.commit()

def get_one_words_paragraph(id):
    mycursor = mydb.cursor()
    sql ="SELECT * FROM words_paragraph WHERE id = %s"
    val = (id,)
    mycursor.execute(sql,val)
    w = mycursor.fetchall()
    if (len(w)>0):
        return result_to_word(w[0])
    return None

def get_all_words_paragraph():
    mycursor = mydb.cursor()
    sql ="SELECT * FROM words_paragraph"
    mycursor.execute(sql)
    lst = []
    for s in mycursor.fetchall():
        lst.append(result_to_words_paragraph(s))
    return lst

def result_to_words_paragraph(result):
    s = WordParagraph(result[0],
                result[1],
                result[2],
                result[3])
    return s
