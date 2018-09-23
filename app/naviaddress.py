import requests


main_url = "https://staging-api.naviaddress.com/api/v1.5/"


def create_user_profile(data: dict) -> requests.Response:
    return requests.post(url=main_url + "Profile", data=data)
