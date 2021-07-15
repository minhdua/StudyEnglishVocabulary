from .connector import *
class Typing:
    def __init__(self,
            english,
            right_times,
            wrong_times,
            pronounce,
            description,
            synonymous,
            antonym,
            units_contain):
        self.english = english
        self.right_times = right_times
        self.wrong_times = wrong_times
        self.pronounce = pronounce
        self.description = description
        self.synonymous = synonymous
        self.antonym = antonym
        self.units_contain = units_contain
    def cursor_to_typing(cursor):
        return Typing(
                    cursor[0],
                    cursor[1],
                    cursor[2],
                    cursor[3],
                    cursor[4],
                    cursor[5],
                    cursor[6],
                    cursor[8])
def insert_type(typing):
    if(typing.english == ""):
        return
    mycursor = mydb.cursor()
    sql = "insert into typing(\
            english,\
            right_times,\
            wrong_times,\
            pronounce,\
            description,\
            synonymous,\
            antonym,\
            units_contain\
            ) \
            values(%s,%s,%s,%s,%s,%s,%s,%s)" 
    val = (
            typing.english,
            typing.right_times,
            typing.wrong_times,
            typing.pronounce,
            typing.description,
            typing.synonymous,
            typing.antonym,
            typing.units_contain
            )
    mycursor.execute(sql, val)
    mydb.commit()

def update_type(typing):
    if(typing.english == ""):
        return
    mycursor = mydb.cursor()
    sql ="UPDATE typing SET \
        right_times = %s,\
        wrong_times = %s,\
        pronounce = %s,\
        description = %s,\
        synonymous = %s,\
        antonym = %s,\
        homonym = %s,\
        units_contain= %s\
        WHERE `english` = %s"
    val =  (
            typing.right_times,
            typing.wrong_times,
            typing.pronounce,
            typing.description,
            typing.synonymous,
            typing.antonym,
            typing.homonym,
            typing.units_contain,
            typing.english)
    mycursor.execute(sql,val)
    mydb.commit()
    
def get_type_all():
    mycursor = mydb.cursor()
    sql ="SELECT * FROM typing"
    mycursor.execute(sql)
    lst = []
    for w in mycursor.fetchall():
        lst.append(Typing.cursor_to_typing(w))
    return lst

def get_type_by_english(english):
    mycursor = mydb.cursor()
    sql ="SELECT * FROM typing WHERE english=%s"
    val = (english,)
    mycursor.execute(sql,val)
    lst = []
    for w in mycursor.fetchall():
        lst.append(Typing.cursor_to_typing(w))
    if(len(lst) > 0):
        return lst[0]
    return None

def increment_right_times(english):
    mycursor = mydb.cursor()
    sql ="UPDATE typing SET \
          right_times = right_times + 1 \
          WHERE english = %s"
    val =  (english,)
    mycursor.execute(sql,val)
    mydb.commit()

def increment_wrong_times(english):
    mycursor = mydb.cursor()
    sql ="UPDATE typing SET \
          wrong_times = wrong_times + 1 \
          WHERE english = %s"
    val =  (english,)
    mycursor.execute(sql,val)
    mydb.commit()