from .connector import *
import eng_to_ipa as ipa
class NewWords:
    unit_code = None
    create_date = None
    last_study_date = None
    right_times = 0;
    wrong_times = 0;
    def __init__(self, order,english,vietnamese,type_word,sentent_english,sentent_vietnamese,unit_code,right_times,wrong_times):
        self.order = order
        self.english = english
        self.vietnamese = vietnamese
        self.type_word = type_word
        self.sentent_english = sentent_english
        self.sentent_vietnamese = sentent_vietnamese
        self.unit_code = unit_code
    def cursor_to_word(cursor):
        return NewWords(cursor[0],
                        cursor[1],
                        cursor[2],
                        cursor[3],
                        cursor[4],
                        cursor[5],
                        cursor[6],
                        cursor[8],
                        cursor[9]
        )
        #order, english, vietnamese, type_word, sentent_example_english, sentent_example_vietnamese, unit_code, pronounce, right_times, wrong_times, date_create, date_last_study, description, synonymous, antonym, homonym, units_contain
def insert_word(word):
    if(word.english == ""):
        return
    
    mycursor = mydb.cursor()
    sql = "insert into \
            new_words(`order`,\
            english,\
            vietnamese,\
            type_word,\
            sentent_example_english,\
            sentent_example_vietnamese,\
            unit_code) \
            values(%s,%s, %s, %s, %s, %s,%s)" 
    val = ( word.order,
            word.english,
            word.vietnamese,
            word.type_word,
            word.sentent_example_english,
            word.sentent_example_vietnamese,
            word.unit_code)
    mycursor.execute(sql, val)
    mydb.commit()

def update_word(word):
    mycursor = mydb.cursor()
    sql ="UPDATE new_words SET \
          english = %s,\
          vietnamese = %s, \
          type_word = %s, \
          sentent_example_english = %s, \
          sentent_example_vietnamese = %s \
          WHERE `order` = %s AND  unit_code = %s"
    val =  (word.english,
            word.vietnamese,
            word.type_word,
            word.sentent_example_english,
            word.sentent_example_vietnamese,
            word.order,
            word.unit_code)
    mycursor.execute(sql,val)
    mydb.commit()

def get_word_by_english(english):
    mycursor = mydb.cursor()
    sql ="SELECT * FROM new_words WHERE english = %s"
    val = (english,)
    mycursor.execute(sql,val)
    lst = []
    for w in mycursor.fetchall():
       lst.append(NewWords.cursor_to_word(w))
    return lst

def get_by_english_and_unit(english,unit):
    mycursor = mydb.cursor()
    sql ="SELECT * FROM new_words WHERE english = %s and unit_code = %s"
    val = (english,unit,)
    mycursor.execute(sql,val)
    lst = []
    for w in mycursor.fetchall():
       lst.append(NewWords.cursor_to_word(w))
    return lst

def get_all_word():
    mycursor = mydb.cursor()
    sql ="SELECT * FROM new_words"
    mycursor.execute(sql)
    lst = []
    for w in mycursor.fetchall():
        lst.append(NewWords.cursor_to_word(w))
    return lst

def get_by_unit(unit_code):
    mycursor = mydb.cursor()
    sql ="SELECT * FROM new_words WHERE unit_code=%s ORDER BY `order` ASC"
    val = (unit_code.upper(),)
    mycursor.execute(sql,val)
    lst = []
    for w in mycursor.fetchall():
        lst.append(NewWords.cursor_to_word(w))
    return lst

