from restkit import request, Resource

try:
    import simplejson as json
except ImportError:
    import json # py2.6 only

class FG_Login(Resource):
    def __init__(self, **kwargs):
        url = "http://192.168.4.13"
        super(FG_Login, self).__init__(url, follow_redirect=True,
                                        max_follow_redirect=10, **kwargs)

    def login(self, query):
        return self.get('login.json', q=query)

    def request(self, *args, **kwargs):
        resp = super(FG_Login, self).request(*args, **kwargs)
        return json.loads(resp.body_string())

if __name__ == "__main__":
    s = TwitterSearch()
    print s.search("gunicorn")