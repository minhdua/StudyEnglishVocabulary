import uuid
from datetime import datetime

import eng_to_ipa

from src.constant import Constant
from src.stuff_util import cover_slash, get_or_default


class BaseModel:
    '''
    this is class base model
    '''
    def __init__(self,id=None,date_create=None,date_last_update=None):
        self.id = str(get_or_default(id,uuid.uuid4()))
        self.date_create = str(get_or_default(date_create,datetime.today().strftime(Constant.DATE_TIME_FORMATOR)))
        self.date_last_update = str(get_or_default(date_last_update,datetime.today().strftime(Constant.DATE_TIME_FORMATOR)))

class Vocabulary(BaseModel):
    '''
        vocabulary model 
    '''
    def __init__(self,id=None,english = '',vietnamese = '',type_word='',unit_code = '',date_create=None,date_last_update=None):
        self.english = english
        self.vietnamese = vietnamese
        self.type_word = get_or_default(type_word,'Undefined')
        self.unit_code = unit_code
        super().__init__(id,date_create,date_last_update)

    def __str__(self):
        return '({0}; {1}; {2}; {3}; {4}; {5}; {6})'\
        .format(self.id,self.english,self.vietnamese,self.unit_code,self.type_word,self.date_create,self.date_last_update)

class Typing(BaseModel):
    '''
    this class is Typing model
    '''
    def __init__(self,id=None, english='', right_times=0, wrong_times=0, pronounce='', description='', synonymous=None, antonym=None, homonym=None, units_contain=None,vietnamese_studied=None, date_create=None, date_last_update=None):
        self.english=english
        self.right_times=str(right_times)
        self.wrong_times=str(wrong_times)
        self.pronounce=get_or_default(pronounce,cover_slash(eng_to_ipa.convert(english)))
        if(description):
            self.description= description.replace('"','\\"')
        self.synonymous=get_or_default(synonymous,'')
        self.antonym=get_or_default(antonym,'')
        self.homonym=get_or_default(homonym,'')
        self.units_contain=units_contain
        self.vietnamese_studied = vietnamese_studied
        super().__init__(id,date_create,date_last_update)
        
    def __str__(self):
        return '{0}; {1}; {2}; {3}; {4}; {5}; {6}; {7}; {8}; {9}; {10}; {11}; {12}'\
            .format(
                self.id,
                self.english,
                self.right_times,
                self.wrong_times,
                self.pronounce,
                self.description,
                self.synonymous,
                self.antonym,
                self.homonym,
                self.units_contain,
                self.vietnamese_studied,
                self.date_create,
                self.date_last_update)

class Unit(BaseModel):
    '''
    this class is Unit model
    '''
    def __init__(self,id=None, unit_code=None, unit_topic=None, description=None, date_create=None, date_last_update=None):
        self.unit_code=unit_code
        self.unit_topic=unit_topic
        self.description=description
        super().__init__(id,date_create,date_last_update)

    def __str__(self):
        return '{0}; {1}; {2}; {3}; {4}; {5}'\
            .format(
                self.id,
                self.unit_code,
                self.unit_topic,
                self.description,
                self.date_create,
                self.date_last_update)

class FileImport(BaseModel):
    '''
    this class is Unit model
    '''
    def __init__(self,id=None, file_name=None,date_create=None,date_last_update=None):
        self.file_name=file_name
        super().__init__(id,date_create,date_last_update)

    def __str__(self):
        return '{0}; {1}; {2}; {3}'\
            .format(
                self.id,
                self.file_name,
                self.date_create,
                self.date_last_update)

class Example(BaseModel):
    
    '''
    this class is Unit model
    '''
    def __init__(self,id=None, english=None, translate=None, example=None, date_create=None, date_last_update=None):
        self.english=english
        self.translate=translate
        self.example=example
        super().__init__(id,date_create,date_last_update)

    def __str__(self):
        return '{0}; {1}; {2}; {3}; {4}; {5}'\
            .format(
                self.id,
                self.english,
                self.translate,
                self.example,
                self.date_create,
                self.date_last_update)