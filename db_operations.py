# -*- coding: utf-8 -*-
"""DB_operations

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QmlhtRH-qc94tyfYKpagStOMZhWfMtZ4
"""

import sqlite3

def createTable():
  dbConnection = sqlite3.connect('research.database.db')
  dbConnection.execute(''' CREATE TABLE IF NOT EXISTS SQUERT_DATA
                  (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
                    TOPIC TEXT ,
                    QUERY TEXT NOT NULL ,
                    ANSWER TEXT ,
                    PAPER_LINK TEXT ,
                    FEEDBACK TEXT); ''' )
  print('SQUERT_DATA created!')
  dbConnection.close()

def insertRecords(topic, query, answer,paperLink, feedback):
        #try:
         with sqlite3.connect("research.database.db") as dbConnection:
            dbCursor = dbConnection.cursor()
            dbCursor.execute("INSERT INTO SQUERT_DATA (TOPIC,QUERY,ANSWER,PAPER_LINK,FEEDBACK) \
               VALUES (?,?,?,?,?)",(topic,query,answer, paperLink, feedback) )
            
            dbConnection.commit()
            print("Data added")
        #except:
         #dbConnection.rollback()
         #print("Exception occurred while inserting Data ")
      
        #finally:
         dbConnection.close()

def updateRecords(topic, query, feedback):
  try:
    dbConnection = sqlite3.connect("research.database.db")
    dbConnection.execute("UPDATE SQUERT_DATA SET FEEDBACK = ? WHERE ID = (SELECT ID FROM SQUERT_DATA WHERE TOPIC = ? AND QUERY = ? ORDER BY ID DESC LIMIT 1)", (feedback, topic, query))
    dbConnection.commit()
  except:
    dbConnection.rollback()

  finally:
    dbConnection.close()

#createTable()
#insertRecords('Deep Learning', 'How are you', 'Ok', 'https://www.google.com/search?q=sql+int+primary+key+autoincrement&rlz=1C1CHBF_enUS853US853&oq=SQL+INT+PRIMARY+KEY+&aqs=chrome.1.69i57j0l7.5362j0j7&sourceid=chrome&ie=UTF-8','Great')

'''conn = sqlite3.connect('research.database.db')
print ('Opened database successfully');

cursor = conn.execute("SELECT ID,TOPIC,QUERY,ANSWER,PAPER_LINK,FEEDBACK from SQUERT_DATA")
for row in cursor:
   print ("ID = ", row[0])
   print ("TOPIC = ", row[1])
   print ("QUERY = ", row[2])
   print ("ANSWER = ", row[3]),
   print ("PAPER_LINK = ", row[4]),
   print ("FEEDBACK = ", row[5]), "\n"

print('Operation done successfully')
conn.close()
'''

#updateRecords('Deep Learning', 'How are you', 'Not not good')