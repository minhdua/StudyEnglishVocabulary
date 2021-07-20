
from src.dao import StatisticsDao, UnitDao, VocabularyDao


class VocabularyService:

    def get_by_unit(self,unit_code):
        return StatisticsDao().get_vdto_by_unit(unit_code)

    def save_vocabulary_and_unit(self,vocabulary,unit):
        UnitDao(unit).loader_unit()
        vocabulary.unit_code = unit.unit_code
        VocabularyDao(vocabulary).save()

