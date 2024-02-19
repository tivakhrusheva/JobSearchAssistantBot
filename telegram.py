from texts import texts as contents
import os
import json
import urllib3
import typing as tp
import requests


START_TEXT: str = contents["start"]
TOKEN = os.getenv('TOKEN')
URL = f"https://api.telegram.org/bot{TOKEN}/"
http = urllib3.PoolManager()


class CommandHandler:
    def __init__(self, chat_id: str):
        self.chat_id = chat_id
        self.tg_inst = TelegramUtils(self.chat_id)
    
    def send_start_message(self):
        url = URL + "sendMessage"
        data = {
                "chat_id": self.chat_id,
                "text": START_TEXT,
                'parse_mode':  'Markdown',
        }
        r = requests.get(url, params=data, headers={'Content-Type': 'application/json'})
        if r.status_code != 200:
           print(f"something went horribly wrong during sending start message: {r.content}")

    def send_search_question(self, question_text: str):
        data = {
                'chat_id': self.chat_id,
                'text': question_text,
                'parse_mode': 'Markdown',
        }
        url = URL + "sendMessage"
        r = requests.get(url, params=data, headers={'Content-Type': 'application/json'})
        if r.status_code != 200:
           print(f"something went horribly wrong during sending question message: {r.content}")

    def send_text_n_buttons(self, text: str, button_list: tp.List[str], callbacks: tp.List[str]):
        #buttons = self.tg_inst.create_answer_keyboard(buttons=button_list, callbacks=callbacks)
        data = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': 'Markdown',
                'reply_markup': self.tg_inst.create_answer_keyboard(buttons=button_list, callbacks=callbacks)
        }
        url = URL + "sendMessage"
        r = requests.get(url, params=data, headers={'Content-Type': 'application/json'})
        if r.status_code != 200:
            print(f"something went horribly wrong during sending text w buttons: {r.content}")

    def send_statistics(self, vacancy: str, permanent_mode, min_salary: str, location: str,):
        mode = "full-time" if permanent_mode else "part-time"
        stats = f"""
        **Current search setup**:\n
        Vacancy: {vacancy}\n
        Minimum salary: {min_salary}\n
        Location: {location}\n
        Mode of work: {mode}\n
     
        """ 
        data = {
                'chat_id': self.chat_id,
                'text': stats,
                'parse_mode': 'Markdown',
        }
        url = URL + "sendMessage"
        r = requests.get(url, params=data, headers={'Content-Type': 'application/json'})
        if r.status_code != 200:
            print(f"something went horribly wrong during stats sending: {r.content}")

    def send_document(self, bytes_content):
        url = URL + "sendDocument"
        r = requests.post(url, data={'chat_id': self.chat_id}, files={'document': bytes_content})
        if r.status_code != 200:
            print(f"something went horribly wrong during doc sending: {r.content}")


class TelegramUtils:
    def __init__(self, chat_id: str):
        self.chat_id = chat_id

    @staticmethod
    def create_answer_keyboard(buttons: tp.List[str], callbacks: tp.List[str] = None):
        arr = []
        for button, callback in zip(buttons, callbacks):
            arr.append({ "text": button, "callback_data": callback})
        return json.dumps(
                { 
                    "inline_keyboard":[
                        arr
                    ]
                }
            )
