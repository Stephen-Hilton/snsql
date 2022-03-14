txt = """
chart BAR 'Account Health by Region - ARR ($M)' 
 Region     as x(label=null)
,sum(ARR)   as y(stacked='Health', format='$0.0M'
				 ,order=('green','yellow','red','black','unclassified') 
				 ,color=('green','yellow','#ff0000','black','grey'))
from file('somefile.csv')
legend (x=120, y=80, border=(backcolor='grey', color='black', style='solid'))
body(style='bod', width=12, height=6)
order by Region
;
"""

import logging as log
log.basicConfig(encoding='utf-8', format='%(asctime)s--%(levelname)s:%(message)s', level=log.DEBUG)
log.info('logging setup')


def getbetween2(txt:str, delimchars:str="()", posStart:int=0, posEnd:int=None):
    startchar = delimchars[:1]
    endchar = startchar if len(delimchars)<2 else delimchars[1:2]
    posEnd = len(txt) if posEnd is None else posEnd 
    pos1 = txt.find(startchar,posStart,posEnd)+1

    # deal with nestable delimiters:
    nestable = ['(', ')', '{', '}' ]
    if startchar in nestable and endchar in nestable:
        nests = 1
        charcount = pos1
        for c in txt[pos1:posEnd]:
            tester = txt[charcount-5:charcount]
            if c == startchar: 
                nests +=1
            if c == endchar: 
                nests -=1
                if nests <= 0: 
                    pos2 = charcount       
                    break
            charcount +=1            
    else:
        pos2 = txt.find(endchar, pos1)

    # deal with double-character escapes:
    double_escapes = ["'", '"']
    if txt[pos2+1:pos2+2] == endchar and (startchar in double_escapes and endchar in double_escapes):
        pos2 = txt.find(endchar, pos2+2)
        txt = txt[pos1:pos2].replace(endchar*2, endchar)
    else:
        txt = txt[pos1:pos2]

    # deal with no starting character found:
    if pos1 == 0:
        txt = ''
        pos2 = 0

    # deal with no ending character found:
    if pos2==-1: pos2 = posEnd

    return (txt, pos1, pos2)
    


print(txt[85:251])
print(getbetween2(txt, "()", 90))