import threading
from copy import deepcopy

from nltk.stem.wordnet import WordNetLemmatizer

from src.connector import Connector
from src.constant import Constant
from src.convertor import (AntonymConvertor, ExampleConvertor, FileImportConvertor, GeneralInforConvertor,
                           List20UnitLastestConvertor, SynonymousConvertor, TypingConvertor,
                           UnitConvertor, VocabularyConvertor,
                           VocabularyDTOConvertor)
from src.dto import GeneralInfor
from src.model import Antonym, Example, FileImport, Synonymous, Typing, Unit, Vocabulary
from src.query_util import QueryBuilder
from src.stuff_util import Browser, get_or_default


class BaseDao:
    def __init__(self,clazz,convertor,ids):
        self.clazz = clazz
        self.conn = Connector()
        self.convertor = convertor
        self.query = QueryBuilder(self.clazz,ids,self.clazz)

    def loader(self):
        pass #comment explaining why this function is empty
        
    def save(self):
        sql = self.query.insert_builder()
        self.conn.commit(sql)
        self.loader()
        return self.clazz

    def update(self,clazz):
        new_clazz = self.convertor.update_from_other(self.clazz,clazz)
        self.query.set_object(new_clazz)
        sql = self.query.update_builder()
        self.conn.commit(sql)
        self.loader()
        return self.clazz

    def update_or_save(self):
        if(not self.get_by_ids()):
            self.save()
        else:
            self.update(self.clazz)

    def get_all(self):
        sql = self.query.select_builder()
        objects = self.convertor.list_copy_from_list_cursor(self.conn.fetchall(sql))
        return objects

    def get_by_ids(self):
        sql = self.query.select_builder()
        return self.convertor.copy_from_cursor(self.conn.fetchone(sql))

    def delete_by_ids(self):
        sql = self.query.delete_builder()
        self.conn.commit(sql)
        return self.clazz

    def get_by_custom_query(self,obj,ids):
        custom_query = deepcopy(self.query)
        custom_query.primaries = ids
        custom_query.set_object_origin(obj)
        sql = custom_query.select_builder()
        return self.convertor.list_copy_from_list_cursor(self.conn.fetchall(sql))

    def delete_by_custom_query(self,obj,ids):
        custom_query = deepcopy(self.query)
        custom_query.primaries = ids
        custom_query.set_object(obj)
        sql = custom_query.delete_builder()
        self.conn.commit(sql)
        return obj

class VocabularyDao(BaseDao):
    '''
        this class to interact with database
        function:
            save: create new vocabulary
            update: update vocabulary with database
            list: retrieve all vocabulary by english, type_word , vietnamese, unit
            get: retrieve one vocabulary by english and unit
            delete: delete vocabulary kick off database
            saveList: save all vocabulary in a list
    '''
    def __init__(self,vocabulary=None):
        self.vocabulary = get_or_default(vocabulary,Vocabulary())
        typing = Typing(english=self.vocabulary.english)
        self.loader_class= TypingDao(typing)
        super().__init__(self.vocabulary,VocabularyConvertor(),['english','unit_code'])

    def loader(self):
        self.loader_class.loader_typing(self.query.object.english)

    def update_or_save(self):
        if(not self.get_by_ids()):
            self.save()
        else:
            self.update(self.vocabulary)

    def get_by_unit(self,unit_code):
        vocabulary = deepcopy(self.vocabulary)
        vocabulary.unit_code = unit_code
        return self.get_by_custom_query(vocabulary,['unit_code'])

    def get_by_english(self,english):
        vocabulary = deepcopy(self.vocabulary)
        vocabulary.english = english
        return self.get_by_custom_query(vocabulary,['english'])

    def get_by_type(self,type_word):
        vocabulary = deepcopy(self.vocabulary)
        vocabulary.type_word = type_word
        return self.get_by_custom_query(vocabulary,['type_word'])

    def delete_by_english(self,english):
        vocabulary = deepcopy(self.vocabulary)
        vocabulary.english = english
        return self.delete_by_custom_query(vocabulary,['english'])

    def delete_by_english(self,unit_code):
        vocabulary = deepcopy(self.vocabulary)
        vocabulary.unit_code = unit_code
        return self.delete_by_custom_query(vocabulary,['unit_code'])

class TypingDao(BaseDao):

    '''
    this class to interact with database
        function:
            save: create new typing
            update: update typing with database
            list: retrieve all typing by english, pronounce , right_time, wrong_time
            get: retrieve one typing by english
            delete: delete typing kick off database
            saveList: save all typing in a list
    '''
    def __init__(self,typing=None):
        self.typing = get_or_default(typing,Typing())
        super().__init__(self.typing,TypingConvertor(),['english'])

    def get_by_pronounce(self,pronounce):
        typing = deepcopy(self.typing)
        typing.pronounce = pronounce
        return self.get_by_custom_query(typing,['pronounce'])

    def get_by_right_times_greater_than(self,right_times):
        typing = deepcopy(self.typing)
        typing.right_times = right_times
        return self.get_by_custom_query(typing,[('right_times',Constant.GREATER)])

    def get_by_wrong_times_greater_than(self,wrong_times):
        typing = deepcopy(self.typing)
        typing.wrong_times = wrong_times
        return self.get_by_custom_query(typing,[('wrong_times',Constant.GREATER)])

    def get_by_right_times_lesser_than(self,right_times):
        typing = deepcopy(self.typing)
        typing.right_times = right_times
        return self.get_by_custom_query(typing,[('right_times',Constant.LESSER)])

    def get_by_wrong_times_lesser_than(self,wrong_times):
        typing = deepcopy(self.typing)
        typing.wrong_times = wrong_times
        return self.get_by_custom_query(typing,[('wrong_times',Constant.LESSER)])

    def loader_homonym(self):
        english = [t.english  for t in self.get_by_pronounce(self.typing.pronounce) if t.english != self.typing.english]
        return Constant.SEPARATOR.join(set(english))

    def loader_units_contain(self):
        vocabulary_dao = VocabularyDao()
        units = [v.unit_code for v in vocabulary_dao.get_by_english(self.typing.english)]
        return Constant.SEPARATOR.join(set(units))

    def loader_vietnamese_studied(self):
        vocabulary_dao = VocabularyDao()
        vietnamese =  [v.vietnamese for v in vocabulary_dao.get_by_english(self.typing.english)]
        return Constant.SEPARATOR.join(set(vietnamese))

    def update_extend(self):
        self.typing.homonym = self.loader_homonym()
        self.typing.units_contain = self.loader_units_contain()
        self.typing.vietnamese_studied = self.loader_vietnamese_studied()

    def loader_typing(self,english):
        self.query.set_object_origin(Typing(english=english))
        typing = self.get_by_ids()
        if(not typing):
            self.query.set_object(Typing(english=english))
            #self.update_extend()
            self.save()
        else:
            self.typing = typing
            #self.update_extend()
            self.update(self.typing)
        return self.typing

class UnitDao(BaseDao):
    '''
    this class to interact with database
        function:
            save: create new unit
            update: update unit with database
            list: retrieve all unit by unit code
            get: retrieve one unit by unit_code
            delete: delete unit kick off database
            saveList: save all unit in a list
    '''
    def __init__(self,unit=None):
        self.unit = get_or_default(unit,Unit())
        super().__init__(self.unit,UnitConvertor(),['unit_code'])

    def loader_unit(self):
        if(not self.get_by_ids()):
            self.save()
        else:
            self.update(self.unit)

class FileImportDao(BaseDao):
    def __init__(self,fileimport=None):
        self.fileimport = get_or_default(fileimport,FileImport())
        super().__init__(self.fileimport,FileImportConvertor(),['file_name'])

    def loader_fileimport(self):
            if(not self.get_by_ids()):
                self.save()
            else:
                self.update(self.fileimport)

class ExampleDao(BaseDao):
    def __init__(self,example=None):
        self.example = get_or_default(example,Example())
        super().__init__(self.example,ExampleConvertor(),['english','example'])

    def get_by_english(self,english):
            example = deepcopy(self.example)
            example.english = english
            return self.get_by_custom_query(example,['english'])

    def delete_by_example(self,sentence):
        example = deepcopy(self.example)
        example.example = sentence
        return self.delete_by_custom_query(example,['english','example'])

class StatisticsDao():
    
    def __init__(self):
        self.query = QueryBuilder(GeneralInfor())
        self.conn = Connector()
        self.general_infor_convertor = GeneralInforConvertor()
        self.list_20_unit_lastest_convertor = List20UnitLastestConvertor()
        self.vocabulary_dto_convertor = VocabularyDTOConvertor()

    def get_general_infor(self):
        return self.conn.callproc()

    def list_unit_lastest(self,n):
        sql = QueryBuilder().list_unit_builder(n)
        return self.conn.fetchall(sql)

    def search_unit(self,unit_code,n):
        sql = QueryBuilder(Unit(unit_code=unit_code),[('unit_code','like')]).list_unit_builder(n)
        return self.conn.fetchall(sql)

    def get_vdto_by_unit(self,unit_code):
        sql = self.query.select_vdto_by_unit_builder(unit_code)
        return self.vocabulary_dto_convertor.list_copy_from_list_cursor(self.conn.fetchall(sql))

class SynonymousDao(BaseDao):

    def __init__(self,synonymous=None):
        self.synonymous = get_or_default(synonymous,Synonymous())
        super().__init__(self.synonymous,SynonymousConvertor(),['english','syn_english'])

    def get_by_english(self,english):
            synonymous = deepcopy(self.synonymous)
            synonymous.english = english
            return self.get_by_custom_query(synonymous,['english'])

class AntonymDao(BaseDao):
    def __init__(self,antonym=None):
        self.antonym = get_or_default(antonym,Antonym())
        super().__init__(self.antonym,AntonymConvertor(),['english','an_english'])

    def get_by_english(self,english):
            antonym = deepcopy(self.antonym)
            antonym.english = english
            return self.get_by_custom_query(antonym,['english'])
        