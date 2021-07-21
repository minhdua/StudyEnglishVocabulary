
import winsound
from os import system

from src.constant import Color
from src.stuff_util import get_or_default, high_light


class Menu(object):

    def __init__(self,title='New Menu',info_display=None,options=None,commands=None):
        self.title = title
        self.info_display = get_or_default(info_display,InforMenu())
        self.options = get_or_default(options,[])
        self.commands = get_or_default(commands,CommandList())
        self.item_size = 0
        self.input = -1
        self.user_input=''
        self.exit_flag = False

    def show_title(self):
        if self.title == None:
            self.title = 'New Menu'
        print((self.title).upper())

    def get_info_display(self):
        return self.info_display

    def show_info_display(self):
        self.info_display = self.get_info_display()
        self.info_display.show()

    def beep(self):
        winsound.Beep(500,200)

    def show_option(self):
        for option in enumerate(self.options):
            print('[{}]. {}'.format(option[0]+1,option[1].text))

    def add_option(self,option):
        self.options.append(option)

    def process_custom(self):
        pass #

    def process_input_string(self,user_input):
        self.user_input = self.commands.processing(user_input)
        if (self.user_input != ''):
            self.process_custom()

    def print_error(self,message):
        print(high_light(message,Color.RED2),"Enter ...")
        input()

    def process_option(self):
        self.current_option.processing()

    def process_input(self,user_input):
        try:
            input_value = int(user_input)
            if (0 < input_value < len(self.options)+1):
                self.current_option = self.options[input_value-1]
                self.process_option()
            if(input_value == 0) : self.exit_flag = True
        except ValueError:
            self.process_input_string(user_input)

    def clear_menu(self):
            system('cls')

    def main_loop(self):
        pass #cusstom

    def show_input_user(self):
        if(self.user_input != ''):
            self.beep()
            print(high_light(self.user_input,Color.RED2))

    def start(self):
        while(not self.exit_flag):
            self.clear_menu()
            self.show_title()
            self.show_info_display()
            self.show_option()
            self.main_loop()
            self.show_input_user()
            self.input = input('\n>>> ')
            self.process_input(self.input)

class Properties(object):
    MARGIN_LEFT_DEFAULT = 2
    MARGIN_TOP_DEFAULT = 0
    def __init__(self,margin_left=None,margin_top=None):
        self.margin_left=get_or_default(margin_left,self.MARGIN_LEFT_DEFAULT)
        self.margin_top=get_or_default(margin_top,self.MARGIN_TOP_DEFAULT)


class ItemInfo(object):

    def __init__(self,key='>>>',value='',color_key=Color.DEFAULT,color_value=Color.DEFAULT,inline_flag=False):
        self.key = key
        self.value = value
        self.color_key = color_key
        self.color_value = color_value
        self.inline_flag = inline_flag
    def colorize_key(self):
        return high_light(self.key,self.color_key)

    def colorize_value(self):
        return high_light(self.value,self.color_value)

    def format_key(self):
        return '[{}].'.format(self.colorize_key())
    
    def format_value(self):
        return '{}'.format(self.colorize_value())

    def format(self,distance):
        return str('{:'+str(distance*2)+'} {}').format(self.format_key(),self.format_value())

class Option(object):

    def __init__(self,text,func=None):
        self.text = text
        self.func = func

    def processing(self):
        self.func()

class CommandList(object):
    def __init__(self):
        self.commands = {}

    def add_command(self,key,func):
        self.commands[key] = func

    def get_prefix(self,input_string):
        inputs = input_string.split(' ')
        self.args = inputs[1:]
    
        return inputs[0]

    def check_prefix(self,prefix):
        try:
            self.func = self.commands[prefix]
            return True
        except KeyError:
            return False

    def processing(self,input_string):
        prefix = self.get_prefix(input_string)
        if(self.check_prefix(prefix)):
            self.func(self.args)
            return ''
        return input_string

class InforMenu(object):
    max_distance = 1
    item_formart =[]
    def __init__(self,items=None):
        self.items = get_or_default(items,[])
        self.find_max_distance()
        self.margin_left = Properties().margin_left
        self.margin_top = Properties().margin_top
        self.item_flag = {}
        self.format_all_item()

    def update_max_distance(self,item):
        if(len(item.key) > self.max_distance):
                self.max_distance = len(item.key)

    def find_max_distance(self):
        for item in self.items:
            self.update_max_distance(item)

    def format_item(self,item):
        return ' '*self.margin_left + item.format(self.max_distance)

    def add_format_item(self,item):
        self.item_flag[self.format_item(item)] = item.inline_flag
        self.item_formart.append(self.format_item(item))
    
    def format_all_item(self):
        self.clear_format_item()
        for item in self.items:
            self.add_format_item(item)

    def clear_format_item(self):
        self.item_formart=[]

    def add_item(self,item):
        self.items.append(item)
        self.format_all_item()
        self.update_max_distance(item)

    def clear_menu(self):
        system('cls')

    def println(self):
        print('\n'*self.margin_top)

    def exit_message(self):
        print('[0]. Exit')

    def get_item_format(self):
        return self.item_formart

    def show(self):
        if(len(self.item_formart) > 0):
            self.println()
            for item in self.get_item_format():
                if(self.item_flag[item]):
                    print(item,end=' - ')
                else:
                    print(item)
            self.println()
            self.exit_message()


