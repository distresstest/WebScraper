import requests
import pandas as pd
import bs4
import os
import codecs
from bs4 import NavigableString, Tag
import pprint
import re



def SoupObjIgnoreChk(SoupChild, IgnoreList):
	# Checking whether to ignore this Tag or not (based on IgnoreList)
	Ignore = False
	for IgnoreString in IgnoreList:
		#print "        Checking for..." + str(IgnoreString)
		if IgnoreString in str(SoupChild): 
			#print "        Found IgnoreString " + IgnoreString + " in child... " 
			Ignore = True
						
	if Ignore == True:
		return True
	return False
	
def CleanStr(MyString):
		# Probably need to clean up "CurrStr" before adding it TableData
		#print "Dirty String = " + MyString
		
		CleanStr = MyString.strip('/"') # Double quotes ant beginning and end
		CleanStr = CleanStr.strip() # Spaces at beginning and end
		CleanStr = re.sub(' +', ' ', CleanStr) # Replace multiple spaces with single
		CleanStr = CleanStr.replace('\n', '').replace('\r', '') # Remove /n & /r within strings
		
		#print "Clean String = " + CleanStr
				
		return CleanStr
	
	

#html
my_html = """
<html>
<body>
   <table>
        <th><td>column 1</td><td>column 2</td></th>
        <tr><td>value 1</td><td>value 2</td></tr>
   </table>
</body>
</html>
"""

# Set up variables
TableIndex = 0
url = "https://en.wikipedia.org/wiki/List_of_UK_Singles_Chart_Christmas_number_ones"
#url = "http://www.noblehousesouthsea.com/index.php/menus/take-away-menu#app"
#url = "https://en.wikipedia.org/wiki/List_of_countries_by_alcohol_consumption_per_capita"

# Get Soup
res = requests.get(url)
res.raise_for_status()

#soup = bs4.BeautifulSoup(res.text, 'html5lib')
soup = bs4.BeautifulSoup(res.text, 'lxml')
#soup = bs4.BeautifulSoup(my_html, 'lxml')

# Extract table
tables = soup.findAll('table')
my_table = tables[TableIndex]


#print("Printing Pretty table before...")
#print(my_table.prettify())

# Init Vars
RowCount=0
TableData = []
MyIgnoreList = ["sortkey", "reference"]

# Get table rows
rows = my_table.findAll('tr')

for row in rows:
	# Init Vars
	CellCount=0
	RowData=[]
	
	#print "############################### START OF ROW " + str(RowCount) + " ###########################################"
	
	cells = row.findAll(['th', 'td'])
	#print cells

	for cell in cells:
		# Init Vars
		CurrStr = ""
		
		#print "--------------- CELL " + str(CellCount) + " ----------------------"
		
		value = cell.string
			
		if value is None:
			# Init Vars
			TotChildChk = 0				
			TotChild = len(cell.contents)
			CurrStr =  ""
			ChildCnt = 0
			
			#print "The value in this cell is %s..." % value
			#print "It has " + str(TotChild) + " Children..."
	
	
			#StrList = []
			#StrCnt = 0
			
			for child in cell.children:
				ChildCnt += 1
				
				if isinstance(child, NavigableString):
					#print("    Child #" + str(ChildCnt) + " of type \"NavigableString\", with \"name\" " + str(child.name))
					
					# Checking to see if anything usefull in this child
					if len(child) > 0:
						TotChildChk += 1
						
						NewStr = str(child)
						#StrList[StrCnt] = CleanStr(NewStr)
						#CleanStr(NewStr)
						CurrStr = CurrStr + CleanStr(NewStr)     # Making all chars into string
						
				if isinstance(child, Tag):
					#print("    Child #" + str(ChildCnt) + " of type \"Tag\", with \"name\" " + str(child.name))		
					
					# If not to be ignored then keep text 		
					if SoupObjIgnoreChk(child, MyIgnoreList):
						#print " IGNORING SOMETHING!"
                                                ignore1 = 0	
					else:	
						#print "        Not Ignoring..."
						#print "CurrStr = " + str(CurrStr)
						CurrStr = CurrStr + " " + child.text    # Using text method to get relevant text from Tag
					
					TotChildChk += 1
					
				CleanStr(CurrStr)
			
			if TotChild == TotChildChk:
				print "*** Child totals checkout! ***"
			else:
				print "*** Child totals broken! ***"
				break
				

		else:		
			#print "The value in this cell is... %s" % value	
			#print "Nothing else to do!"		
			CurrStr = value
			
		# Probably need to clean up "CurrStr" before adding it TableData
		CleanStr(CurrStr)
		
			
		RowData.append(CellCount)	
		RowData[CellCount] = CleanStr(CurrStr)
		print RowData
		CellCount += 1	
	
	TableData.append(RowCount)
	TableData[RowCount] = RowData
	RowCount += 1	

pprint.pprint(TableData, width=250)
			
		

