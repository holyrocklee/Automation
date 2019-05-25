import requests


class requestutil:
    def __init__(self, url=None, data=None, headers=None):
        self.headers = headers
        self.url = url
        self.data = data

    def setData(self, data):
        self.data = data

    def setUrl(self, url):
        self.url = url

    def setHeaders(self, headers):
        self.headers = headers

    def get(self):
        return requests.get(self.url, self.data, headers=self.headers)

    def post(self, json=True):
        return requests.post(self.url, self.data, json, headers=self.headers)

    def request(self, method, json=True, isjson=True):
        if method == 'get':
            response = self.get()
        else:
            response = self.post()
        if isjson:
            return response.json()
        return response.text
