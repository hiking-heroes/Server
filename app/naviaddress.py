import requests


main_url = "https://staging-api.naviaddress.com/api/v1.5"


def post_req(method: str, data: dict) -> requests.Response:
    return requests.post(url=main_url + method, data=data)
