
def tokenize_quotes(txt:str, iteration_limit:int = 0, enclosing_character:str = "'", tokenname_prefix:str = 'SQ') ->dict:
    tokencount = p1 = p2 = 0
    tokens = []
    enc = enclosing_character
    txt = txt.strip()
    
    while txt.find(enc) >= 0:
        p1 = txt.find(enc)
        p2 = txt.find(enc, p1+1)
        while txt[p2+1:p2+2] == enc:
            p2 = txt.find(enc, p2+2)
        p2 = p2 +1
        tokentext = txt[p1:p2]
        tokenname = '{{{%s%s}}}' %(tokenname_prefix, str(tokencount).zfill(3))
        tokens.append({'name':tokenname, 'pos1':p1, 'pos2':p2, 'text':tokentext})
        tokencount +=1
        txt = txt.replace(tokentext, tokenname)
        if tokencount >= iteration_limit and not iteration_limit == 0: break 
    return txt, tokens

def tokenize_parens(txt:str, iteration_limit:int = 0, enclosing_start:str = "(",  enclosing_end:str = ")", tokenname_prefix:str = 'PN') ->dict:
    tokencount = p1 = p2 = 0
    tokens = []
    encS = enclosing_start
    encE = enclosing_end
    txt = txt.strip()
    
    while txt.find(encS) >= 0:
        p1 = txt.find(encS)
        p2 = txt.find(encE, p1+1)+1
        p1n = 0
        while p1n < p2 and not p1n==-1: # check for nested parens
            p1 = txt.find(encS, p1n)
            p1n = txt.find(encS, p1+1)
            p2 = txt.find(encE, p1+1)+1
        tokentext = txt[p1:p2]
        tokenname = '{{{%s%s}}}' %(tokenname_prefix, str(tokencount).zfill(3))
        tokens.append({'name':tokenname, 'pos1':p1, 'pos2':p2, 'text':tokentext})
        tokencount +=1
        txt = txt.replace(tokentext, tokenname)
        if tokencount >= iteration_limit and not iteration_limit == 0: break 
    return txt, tokens
    
    
def ireplace(old, new, text):
    idx = 0
    while idx < len(text):
        index_l = text.lower().find(old.lower(), idx)
        if index_l == -1:
            return text
        text = text[:index_l] + new + text[index_l + len(old):]
        idx = index_l + len(new) 
    return text
    
def token_text(tokens:list, checkstring:str, allowrecursive:bool=True) -> str:
    for token in tokens:
        checkstring = ireplace(token['name'].lower(), token['text'], checkstring)    
    itermax = 10
    while '{{{' in checkstring and itermax >=0 and allowrecursive:
        checkstring = token_text(tokens, checkstring, False)
        itermax -=1
    return checkstring




# custom processing for snsql:
qrytmp = qry
qrytmp, tokens = tokenize_quotes(qrytmp,1)
qrytmp, ptokens = tokenize_parens(qrytmp)
tokens.extend(ptokens)


# normalize whitespace:
qrytmp = qrytmp.replace('{{{',' {{{').replace('}}}', '}}} ').replace('\n',' ').lower().strip()
while qrytmp.find('  ') >0:
    qrytmp = qrytmp.replace('  ',' ')

# first 3 tokens are known and consistent:
keywords = qrytmp.split(' ')

# CHART keyword always first
charttest = keywords.pop(0)
if not charttest == 'chart':
    print('ERROR: snsql must start with CHART keyword')

# chart type always second
charttype = keywords.pop(0)
if charttype not in ['bar','line','heatmap']:
    print('ERROR: supported chart types are BAR, LINE, HEATMAP')
else:
    print('Chart Type: %s' %charttype)

# chart title always third (string or null)
charttitle = token_text(tokens, keywords.pop(0))
if charttitle.lower() == 'null': charttitle = ''
print('Chart Title: %s' %charttitle)


# after 3 constistent keywords, we have N-Number of series/column definitions
chartseries = []
nextkeyword = ','
while nextkeyword[:1] == ',':
    
    series = {}
    if keywords[1] == 'as':   # 4 parts:  col as x(options)
        series['aggr'] = ''
        series['name'] = keywords.pop(0) #0
        series['_as_'] = keywords.pop(0) #1
        series['axis'] = keywords.pop(0) #2
        series['opts'] = keywords.pop(0) #3
    elif keywords[2] == 'as': # 5 parts:  agg(col) as x(options)
        series['aggr'] = keywords.pop(0) #0
        series['name'] = keywords.pop(0) #1
        series['_as_'] = keywords.pop(0) #2
        series['axis'] = keywords.pop(0) #3
        series['opts'] = keywords.pop(0) #4
    if series['name'][:1]==',': series['name']=series['name'][1:]
    if series['aggr'][:1]==',': series['aggr']=series['aggr'][1:]
    chartseries.append(series)
    nextkeyword = keywords[0]
        
        
# after this it's easy:  everything has 2 elements except From and Order By
chartsetup = []
while len(keywords) >0:
    if keywords[0]=='order' and  keywords[1]=='by': 
        keywords[1] = 'order by'
        keywords.pop(0)
    elif keywords[0]=='from':
        keywords[1] = {'sourcetype':keywords[1], 'source':token_text(tokens,keywords.pop(2))}
    chartsetup.append({'keyword':keywords.pop(0), 'options':keywords.pop(0)})
    

# go thru everything and put back all the tokens:
charttype = token_text(tokens, charttype)
charttitle = token_text(tokens, charttitle)
lists_of_lists = [chartseries, chartsetup]
for lists_of_dicts in lists_of_lists:
    for onedict in lists_of_dicts:
        for n,v in onedict.items():
            if type(v)==str: onedict[n] = token_text(tokens, v)
            if type(v)==dict:
                for n1,v1 in v.items():
                    series[n1] = token_text(tokens, v1)
                    

# wrap up into a final output package:
snsql = {'chart type': charttype
        ,'chart title': charttitle
        ,'chart series': chartseries
        ,'chart setup': chartsetup
        ,'original query': qry}


print('')
ind=0
for n1,v1 in snsql.items():
    if type(v1) == str: 
        ind = 0
        print(' '*ind, n1.ljust(20), str(v1))
    if type(v1) == list:
        ind = 4
        print('','list of %s' %n1)
        for itm in v1:
            if type(itm)==dict:
                for n2,v2 in itm.items():
                    print(' '*ind, n2.ljust(20), str(v2))

print("")
print(tokens)
