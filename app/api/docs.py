from flask import redirect

from . import api


@api.route("/help")
def help_api():
    return redirect(
        "https://github.com/hiking-heroes/Server#Документация-api"
    )
