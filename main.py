from src.query_word import *
from src.import_excel import *
from src.config import *
from src.constant import *

from os import system
import random
from termcolor import colored
import pyttsx3
import eng_to_ipa as ipa

import webbrowser

dash ="=============================================================="
dashln =dash+"\n"
session_word = []

def sound(english):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices");
    engine.setProperty('rate', 125)  
    engine.setProperty("voice",voices[0].id)
    engine.say(english)
    engine.runAndWait()

def soundVN(vietnamese):
    engine2 = pyttsx3.init()
    voices = engine2.getProperty("voices");
    engine.setProperty('rate', 100)  
    engine2.setProperty("voice",voices[2].id)
    engine2.say(vietnamese)
    engine2.runAndWait()
    
def ok():
    sound("Good")
    print(colored('OK', 'green'))
    print(dashln)

def wrong():
    sound("write again")
    print(colored('WRONG', 'red'))

def high_light(word,senence,color):
    if senence == None:
        result = color+word+CEND
    else:
        result = senence.replace(word,color+word+CEND)
        result = senence.replace(word.lower(),color+word.lower()+CEND)
    return result

def main_menu():
    print(dash)
    print("---------------HACKNAO1500---------------")
    print(dashln)
    print("[1]. Update vocabulary!")
    print("[2]. Study vocabulary!")
    print("[3]. Revise vocabulary!")
    print("[4]. split words in paragraph!")
    print("[5]. split sentences paragraph!")
    print("\n[0]. Exit!")
    print("-----------------------------------------\n")

def update_vocabulary():
    loc="LanguageLearning.xlsx"
    import_excel(loc)

def sub_menu2():
    print(dash)
    print("-----------2.STUDY VOCABULARY------------")
    print(dashln)
    print("[1]. Unit!")
    print("[2]. Total_times!")
    print("[3]. Fail_ratio!")

    print("\n[0]. Return HACKNAO1500!")
    print(dashln)
def reset_menu(menu):
    system("cls")
    if(menu == "main_menu"):
        main_menu()
    elif(menu == "sub_menu2"):
        sub_menu2()

def vocabularies_of_unit():
    while True:
        command = input(">>> command/unit_code: ")
        unit_code = command
        if (command == "-h"):
            print("\nOption h/help l/list")
        elif (command == "-l"):
            units = get_all_unit()
            i = 0
            for u in units:
                i +=1
                if (i % 15 == 0):
                    input(">>> Enter to continue!")
                print("\n",u.unit_code," ===> ",u.unit_topic)
        elif (get_by_unit(unit_code) != None):
            return get_by_unit(unit_code)
        elif (command == '-q' or command == "-quit"):
            reset_menu("sub_menu2")
            break
        elif (get_one_unit(unit_code) == None):
            print("\nunit code not found!")
        else:
            return get_vocabularies()
    return None



def vocabularies_of_total_times():
    print("vocabulary of total times")

def vocabularies_of_fail_ratio():
    print("vocabulary of ratio")

def check_read(list_words):
    system("cls")
    print("========== CHECK READ ================")
    for w in list_words:
        print("[",w.order,"].",high_light(w.english,None,CGREEN2)," >>> ",high_light(w.vietnamese,None,CYELLOW2))
    input("Enter to continue ...")
    random.shuffle(list_words)
    list_wrong_words = []

    for w in list_words:
        print("[",w.order,"]. CHECK READ")
        print("English: ?")
        print("Type: ",w.type_word)
        print("VietNamese: ",w.vietnamese)
        print("Example: ",high_light(w.vietnamese,w.sentent_vietnamese,CYELLOW2))
        print(dash)

        input_word = input(">>> ")
        if(input_word == "-q" or input_word == "-quit"):
            list_wrong_words = []
            break
        elif (input_word == "-w" or input_word == "-wrong"):
            break
        elif (input_word == "-expw" or input_word == "-export_web"):
            export_web(list_words)
            input("export web successful!, enter to continue...")
            break
        elif (input_word == "-expc" or input_word == "-export_csv"):
            export_csv(list_words)
            input("export csv successful!, enter to continue...")
            break
        if(input_word.lower() == w.english.lower()):
            print("English: "+high_light(w.english,None,CBLUE2))
            ok()
            increment_right_times(w.english)
            sound(w.english)
            soundVN(w.vietnamese)          
        else:
            list_wrong_words.append(w)
            print("English: "+high_light(w.english,None,CRED2))
            increment_wrong_times(w.english)
            wrong()

    return list_wrong_words

def check_listen(list_words):
    system("cls")
    print("========== CHECK LISTEN ================")
    for w in list_words:
        print("[",w.order,"].",high_light(w.english,None,CGREEN2)," >>> ",high_light(w.vietnamese,None,CYELLOW2))
    input("Enter to continue ... ")
    random.shuffle(list_words)
    list_wrong_words = []
    for w in list_words:
        print("[",w.order,"]. CHECK LISTEN")
        print("English: ?")
        print(dash)
        sound(w.english)
        soundVN(w.vietnamese)
        input_word = input(">>> ")

        if(input_word== "-q" or input_word == "-quit"):
            return []
        if(input_word.lower() == w.english.lower()):
            print("English: "+high_light(w.english,None,CBLUE2))
            print("VietNamese: ",high_light(w.vietnamese,None,CYELLOW2))
            ok()
            increment_right_times(w.english)
        else:
            list_wrong_words.append(w)
            print("English: "+high_light(w.english,None,CRED2))
            wrong()
            increment_wrong_times(w.english)
    return list_wrong_words

def getListWord(list_words):
    list_idx = []
    try:
        indexs = input("Enter/index to Continue...")
        list_index = indexs.split(",");
        for idxs in list_index:
            lst_idx = idxs.split("-")
            if(len(lst_idx)>1) :
                for i in range(int(lst_idx[0]),int(lst_idx[1])+1):
                        list_idx.append(int(i))
            elif(lst_idx[0]!=""):
                list_idx.append(int(lst_idx[0]))
        words = []
        for w in list_words:
            if(w.order in list_idx):
                words.append(w)
        if(len(words)>0):
            list_words = words
    except:
        pass
    return list_words
def printWordList(list_words):
     for w in list_words:
        print("[",w.order,"].",high_light(w.english,None,CGREEN2)," >>> ",high_light(w.vietnamese,None,CYELLOW2))

def check_again(list_words):
    system("cls")
    printWordList(list_words)
    list_words = getListWord(list_words)

    lst_words_wrong = check_read(list_words)
    while len(lst_words_wrong) > 0 :
        lst_words_wrong = check_read(lst_words_wrong)
    lst_words_wrong = check_listen(list_words)
    while len(lst_words_wrong) > 0 :
        lst_words_wrong = check_listen(lst_words_wrong)

def additional_words(list_words):
    lst_words_wrong = check_read(list_words)
    while len(lst_words_wrong) > 0 :
        lst_words_wrong = check_read(lst_words_wrong)
        

def word_info(word):
    system("cls")
    print("[",word.order,"]. STUDY VOCABULARY ")
    print("English: ",high_light(word.english,None,CBLUE2))
    print("Vietnamese: ",high_light(word.vietnamese,None,CYELLOW2))
    print("Pronunce: /",word.pronounce,"/")
    print("Type: ",TYPE_WORD[word.type_word])
    print("Example: ",high_light(word.english,word.sentent_english,CBLUE2))
    print("IPA:    /",ipa.convert(word.sentent_english),"/")
    print("Mean: ",high_light(word.vietnamese,word.sentent_vietnamese,CYELLOW2))

    print("\nRight times: ",colored(word.right_times, 'green'))
    print("Wrong times: ",colored(word.wrong_times, 'red'))
    print(dash)

def study_word(word):
    while True:
        word_info(word)
        input_word = input(">>> ")
        if(input_word.startswith("-")):
            if((input_word == "-n" or input_word == "-next")
                or (input_word == "-p" or input_word == "-prefix")
                or (input_word == "-nn" or input_word == "-nextnot")
                or (input_word == "-q"or input_word == "-quit")
                or (input_word.startswith("-j"))
                or (input_word.startswith("-ja"))
                or (input_word == "-u" or input == "-update")
                or (input_word == "-br" or input == "-browse")):
                return input_word
            elif(input_word == "-cl"or input_word == "-clear"):
                global session_word
                session = []
            elif(input_word == "-ch"or input_word == "-check"):
                check_again([word])
            elif(input_word.startswith("-cha")):
                session_word.append(word)
                session_word = list(set(session_word))
                session_word.sort(key=orderWord)
                nearestAmount = input_word[4:]
                startNumber = 0;
                if('' != nearestAmount):
                    startNumber =  -int(nearestAmount)
                check_again(session_word[startNumber:])# make list to unique
            elif(input_word.startswith("-expw")):
                session_word.append(word)
                session_word = list(set(session_word))
                session_word.sort(key=orderWord)
                nearestAmount = input_word[5:]
                startNumber = 0;
                if('' != nearestAmount):
                    startNumber =  -int(nearestAmount)
                export_web(session_word[startNumber:])
                input("export web successful!, enter to continue...")
            elif(input_word == "-h"or input_word == "-help"):
                print("-n/-next : next word and save into session")
                print("-nn/-nextnot : next word and not save into session")
                print("-p/-prefix: prefix word")
                print("-j/-jump<order>: go to order word")
                print("-ch/-check : check current word and save it into session")
                print("-cha/-checkall : next all words in session")
                print("-expw/-exportweb : export vocabularies in web")
                print("-q/-quit : quit study vocabularies")
                print("-h/-help : show all command")
                input("Enter to continue...")
            else:
                input("Command not found...")
        else:
            if (input_word.lower() == word.english.lower()):
                word.right_times += 1
                increment_right_times(word.english)
                print("Vietnamese: ",colored(word.vietnamese, 'yellow'))
                sound(input_word.lower())
                soundVN(word.vietnamese)
            else:
                word.wrong_times +=1
                increment_wrong_times(word.english)
    return input_word

def orderWord(e):
  return e.order

def study_start(vocabularies):
    global session_word
    breakpoint=1
    for v in vocabularies:
        if(v.right_times>0):
            print("[",v.order,"].",high_light(v.english+" >>> "+v.vietnamese,None,CGREEN2))
            breakpoint = v.order;
        else:
            print("[",v.order,"] ",v.english," ===> ",v.vietnamese)
    i = jumpOrder(vocabularies,breakpoint);
    input("Enter to continue...")
    #random.shuffle(vocabularies)
    while True:
        word_info(vocabularies[i])
        sound(vocabularies[i].english)
        input_word = study_word(vocabularies[i])
        if(input_word == "-n" or input_word == "-next"):
            session_word.append(vocabularies[i])
            session_word = list(set(session_word))
            if(i<len(vocabularies)-1):
                i += 1
        elif(i<len(vocabularies) and (input_word == "-nn" or input_word == "-nextnot")):
            i += 1
        elif(i>0 and (input_word == "-p" or input_word == "-prefix")):
            i -= 1
        elif(input_word == "-br" or input == "-browse"):
            browser_image(vocabularies[i].english)
        elif(input_word.startswith("-ja")):
            try:
                idx = int(input_word[3:])
                i = jumpOrder(vocabularies,idx);
            except:
                pass

        elif(input_word.startswith("-j")):
            try:
                i = int(input_word[2:]) - 1
            except:
                pass
        elif (input_word == "-u" or input_word == "-update"):
            update_vocabulary()
            vocabularies = get_vocabularies()
        elif(input_word == "-q"or input_word == "-quit"):
            reset_menu("sub_menu2")
            break

def jumpOrder(vocabularies,idx):
    global session_word
    session_word = []
    count = 0
    for v in vocabularies:
        if(v.order<=idx):
            count += 1
            session_word.append(v)
    return count - 1
    session_word = list(set(session_word))

def study_vocabulary():
    sub_option = -1
    while sub_option != 0:
        if(sub_option == 1):
            vocabularies = get_vocabularies()
            if(vocabularies != None):
                if(len(vocabularies) > 0):
                    study_start(vocabularies)
                else:
                    print("Not any vocabulary!")
                    reset_menu("sub_menu2")
        elif (sub_option == 2):
            vocabularies_of_total_times()
        elif (sub_option == 3):
            vocabularies_of_fail_ratio()
        else:
            reset_menu("sub_menu2")
        try:
            sub_option = int(input(">>> Your choice: "))
        except:
            sub_option = -1
    reset_menu("main_menu")

def get_vocabularies():
    global session_word
    session_word = []
    # get all unit
    units = get_all_unit()
    for i in range(len(units)):
        print("["+str(i+1)+"]     Code:",units[i].unit_code,"     Topic:",units[i].unit_topic)

    print("\n 0 >>>If you want quit!")
    # get chooses
    chooses = input("input choose: ")
    if(chooses.startswith("0")):
        return
    u_list = []
    for u in chooses.split(","):
        us = u.split("-")
        if len(us)>1 :
            try:
                start = int(us[0])
                end = min(int(us[1])+1,len(units)+1)
                for i in range(start,end):
                    u_list.append(i)
            except:
                pass
        else:
             u_list.append(u)

    # get unit code list

    unit_code_list = []
    for i in u_list:
        try:
            idx = int(i)-1
            unit_code_list.append(units[idx].unit_code)
        except:
            pass

    # get vocabularies
    vocabularies = []
    for uc in unit_code_list:
        vocabularies.extend(get_by_unit(uc))
    return vocabularies

def revise_vocabulary():
    vocabularies = get_vocabularies()
    # revise
    lst_words_wrong = check_read(vocabularies)
    while len(lst_words_wrong) > 0 :
        lst_words_wrong = check_read(lst_words_wrong)

def main():
    global session_word
    session_word=[]
    option = -1
    while (option != 0):
        if (option == 1):
            update_vocabulary()
        elif (option == 2):
            study_vocabulary()
        elif (option == 3):
            revise_vocabulary()
        elif (option == 4):
            split_words()
        elif (option == 5):
            split_sentences()
        try:
            reset_menu("main_menu")
            option = int(input(">>> Your choice: "))
        except:
            option = -1
def browser_image(word):
    webbrowser.open("https://www.google.com/search?q=\""+word+"\"&sxsrf=ALeKk0012V3QswvLOJdsl0NmnJiMQsCMKQ:1625965767100&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj0yNu_6tnxAhXKWisKHVbBCTkQ_AUoAXoECAEQAw",new = 0,autoraise=True)
    
def export_data(words):
    f = open('static/data.js', 'w',encoding="utf-8")
    f.write('var words =[')
    i=0
    for w in words:
        i +=1
        s = '{no:\"'+str(w.order)+'\",english:\"'+w.english+'\",vietnamese:\"'+w.vietnamese+'\",pronoun:\"'+ipa.convert(w.english)+'\"}'
        f.write(s)
        if(i<len(words)):
            f.write(',\n')
        else:
            f.write('];')
    f.close()
def export_web(words):
    f = open('static/list.js', 'w',encoding="utf-8")
    f2 = open('Toiec1Tool/data.js', 'w',encoding="utf-8")
    f.write('var vocabularies =[')
    f2.write('var words =[')
    i=0
    for w in words:
        i +=1
        s = '{no:\"'+str(w.order)+'\",english:\"'+w.english+'\",vietnamese:\"'+w.vietnamese+'\",pronoun:\"'+ipa.convert(w.english)+'\"}'
        f.write(s)
        f2.write(s)
        if(i<len(words)):
            f.write(',\n')
            f2.write(',\n')
        else:
            f.write('];')
            f2.write('];')
    f.close()
    f2.close()

def export_csv(words):
    f = open('static/list.csv', 'w',encoding="utf-8")
    i=0
    for w in words:
        i +=1
        s = str(i)+','+w.english+','+w.vietnamese+'\n'
        f.write(s)
    f.close()

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 
from googletrans import Translator 
import goslate
import re

import enchant

def hasNumbers(inputString):
    for w in inputString:
        if w in ['1','2','3','4','5','6','7','8','9','0']:
            return True
    return False

def split_words():
    d = enchant.Dict("en_US")
    basePath = "sample_sentence/"
    basePathWord = "output_word_sample/"
    stop_words_locally = ['.',',','the']
    translator = Translator()
    gs = goslate.Goslate()
    while True:
        fName = input("input file name >>> ")
        outFile = open(basePathWord+fName+".csv", 'w',encoding="utf-8")
        try:
            print("path",basePath+fName+".txt")
            text = open(basePath+fName+".txt", 'r',encoding="utf8").read()
            print("text",text)
            stop_words = set(stopwords.words('english'))
            word_tokens = word_tokenize(text)
            print("word_token",word_tokens)
            filtered_sentence = [w for w in word_tokens if (not w in stop_words) and (len(w) > 1) and (not w.isnumeric())] 
            filtered_sentence = list(set(filtered_sentence))
            filtered_sentence.sort()
            print(filtered_sentence)
            for w in filtered_sentence:
                if (not hasNumbers(w)) and d.check(w) :
                    word = get_one_word(w)
                    if(word == None):
                        en = w
                        try:
                            vi = translator.translate(w,src='en',dest='vi').text
                            if en == vi:
                                vi = gs.translate(en, 'vi')
                                if en == vi:
                                    vi = ""
                            s = en+','+vi+'\n'
                        except:
                            s = w + ", >>>\n"
                        print(s)
                        outFile.write(s) 
            break
        except:
            pass
        outFile.close()
from nltk.tokenize import sent_tokenize
def split_sentences():
    basePath = "sample_sentence/"
    basePathWord = "output_sentences_sample/"
    translator = Translator()
    gs = goslate.Goslate()
    while True:
        fName = input("input file name >>> ")
        outFile = open(basePathWord+fName+".csv", 'w',encoding="utf-8")
        try:
            text = open(basePath+fName+".txt", 'r').read()
            print(text)
            sent_tokens = sent_tokenize(text) 
            print(sent_tokens)
            for s in sent_tokens:
                en = s
                vi = translator.translate(s,src='en',dest='vi').text
                if en == vi:
                    se = en+'\n'
                    # vi = gs.translate(en, 'vi')
                else:
                    se = en+','+vi+'\n' 
                print(se)
                outFile.write(se)
            break
        except:
            pass
        outFile.close()
main()
