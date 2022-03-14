
import logging as log
log.basicConfig(encoding='utf-8', format='%(asctime)s--%(levelname)s:%(message)s', level=log.DEBUG)
log.info('logging setup')


class snsql_parse():
    query_original = ''
    query_compressed = ''
    parsed_instructions = []

    def __init__(self, snsql_query:str='') -> None:
        self.query_original = snsql_query
        if self.query_original != '': 
            self.query_compressed = self.removewhitespace(self.query_original)
            self.snsql_parse(self.query_compressed)

    

    def get_between(self, txt:str, open_char:str="'", close_char:str="'", start:int=1 ):
        """Parse all content in supplied text that appears between the open and close characters, exclusively.
        If txt is empty, or open_char is not found, returns ('', -1, -1).  If the close_char is never found, 
        returns the txt from the starting positon through the end of the txt.

        Args:
            txt (str): String text to parse out subset.
            open_char (str, optional): Character defining the opening of the subset. Defaults to "'".
            close_char (str, optional): Character defining the close of the subset. Defaults to "'".
            start (int, optional): Position in txt to start searching. Defaults to 1.

        Returns:
            tuple: (subset:str, starting position of subset:int, ending position of subset:int)
        """
        sp = txt.find(open_char, start)
        ep = sp+1
        if sp == -1 or open_char=='' or close_char=='': return ('',-1,-1) # if not found, or empty

        if open_char == close_char:  # quote like things
            while ep <= len(txt):
                ep1 = txt.find(close_char, ep)
                ep = len(txt)+1 if ep1 == -1 else ep1+1 
                if txt[ep1:ep1+1] == close_char and close_char not in [txt[ep1-1:ep1], txt[ep1+1:ep1+2]]:
                    break 
        else: # paren-like things
            i = 0
            for c in txt[sp:]:
                if c == open_char: i+=1
                if c == close_char: i -=1
                if i == 0: break
                ep +=1
        sp +=1
        ep -=1
        return (txt[sp:ep].replace(open_char*2, open_char) if open_char == close_char else txt[sp:ep], sp, ep)


    def removewhitespace(self, txt:str) ->str:
        txt = txt.replace('\n', ' ').replace('\t',' ').strip()
        while txt.find('  ') >0:
            txt = txt.replace('  ',' ')
        return txt


    def get_chart_type(self, txt:str, start:int=0) ->dict:
        if txt[:5] != 'chart':
            raise Exception("Syntax expecting command to start with 'chart'.")
        else:
            word = ''
            p1 = p2 = 6
            for c in txt[6:]:
                if c == ' ': break 
                p2 +=1
        return {'item':'chart type', 'chart type':txt[p1:p2], 'start':p1, 'end':p2}

    def get_chart_title(self, txt:str, start:int=0) -> dict:
        rtn = self.get_between(txt,"'", "'", start)
        return {'item':'title', 'title':rtn[0], 'start':rtn[1], 'end':rtn[2]+1}

    def get_next_series(self, txt:str, start:int=0) -> dict:
        p2 = txt.find(' ', start)
        while p2 <= start: 
            start +=1
            p2 = txt.find(' ', start)
        colname = txt[start:p2]
        (seriesdef, p3, p4) = self.get_between(txt, "(", ")", p2 + 1)
        colaxis = txt[p3-2:p3-1]
        return {'item':'series', 'column name':colname, 'axis':colaxis, 'definition':seriesdef, 'start':start, 'end':p4+1}

    def get_chart_from(self, txt:str, start:int=0) -> dict:
        frm = self.get_next_token(txt, start)
        if frm[0].lower() != 'from': 
            raise Exception("FROM statement is malformed, try  FROM file('./some/filepath.csv')  or  FROM dataframe(dfname)")
        frmtype = self.get_next_token(txt, frm[2])
        frmname = self.get_between(txt,"(", ")", frmtype[2])
        return { 'item':'from', 'type':frmtype[0], 'name':frmname[0], 'start':frm[2], 'end':frmname[2] }
        
    def get_chart_body(self, txt:str, start:int=0) -> dict:
        token = self.get_next_token(txt, start)
        if token[0].lower() != 'body': 
            raise Exception("BODY statement is malformed, try  BODY( <format statements> )")
        tokendef = self.get_between(txt,"(", ")", token[2])
        return { 'item':'body', 'definition':tokendef[0], 'start':token[1], 'end':tokendef[2] }
        
    def get_chart_legend(self, txt:str, start:int=0) -> dict:
        token = self.get_next_token(txt, start)
        if token[0].lower() != 'legend': 
            raise Exception("LEGEND statement is malformed, try  LEGEND( <format statements> )")
        tokendef = self.get_between(txt,"(", ")", token[2])
        return { 'item':'legend', 'definition':tokendef[0], 'start':token[1], 'end':tokendef[2] }

    def get_chart_title_def (self, txt:str, start:int=0) -> dict:
        token = self.get_next_token(txt, start)
        if token[0].lower() != 'title': 
            raise Exception("TITLE format statement is malformed, try  TITLE( <format statements> )")
        tokendef = self.get_between(txt,"(", ")", token[2])
        return { 'item':'title', 'definition':tokendef[0], 'start':token[1], 'end':tokendef[2] }
        
    def get_chart_orderby (self, txt:str, start:int=0) -> dict:
        while txt[start:start+1] == ' ': start +=1
        p1 = start + 8
        if txt[start:p1].lower() != 'order by': 
            raise Exception("ORDER BY format statement is malformed, try  ORDER BY <column1> [asc|desc], <columnN> [asc|desc] <EOF>")
        orderby = [col.strip() for col in txt[p1:].split(',')]
        rtnlist = []
        for col in orderby:
            rtn = col.split(' ')
            if len(rtn) == 1:  
                rtn.append('asc')
            else:
                if rtn[1] not in ['asc','desc']:
                    raise Exception("ORDER BY format statement is malformed, try  ORDER BY <column1> [asc|desc], <columnN> [asc|desc] <EOF>")
            rtnlist.append(rtn)
        return { 'item':'order by', 'definition':rtnlist, 'start':start, 'end':len(txt) }
        

    def get_next_token(self, txt:str, start:int=0) -> str:
        if start >= len(txt): return None 
        while txt[start:start+1] == ' ': start +=1
        for i in range(start, len(txt)):
            c = txt[i:i+1]
            if not self.wordpart(c):
                break
        if i == start: i+=1
        token = txt[start:i]
        return (token, start, i)

    def wordpart(self, char:str) -> bool:
        ci = ord(char)
        return (ci in range(48,57) or ci in range(65,90) or ci in range(97,122) or ci in[95])


    def snsql_parse(self, txt:str) -> list:
        qry = []
        t = self.removewhitespace(txt)

        rtn = self.get_chart_type(t)  # Get Chart Type
        qry.append(rtn)
        pos =  rtn['end'] + 1

        rtn = self.get_chart_title(t, pos)  # Get Chart Title 
        qry.append(rtn)
        pos =  rtn['end'] + 1

        rtn = self.get_next_series(t, pos)  # Get first Axis definitions
        qry.append(rtn)
        pos =  rtn['end'] + 1

        while self.get_next_token(t, pos)[0] == ',':   # Get all remaining Axis definitions
            rtn = self.get_next_series(t, pos+1)
            qry.append(rtn)
            pos =  rtn['end'] + 1

        while pos < len(t):
            next_section = self.get_next_token(t, pos)  # Get all remaining sections (from, body, legend, order by, etc.)

            if next_section[0].lower() == 'from':
                rtn = self.get_chart_from(t, pos)  # Get From
                qry.append(rtn)
                pos =  rtn['end'] + 1

            elif next_section[0].lower() == 'body':
                rtn = self.get_chart_body(t, pos)  # Get chart body formatting
                qry.append(rtn)
                pos =  rtn['end'] + 1

            elif next_section[0].lower() == 'legend':
                rtn = self.get_chart_legend(t, pos)  # Get legend formatting
                qry.append(rtn)
                pos =  rtn['end'] + 1

            elif next_section[0].lower() == 'title':
                rtn = self.get_chart_title_def(t, pos)  # Get extra title formatting
                qry.append(rtn)
                pos =  rtn['end'] + 1

            elif next_section[0].lower() == 'order' and self.get_next_token(t, next_section[2])[0].lower() == 'by':
                rtn = self.get_chart_orderby(t, pos)  # Get legend formatting
                qry.append(rtn)
                pos =  rtn['end'] + 1

        self.parsed_instructions = qry
        return qry 




txt = """
chart line 'COA Chart of ''Unknown'' Upper Bound (test)' 
LogDate    as x(label=null, (format=('yyyy-mm'))) 
,CPU_Idle   as y(label='Idle', color='grey')
,CPU_OS     as y(label='OS', color='light BLUE')
,CPU_IOWait as y(label='IOWait', color='yellow')
,CPU_DBMS   as y(label='DBMS', color='blue')
,100        as y(label='total', color='#ff0000')
,80         as y(label='warning line', color='orange', line='dash')
FROM dataframe(df)
body (style='coa', width=12, height=6)
legend (x=120%, y=10%, backcolor='grey', line='solid')
order by LogDate asc, CPU_DBMS desc, CPU_OS
"""


snsql = snsql_parse(txt)
for q in snsql.parsed_instructions:
    print(q)











