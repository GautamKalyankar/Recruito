import sqlite3
import pandas as pd
import numpy as np

connection = sqlite3.connect("solvathon.db")
cursor = connection.cursor()
# cursor.execute('''CREATE TABLE APPLICANT_SCORE(application_id INTEGER PRIMARY KEY AUTOINCREMENT, ap_id int, job_id int, leadership_score int, 
#                  communication_score int, time_score int, team_score int, general_score int,
#                   FOREIGN KEY(ap_id) REFERENCES APPLICANT(ap_id), FOREIGN KEY(job_id) REFERENCES JOB_DESCRIPTION(JD_NO) );''')
cursor.execute("SELECT ap_id FROM APPLICANT ORDER BY ap_id DESC LIMIT 1")
print(cursor.fetchall()[0][0])
connection.commit()
connection.close()
