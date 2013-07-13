import sys
import flask
import subprocess

from flask import Flask
from linkedin import linkedin
from flask import render_template, request, redirect, url_for

host = subprocess.check_output('hostname').strip()
try:
    dns = subprocess.check_output('dnsdomainname').strip()
    if dns:
        host = host + '.' + dns
    else:
        host = subprocess.check_output('hostname -i').strip()
except OSError:
    pass  # this happens when you are on a computer not set up as a server
app = Flask(__name__)


def initialize():
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    USER_TOKEN = ''
    USER_SECRET = ''
    RETURN_URL = ''

    authentication = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET,
                                                              USER_TOKEN, USER_SECRET,
                                                              RETURN_URL, linkedin.PERMISSIONS.enums.values())
    application = linkedin.LinkedInApplication(authentication)
    application.get_profile()


@app.route("/")
def start():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
