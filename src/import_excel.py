import xlrd
from . import new_word
from .query_unit import *
from .query_word import *
from .query_typing import *
import re
from .search import search
# Give the location of the file


def standard_string(st):
    pattern = re.compile(r'(^\s+)|(\s+$)|\s\s')
    st = re.sub(pattern,'',st)
    return st.capitalize()

def standard(e):
    lst = []
    lst.append(int(e[0]))
    for i in range(1,6) :
        lst.append(standard_string(str(e[i])))
    return lst

def import_excel(loc):
    wb = xlrd.open_workbook(loc)
    for sheet in wb.sheets():
        unit_code = sheet.cell_value(0,1).upper()
        unit_topic = sheet.cell_value(1,1)
        print(unit_code," ===> ",unit_topic)
        update_or_insert_unit(unit_code,unit_topic)
        start = 4
        #pronounce,
        #description,
        #synonymous,
        #antonym,
        #units_contain
        for i in range(start,sheet.nrows):
            e = sheet.row_values(i)
            e = standard(e)
           # print(english) 
            typing = get_type_by_english(e[1])
            words = get_word_by_english(english)
            units_contain = ''
            if(len(words) != 0):
                for word in words:
                    print(word)
                    units_contain = units_contain + word.unit_code + '; '
            if(typing == None):
                #insert
                result = search(english)
                insert_type(Typing(e[1],0,0,result[0],result[1],result[2],result[3],units_contain))
            else:
                #update
                typing.units_contain = units_contain
                update_type(typing)
            
            #word = new_word.NewWords(e[1],e[2],e[3],e[4],e[5],unit_code,result[0],result[1],result[2],result[3])
            #update_or_insert_word(e[0],e[1],e[2],e[3],e[4],e[5],unit_code,result[0],result[1],result[2],result[3],units_contain)
