import pyresparser
import nltk
#nltk.download("all")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import sqlite3
import random
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from word_data import word_data

'''
pip install nltk

pip install spacy==2.3.5

pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz

pip install pyresparser



'''


def get_resume_data(path_to_file: str):
    '''
    Function to extract Resume data
    from Resumes.
    '''
    data = pyresparser.ResumeParser(path_to_file).get_extracted_data()
    return data

#print(get_resume_data("AakashChavanResume.pdf"))

def get_similarity(sentence1: str, sentence2: str):
    '''
    Function to get similarity between
    two sentences.
    '''
    X_list = word_tokenize(sentence1)
    Y_list = word_tokenize(sentence2)

    words_not_required = stopwords.words('english')

    Y_set = {w for w in Y_list if not w in words_not_required}
    X_set = {w for w in X_list if not w in words_not_required}

    rvector = X_set.union(Y_set)
    l1 = []
    l2 = []
    for w in rvector:
        if w in X_set:
            l1.append(1)
        else:
            l1.append(0)
            
        if w in Y_set:
            l2.append(1)
        else:
            l2.append(0)

    c = 0
    for i in range(len(rvector)):
        c += l1[i]*l2[i]
        
    cosine = c / float((sum(l1)*sum(l2))**0.5)

    return cosine

def get_jds(user_data,total_experience):
    connection = sqlite3.connect("solvathon.db")
    cursor = connection.cursor()
    connection.row_factory = sqlite3.Row
    cursor.execute("select * from JOB_DESCRIPTION;")
    jobs = cursor.fetchall()
    maxx_score = 0.065
    suggestions= {}
    for job in jobs:
        if job[3] <= total_experience:
            curr_score = get_similarity(user_data, job[2])
            print("score"+str(curr_score))
            if curr_score > maxx_score:
                #print(job)
                temp = {}
                temp['title'] = job[1]
                temp['description'] = job[2]
                suggestions[job[0]] = temp
    connection.close()
    #print(suggestions)        
    return suggestions

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


with open("tokenizer.pkl", "rb") as file:
  tokenizer = pickle.load(file)

model = tf.keras.models.load_model("model.hdf5")

def get_positivity(sentences, types):
  sequences = tokenizer.texts_to_sequences(sentences)
  padded = pad_sequences(sequences, maxlen=200)
  ans = [i[2] for i in model.predict(padded)]
  similarity_score = [get_similarity(sentences[i], word_data[types[i]]) for i in range(2)]

  final_ans = []
  for i in range(2):
    if (ans[i]+similarity_score[i])*5 < 5:
      final_ans.append((ans[i]+similarity_score[i])*5)
    else:
      final_ans.append(5)
  
  marks_list={}
  for item in types:
    marks_list[item]=0.0

  sentences[0]=final_ans[0]
  sentences[1]=final_ans[1]
  for i in range(12):
    marks_list[types[i]]=marks_list[types[i]]+float(sentences[i])
    

  for item in marks_list.keys():
    if(item in types[:2]):
      #marks_list[item]="{:.2f}/5".format(marks_list[item]/3.0)
      marks_list[item]=str(round(marks_list[item]/3.0))
    else:
      #marks_list[item]="{:.2f}/5".format(marks_list[item]/2.0)
      marks_list[item]=str(round(marks_list[item]/2.0))

  return marks_list

def get_job_titles():
    connection = sqlite3.connect("solvathon.db")
    cursor = connection.cursor()
    cursor.execute("SELECT jd_no,title  FROM JOB_DESCRIPTION;")
    jobTitles=cursor.fetchall()
    job_list=[]
    job_ids=[]
    job_list+=[i[1] for i in jobTitles]
    job_ids+=[i[0] for i in jobTitles]
    print(job_list,job_ids)
    connection.close()
    return job_ids,job_list