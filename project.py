# import all the packages
import re
import bs4 as bs
import urllib.request
import sqlite3

#Question1: Download the main table from the web page using python

#URL link
URL = "https://en.wikipedia.org/wiki/Farebox_recovery_ratio"

#use the urllib to read the URL link
source=urllib.request.urlopen(URL).read()

#use the beautifulsoup package to access the html
soup = bs.BeautifulSoup(source,'lxml')

#From the html, find the table that we want and the web page has several tables, the main table that we want is the second
table = soup.findAll("table")[1]

#use find_all method and tr to find the table_rows that we wnat to access
table_rows=table.find_all('tr')

#create an empty dictionary which stores our data set
savedfile={}

#set counter=0 
counter=0

#use a for loop to access the table data and then store them in the dictionary using counter as the dictionary key and the value of the dictionary is also a list
for tr in table_rows:
    td=tr.find_all('td')
    row=[i.text for i in td]
    if len(row)>0:
        for i in range(len(row)):
            row[i]=row[i].replace('\n','')
        counter+=1
        savedfile[counter]=row

#define a fuction which cleans the footnote "[]" thing
def cleannumbers(string):
    start=len(string)
    for i in string:
        if ord(i)==91:
            start=string.find(i)
    string=string[0:start]
    return string


#create a currency dictionary which we can use to convert currency into us dollars
currency={'Australia': 1.37,
          'Canada': 1.33,
          'Switzerland': 0.99926,
          'China': 6.95,
          'Czech Republic': 22.82,
          'Austria':0.88,
          'Germany':0.88,
          'Finland':0.88,
          'Australia':1.37,
          'Hong Kong':7.83,
          'Taiwan':30.83,
          'Pakistan':133.43,
          'Sweden':9.04,
          'Singapore':1.37,
          'Japan':113.46,
          'France':0.88,
          'US':1
          }

#define a function which calculates the average of a list
def average(lista):
    for i in range(len(lista)):
        lista[i]=float(lista[i])    
    x=("%.2f" % (float(sum(lista))/float(len(lista))))
    return x


#define a function which processess the messy string and turn that into a float number
def convertrate(country,fare_rate):
    if fare_rate.isspace() == False and fare_rate !="":
        #give an int exchange rate
        exchange_rate=currency[country]  
        rate=re.findall(r"[-+]?\d*\.\d+|\d+",fare_rate)
        # find all the numbers in the string in the form of list 
        number=("%.2f" % (float(average(rate)) / float(exchange_rate)))
        return ("$"+number)
    else:
        return ("missing")

#define a fuction which convert the percentage number to float numbers
def convertpercentage(string):
    number=("%.2f" % (float(string.replace(" ","").strip('%'))/100))
    return number

#check whether a string is blank
def checkmissing(string):
    if string.isspace() == True or string =="":
        return ("missing")
    else:
        return string

#Question2: clean up the dataset
    
for i in savedfile:
    savedfile[i][3]=cleannumbers(savedfile[i][3])
    savedfile[i][3]=convertpercentage(savedfile[i][3])
    savedfile[i][6]=cleannumbers(savedfile[i][6])
    savedfile[i][5]=convertrate(savedfile[i][1],savedfile[i][5])
    savedfile[i][4]=checkmissing(savedfile[i][4])
    


# Connecting to the database file
conn = sqlite3.connect('project.db')
c = conn.cursor()

#Create the table

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS newtable(Continent TEXT,Country TEXT,System TEXT,Ratio REAL,Fare_System Text,Fare_Rate Real,Year Text)")

def data_entry(list):
    c.execute("INSERT INTO newtable (Continent, Country, System, Ratio, Fare_System, Fare_Rate, Year) VALUES(?,?,?,?,?,?,?)",
              (list[0],list[1],list[2],list[3],list[4],list[5],list[6]))

create_table()
for i in savedfile:
    data_entry(savedfile[i])
              
conn.commit()
c.close()
conn.close()

