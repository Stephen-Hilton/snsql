
chart bar 'this is my title' 
 colA as x(label='revenue', format='$0.00M')
,colB as y(label=null)
,100 as y(type=line, color='#ff0000')
,20 as x(type=line, color='orange')
from "./some/file.csv"
where colC = 'test'
legend (null)
order by colB desc 
;

chart line 'coa chart of unknown upper bound' 
 logdate    as x(label=null, format='yyyy-mm')
,CPU_Idle   as y(label='Idle', color='grey')
,CPU_OS     as y(label='OS', color='light blue')
,CPU_IOWait as y(label='IOWait', color='yellow')
,CPU_DBMS   as y(label='DBMS', color='blue')
,100        as y(label='total', color='#ff0000')
,80         as y(label='warning line', color='orange', style='dash')
from dataframe(df)
body (style='coa', width=12, height=6)
legend (x=120, y=80, border=(backcolor='grey', color='black', style='solid'))
order by LogDate
;


chart Bar 'Account Health by Region - Count' 
 body(style='bod', width=12, height=6)
,Region     as x(label=null)
,count(*)   as y(stacked='Health'
				 ,order=('green','yellow','red','black','unclassified') 
				 ,color=('green','yellow','#ff0000','black','grey'))
from file('somefile.csv')
legend (x=120, y=80, border=(backcolor='grey', color='black', style='solid'))
order by Region
;


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



set chart style 'coa-square'
 body(style='coa', width=9, height=9, border=(backcolor='white', color='#001234', style='solid:2'))
; -- extends/overrides style 'coa' 



chart heatmap 'CPU% by day by hour'
 body(style='coa-square' )
,LogDate as x(label=null)
,LogHour as y(label='hour')
,CPU_pct as i(min=0, max=100, color=('white','green','yellow','red'), square=True, font=())
from file('somefile.csv')
;