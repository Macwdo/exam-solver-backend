# It is Proxy lambda to prevent blocking requeusts
import requests


def lambda_handler(event, context):
    url = event["url"]
    method = event["method"]
    headers = event["headers"]
    body = event["body"]

    response = requests.request(method, url, headers=headers, data=body)

    return response.json()
