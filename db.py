import os
import requests
import json 


class DatabaseUtils:
    def __init__(self, user_id: int):
        self.user_id = user_id

    def create_user(self):
        r = requests.post("https://d5dd8h3anuqsgucmove7.apigw.yandexcloud.net/users/new_user", data=json.dumps({
        "search_stage": "title",
        "id": self.user_id
        }), headers={'Content-Type': 'application/json'})
        if r.status_code != 200:
            print(f"during user creation someting wenth horribly wrong: {r.content}")
    
    def get_user_data(self):
        res = requests.get(f"https://d5dd8h3anuqsgucmove7.apigw.yandexcloud.net/users/{self.user_id}")
        if res.status_code == 200:
            return json.loads(res.content.decode("utf-8"))
        else:
            return []

    def get_user_status(self):
        user_data = self.get_user_data()
        if user_data:
            return user_data['search_stage']
        else:
            return []

    def get_user_location(self):
        user_data = self.get_user_data()
        if user_data:
            if 'location' in user_data:
                return user_data['location']
            else:
                return []
        else:
            return []

    def update_user_vacancy(self, vacancy: str):
        r = requests.put(f"https://d5dd8h3anuqsgucmove7.apigw.yandexcloud.net/users/{self.user_id}", data=json.dumps({
            "search_stage": "job_mode",
            "vacancy": vacancy
            }), headers={'Content-Type': 'application/json'})
        if r.status_code == 200:
            print(f"updated user {self.user_id} vacancy title sucessfully")
        else:
            print(f"during update for user {self.user_id} vacancy title smth went wrong: {r.content}")

    def update_user_job_mode(self, permanent: bool):
        r = requests.put(f"https://d5dd8h3anuqsgucmove7.apigw.yandexcloud.net/users/{self.user_id}", data=json.dumps({
            "search_stage": "salary",
            "permanent": permanent
            }), headers={'Content-Type': 'application/json'})
        if r.status_code == 200:
            print(f"updated user {self.user_id} job mode sucessfully")
        else:
            print(f"during update of job mode for {self.user_id}  smth went wrong: {r.content}")

    def update_user_job_expectations(self, min_salary: str):
        r = requests.put(f"https://d5dd8h3anuqsgucmove7.apigw.yandexcloud.net/users/{self.user_id}", data=json.dumps({
            "search_stage": "location",
            "min_salary": min_salary
            }), headers={'Content-Type': 'application/json'})
        if r.status_code == 200:
            print(f"updated user {self.user_id} min salary sucessfully")
        else:
            print(f"during update of salary for {self.user_id} smth went wrong: {r.content}")

    def update_user_location(self, location: str):
        r = requests.put(f"https://d5dd8h3anuqsgucmove7.apigw.yandexcloud.net/users/{self.user_id}", data=json.dumps({
            "search_stage": "over",
            "location": location
            }), headers={'Content-Type': 'application/json'})
        if r.status_code == 200:
            print(f"updated user {self.user_id} location sucessfully")
        else:
            print(f"during update of location for {self.user_id} smth went wrong: {r.content}")

    def set_final_status(self):
        r = requests.put(f"https://d5dd8h3anuqsgucmove7.apigw.yandexcloud.net/users/{self.user_id}", data=json.dumps({
            "search_stage": "set"
            }), headers={'Content-Type': 'application/json'})
        if r.status_code == 200:
            print(f"updated user {self.user_id} final status sucessfully")
        else:
            print(f"during update of final status for {self.user_id} smth went wrong: {r.content}")