import requests
import json


def search(vacancy_desc: str, location: str = None, what_exclude: str = None, min_salary: str = None, full_time: str = None):
    full_time = 1 if full_time == "true" else 0
    r = requests.get(f"https://d5dd8h3anuqsgucmove7.apigw.yandexcloud.net/vacancies/vacancy?country={location}&vacancy={vacancy_desc}&full_time={full_time}&salary_min={min_salary}&remote=false")
    if r.status_code == 200:
        res = json.loads(r.content.decode("utf-8"))['results'][:5]
        print(f"!!!results {res}")
        s = ""
        for j in res:
            s+=f"Title: {j['title']}\nJob Description: {j['description']}\nCompany: {j['company']['display_name']}\nMin salary: {j['salary_min'] if 'salary_min' in j else '-'}\nMax salary: {j['salary_max'] if 'salary_max' in j else '-'}\nCompany domain: {j['label'] if 'label' in j else '-'}\nVacancy Placed: {j['created']}\n\n"
        return s    
    else:
        print(f"ERROR! {r.content}")
        return []
