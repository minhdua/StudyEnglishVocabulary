from datetime import datetime

from src.constant import Constant
from src.dto import GeneralInfor, List20UnitLastest, VocabularyDTO
from src.model import Antonym, Example, FileImport, Synonymous, Typing, Unit, Vocabulary
from src.stuff_util import get_or_default


class BaseConvertor:
    def __init__(self,clazz):
        self.clazz = clazz

    def update_from_other(self,old,new):
        new.date_create = str(get_or_default(old.date_create,datetime.today().strftime(Constant.DATE_TIME_FORMATOR)))
        return new

    def from_cursor(self,cursor):
        self.cursor = cursor
        return self.clazz

    def copy_from_cursor(self,cursor):
        if (cursor):
            return self.from_cursor(cursor)
        return None

    def list_copy_from_list_cursor(self,cursors):
        result = []
        for cursor in cursors:
            result.append(self.copy_from_cursor(cursor))
        return result

class VocabularyConvertor(BaseConvertor):

    def __init__(self):
        super().__init__(Vocabulary())

    def from_cursor(self,cursor):
        return Vocabulary(cursor[0],cursor[1],cursor[2],cursor[3],cursor[4],cursor[5],cursor[6])

class TypingConvertor(BaseConvertor):

    def __init__(self):
        super().__init__(Typing())

    def from_cursor(self,cursor):
        return Typing(cursor[0],cursor[1],cursor[2],cursor[3],cursor[4],cursor[5],cursor[6],
            cursor[7],cursor[8],cursor[9],cursor[10],cursor[11],cursor[12])

class UnitConvertor(BaseConvertor):

    def __init__(self):
        super().__init__(Unit())

    def from_cursor(self,cursor):
        return Unit(cursor[0],cursor[1],cursor[2],cursor[3],cursor[4],cursor[5])

class GeneralInforConvertor(BaseConvertor):
    def __init__(self):
        super().__init__(GeneralInfor())

    def from_cursor(self,cursor):
        return GeneralInfor(cursor[0],cursor[1],cursor[2])

class List20UnitLastestConvertor(BaseConvertor):
    def __init__(self):
        super().__init__(List20UnitLastest())

    def from_cursor(self,cursor):
        return List20UnitLastest(cursor[0],cursor[1],cursor[2],cursor[3])

class VocabularyDTOConvertor(BaseConvertor):
    def __init__(self):
        super().__init__(VocabularyDTO())

    def from_cursor(self,cursor):
        return VocabularyDTO(cursor[0],cursor[1],cursor[2],cursor[3],cursor[4],cursor[5],cursor[6],cursor[7],cursor[8],cursor[9],cursor[10],cursor[11],cursor[12])

class FileImportConvertor(BaseConvertor):

    def __init__(self):
        super().__init__(FileImport())

    def from_cursor(self,cursor):
        return Unit(cursor[0],cursor[1],cursor[2],cursor[3])

class ExampleConvertor(BaseConvertor):
    def __init__(self):
        super().__init__(Example())

    def from_cursor(self,cursor):
        return Example(cursor[0],cursor[1],cursor[2],cursor[3],cursor[4],cursor[5])


class SynonymousConvertor(BaseConvertor):
    def __init__(self):
        super().__init__(Synonymous())

    def from_cursor(self,cursor):
        return Synonymous(cursor[0],cursor[1],cursor[2],cursor[3],cursor[4])

class AntonymConvertor(BaseConvertor):
    def __init__(self):
        super().__init__(Antonym())

    def from_cursor(self,cursor):
        return Antonym(cursor[0],cursor[1],cursor[2],cursor[3],cursor[4])