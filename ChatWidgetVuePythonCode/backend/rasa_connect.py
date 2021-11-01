# import string
# import random
# import requests
# import json

# def id_gen(size=6, chars=string.ascii_uppercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))

# rasa_url="https://ffa0-103-206-135-160.ngrok.io/webhooks/rest/webhook"
# data = '{"sender":"UserA","message":"apply for job"}'
# reply=requests.post(url = rasa_url, data = data)
# print(reply.text)
# data = reply.json()
# data=data[0]
# print(data)
# text=data['text']
# if('buttons' in data):
#     suggestion=[]
#     for items in data['buttons']:
#         suggestion.append(items['title'])
    
#     print(json.dumps({"suggestion":suggestion, "respMessage":text}))
# else:
#     print(json.dumps({"respMessage":text}))


from flask import Flask
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)

@app.route('/get', methods = ['GET'])
def hello():
    questions=["First question","Second question","Third question","Fourth question","Fifth question",
                "Sixth question","Seventh question","Eight question","Nine question","Tenth question",]
    return json.dumps(questions)
  
if __name__ == "__main__":
  app.run(port=5001)