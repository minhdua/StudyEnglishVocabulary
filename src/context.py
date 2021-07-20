import csv
import webbrowser
from os import listdir
from os.path import isfile, join

import eng_to_ipa
import pyttsx3

from src.constant import Color
from src.dao import FileImportDao, TypingDao, UnitDao, VocabularyDao
from src.fragment import Fragment
from src.menu import InforMenu, ItemInfo, Menu, Option
from src.model import FileImport, Typing, Unit, Vocabulary
from src.service import VocabularyService
from src.stuff_util import translate


class VocabularyContext(Menu):
    '''
    this class to operation with vocabulary list passed from menu
    function:
        info: #print current vocabulary basic information
        infoExtend: #print current vocabulary extend information
        checkInput: check current english vocabulary with entered word from keyboard
        nextWord: get next vocabulary in vocabulary list
        preWord: get previous vocabulary in vocabulary list
        updateWordToDB: update vocabulary into database
        updateWordFromDB: update vocabulary from database
        deleteWordToDB: delete vocabulary into database
        insertWordToDB: inset new vocabulary into database
        #printAll: #print all vocabulary in list include english and vietnamese
        soundEnglish: speech english value of vocabulary
        soundVietnamese: speech vietnamese value of vocabulary
        AutoExportCsv: Automatic update csv while change db
        AutoExportWeb: Automatic export web page while change db
        browseImage: browse image from google Image display on google chrome browser
        browseVideo: browse video from Youtube display on google chrome browser
    '''

    def __init__(self,units=None,current_index = 0,speaken_lag=True,speakvi_lag=True,browseimg_flag=False):
        self.units = units
        self.vocabularies = self.get_vocabularies()
        self.current_index = current_index
        self.vocabulary = self.current_vocabulary()
        self.speaken_lag = speaken_lag
        self.speakvi_lag = speakvi_lag
        self.browseimg_flag = browseimg_flag
        self.already_browse = False
        super().__init__('Study My vocabulary')
        self.add_option()
        self.add_command()
        if(self.is_empty()):
            self.message_error("Not found any vocabulary")

    def is_empty(self):
        return self.vocabularies and len(self.vocabularies) == 0

    def add_option(self):
        pass

    def browse(self,_url):
        webbrowser.open_new_tab(_url)

    def browse_image(self):
        _url = 'https://www.google.com/search?q={}&sxsrf=ALeKk03EFAl6_PKISQWrTKI0BXCHyhL6oA:1626692109365&source=lnms&tbm=isch&sa=X&ved=2ahUKEwi5ltmq_O7xAhXQ7XMBHYLJDfUQ_AUoAXoECAEQAw&biw=1137&bih=730'
        if(self.browseimg_flag and not self.is_empty() and not self.already_browse):
            self.already_browse = True
            self.browse(_url.format(self.vocabulary.english))


    def sound_english(self):
        if(self.speaken_lag and not self.is_empty()):
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)
            engine.say(self.vocabulary.english)
            engine.runAndWait()

    def sound_vietnamese(self):
        if(self.speakvi_lag and not self.is_empty()):
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[2].id)
            engine.say(self.vocabulary.vietnamese)
            engine.runAndWait()


    def main_loop(self):
        self.sound_english()
        self.sound_vietnamese()
        self.browse_image()

#
#                COMMAND LIST
#
    def next_word(self,args):
        self.already_browse = False
        self.current_index = self.current_index + 1 if self.current_index < len(self.vocabularies)-1 else len(self.vocabularies)-1
        self.current_vocabulary()

    def pre_word(self,args):
        self.already_browse = False
        self.current_index = self.current_index - 1 if self.current_index > 0 else 0
        self.current_vocabulary()

    def toggle_speak_english_flag(self,args):
        self.speaken_lag = not self.speaken_lag


    def toggle_speak_vietnamese_flag(self,args):
        self.speakvi_lag = not self.speakvi_lag


    def export_web(self,args):
        words = self.vocabularies
        f = open('revision_web/data.js', 'w',encoding="utf-8")
        f.write('var words =[')
        i=0
        for w in words:
            i = i + 1
            s = '{no:\"'+str(i)+'\",english:\"'+w.english+'\",vietnamese:\"'+w.vietnamese+'\",pronounce:\"'+w.pronounce+'\"}'
            f.write(s)
            if(i<len(words)):
                f.write(',\n')
            else:
                f.write('];')
        f.close()
        input("Exported, enter to continue")
        _url = 'file:///D:/study_english_vocabularies-master/revision_web/index.html'
        self.browse(_url)

    def toggle_browse_image_flag(self,args):
        self.browseimg_flag = not self.browseimg_flag

    def get_vocabularies(self):
        vocabularies = []
        for unit in self.units:
            vocabularies.extend(VocabularyService().get_by_unit(unit))
        return vocabularies
        
    def get_unit_code(self):
        return self.vocabulary.unit_code

    def type_word_vocabulary(self,args):
        if len(args) >= 2:
            if args[0] == 'u':
                self.vocabulary.type_word = ' '.join(args[1:])
            elif args[0] == 'auto':
                self.vocabulary.type_word = eng_to_ipa(self.vocabulary.english)
            self.update_vocabulary()

    def vietnamese_vocabulary(self,args):
        if len(args) >= 2:
            if args[0] == 'u':
                self.vocabulary.vietnamese = ' '.join(args[1:])
                self.update_vocabulary()
            elif args[0] == 'spk':
                self.toggle_speak_vietnamese_flag(args)


    def english_vocabulary(self,args):
        if args[0] == 'u':
            self.vocabulary.english = ' '.join(args[1:])
            self.update_vocabulary()
        elif args[0] == 'spk':
            self.toggle_speak_english_flag(args)
        elif args[0] == 'br':
            self.toggle_browse_image_flag(args)
        elif args[0] == 'camb':
            self.cambridge(args)

    def update_vocabulary(self):
        vocabulary_dao = self.get_vocabulary_dao()
        vocabulary_dao.update(self.vocabulary)
        #self.vocabularies = self.get_vocabularies()

    def extend_info(self,args):
        input(self.vocabulary.description)

    def cambridge(self,args):
        _url = 'https://dictionary.cambridge.org/vi/dictionary/english/{}'
        self.browse(_url.format(self.vocabulary.english))

    def add_command(self):
        self.commands.add_command('-n',self.next_word)
        self.commands.add_command('-p',self.pre_word)
        self.commands.add_command('-en',self.english_vocabulary)
        self.commands.add_command('-vi',self.vietnamese_vocabulary)
        self.commands.add_command('-t',self.type_word_vocabulary)
        self.commands.add_command('-exp',self.export_web)
        self.commands.add_command('-ext',self.extend_info)

    def set_info_display(self,info_display):
        self.info_display = info_display

    def current_vocabulary(self):
        self.vocabulary = self.vocabularies[self.current_index]
        return self.vocabulary

    def get_vocabulary_dao(self):
        return VocabularyDao(Vocabulary(english=self.vocabulary.english,unit_code=self.vocabulary.unit_code))
    
    def get_typing_dao(self):
        return TypingDao(Typing(english=self.vocabulary.english))

    def get_info_display(self):
            return self.base_info()

    def base_info(self):
        infor_menu = InforMenu()
        infor_menu.add_item(ItemInfo('No',self.current_index))
        infor_menu.add_item(ItemInfo('English',self.vocabulary.english,color_value=Color.BLUE2))
        infor_menu.add_item(ItemInfo('Vietnamese',self.vocabulary.vietnamese,color_value=Color.YELLOW2))
        infor_menu.add_item(ItemInfo('Pronounce',self.vocabulary.pronounce))
        infor_menu.add_item(ItemInfo('Type of word',self.vocabulary.type_word))
        infor_menu.add_item(ItemInfo('Right times',self.vocabulary.right_times,color_value=Color.GREEN2))
        infor_menu.add_item(ItemInfo('Wrong times',self.vocabulary.wrong_times,color_value=Color.RED2))
        return infor_menu

    def equals(self):
        return self.user_input.lower() ==  self.vocabulary.english.lower()



    def process_when_right(self):
        self.user_input = ''
        self.vocabulary.right_times = self.vocabulary.right_times + 1
        typing_dao = self.get_typing_dao()
        typing = typing_dao.get_by_ids()
        typing.right_times = self.vocabulary.right_times
        typing_dao.update(typing)

    def process_when_wrong(self):
        self.vocabulary.wrong_times = self.vocabulary.wrong_times + 1
        typing_dao = self.get_typing_dao()
        typing = typing_dao.get_by_ids()
        typing.wrong_times = self.vocabulary.wrong_times
        typing_dao.update(typing)
   
    def process_custom(self):
        if(self.equals()):
            self.process_when_right()
        elif(self.user_input != ''):
            self.process_when_wrong()
        
    
class UnitContext(Menu):

    def __init__(self,title='Enter unit code :',display_info=None,options=None,commands=None):
        super().__init__(title,display_info,options,commands)
        self.units = UnitDao().get_all()
        self.units_choice = set()
        self.current_index = 0
        self.get_current_unit()
        self.info_display = self.get_info_display()
        self.add_option()
        self.add_command()

    def get_current_unit(self):
        self.unit = self.units[self.current_index]
        return self.unit

    def process_custom(self):
        unit = UnitDao(Unit(unit_code=self.user_input)).get_by_ids()
        if(unit):
            self.unit_code = self.user_input
            self.goto_unit_code(self.user_input)
            self.user_input = ''
            self.add_unit_choice([self.unit_code])

    def goto_unit_code(self,unit_code):
        index = 0
        for unit in self.units:
            index = index + 1
            if(unit_code == unit.unit_code):
                break
        self.move_to([index])
        
    def get_info_display(self):
        return self.unit_info()

    def unit_info(self):
        
        list_info = [ItemInfo('No',self.current_index + 1),
                    ItemInfo('Unit code',self.unit.unit_code.upper()),
                    ItemInfo('Unit topic',self.unit.unit_topic.capitalize()),
                    ItemInfo(value='; '.join(self.units_choice),color_value=Color.BLUE2)]

        return InforMenu(list_info)

#          COMMAND LIST

    def next_unit(self,args):
        try:
            step = int(args[0])
        except:
            step = 1

        n = len(self.units)
        self.current_index = self.current_index + step if self.current_index+step <= n-1 else n-1
        self.get_current_unit()

    def pre_unit(self,args):
        try:
            step = int(args[0])
        except:
            step = 1
        self.current_index = self.current_index - step if self.current_index-step >= 0 else 0
        self.get_current_unit()

    def list_unit_lastest(self,args):
        try:
            n = int(args[0])
        except:
            if(len(args) >0 and args[0] == 'a'):
                n = len(self.units)
            else:
                n = 20
        try:
            unit_code = ' '.join(args[1:])
        except:
            unit_code = ''

        Fragment().find_unit(unit_code.upper(),n)
        input('Enter to continue ...')

    def add_unit_choice(self,args):
        if(len(args)==0):
            self.units_choice.add(self.unit.unit_code.upper())
        else:
            for arg in args:
                if(UnitDao(Unit(unit_code=arg)).get_by_ids):
                    self.units_choice.add(arg.upper())

    def remove_unit_choice(self,args):
        try:
            if(len(args)==0):
                self.units_choice.remove(self.unit.unit_code.upper())
            else:
                for arg in args:
                    if(UnitDao(Unit(unit_code=arg)).get_by_ids):
                        self.units_choice.remove(arg.upper())
        except:
            pass

    def move_to(self,args):
        try:
            n = int(args[0])
        except:
            n = 0
        if(0 < n < len(self.units)+ 1):
            self.current_index = n-1
            self.get_current_unit()

    def overview(self,args):
        if(len(args)==0):
            Fragment().general_info()
            input('Enter to continue...')
        elif(args[0]=='d'):
            self.list_unit_lastest(['a',self.unit.unit_code])
        

    def add_command(self):
        self.commands.add_command('-m',self.move_to)
        self.commands.add_command('-n',self.next_unit)
        self.commands.add_command('-p',self.pre_unit)
        self.commands.add_command('-l',self.list_unit_lastest)
        self.commands.add_command('-a',self.add_unit_choice)
        self.commands.add_command('-rm',self.remove_unit_choice)
        self.commands.add_command('-o',self.overview)


#          OPTION LIST
    def study_vocabulary(self):
        if(len(self.units_choice)==0):
            self.print_error("there are not unit any Chose")
        else:
            context = VocabularyContext(self.units_choice)
            context.start()

    def list_file(self):
        mypath = 'import'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        onlyfiles = [f for f in onlyfiles if f.endswith('.csv') and (not FileImportDao(FileImport(file_name=f)).get_by_ids())]
        for file in onlyfiles:
            print(file)
        print()

    def choose_file(self):
        return input('Enter filename: ')

    def save_or_update_file(self,filename):
        FileImportDao(FileImport(file_name=filename)).loader_fileimport()

    def read_file(self,filename):
        try:
            with open('import/'+filename, 'r',encoding='utf-8') as file:
                reader = csv.reader(file)
                idx = 0
                vocabularies = []
                for row in reader:
                    idx = idx + 1
                    if(idx == 1):
                        
                        unit = Unit(unit_code=row[0][1:],unit_topic=row[1])
                    else:
                        while(len(row)<2):
                            row.append('')
                        vocabulary = Vocabulary(english=row[0],vietnamese=','.join(row[1:]))
                        vocabularies.append(vocabulary)
                UnitDao(unit).update_or_save()
                for v in vocabularies:
                    if(v.english !=''):
                        v.unit_code = unit.unit_code
                        result = translate(v.english)
                        print(v.english,' >>> ',result)
                        if(v.vietnamese == ''):
                            v.vietnamese = result[0]
                        if(v.type_word == 'Undefined' and result[1] != ''):
                            v.type_word = result[1]
                        VocabularyDao(v).update_or_save()
                self.save_or_update_file(filename)
            input("Enter to continue...")
        except FileNotFoundError as e:
            input(e)
        except Exception as e:
            input(e)

    def import_csv(self):
        self.list_file()
        filename = self.choose_file()
        self.read_file(filename)

    def add_option(self):
            self.options.append(Option('study vocabulary',self.study_vocabulary))
            self.options.append(Option('import file',self.import_csv))
            pass

    