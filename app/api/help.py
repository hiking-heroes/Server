from flask import redirect

from . import api


@api.route("/help")
def help_api():
    redirect("https://github.com/hiking-heroes/Server/blob/master/README.md")
