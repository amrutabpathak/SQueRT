import csv
import sqlite3

try:
  conn = sqlite3.connect('research.database.db')
  cursor = conn.execute("SELECT ID,TOPIC,QUERY,ANSWER,PAPER_LINK,FEEDBACK from SQUERT_DATA")
  dbDump = open('SquertData.tsv', 'w')
  research_writer = csv.writer(dbDump, delimiter="\t")
  research_writer.writerow([curr[0] for curr in cursor.description])
  research_writer.writerows(cursor)
except:
  print('Error! ')
finally:
  conn.close()
  dbDump.close()


