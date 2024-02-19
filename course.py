import ydb
import os

driver_config = ydb.DriverConfig(
    endpoint=os.getenv('YDB_ENDPOINT'), 
    database=os.getenv('YDB_DATABASE'),
    credentials=ydb.iam.ServiceAccountCredentials.from_file("key.json")
)
driver = ydb.Driver(driver_config)
driver.wait(fail_fast=True, timeout=5)
pool = ydb.SessionPool(driver)
TABLENAME = os.getenv('TABLENAME')


def get_course(vacancy: str):
        text = f"SELECT link FROM {TABLENAME} WHERE title = '{vacancy}';"
        res = pool.retry_operation_sync(lambda s: s.transaction().execute(
            text,
            commit_tx=True,
            settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
        ))
        if any(res[0].rows):
            return res[0].rows[0]['link']
        else:
            print(f"no such vacancy as {vacancy} in db")
            return []

def handler(event, context):
    print(f"event {event}")
    if 'params' in event:
        if 'vacancyTitle' in event['params']:
            d = {"python-developer-course": "Python Developer", 
                "data-analyst-course": "Data Analyst", 
                "data-scientist-course": "Data Scientist",
                "frontend-developer-course": "Frontend Developer",
                "java-developer-course": "Java Developer",
                "ml-engineer-course": "ML Engineer"
            }
            vac_button = event['params']['vacancyTitle']
            print(f"vac_button {vac_button}")
            vac = d[vac_button]
            с = get_course(vac)
            print(f"с {с}")
            return {
                'statusCode': 200,
                'body': с
            }
    return {
        'statusCode': 200,
        'body': 'Hello World!',
    }