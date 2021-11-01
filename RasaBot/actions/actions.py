# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import json

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher, tracker, domain):
        print("text ", tracker.latest_message['text'])

        if "applicant" in tracker.latest_message['text']:
            print("applicant")
            persona='applicant'
            dispatcher.utter_message(text="Hey I am Recruito! Welcome to the LTI Campus Portal. Please share your resume, and I'll find the perfect job for you!")
        elif "recruiter" in tracker.latest_message['text']:
            print("recruiter")
            persona='recruiter'
            dispatcher.utter_message(text="Hey I am Recruito! How can I help you today?")
        else:
            print("null")
            persona='null'
            dispatcher.utter_message(text="Hey I am Recruito! Welcome to the LTI Campus Portal. Please share your resume, and I'll find the perfect job for you!")

        role = tracker.get_slot('persona')
        print("role: ", role)

        return [SlotSet('persona',persona)]


# class ActionFetchQuestions(Action):
#     def name(self):
#         return 'action_fetch_questions'
#     def run(self, dispatcher, tracker, domain):
#         url = "http://c215-1-186-178-30.ngrok.io/get"
#         status = requests.get(url).json
#         print(status)
#         return []

#['first question"]