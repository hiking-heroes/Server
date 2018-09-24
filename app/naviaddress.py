import requests

main_url = "https://staging-api.naviaddress.com/api/v1.5"


def get_req(method: str, params: dict = None, **kwargs) -> requests.Response:
    return requests.get(url=main_url + method, params=params, **kwargs)


def post_req(method: str, data: dict = None, json: dict = None,
             **kwargs) -> requests.Response:
    return requests.post(url=main_url + method, data=data, json=json, **kwargs)


def put_req(method: str, data: dict = None, **kwargs) -> requests.Response:
    return requests.put(url=main_url + method, data=data, **kwargs)


def delete_req(method: str, **kwargs) -> requests.Response:
    return requests.delete(url=main_url + method, **kwargs)
