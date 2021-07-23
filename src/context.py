import csv
from src.query_util import QueryBuilder
import webbrowser
from os import execlp, listdir
from os.path import isfile, join
from goslate import Goslate as gs
import re
import eng_to_ipa
import pyttsx3

from src.constant import Color
from src.dao import AntonymDao, ExampleDao, FileImportDao, StatisticsDao, SynonymousDao, TypingDao, UnitDao, VocabularyDao
from src.fragment import Fragment
from src.menu import InforMenu, ItemInfo, Menu, Option
from src.model import Antonym, Example, FileImport, Synonymous, Typing, Unit, Vocabulary
from src.service import VocabularyService
from src.stuff_util import get_or_default, high_light, translate


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
        self.current_item = self.current_vocabulary()
        self.speaken_lag = speaken_lag
        self.speakvi_lag = speakvi_lag
        self.browseimg_flag = browseimg_flag
        self.camb_flag = False
        self.oxford_flag = False
        self.hellochao_flag = False
        self.revision = False
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
            self.browse(_url.format(self.current_item.english))


    def sound_english(self):
        if(self.speaken_lag and not self.is_empty()):
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)
            engine.say(self.current_item.english)
            engine.runAndWait()

    def sound_vietnamese(self):
        if(self.speakvi_lag and not self.is_empty()):
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[2].id)
            engine.say(self.current_item.vietnamese)
            engine.runAndWait()


    def main_loop(self):
        self.sound_english()
        self.sound_vietnamese()
        self.browse_image()
        if(self.camb_flag and not self.already_browse):
            self.already_browse = True
            self.cambridge(self.current_item.english)
        if(self.oxford_flag and not self.already_browse):
            self.already_browse = True
            self.oxford(self.current_item.english)
        if(self.hellochao_flag and not self.already_browse):
            self.already_browse = True
            self.hello_chao(self.current_item.english)

#
#                COMMAND LIST
#
    def next_word(self,args):
        self.already_browse = False
        if(len(args)>0):
            try:
                n = int(args[0])
            except:
                n = 0
            self.current_index = self.current_index + n if self.current_index + n <= len(self.vocabularies)-1 else len(self.vocabularies)-1
        else:
            self.current_index = self.current_index + 1 if self.current_index + 1 <= len(self.vocabularies)-1 else len(self.vocabularies)-1
        self.current_vocabulary()

    def pre_word(self,args):
        self.already_browse = False
        if(len(args)>0):
            try:
                n = int(args[0])
            except:
                n = 0
            self.current_index = self.current_index - n if self.current_index - n >= 0 else 0
        else:
            self.current_index = self.current_index - 1 if self.current_index - 1 >= 0 else 0
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
        return self.current_item.unit_code

    def type_word_vocabulary(self,args):
        if len(args) >= 2 and args[0] == 'u':
                vocabulary_dao = self.get_vocabulary_dao()
                vocabulary = vocabulary_dao.get_by_ids()
                self.current_item.type_word = ' '.join(args[1:])
                vocabulary.type_word = self.current_item.type_word
                self.update_vocabulary(vocabulary)

    def pronoun_vocabulary(self,args):
        if len(args) >= 2 and args[0] == 'u':
                typing_dao = self.get_typing_dao()
                typing = typing_dao.get_by_ids()
                self.current_item.pronounce = ' '.join(args[1:])
                typing.pronounce = self.current_item.pronounce
                self.update_typing(typing)

    def vietnamese_vocabulary(self,args):
        if len(args) >= 2:
            if args[0] == 'u':
                vocabulary_dao = self.get_vocabulary_dao()
                vocabulary = vocabulary_dao.get_by_ids()
                self.current_item.vietnamese = ' '.join(args[1:])
                vocabulary.vietnamese = self.current_item.vietnamese 
                self.update_vocabulary(vocabulary)
            elif args[0] == 'spk':
                self.toggle_speak_vietnamese_flag(args)


    def english_vocabulary(self,args):
        if args[0] == 'u':
            vocabulary_dao = self.get_vocabulary_dao()
            vocabulary = vocabulary_dao.get_by_ids()
            english = ' '.join(args[1:])
            vocabulary.english = english
            self.update_vocabulary(vocabulary)
            self.vocabularies = self.get_vocabularies()
        elif args[0] == 'spk':
            self.toggle_speak_english_flag(args)
        elif args[0] == 'br':
            self.toggle_browse_image_flag(args)
        elif args[0] == 'camb':
            self.cambridge(args)
        elif args[0] == 'oxford':
            self.oxford(args)

    def update_typing(self,typing):
        typing_dao = self.get_typing_dao()
        typing_dao.update(typing)

    def update_vocabulary(self,vocabulary):
        vocabulary_dao = self.get_vocabulary_dao()
        vocabulary_dao.update(vocabulary)
        self.current_vocabulary()
        #self.vocabularies = self.get_vocabularies()

    def extend_info(self,args):
        if(len(args)>0):
            if(args[0]=='d'):
                input(self.current_item.description)
            elif(args[0]=='unit'):
                input(self.current_item.unit_code)
            elif(args[0]=='vi'):
                input(self.current_item.vietnamese_studied)
            else:
                print('d(description)\nunit(unit_code)\nunits(units_contain)\nvi(vietnamese_studied)\nsyn(synonymous)\nan(antonym)\nhom(homonym)\n')
                input('Enter to continue')


    def cambridge(self,args):
        try:
            _url = 'https://dictionary.cambridge.org/vi/dictionary/english/{}'
            self.browse(_url.format(self.current_item.english.replace(" ","-")))
        except Exception as e:
            input(e)
        

    def oxford(self,args):
        try:
            _url = 'https://www.oxfordlearnersdictionaries.com/definition/english/hello_1?q={}'
            self.browse(_url.format(self.current_item.english.replace(" ","+")))
        except Exception as e:
            input(e)
            
    def hello_chao(self,args):
        try:
            _url = 'https://www.hellochao.vn/tu-dien-tach-ghep-am/?act=search&type=word&sct={}'
            self.browse(_url.format(self.current_item.english.replace(" ","+")))
        except Exception as e:
            input(e)

    def revision_mode(self,args):
        if(self.revision):
            self.revision = False
        else:
            self.revision = True
            self.speaken_lag = False

    def update_extend(self,args):
        try:
            # typing_dao = self.get_typing_dao()
            # typing = typing_dao.get_by_ids()
            if(args[0]=='syn'):
                synonymous_dao = self.get_synonymous_dao()
                synonymities = ' '.join(args[1:]).split('; ')
                for syn in synonymities:
                    synonymous_dao.query.object_origin.syn_english = syn
                    synonymous_dao.save()
                    synonymous_dao.query = QueryBuilder( Synonymous(english=syn,syn_english=self.current_item.english),['english','syn_english'])
                    synonymous_dao.save()
            elif(args[0]=='-syn'):
                synonymous_dao = self.get_synonymous_dao()
                synonymities = ' '.join(args[1:]).split('; ')
                for syn in synonymities:
                    synonymous_dao.query.object_origin.syn_english = syn
                    synonymous_dao.delete_by_ids()
                    synonymous_dao.query = QueryBuilder( Synonymous(english=syn,syn_english=self.current_item.english),['english','syn_english'])
                    synonymous_dao.delete_by_ids()
            elif(args[0]=='an'):
                antonym_dao = self.get_antonym_dao()
                antonym = ' '.join(args[1:]).split('; ')
                for an in antonym:
                    antonym_dao.query.object_origin.an_english = an
                    antonym_dao.save()
                    antonym_dao.query =  QueryBuilder(Antonym(english=an,an_english=self.current_item.english),['english','an_english'])
                    antonym_dao.save()
            elif(args[0]=='-an'):
                antonym_dao = self.get_antonym_dao()
                antonym = ' '.join(args[1:]).split('; ')
                for an in antonym:
                    antonym_dao.query.object_origin.an_english = an
                    antonym_dao.delete_by_ids()
                    antonym_dao.query =  QueryBuilder(Antonym(english=an,an_english=self.current_item.english),['english','an_english'])
                    antonym_dao.delete_by_ids()
        except KeyError:
                pass

    def delete_word(self,args):
        vocabulary_dao = self.get_vocabulary_dao()
        vocabulary_dao.delete_by_ids()
        self.vocabularies = self.get_vocabularies()

    def reload(self):
        self.vocabularies = self.get_vocabularies()

    def add_command(self):
        self.commands.add_command('-n',self.next_word)
        self.commands.add_command('-p',self.pre_word)
        self.commands.add_command('-reload',self.reload)
        self.commands.add_command('-en',self.english_vocabulary)
        self.commands.add_command('-vi',self.vietnamese_vocabulary)
        self.commands.add_command('-t',self.type_word_vocabulary)
        self.commands.add_command('-pr',self.pronoun_vocabulary)
        self.commands.add_command('-exp',self.export_web)
        self.commands.add_command('-typing',self.extend_info)
        self.commands.add_command('-exa',self.example)
        self.commands.add_command('-revision',self.revision_mode)
        self.commands.add_command('-ext',self.update_extend)
        self.commands.add_command('-delete',self.delete_word)
        self.commands.add_command('-camb',self.toggle_camb)
        self.commands.add_command('-oxford',self.toggle_oxford)
        self.commands.add_command('-hellochao',self.toggle_hellochao)

    def toggle_camb(self,args):
        self.camb_flag = not self.camb_flag
    
    def toggle_oxford(self,args):
        self.oxford_flag = not self.oxford_flag

    def toggle_hellochao(self,args):
        self.hellochao_flag = not self.hellochao_flag

    def example(self,args):
        if(len(args)>1):
            if args[0] == 'a':
                sentence = ' '.join(args[1:])
                ExampleDao(Example(english=self.current_item.english,example=sentence)).update_or_save()
            elif args[0] == 'rm':
                sentence = ' '.join(args[1:])
                ExampleDao(Example(english=self.current_item.english,example=sentence)).delete_by_example(sentence)
        else:
            examples = ExampleDao(Example()).get_by_english(english=self.current_item.english)
            for example in examples:
                print('>>> ',example.example)
            input('Enter to continue!')

    def set_info_display(self,info_display):
        self.info_display = info_display

    def current_vocabulary(self):
        self.current_item = self.vocabularies[self.current_index]
        return self.current_item

    def get_vocabulary_dao(self):
        return VocabularyDao(Vocabulary(english=self.current_item.english,unit_code=self.current_item.unit_code))
    
    def get_typing_dao(self):
        return TypingDao(Typing(english=self.current_item.english))

    def get_synonymous_dao(self):
        return SynonymousDao(Synonymous(english=self.current_item.english))

    def get_antonym_dao(self):
        return AntonymDao(Antonym(english=self.current_item.english))

    def get_info_display(self):
            if(self.revision):
                return self.revion_mode()
            return self.base_info()
    def colorize(self,sentence):
        english = self.current_item.english
        sentence = sentence.replace(english,high_light(english,Color.BEIGE2))
        return sentence.replace(english.capitalize(),high_light(english.capitalize(),Color.BEIGE2))

    def base_info(self):
        examples = [self.colorize(example.example) for example in ExampleDao(Example()).get_by_english(english=self.current_item.english)]
        synonymous = [synonymous.syn_english for synonymous in SynonymousDao(Synonymous()).get_by_english(self.current_item.english)]
        antonym = [antonym.an_english for antonym in AntonymDao(Antonym()).get_by_english(self.current_item.english)]
        unit_contains = [v.unit_code for v in VocabularyDao(Vocabulary()).get_by_english(self.current_item.english)]
        vietnamese_studied = [v.vietnamese.lower() for v in VocabularyDao(Vocabulary()).get_by_english(self.current_item.english)]
        vietnamese = []
        for vi in vietnamese_studied:
            for v in re.split('[\.|\,|\;]',vi):
                vietnamese.append(v.strip())
        vietnamese = set(vietnamese)
        infor_menu = InforMenu()
        infor_menu.add_item(ItemInfo('No',str(self.current_index+1)+'/'+ str(len(self.vocabularies)),Color.VIOLET2))
        infor_menu.add_item(ItemInfo('English',self.current_item.english,Color.VIOLET2,Color.BLUE2))
        infor_menu.add_item(ItemInfo('IPA',self.current_item.pronounce,Color.VIOLET2))
        infor_menu.add_item(ItemInfo('Label',self.current_item.type_word,Color.VIOLET2))
        infor_menu.add_item(ItemInfo('Translated',self.current_item.vietnamese,Color.VIOLET2,Color.YELLOW2))
        infor_menu.add_item(ItemInfo('Example','\n'.join(examples),Color.VIOLET2,Color.ITALIC))
        infor_menu.add_item(ItemInfo('Synonymous','; '.join(synonymous),Color.VIOLET2,Color.YELLOW2))
        infor_menu.add_item(ItemInfo('Antonym','; '.join(antonym),Color.VIOLET2,Color.BEIGE2))
        infor_menu.add_item(ItemInfo('Unit','; '.join(unit_contains),Color.VIOLET2,Color.BLINK2))
        infor_menu.add_item(ItemInfo('Mean other','; '.join(vietnamese),Color.VIOLET2,Color.YELLOW2))
        infor_menu.add_item(ItemInfo('RTS',self.current_item.right_times,Color.VIOLET2,Color.GREEN2,inline_flag=True))
        infor_menu.add_item(ItemInfo('WTS',self.current_item.wrong_times,Color.VIOLET2,Color.RED2))
        
        return infor_menu

    def revion_mode(self):
        infor_menu = InforMenu()
        infor_menu.add_item(ItemInfo('No',self.current_index+1,Color.VIOLET2))
        infor_menu.add_item(ItemInfo('English','**********',Color.VIOLET2,Color.BLUE2))
        infor_menu.add_item(ItemInfo('Translated',self.current_item.vietnamese,Color.VIOLET2,Color.YELLOW2))
        infor_menu.add_item(ItemInfo('Pronounce','********'))
        infor_menu.add_item(ItemInfo('Lable',self.current_item.type_word,Color.VIOLET2))
        infor_menu.add_item(ItemInfo('RTS',self.current_item.right_times,Color.VIOLET2,Color.GREEN2))
        infor_menu.add_item(ItemInfo('WTS',self.current_item.wrong_times,Color.VIOLET2,Color.RED2))
        return infor_menu

    def equals(self):
        return self.current_item.english.lower() in  self.user_input.lower().split(' ')



    def process_when_right(self):
        self.user_input = ''
        self.current_item.right_times = self.current_item.right_times + 1
        typing_dao = self.get_typing_dao()
        typing = typing_dao.get_by_ids()
        typing.right_times = self.current_item.right_times
        typing_dao.update(typing)

    def process_when_wrong(self):
        self.current_item.wrong_times = self.current_item.wrong_times + 1
        typing_dao = self.get_typing_dao()
        typing = typing_dao.get_by_ids()
        typing.wrong_times = self.current_item.wrong_times
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

    def is_complete(self):
        results = StatisticsDao().search_unit(self.unit.unit_code,len(self.units))
        if(len(results)>0):
            result = results[0][0]
            res =  result.split('/')
            return res[0]==res[1]
        return False

    def unit_info(self):
        color = Color.DEFAULT
        if(self.is_complete()):
            color = Color.GREEN2
        list_info = [ItemInfo('No',self.current_index + 1,color_key=color,color_value=color),
                    ItemInfo('Unit code',self.unit.unit_code.upper(),color_key=color,color_value=color),
                    ItemInfo('Unit topic',self.unit.unit_topic.capitalize(),color_key=color,color_value=color),
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
                        
                        unit = Unit(unit_code=row[0],unit_topic=row[1])
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
                        if(v.vietnamese == ''):
                            v.vietnamese = result[0] if result[0] != '' else gs().translate(v.english,'vi')
                        if(v.type_word == 'Undefined' and result[1] != ''):
                            v.type_word = result[1]
                        print(v.english,' >>> ',v.vietnamese,'(',v.type_word,')')
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

    