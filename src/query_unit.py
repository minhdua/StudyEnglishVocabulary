from .connector import *
from .unit import *
def insert_unit(unit_code,unit_topic):
    mycursor = mydb.cursor()
    sql = "insert into units(unit_code,unit_topic) values (%s, %s)"
    val = (unit_code, unit_topic)
    mycursor.execute(sql, val)
    mydb.commit()

def update_or_insert_unit(unit_code,unit_topic):
    if (get_one_unit(unit_code) == None):
        insert_unit(unit_code,unit_topic)
    else:
        update_unit(unit_code,unit_topic)


def update_unit(unit_code,unit_topic):
    mycursor = mydb.cursor()
    sql ="UPDATE units SET unit_topic = %s WHERE unit_code = %s"
    val = (unit_topic,unit_code)
    mycursor.execute(sql,val)
    mydb.commit()

def get_one_unit(unit_code):
    mycursor = mydb.cursor()
    sql ="SELECT * FROM units WHERE unit_code = %s"
    val = (unit_code.upper(),)
    mycursor.execute(sql,val)
    u = mycursor.fetchall()
    if (len(u)>0):
        return result_to_unit(u[0])
    return None

def get_all_unit():
    mycursor = mydb.cursor()
    sql ="SELECT * FROM units"
    mycursor.execute(sql)
    us = mycursor.fetchall()
    lst = []
    for u in us:
        lst.append(result_to_unit(u))
    return lst

def result_to_unit(result):
    u = Units(result[0],result[1])
    u.set_date_create = result[2]
    u.set_date_update = result[3]
    return u
