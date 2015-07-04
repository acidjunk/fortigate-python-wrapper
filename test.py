import requests, sys

URL='http://192.168.4.13'
session = requests.session()
res = session.post(URL + '/logincheck', data='username=admin&secretkey=', verify = False)
print res.text

if res.text.find('error') != -1:
    # Found some error in the response, consider login failed
    print 'LOGIN fail'
    sys.exit()
else:
    print 'LOGIN succeed'

# Retrieve server csrf and update session's headers
for cookie in session.cookies:
    if cookie.name == 'ccsrftoken':
        csrftoken = cookie.value[1:-1] # token stored as a list
        print "using crsftoken: %s" % csrftoken
        session.headers.update({'X-CSRFTOKEN': csrftoken})

res = session.get(URL + '/api/v2/cmdb/firewall/policy')
print res.text