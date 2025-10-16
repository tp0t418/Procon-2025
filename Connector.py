import requests
import json

from Config import *

class Connector:
    def fetch_problem(question_id: str):
        if question_id == "":
            return
        
        headers = {"Authorization": TOKEN}
        res = requests.get(f"{URL}/question/{question_id}", headers=headers)
        print(LogHeader.OKCYAN + f"Status code: {res.status_code}")

        j_res = res.json()
        q_data = json.loads(j_res["question_data"])

        return q_data["field"]["entities"]

    def send_answer(question_id, ops):
        headers = {"Authorization": TOKEN}

        payload = {"question_id": question_id, "answer_data": {"ops": ops}}
        try:
            response = requests.post(f"{URL}/answer", json=payload, headers=headers)
            print("----------------------------------------")
            print(LogHeader.OKCYAN + f"Status code: {response.status_code}")
            print("----------------------------------------")
        except:
            print(LogHeader.FAIL + "Timed out!")
