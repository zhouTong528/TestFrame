import requests


class SendReportMessage:

    @staticmethod
    def send_message(data):
        url = ""
        params = {"text": {"content": data}, "msgtype": "text"}
        res = requests.post(url=url, json=params).json()



