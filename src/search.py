from bs4 import BeautifulSoup
import urllib.request
import eng_to_ipa as ipa
def search(word):
    #word = 'accept'
    pronounce = ipa.convert(word)
    word = word.replace(' ','+')
    response = urllib.request.urlopen('https://vdict.com/word?word='+word+'&select-dictionary=1')
    html = response.read()
    #print(html)
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(strip=True)
    try:
        pronounce = soup.select_one('.pronounce').string
    except:
        pass
    #print('pronounce',pronounce.string)
    result = soup.select('.phanloai, .list1, .list2')
    #print(f"Print the title: {len(result)} ")
    description = ''
    for r in result:
        try:
           # print('tag === ',r['class'][0])
            if(r.has_attr('class') and r['class'][0] == 'phanloai'):
                description = description + '\n'+ r.string + ': \n'
            elif(r.has_attr('class') and r['class'][0] == 'list1'):
                tag = str(r.select_one('li b').string)
                if (tag != 'None'):
                    description = description+ '-'+tag +'\n '
            elif(r.has_attr('class') and r['class'][0] == 'list2'):
                ul = r.select('.list2 li')
                if(len(ul) > 0):
                   for li in ul:
                    description = description+'>>>'+ li.select_one('.example-original').string +'\n '
                    description = description+ '('+li.contents[2] +')\n '
                           
                           
        except:
            pass
         #for r in result.contents:
    #print(description)

    synonymous  = ''
    antonym = ''
    relatedWord = soup.select('.relatedWord .list1 li')
    #print(len(relatedWord))
    for rr in relatedWord:
        strong = rr.select_one('strong')
        title = strong.contents[0].string
        if(str(title).startswith('Từ đồng nghĩa')):
            words = rr.select('a')
            for w in words:
                #print(word.string)
                try:
                    synonymous = synonymous + w.string + '; '
                except:
                    print('w = ',w,'\n>>type w =',type(w))
        if(str(title).startswith('Từ trái nghĩa')):
            words = rr.select('a')
            for w in words:
                #print(word.string)
                try:
                    antonym = antonym + w.string + '; '
                except:
                    print('w = ',w,'\n>>type w =',type(w))
        #if(stron)
        #relationWord = relationWord + rr.select_one('strong').string + ':\n'

   # print('Từ đồng nghĩa',synonymous)
    #print('Từ trái nghĩa',antonym)
    
    return [str(pronounce),description,synonymous,antonym]