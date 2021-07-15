from .connector import *
from .sentence import *
import eng_to_ipa as ipa

def insert_sentence(english,vietnamese,paragraph_id,sentence_order):

    mycursor = mydb.cursor()
    sql = "insert into \
            sentences_paragraph(english,vietnamese,paragraph_id,sentence_order) \
            values(%s,%s,%s,%s)"
    val = (english,vietnamese,paragraph_id,sentence_order)
    mycursor.execute(sql, val)
    mydb.commit()

def update_sentence(id,english,vietnamese,paragraph_id,sentence_order):
    mycursor = mydb.cursor()
    sql ="UPDATE sentences_paragraph SET \
          english= %s,\
          vietnamese= %s,\
          paragraph_id= %s,\
          sentence_order = %s\
          WHERE id = %s"
    val =  (english,vietnamese,paragraph_id,sentence_order,id)
    mycursor.execute(sql,val)
    mydb.commit()

def get_one_sentence(id):
    mycursor = mydb.cursor()
    sql ="SELECT * FROM sentences_paragraph WHERE id = %s"
    val = (id,)
    mycursor.execute(sql,val)
    w = mycursor.fetchall()
    if (len(w)>0):
        return result_to_word(w[0])
    return None

def get_all_sentence():
    mycursor = mydb.cursor()
    sql ="SELECT * FROM sentences_paragraph"
    mycursor.execute(sql)
    lst = []
    for s in mycursor.fetchall():
        lst.append(result_to_sentence(s))
    return lst

def get_sentences_by_paragraph_id(id):
    mycursor = mydb.cursor()
    sql ="SELECT * FROM sentences_paragraph WHERE id = %s ORDER BY sentence_order"
    val =  (id,)
    mycursor.execute(sql)
    lst = []
    for s in mycursor.fetchall():
        lst.append(result_to_sentence(s))
    return lst

def result_to_sentence(result):
    s = Sentence(result[0],
                result[1],
                result[2],
                result[3])
    return s
