from terminaltables import AsciiTable

from src.dao import StatisticsDao


class Fragment:

    def __init__(self) -> None:
        # self.units = UnitDao().get_all()
        # self.words = TypingDao().get_all()
        pass

    def show(self,table_data):
        table = AsciiTable(table_data)
        print (table.table)

    def general_info(self):
        unit_data = [
            ['Unit total','Vocabulary status','Typing status']
            ]
        unit_data.append(StatisticsDao().get_general_infor())
        self.show(unit_data)
        

    def list_unit_newest(self,n):
        unit_data = [
            ['Word status','Typing status','Unit code','Unit name']
        ]
        unit_data.extend(StatisticsDao().list_unit_lastest(n))
        self.show(unit_data)

    def find_unit(self,unit_code,n):
        unit_data = [
            ['Word status','Typing status','Unit code','Unit name']
        ]
        unit_data.extend(StatisticsDao().search_unit(unit_code,n))
        self.show(unit_data)
