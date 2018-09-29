import requests


def send_notification(server_key: str, registration_ids: list,
                      notification: dict = None):
    requests.post(
        url="https://fcm.googleapis.com/fcm/send",
        headers={
            "Authorization": "key={0}".format(server_key),
            "Content-Type": "application/json"
        },
        json={
            "registration_ids": registration_ids,
            "notification": notification
        }
    )
