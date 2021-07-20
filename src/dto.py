class RelationInfo:
    def __init__(self,synonymous=None,antonym=None):
        self.synonymous=synonymous
        self.antonym=antonym
        
class ExtendInfo:
    def __init__(self,pronounce=None,description=None,relation_info=None):
        self.pronounce=pronounce
        self.description=description
        self.relation_info=relation_info

class VocabularyDTO:
    def __init__(self,english=None,vietnamese=None,type_word=None,unit_code=None,right_times=0,wrong_times=0,pronounce=None,description=None,synonymous=None,antonym=None,homonym=None,units_contain=None,vietnamese_studied=None):
            self.english = english
            self.vietnamese = vietnamese
            self.type_word = type_word
            self.unit_code = unit_code
            self.right_times = right_times
            self.wrong_times = wrong_times
            self.total_times_typing = self.right_times + self.wrong_times
            self.pronounce = pronounce
            self.description = description
            self.synonymous = synonymous
            self.antonym = antonym
            self.homonym = homonym
            self.units_contain = units_contain
            self.vietnamese_studied = vietnamese_studied

    def __str__(self): 
        result = 'english = {0},\n'+\
            'vietnamese = {1},\n'+\
            'type_word = {2},\n'+\
            'unit_code = {3},\n'+\
            'right_times = {4},\n'+\
            'wrong_times = {5},\n'+\
            'total_times_typing = {6},\n'+\
            'pronounce = {7},\n'+\
            'description ={8},\n'+\
            'synonymous = {9},\n'+\
            'antonym = {10},\n'+\
            'homonym = {11},\n'+\
            'units_contain = {12},\n'+\
            'vietnamese_studied = {13},\n'
        return result.format(
                self.english,
                self.vietnamese,
                self.type_word,
                self.unit_code,
                self.right_times,
                self.wrong_times,
                self.total_times_typing,
                self.pronounce,
                self.description,
                self.synonymous,
                self.antonym,
                self.homonym,
                self.units_contain,
                self.vietnamese_studied)

class GeneralInfor:
    def __init__(self,unit_total=None,vocabulary_status=None,typing_status=None):
        self.unit_total = unit_total
        self.vocabulary_status = vocabulary_status
        self.typing_status = typing_status
    
    def __str__(self):
        return 'unit_total {}; vocabulary_status {}; typing_status {}'.format(self.unit_total,self.vocabulary_status,self.typing_status)

class List20UnitLastest:

    def __init__(self,word_status=None,typing_status=None,unit_code=None,unit_topic=None):
        self.word_status = word_status
        self.typing_status = typing_status
        self.unit_code = unit_code
        self.unit_topic = unit_topic
    
    def __str__(self):
        return 'word_status {}; typing_status {}; unit_code {}; unit_topic {}'.format(self.word_status,self.typing_status,self.unit_code,self.unit_topic)
