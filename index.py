import os
import requests
from telegram import CommandHandler, TelegramUtils
from job_search_api import search
import json
from texts import texts as contents
from db import DatabaseUtils
import random

RESPONSE_WAITING_MODE: bool = False
SEND_DOCUMENT_MODE: bool = False

class Stages:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.tg_helper = CommandHandler(self.chat_id)
        self.db_user = DatabaseUtils(self.chat_id)
    
    def permanent_specifier(self, message_text: str = None):
        """Updates vacancy, asks for mode of work"""
        print("permanent_specifier launched")
        if message_text:
            print(f"we've received title which is {message_text}")
            self.db_user.update_user_vacancy(vacancy=message_text)
        self.tg_helper.send_text_n_buttons(text=contents["mode_spec"], button_list=["Full time", "Part time"], callbacks=["full_time", "part_time"])
        RESPONSE_WAITING_MODE = True
    
    def min_salary_specifier(self, message_text: str = None):
        """Updates mode, asks for desired minimum salary"""
        if message_text:
            mode = "true" if message_text == "full_time" else "false"
            print(f"we've received mode which is {mode}")
            self.db_user.update_user_job_mode(permanent=mode)
        self.tg_helper.send_search_question(question_text=contents["salary_spec"])
        RESPONSE_WAITING_MODE = True
    
    def location_specifier(self, message_text: str = None):
        """Updates minimum salary, asks for desired location"""
        if message_text:
            try:
                message_text = int(message_text)
            except ValueError:
                message_text = int(0)
            print(f"we've received salary which is {message_text}")
            self.db_user.update_user_job_expectations(min_salary=message_text)
        self.tg_helper.send_text_n_buttons(text=contents["location"],button_list=["Great Britain", "Germany", "France", "Spain", "Italy", "USA", "Brazil", "Canada"], callbacks=["gb", "de", "fr", "es", "it", "us", "br", "ca"])
        #self.tg_helper.send_search_question(question_text=contents["location"])
        RESPONSE_WAITING_MODE = True
    
    def final_specifier(self, message_text: str = None):
        """Updates received location, sends confirmation"""
        print(f"we've received location which is {message_text}")
        if message_text:
            self.db_user.update_user_location(location=message_text)
    

def handler(event, context):
    # return {
    #     'statusCode': 200,
    #     'body': 'Hello World!',
    # }
    global RESPONSE_WAITING_MODE
    global SEND_DOCUMENT_MODE
    if 'body' in event:
        message = json.loads(event['body'])
        print(f"message = {message}")
        if 'message' in message.keys():
            print("!Got message in message.keys()!")
            chat_id = message['message']['chat']['id']
            message_text = message['message']['text']
            message_proc = Stages(chat_id)

            if message_text == "/start":
                print(f"text is /start")
                message_proc.tg_helper.send_start_message()
            
            if message_text == "/reset":
                print(f"text is /reset")
                requests.delete(f"https://d5dd8h3anuqsgucmove7.apigw.yandexcloud.net/users/{chat_id}")
                message_proc.tg_helper.send_search_question(question_text="Search settings were reset.")
            
            if message_text == "/recommend_course":
                print(f"text is /recommend_course")
                message_proc.tg_helper.send_text_n_buttons(text=contents["vacancy_choice"], button_list=["Python Developer", "Data Analyst", "Data Scientist", 'Frontend Developer', 'Java Developer', 'ML Engineer'], callbacks=['python-developer-course', 'data-analyst-course', 'data-scientist-course', 'frontend-developer-course', 'java-developer-course', 'ml-engineer-course'])

            if message_text == "/useful":
                print(f"text is /useful")
                SEND_DOCUMENT_MODE = True
                message_proc.tg_helper.send_text_n_buttons(text=contents["vacancy_choice"], button_list=["Python Developer", "Data Analyst", "Data Scientist", 'Frontend Developer', 'Java Developer', 'ML Engineer'], callbacks=['python-developer', 'data-analyst', 'data-scientist', 'frontend-developer', 'java-developer', 'ml-engineer'])
            
            if message_text == "/get_top_salary_cities":
                print(f"text is /get_top_salary_cities")
                r = requests.get("https://d5dd8h3anuqsgucmove7.apigw.yandexcloud.net/salaries/cities")
                if r.status_code == 200:
                    list_cities = json.loads(r.content.decode("utf-8"))
                    newlist = sorted(list_cities, key=lambda d: d['salary'], reverse=True) 
                    top_5 = newlist[:5]
                    s = ""
                    for idx, c in enumerate(top_5):
                        s += f"{(idx+1)}. City: {str(c['city'])}\nMedian salary: {str(c['salary'])} RUB\n"
                    message_proc.tg_helper.send_search_question(question_text="Here is the top-5 list of Russian cities with largest median salary (in RUB) in 2023:")
                    message_proc.tg_helper.send_search_question(question_text=s)
                else:
                    print(f"smth went wrong during retrieving top cities by salary")
                    message_proc.tg_helper.send_search_question(question_text="Sorry, something went wrong during retrieving information.. We're already working to fix it, please try later.")
            

            if message_text == "/get_top_companies":
                print(f"text is /get_top_companies")
                r = requests.get("https://d5dd8h3anuqsgucmove7.apigw.yandexcloud.net/salaries/companies")
                if r.status_code == 200:
                    list_companies = json.loads(r.content.decode("utf-8"))
                    newlist = sorted(list_companies, key=lambda d: d['salary'], reverse=True) 
                    top_5 = newlist[:5]
                    s = ""
                    for idx, c in enumerate(top_5):
                        s += f"{(idx+1)}. Company: {str(c['company_name'])}\nMedian salary: {str(c['salary'])} RUB\n"
                    message_proc.tg_helper.send_search_question(question_text="Here is the top-5 list of Russian companies with largest median salary (in RUB) in 2023:")
                    message_proc.tg_helper.send_search_question(question_text=s)
                else:
                    print(f"smth went wrong during retrieving top companies by salary")
                    message_proc.tg_helper.send_search_question(question_text="Sorry, something went wrong during retrieving information.. We're already working to fix it, please try later.")
            
            if message_text == "/interview_advice":
                print(f"text is /interview_advice")
                r = requests.get("https://d5dd8h3anuqsgucmove7.apigw.yandexcloud.net/materials/interview")
                if r.status_code == 200:
                    text_to_send = r.content.decode("utf-8")
                    message_proc.tg_helper.send_search_question(question_text=text_to_send)
                else:
                    message_proc.tg_helper.send_search_question(question_text=contents['error'])

            if message_text == "/search":
                print(f"text is /search")
                if not any(message_proc.db_user.get_user_status()):
                    message_proc.db_user.create_user()
                user_data = message_proc.db_user.get_user_data()
                if "vacancy" in user_data:
                    search_res = search(vacancy_desc=user_data['vacancy'], location=user_data['location'], min_salary=user_data['min_salary'], full_time=user_data['permanent'])
                    if search_res:
                        message_proc.tg_helper.send_search_question(question_text="Here are the search results:")
                        message_proc.tg_helper.send_search_question(question_text=search_res)
                    else:
                        message_proc.tg_helper.send_search_question(question_text="Sorry, something went wrong with the search.. Our specialists are already working to fix this issue, please, try later")
                    # if None in user_data.values():
                    #     first_none = [key for key in user_data.keys() if user_data[key] is None][0]
                    #     print(f"first_none {first_none}")
                    #     if first_none == "vacancy":
                    #         message_proc.tg_helper.send_search_question(question_text=contents["job_spec"])
                    #     if first_none == "permanent":
                    #         message_proc.permanent_specifier()
                    #     if first_none == "min_salary":
                    #         message_proc.min_salary_specifier()
                    #     if first_none == "location":
                    #         message_proc.location_specifier()
                    # else: 
                    #     message_proc.tg_helper.send_text_n_buttons(text=contents["job_spec_repeat"], button_list=["Yes", "No"], callbacks=["new_search", "old_search"])
                else:
                    message_proc.tg_helper.send_search_question(question_text=contents["job_spec"])
                RESPONSE_WAITING_MODE = True
            if (not message_text.startswith("/")) & (message_proc.db_user.get_user_status() == "title"):
                message_proc.permanent_specifier(message_text)
            if (not message_text.startswith("/")) & (message_proc.db_user.get_user_status() == "salary"):
                message_proc.location_specifier(message_text)
            # if (RESPONSE_WAITING_MODE == False) & (not message_text.startswith("/")) & ((message_proc.db_user.get_user_status() == "location") | (message_proc.db_user.get_user_status() == "over")):
            #     message_proc.final_specifier(message_text)
            #     user_data = message_proc.db_user.get_user_data()
            #     if user_data['location'] != str(user_data['min_salary']):
            #         if len(user_data['location']) > 2:
            #             message_proc.tg_helper.send_search_question(question_text="The search with the following settings was successfully set up:")
            #             user_data = message_proc.db_user.get_user_data()
            #             message_proc.tg_helper.send_statistics(*user_data.values())
            #             message_proc.db_user.set_final_status()

            print(f"message_text is {message_text}, RESPONSE_WAITING_MODE is {RESPONSE_WAITING_MODE}, CURRENT_STAGE = {message_proc.db_user.get_user_status()} ")
    
        if 'callback_query' in message.keys():
            print("callback_query in message.keys()")
            chat_id = message['callback_query']['from']['id']
            message_proc = Stages(chat_id)
            if 'data' in message['callback_query']:
                if message['callback_query']['data'] in ['python-developer', 'data-analyst', 'data-scientist', 'frontend-developer', 'java-developer', 'ml-engineer']:
                    career = message['callback_query']['data']
                    random_n = random.randint(1, 3)
                    r = requests.get(f'https://d5dd8h3anuqsgucmove7.apigw.yandexcloud.net/materials/{career}/{random_n}')
                    if r.status_code == 200:
                        print(f"file for career {career} and user {chat_id} found successfully")
                        message_proc.tg_helper.send_search_question(question_text=contents['file_success'])
                        message_proc.tg_helper.send_document(r.content)
                    else:
                        print(f"error during file retraction attempt for career {career} and user {chat_id}: {r.content}")
                elif message['callback_query']['data'] in ['python-developer-course', 'data-analyst-course', 'data-scientist-course', 'frontend-developer-course', 'java-developer-course', 'ml-engineer-course']:
                    print(f"message['callback_query']['data'] = {message['callback_query']['data']}")
                    r = requests.get(f"https://d5dd8h3anuqsgucmove7.apigw.yandexcloud.net/materials/courses/{message['callback_query']['data']}")
                    if r.status_code == 200:
                        message_proc.tg_helper.send_search_question(question_text=f"We recommend you this course:\n{r.content.decode('utf-8')}")
                elif message['callback_query']['data'] in ["gb", "de", "fr", "es", "it", "us", "br", "ca"]:
                    message_proc.final_specifier(message['callback_query']['data'])
                    user_data = message_proc.db_user.get_user_data()
                    #if user_data['location'] != str(user_data['min_salary']):
                        #if len(user_data['location']) > 2:
                    message_proc.tg_helper.send_search_question(question_text="The search with the following settings was successfully set up:")
                    user_data = message_proc.db_user.get_user_data()
                    message_proc.tg_helper.send_statistics(user_data['vacancy'], user_data['permanent'], user_data['min_salary'], user_data['location'])
                    message_proc.db_user.set_final_status()
                    search_res = search(vacancy_desc=user_data['vacancy'], location=user_data['location'], min_salary=user_data['min_salary'], full_time=user_data['permanent'])
                    print(f"search_res = {search_res}")
                    if search_res:
                        message_proc.tg_helper.send_search_question(question_text="Here are the search results:")
                        message_proc.tg_helper.send_search_question(question_text=search_res)
                    else:
                        message_proc.tg_helper.send_search_question(question_text="Sorry, something went wrong with the search.. Our specialists are already working to fix this issue, please, try later")
                else:
                    if (message_proc.db_user.get_user_status() == "job_mode"):
                        mode = message['callback_query']['data']
                        message_proc.min_salary_specifier(mode)
                    else:
                        if message['callback_query']['data'] == "new_search":
                            message_proc.tg_helper.send_search_question(question_text=contents["job_spec"])
                        if message['callback_query']['data'] == "old_search":
                            user_data = message_proc.db_user.get_user_data()
                            message_proc.tg_helper.send_statistics(*user_data.values())
    return {
        'statusCode': 200,
        'body': 'Hello World!',
    }