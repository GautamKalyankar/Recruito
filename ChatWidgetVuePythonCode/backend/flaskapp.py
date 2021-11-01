from sqlite3.dbapi2 import Cursor
from functions import get_resume_data,get_similarity,get_jds,get_questions,get_positivity,get_job_titles
from flask import Flask, jsonify, request
#from flask_marshmallow import Marshmallow
from werkzeug.wrappers import response
from werkzeug.utils import secure_filename
from flask_cors import CORS
import requests,json
import sqlite3
import random,string

app= Flask(__name__)
CORS(app)
#ma = Marshmallow(app)

user_data={}
jd_data={}
jd_flag=0
rc_flag=0
jd_selected={}
candidate_selected={}
all_candidates=[]
question_index=0
question_list=[]
scale_list=[]
category_list=[]
user_answers=[]
rasa_url="http://localhost:5005/webhooks/rest/webhook"
user="adwq1"
user_info={}

def check_if_present(rdata,value):
    if(value in rdata and type(rdata[value])==list):
        return ", ".join(rdata[value])
    else:
        return "NA"

def send_rasa_recruiter(input_message):
    global rc_flag,candidate_selected,all_candidates
    print(input_message)
    if(rc_flag==1):
        job_ids,job_titles=get_job_titles()
        job_titles=[item.lower() for item in job_titles]
        rc_job=input_message.lower()
        print(rc_job,job_titles)
        if(rc_job not in job_titles):
            text="Sorry, there are no candidates yet who have applied for this job."
        else:
            candidate_selected["job_title"]=rc_job
            candidate_selected["job_id"]=job_ids[job_titles.index(rc_job)]
            rc_flag=2
            data1 = json.dumps({"sender":user,"message":input_message})
            reply=requests.post(url = rasa_url, data = data1)
            print(reply.text)
            data = reply.json()
            data=data[0]
            print(data)
            text=data['text']
        return {"respMessage": text}
    elif(rc_flag==2):
        numbers=[int(s) for s in input_message.split() if s.isdigit()]
        rc_years=numbers[0]
        connection=sqlite3.connect("solvathon.db")
        cursor=connection.cursor()
        cursor.execute('''SELECT ap_id, name,skills,years_of_experience FROM APPLICANT WHERE years_of_experience>=? 
                        AND ap_id IN (SELECT ap_id FROM APPLICANT_SCORE WHERE job_id=?);''',
                        (rc_years,candidate_selected["job_id"]))
        all_candidates=cursor.fetchall()
        connection.close()
        print(all_candidates)
        data1 = json.dumps({"sender":user,"message":input_message})
        reply=requests.post(url = rasa_url, data = data1)
        print(reply.text)
        data = reply.json()
        data=data[0]
        print(data)
        print(all_candidates)
        # text=data['text']
        rc_flag=3
        if(len(all_candidates)==0):
            text="Sorry, there are no candidates who meet the given criteria for this job."
            rc_flag=4
            return {"respMessage": text}
        else:
            suggestion=[]
            text="Here is the list of suitable candidates.\nPlease select a candidate to view his/her details:"
            for item in all_candidates:
                suggestion.append({"label":str(item[1]),"value":str(item[0])})
            return {"suggestion":suggestion, "respMessage":text}
    elif(rc_flag==3):
        if(len(all_candidates)==0):
            text="Sorry, there are no candidates who meet the given criteria for this job."
            rc_flag=4
            return {"respMessage": text}
        else:
            if(input_message.lower()=="no"):
                suggestion=[]
                text="Please select a candidate to view his/her details:"
                for item in all_candidates:
                    suggestion.append({"label":str(item[1]),"value":str(item[0])})
                return {"suggestion":suggestion, "respMessage":text}
            else:
                for item in all_candidates:
                    #print(item[0])
                    if(str(input_message)==str(item[0])):
                        print("found")
                        candidate_selected["ap_id"]=item[0]
                        candidate_selected["name"]=item[1]
                        candidate_selected["skills"]=item[2]
                        candidate_selected["years_of_experience"]=item[3]
                        break;
                text="Applicant Name: %s\n\nSkills:\n %s\n\nYears of Experience:\n%s\n"%(str(candidate_selected["name"]),str(candidate_selected["skills"]),str(candidate_selected["years_of_experience"]))
                connection=sqlite3.connect("solvathon.db")
                cursor=connection.cursor()
                cursor.execute('''SELECT leadership_score,communication_score,time_score,team_score,general_score 
                                FROM APPLICANT_SCORE WHERE ap_id=?;''',(candidate_selected["ap_id"],))
                scores=cursor.fetchall()
                connection.close()
                print(scores)
                temp_text=""
                chartLabel=[]
                chartData=[scores[0][0],scores[0][1],scores[0][2],scores[0][3],scores[0][4]]
                for i in range(len(chartData)):
                    chartData[i]=str(int(chartData[i]*20))
                if('hr' in candidate_selected["job_title"]):
                    chartLabel=["Leadership Management","Communication Skills","Time Management",
                                "Team Mangement","Flexibility Adaptability"]
                else:
                    chartLabel=["Leadership Management","Communication Skills","Time Management",
                                "Team Mangement","Problem-Solving Decision-Making"]
                text=text+"^Do you want to shortlist this candidate?"
                suggestion=[]
                suggestion.append({"label":"Yes","value":"Yes"})
                suggestion.append({"label":"No","value":"No"})
                return {"suggestion":suggestion, 
                        "respMessage":text,
                        "attachment": {
                            "type": "chart",
                            "chartLabel": chartLabel,
                            "chartData": chartData
                        }
                }
    else:
        print(input_message,rc_flag)
        data1 = json.dumps({"sender":user,"message":input_message})
        reply=requests.post(url = rasa_url, data = data1)
        print(reply.text)
        data = reply.json()
        data=data[0]
        print(data)
        text=data['text']
        if(rc_flag==0):
            rc_flag=1
        return {"respMessage": text}

def set_answer():
    suggestion=[]
    ans=["Strongly Agree","Agree","Neutral","Disagree","Strongly Disagree"]
    for item in ans:
        suggestion.append({"label":str(item),"value":str(item)})
    return suggestion

def get_scale_score(input,scale_type):
    ans=["Strongly Agree","Agree","Neutral","Disagree","Strongly Disagree"]
    score=0
    if(scale_type=="1"):
        score=5-ans.index(input)
    elif(scale_type=="-1"):
        score=1+ans.index(input)
    return str(score)


def get_rasa_reply(input_message,toself=""):
    global jd_data,user_data,jd_flag,jd_selected,question_index,question_list,scale_list
    if(input_message=="Done Matching"):
        jd_flag=1
        text=""
        data1 = json.dumps({"sender":user,"message":input_message})
        reply=requests.post(url = rasa_url, data = data1)
        print(reply.text)
        data = reply.json()
        data=data[0]
        print(data)
        text=data['text']
        suggestion=[]
        jd_data=get_jds(user_data["user_data"],user_data["total_experience"])
        if len(jd_data) == 0:
            text="Sorry, there are no jobs available matching your profile right now.\n Thank you for using Recruito."
            return {"respMessage":text}
        for key,value in jd_data.items():
            suggestion.append({"label":str(value['title']),"value":str(value['title'])})
        return {"suggestion":suggestion, "respMessage":text}

    elif jd_flag==1:
        text=""
        suggestion=[]
        if(input_message.lower()=="no"):
            text="Please select which job you want to apply for:"
            for key,value in jd_data.items():
                suggestion.append({"label":str(value['title']),"value":str(value['title'])})
            return {"suggestion":suggestion, "respMessage":text}
        else:
            for key,value in jd_data.items():
                if(input_message==value["title"]):
                    jd_selected={"id":key,"title": value["title"],"description":value["description"]}
                    text=value["title"]+"\n"+value["description"]+"\n\n"+"Do you want to apply for this job?"
                    suggestion.append({"label":"Yes","value":"Yes"})
                    suggestion.append({"label":"No","value":"No"})
                    return {"suggestion":suggestion, "respMessage":text}
            text="CodeBreak"
            return {"respMessage":text}
    elif(jd_flag==3):
        text=""
        suggestion=set_answer()
        if(question_index==0):
            text="Q %s] "%(question_index+1)+question_list[question_index]
            question_index=question_index+1
            return {"respMessage":text}
        
        elif(question_index<12):
            prev_scale_type=scale_list[question_index-1]
            if(prev_scale_type!="0"):
                user_answers.append(get_scale_score(input_message,prev_scale_type))
            else:
                user_answers.append(input_message)
            text="Q %s] "%(question_index+1)+question_list[question_index]
            scale_type=scale_list[question_index]
            question_index=question_index+1
            if(scale_type=="0"):
                return {"respMessage":text}
            else:
                return {"suggestion":suggestion, "respMessage":text}
        else:
            prev_scale_type=scale_list[question_index-1]
            if(prev_scale_type!=0):
                user_answers.append(get_scale_score(input_message,prev_scale_type))
            else:
                user_answers.append(input_message)
            jd_flag=4
            print(user_answers)
            text="Thank you for applying!\nYour application for %s has been successfully received by us.\nWe will get back to you shortly.\n\nBelow is your L0 score card."%jd_selected["title"]
            final_marks=get_positivity(user_answers,category_list)
            chartLabel=[]
            chartData=[]
            connection=sqlite3.connect("solvathon.db")
            cursor=connection.cursor()
            for key,value in final_marks.items():
                # text=text+"%s\n Score : %s\n"%(key,value)
                key=key.replace("em So","em-So")
                key=key.replace("on Ma","on-Ma")
                chartLabel.append(key)
                chartData.append("%s"%(int(value)*20))
            print(chartLabel)
            if(user_info["role"]=="hr"):
                cursor.execute('''INSERT INTO APPLICANT_SCORE 
                (ap_id,job_id,leadership_score,communication_score,time_score,team_score,general_score)
                VALUES (?,?,?,?,?,?,?)''',(user_info["ap_id"],user_info["job_id"],
                final_marks["Leadership and Management"],final_marks["Communication Skills"],
                final_marks["Time Management"],final_marks["Team Mangement"],
                final_marks["Flexibility Adaptability"]))
            else:
                cursor.execute('''INSERT INTO APPLICANT_SCORE 
                (ap_id,job_id,leadership_score,communication_score,time_score,team_score,general_score)
                VALUES (?,?,?,?,?,?,?)''',(user_info["ap_id"],user_info["job_id"],
                final_marks["Leadership and Management"],final_marks["Communication Skills"],
                final_marks["Time Management"],final_marks["Team Mangement"],
                final_marks["Problem Solving Decision Making"]))
            connection.commit()
            connection.close()
            print(final_marks)
            #upload to db
            return {
                "respMessage": text,
                "attachment": {
                    "type": "chart",
                    "chartLabel": chartLabel,
                    "chartData": chartData
                }
            }
            # return {"respMessage":text}

    elif(jd_flag==4):
        text="Thank you have a nice day!"
        return {"respMessage":text}

    else:
        data1 = json.dumps({"sender":user,"message":input_message})
        reply=requests.post(url = rasa_url, data = data1)
        print(reply.text)
        data = reply.json()
        data=data[0]
        print(data)
        text=data['text']
        text=text.replace("\\n","\n")
        print(text)
        if(toself=="GotResume"):
            return {"toself":toself,"respMessage":text}
        elif('buttons' in data):
            suggestion=[]
            for items in data['buttons']:
                #suggestion.append(items['title'])
                suggestion.append({"label":str(items['title']),"value":str(items['title'])})
            
            return {"suggestion":suggestion, "respMessage":text}
        else:
            return {"respMessage":text}




@app.route('/get',methods = ['GET'])
def get_message():
    return jsonify({"Hello":"World"})

@app.route('/post', methods = ['POST'])
def add_message():
    print(request.data)
    global jd_flag, question_index,question_list,scale_list,category_list,jd_selected,user_answers,user,user_info
    input_message=request.json['message']
    if(type(input_message)!=str):
        input_message=input_message['value']
        if(input_message.lower()=="yes" and jd_flag==1):
            
            user_info["job_id"]=jd_selected["id"]
            
            role="dev"
            if("hr" in jd_selected["title"].lower()):
                role="hr"
            user_info["role"]=role
            question_list,scale_list,category_list=get_questions(role)
            print(question_list,scale_list,category_list)
            jd_flag=2
        elif(input_message.lower()=="start" and jd_flag==2):
            jd_flag=3
            question_index=0
    else:
        if(input_message.lower()=="start" and jd_flag==2):
            jd_flag=3
            question_index=0
        elif("hi "in input_message.lower()):
            jd_flag=0
            user=''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            print(user)
            jd_selected={}
            user_answers=[]

    return jsonify(get_rasa_reply(input_message))

@app.route('/postresume', methods = ['POST'])
def add_resume():
    print(request.data)
    resume=request.files['file']
    resume.save(secure_filename(resume.filename))
    print(get_resume_data(resume.filename))
    rdata=get_resume_data(resume.filename)
    
    skills = check_if_present(rdata,"skills")
    experience= check_if_present(rdata,"experience")

    name=rdata['name']
    email=rdata['email']
    mobile=rdata['mobile_number']
    years_of_experience=rdata["total_experience"]
    
    connection=sqlite3.connect('solvathon.db')
    cursor=connection.cursor()
     
    global user_info
    cursor.execute("INSERT INTO APPLICANT (mobile,name,email,experience,skills,years_of_experience) values (?,?,?,?,?,?)",(mobile,name,email,experience,skills,years_of_experience))
    connection.commit()
    cursor.execute("SELECT ap_id FROM APPLICANT ORDER BY ap_id DESC LIMIT 1")
    user_info["ap_id"]=cursor.fetchall()[0][0]
    connection.close()
    BotMessage= "Resume"

    #years_of_experience=4
    print(years_of_experience)

    global user_data
    user_data={"user_data":skills+" "+experience,"total_experience":years_of_experience}

    return jsonify(get_rasa_reply(BotMessage,"GotResume"))


@app.route('/post2recruiter', methods = ['POST'])
def send_for_recruiter():
    global rc_flag
    print(request.data)
    input_message=request.json['message']
    if(type(input_message)!=str):
        input_message=input_message['value']
    if(input_message.lower()=="hi recruiter"):
        rc_flag=0
    if(rc_flag==3 and input_message.lower()=="yes"):
        input_message="select candidate"
        rc_flag=4
    return jsonify(send_rasa_recruiter(input_message))




if(__name__ == "__main__"):
    app.config['UPLOAD_FOLDER']='resumes/'
    app.run(debug=True)