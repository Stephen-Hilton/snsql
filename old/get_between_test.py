import unittest

from get_between import get_between

class test_get_between(unittest.TestCase):
    textA = "thing1 as x(colors=(a,b,c), label='cats', size=123), thing2 as y(label='dogs', colors=(x,y,z))"

    def test_parens_1a(self):
        result = get_between(self.textA, "(", ")", 0)
        self.assertEqual(result[0], "colors=(a,b,c), label='cats', size=123" )

    def test_parens_2a(self):
        result = get_between(self.textA, "(", ")", 12)
        self.assertEqual(result[0], "a,b,c" )    

    def test_parens_3a(self):
        result = get_between(self.textA, "(", ")", 22)
        self.assertEqual(result[0], "label='dogs', colors=(x,y,z)" 
        )  
    def test_parens_4a(self):
        result = get_between(self.textA, "(", ")", 70)
        self.assertEqual(result[0], "x,y,z" )  

    def test_quote_1a(self):
        result = get_between(self.textA, "'", "'", 0)
        self.assertEqual(result[0], "cats" )

    def test_quote_2a(self):
        result = get_between(self.textA, "'", "'", 32)
        self.assertEqual(result[0], "cats" )

    def test_quote_3a(self):
        result = get_between(self.textA, "'", "'", 48)
        self.assertEqual(result[0], "dogs" )

    def test_quote_4a(self):
        result = get_between(self.textA, "'", "'", 37)
        self.assertEqual(result[0], ", size=123), thing2 as y(label=" )


    textB = """
    chart line 'COA Chart of ''Unknown'' Upper Bound (test)' 
    logdate    as x(label=null, (format=('yyyy-mm'))) 
    ,CPU_Idle   as y(label='Idle', color='grey')
    ,CPU_OS     as y(label='OS', color='light BLUE')
    ,CPU_IOWait as y(label='IOWait', color='yellow')
    ,CPU_DBMS   as y(label='DBMS', color='blue')
    ,100        as y(label='total', color='#ff0000')
    ,80         as y(label='warning line', color='orange', style='dash')
    from dataframe(df)
    body (style='coa', width=12, height=6)
    legend (x=120, y=80, border=(backcolor='grey', color='black', style='solid'))
    order by LogDate
    """

    def test_parens_1b(self):
        result = get_between(self.textB, "(", ")", 0)
        self.assertEqual(result[0], "test" )

    def test_parens_2b(self):
        findstr = "logdate"
        pos = self.textB.find(findstr)+len(findstr)
        result = get_between(self.textB, "(", ")", pos)
        self.assertEqual(result[0], "label=null, (format=('yyyy-mm'))" )

    def test_parens_3b(self):
        findstr = "x(label"
        pos = self.textB.find(findstr)+len(findstr)
        result = get_between(self.textB, "(", ")", pos)
        self.assertEqual(result[0], "format=('yyyy-mm')" )

    def test_parens_4b(self):
        findstr = "x(label=null, (for"
        pos = self.textB.find(findstr)+len(findstr)
        result = get_between(self.textB, "(", ")", pos)
        self.assertEqual(result[0], "'yyyy-mm'" )

    def test_quote_1b(self):
        result = get_between(self.textB, "'", "'", 0)
        self.assertEqual(result[0], "COA Chart of 'Unknown' Upper Bound (test)" )

    def test_quote_2b(self):
        findstr = "logdate"
        pos = self.textB.find(findstr)+len(findstr)
        result = get_between(self.textB, "'", "'", pos)
        self.assertEqual(result[0], "yyyy-mm" )

    def test_quote_3b(self):
        findstr = "CPU_IOWait"
        pos = self.textB.find(findstr)+len(findstr)
        result = get_between(self.textB, "'", "'", pos)
        self.assertEqual(result[0], "IOWait" )

    def test_quote_4b(self):
        findstr = "80"
        pos = self.textB.find(findstr)+len(findstr)
        result = get_between(self.textB, "'", "'", pos)
        self.assertEqual(result[0], "warning line" )
        
    def test_quote_5b(self):
        findstr = " y(label='warning line'"
        pos = self.textB.find(findstr)+len(findstr)
        result = get_between(self.textB, "'", "'", pos)
        self.assertEqual(result[0], "orange" )

    def test_breakit_1b(self):
        pos = len(self.textB)+1
        result = get_between(self.textB, "'", "'", pos)
        self.assertEqual(result[0], "" )

    def test_breakit_2b(self):
        result = get_between(self.textB, "~", "~", 0)
        self.assertEqual(result[0], "" )

    def test_breakit_3b(self):
        result = get_between(self.textB, "", "", 0)
        self.assertEqual(result[0], "" )


if __name__ == "__main__":
    unittest.main()


