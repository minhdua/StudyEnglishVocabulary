from .connector import *
from .paragraph import *
import eng_to_ipa as ipa



def insert_paragraph(topic):
    mycursor = mydb.cursor()
    #mydb.insert_id()
    print(mycursor.lastrowid)
    sql = "insert into \
            paragraph(topic) \
            values(%s)"
    val = (topic,)
    #id = mycursor.fetchone(sql, val)
    mycursor.execute(sql,val)
    mydb.commit()

def update_paragraph(id,topic):
    mycursor = mydb.cursor()
    sql ="UPDATE paragraph SET \
          topic = %s, \
          WHERE id = %s"
    val =  (topic,id)
    mycursor.execute(sql,val)
    mydb.commit()

def get_one_paragraph(id):
    mycursor = mydb.cursor()
    sql ="SELECT * FROM paragraph WHERE id = %s"
    val = (id,)
    mycursor.execute(sql,val)
    w = mycursor.fetchall()
    if (len(w)>0):
        return result_to_word(w[0])
    return None

def get_last_id():
    mycursor = mydb.cursor()
    sql ="SELECT max(id) FROM paragraph"
    mycursor.execute(sql)
    w = mycursor.fetchone()
    return w

def get_all_paragraph():
    mycursor = mydb.cursor()
    sql ="SELECT * FROM paragraph"
    mycursor.execute(sql)
    lst = []
    for p in mycursor.fetchall():
        lst.append(result_to_paragraph(p))
    return lst

def result_to_paragraph(result):
    p = Paragraph(result[0],
                result[1])
    return p
