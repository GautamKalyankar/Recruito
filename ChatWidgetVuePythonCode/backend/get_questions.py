import sqlite3
import random
def get_questions(job_type):
    questions = []
    scale = []
    category = []
    if job_type=="hr":
        
        connection = sqlite3.connect("solvathon.db")
        cursor = connection.cursor()
        connection.row_factory = sqlite3.Row
        
        cursor.execute("select questions, scale, category from QUESTIONNAIRE WHERE  is_prelim=='1' and is_hr=='1';")
        choices = random.sample(cursor.fetchall(), k = 2)
        questions += [i[0] for i in choices]
        scale += [i[1] for i in choices]
        category +=[i[2] for i in choices]
        

        cursor.execute("select questions, scale, category from QUESTIONNAIRE WHERE category=='Leadership and Management' and is_prelim=='0' and is_hr=='1';")
        choices = random.sample(cursor.fetchall(), k = 2)
        questions += [i[0] for i in choices]
        scale += [i[1] for i in choices]
        category +=[i[2] for i in choices]
        
        cursor.execute("select questions, scale, category from QUESTIONNAIRE WHERE category=='Communication Skills' and is_prelim=='0' and is_hr=='1';")
        choices = random.sample(cursor.fetchall(), k = 2)
        questions += [i[0] for i in choices]
        scale += [i[1] for i in choices]
        category +=[i[2] for i in choices]
        
        cursor.execute("select questions, scale, category from QUESTIONNAIRE WHERE category=='Time Management' and is_prelim=='0' and is_hr=='1';")
        choices = random.sample(cursor.fetchall(), k = 2)
        questions += [i[0] for i in choices]
        scale += [i[1] for i in choices]
        category +=[i[2] for i in choices]
        
        cursor.execute("select questions, scale, category from QUESTIONNAIRE WHERE category=='Flexibility Adaptability' and is_prelim=='0' and is_hr=='1';")
        choices = random.sample(cursor.fetchall(), k = 2)
        questions += [i[0] for i in choices]
        scale += [i[1] for i in choices]
        category +=[i[2] for i in choices]

        cursor.execute("select questions, scale, category from QUESTIONNAIRE WHERE category=='Team Mangement' and is_prelim=='0' and is_hr=='1';")
        choices = random.sample(cursor.fetchall(), k = 2)
        questions += [i[0] for i in choices]
        scale += [i[1] for i in choices]
        category +=[i[2] for i in choices]
        
        connection.close()    
    
    else:
        connection = sqlite3.connect("solvathon.db")
        cursor = connection.cursor()
        connection.row_factory = sqlite3.Row
        cursor.execute("select questions, scale, category from QUESTIONNAIRE WHERE  is_prelim=='1' and is_dev=='1';")
        choices = random.sample(cursor.fetchall(), k = 2)
        questions += [i[0] for i in choices]
        scale += [i[1] for i in choices]
        category +=[i[2] for i in choices]
        
        cursor.execute("select questions, scale, category from QUESTIONNAIRE WHERE category=='Leadership and Management' and is_prelim=='0' and is_dev=='1';")
        choices = random.sample(cursor.fetchall(), k = 2)
        questions += [i[0] for i in choices]
        scale += [i[1] for i in choices]
        category +=[i[2] for i in choices]
        
        cursor.execute("select questions, scale, category from QUESTIONNAIRE WHERE category=='Problem Solving Decision Making' and is_prelim=='0' and is_dev=='1';")
        choices = random.sample(cursor.fetchall(), k = 2)
        questions += [i[0] for i in choices]
        scale += [i[1] for i in choices]
        category +=[i[2] for i in choices]
        
        cursor.execute("select questions, scale, category from QUESTIONNAIRE WHERE category=='Communication Skills' and is_prelim=='0' and is_dev=='1';")
        choices = random.sample(cursor.fetchall(), k = 2)
        questions += [i[0] for i in choices]
        scale += [i[1] for i in choices]
        category +=[i[2] for i in choices]
        
        cursor.execute("select questions, scale, category from QUESTIONNAIRE WHERE category=='Time Management' and is_prelim=='0' and is_dev=='1';")
        choices = random.sample(cursor.fetchall(), k = 2)
        questions += [i[0] for i in choices]
        scale += [i[1] for i in choices]
        category +=[i[2] for i in choices]
        
        cursor.execute("select questions, scale, category from QUESTIONNAIRE WHERE category=='Team Mangement' and is_prelim=='0' and is_hr=='1';")
        choices = random.sample(cursor.fetchall(), k = 2)
        questions += [i[0] for i in choices]
        scale += [i[1] for i in choices]
        category +=[i[2] for i in choices]

        # cursor.execute("select questions, scale, category from QUESTIONNAIRE WHERE category=='Flexibility Adaptability' and is_prelim=='0' and is_dev=='1';")
        # choices = random.sample(cursor.fetchall(), k = 2)
        # questions += [i[0] for i in choices]
        # scale += [i[1] for i in choices]
        # category +=[i[2] for i in choices]
        
        connection.close()

    return (questions, scale, category)

print(get_questions("dev"))