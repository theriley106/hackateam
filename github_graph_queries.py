#!flask/bin/python
from flask import Flask, jsonify
import requests
import urllib
import json
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

app = Flask(__name__)

def fetch_github_data():
    github_url = "https://api.github.com/graphql"
    #json = { "query" : "{ viewer { login } }" }
    json = {"query" : "query{ viewer{ "
                "login,"
                "repositories {"
                  "totalCount"
                "},"
                "contributedRepositories {"
                  "totalCount"
                "},"
                "pinnedRepositories {"
                  "totalCount"
                "},"
                "followers {"
                  "totalCount"
                "},"
                "issues {"
                 " totalCount"
                "},"
                "organizations {"
                 " totalCount"
                "}"
              "}}"
            }
    api_token = "dde7406d2642258b686aa2ef8dcaebd187da8acb"
    headers = {"Authorization": "token %s" % api_token}
    github_data = requests.post(url = github_url, json = json, headers = headers)

    return github_data.text

@app.route('/')
def index():
    return fetch_github_data()

if __name__ == '__main__':
    app.run(debug=True, port=50981
    )
