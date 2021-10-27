breakingchars = [b for b in "()',=; "]
quotechars = ["'", '"']

# preset beginning position
sym = []
i = wordcount = p1 = p2 = nest = 0
word = []
debugs = []
in_singleqoutes = False
in_doubleqoutes = False
symchar = True
wordbreak = False
symtype = 'keyword'
nextc = ''
lastc = ''
newword = ''

# for every character in the query:
txt = """test 'foo ''and'' bar' poomba ;"""
print(txt)
for c in txt:
    
    # for readability, let's collect everything we know up front:
    symchar = True
    wordbreak = c in breakingchars
    nextc = txt[i+1:i+2]
    
            
    # ------------ QUOTE STRING HANDLING -------------- #
    # if single quote found and not already in a double quote and c isn't repeated (escaped)...
    if c == "'" and not in_doubleqoutes and (c != nextc or c != lastc): 
        in_singleqoutes = not in_singleqoutes  # toggle state (starting/ending)
        symchar = (nest != 0)
        symtype = 'quoteS'       

    # if double quote found and not already in a single quote and c isn't repeated (escaped)...
    if c == '"' and not in_singleqoutes and (c != nextc or c != lastc): 
        in_doubleqoutes = not in_doubleqoutes # toggle state (starting/ending)
        symchar = (nest != 0)
        symtype = 'quoteD'            

    # ------------ NESTED PARENS HANDLING -------------- #
    if c == '(' and not in_doubleqoutes and not in_singleqoutes: 
        nest +=1
        symchar = False
        symtype = 'parens'
    if c == ')' and not in_doubleqoutes and not in_singleqoutes: 
        nest -=1
        symchar = False
        symtype = 'parens'

    # ------------ ADD CHARACTER TO SYMBOL (OR NOT) -------------- #
    if wordbreak and not in_doubleqoutes and not in_singleqoutes and len(word)>0 and nest==0: 
        newword = ''.join(word)
        sym.append( {'symbol':newword, 'type':symtype, 'start':p1, 'end':p2} )
        wordcount +=1
        word = []
        symtype = 'keyword'
        p2 = i

    else:
        if symchar:
            if word==[]: p1 = i
            word.append(c)
            
            
    
    # record debug info:
    if type(debugs) == list:
        debugs.append({'i':i, 'p1':p1, 'p2':p2, 'words':wordcount, 'char':c, 'nextc':nextc, 'lastc':lastc , 'nest':nest ,'wordc':str(symchar), 'brk':str(wordbreak), 'quoteS':str(in_singleqoutes), 'quoteD':str(in_doubleqoutes), 'wordlen':str(len(word)), 'lastword':'[%s]' %newword })
    
    # always do these:
    lastc = c
    i +=1

    
if type(debugs) == list:
    print(''.join([k.ljust(7) for k in debugs[0]]))
    for d in debugs:
        msg=[]
        for n,v in d.items():
            msg.append(str(v).ljust(7))
        print(''.join(msg))
        

for s in sym:
    msg = 'p1:%s p2:%s Type:%s Symbol:[%s]' %(str(s['start']).ljust(3), str(s['end']).ljust(3), s['type'].ljust(10), s['symbol'])
    print(msg)
    
print(txt)
