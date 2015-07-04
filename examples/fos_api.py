#!/usr/bin/env python
import requests, sys
from pprint import pprint

# API class to access FOS REST API
class FGT(object):
    """
    Base class to provide access to FGT APIs:
        . Monitor API
        . CMDB API
    Script will start a session by login into the FGT
    All subsequent calls will use the session's cookies and CSRF token
    """
    def __init__(self, host):
        self.host = host
        self.url_prefix = 'https://' + self.host
        self.session = requests.session() # use single session for all requests

    def update_csrf(self):
        # Retrieve server csrf and update session's headers
        for cookie in self.session.cookies:
            if cookie.name == 'ccsrftoken':
                csrftoken = cookie.value[1:-1] # token stored as a list
                self.session.headers.update({'X-CSRFTOKEN': csrftoken})

    def login(self, name, key):
        url = self.url_prefix + '/logincheck'
        res = self.session.post(url,
                                data='username=' + name + '&secretkey=' + key,
                                verify = False)

        if res.text.find('error') != -1:
            # Found some error in the response, consider login failed
            print 'LOGIN fail'
        else:
            print 'LOGIN succeed'

        # Update session's csrftoken
        self.update_csrf()

    def logout(self):
        url = self.url_prefix + '/logout'
        res = self.session.post(url)
        print 'LOGOUT'

    def get(self, url_postfix, params=None, data=None, verbose=True):
        url = self.url_prefix + url_postfix
        res = self.session.get(url, params=params, data=data)
        self.update_csrf() # update session's csrf
        return self.check_response(res, verbose)

    def post(self, url_postfix, params=None, data=None, verbose=True):
        url = self.url_prefix + url_postfix
        res = self.session.post(url, params=params, data=`data`)
        self.update_csrf() # update session's csrf
        return self.check_response(res, verbose)

    def put(self, url_postfix, params=None, data=None, verbose=True):
        url = self.url_prefix + url_postfix
        res = self.session.put(url, params=params, data=`data`)
        self.update_csrf() # update session's csrf
        return self.check_response(res, verbose)

    def delete(self, url_postfix, params=None, data=None, verbose=True):
        url = self.url_prefix + url_postfix
        res = self.session.delete(url, params=params, data=`data`)
        self.update_csrf() # update session's csrf
        return self.check_response(res, verbose)

    def get_v1(self, url_postfix, params=None, data=None, verbose=True):
        url = self.url_prefix + url_postfix
        # Pass 'request' or 'json' data as parameters for V1
        payload = params
        if params:
            if 'request' in params:
                payload = 'request' + '=' + `params['request']`
            elif 'json' in params:
                payload = 'json' + '=' + `params['json']`

        # Send request
        res = self.session.get(url, params=payload, data=`data`)
        self.update_csrf() # update session's csrf
        return self.check_response(res, verbose)

    def post_v1(self, url_postfix, params=None, data=None, verbose=True):
        url = self.url_prefix + url_postfix
        # Pass 'request' or 'json' data as parameters for V1
        payload = params
        if params:
            if 'request' in params:
                payload = 'request' + '=' + `params['request']`
            elif 'json' in params:
                payload = 'json' + '=' + `params['json']`

        # Send request
        res = self.session.post(url, params=payload, data=`data`)
        self.update_csrf() # update session's csrf
        return self.check_response(res, verbose)

    def put_v1(self, url_postfix, params=None, data=None, verbose=True):
        url = self.url_prefix + url_postfix
        # Pass 'request' or 'json' data as parameters for V1
        payload = params
        if params:
            if 'request' in params:
                payload = 'request' + '=' + `params['request']`
            elif 'json' in params:
                payload = 'json' + '=' + `params['json']`

        # Send request
        res = self.session.put(url, params=payload, data=`data`)
        self.update_csrf() # update session's csrf
        return self.check_response(res, verbose)

    def delete_v1(self, url_postfix, params=None, data=None, verbose=True):
        url = self.url_prefix + url_postfix
        # Pass 'request' or 'json' data as parameters for V1
        payload = params
        if params:
            if 'request' in params:
                payload = 'request' + '=' + `params['request']`
            elif 'json' in params:
                payload = 'json' + '=' + `params['json']`

        # Send request
        res = self.session.delete(url, params=payload, data=`data`)
        self.update_csrf() # update session's csrf
        return self.check_response(res, verbose)

    def check_response(self, response, verbose=True):
        if verbose:
            print '{0} {1}'.format(response.request.method,
                                   response.request.url)

        # Check response status, content and compare with original request
        if response.status_code == 200:
            # Success code, now check json response
            try:
                # Retrieve json data
                res = response.json()
            except:
                if verbose:
                    print 'Fail invalid JSON response'
                    print response.text
                return False

            else:
                # Check if json data is empty
                if not res:
                    if verbose:
                        print "JSON data is empty"
                        print response.text
                    return False

                # Check status
                if 'status' in res:
                    if res['status'] != 'success':
                        if verbose:
                            print 'JSON error {0}\n{1}'.format(res['error'], res)
                        return False

                # Check http_status if any
                if 'http_status' in res:
                    if res['http_status'] != 200:
                        if verbose:
                            print 'JSON error {0}\n{1}'.format(res['error'], res)
                        return False

                # Check http method
                if 'http_method' in res:
                    if res['http_method'] != response.request.method:
                        if verbose:
                            print 'Incorrect METHOD request {0},\
                                  response {1}'.format(response.request.method,
                                                       res['http_method'])
                        return False

                # Check results
                if 'results' in res:
                    #print res['results']
                    if not res['results']:
                        if verbose:
                            print 'Results is empty'
                        return False

                # Check vdom

                # Check path

                # Check name

                # Check action

                # All pass
                if verbose:
                    print 'Succeed with status: {0}'.format(response.status_code)
                    pprint(res)
                return True
        else:
            try:
                # Retrieve json data
                res = response.json()
            except:
                pass
                if verbose:
                    print 'Fail with status: {0}'.format(response.status_code)
            else:
                pass
                if verbose:
                    print 'Fail with status: {0}'.format(response.status_code)
                    #print response.json()
            finally:
                if verbose:
                    print response.text
                return False

if __name__ == '__main__':
    # Parse for command line argument for fgt ip
    if len(sys.argv) != 3:
        # Requires fgt ip and vdom
        print "Please specify fgt ip address and vdom"
        exit()
    ip = sys.argv[1]
    vdom = sys.argv[2]

    # Login into the FGT
    fgt = FGT(ip)
    fgt.login('admin','')

    # Example of CMDB API requests
    fgt.get('/api/v2/cmdb')

    # Uncomment below to run other sample requests
    """
    fgt.get('/api/v2/cmdb/firewall/address', params={"action":"schema", "vdom":vdom})
    fgt.get('/api/v2/cmdb/firewall/address', params={"action":"default", "vdom":vdom})
    fgt.get('/api/v2/cmdb/firewall/address', params={"vdom":vdom})
    fgt.post('/api/v2/cmdb/firewall/address', params={"vdom":vdom},
                                              data={"json":{"name":"attacker1",
                                                            "subnet":"1.1.1.1 255.255.255.255"}},
                                              verbose=True)
    fgt.post('/api/v2/cmdb/firewall.service/custom', params={"vdom":vdom},
                                                     data={"json":{"name":"server1_port",
                                                                   "tcp-portrange":80}},
                                                     verbose=True)
    fgt.put('/api/v2/cmdb/firewall/address/address1', params={"vdom":vdom},
                                              data={"json":{"name":"address2"}})
    fgt.post('/api/v2/cmdb/firewall/policy', params={"vdom":vdom},
                                             data={"json":{"policyid":0,
                                                           "srcintf":[{"name":"lan"}],
                                                           "srcaddr":[{"name":"all"}],
                                                           "dstintf":[{"name":"wan1"}],
                                                           "dstaddr":[{"name":"all"}],
                                                           "service":[{"name":"ALL"}],
                                                           "schedule":"always",
                                                           "action":"accept"}})
    fgt.put('/api/v2/cmdb/firewall/policy/1', params={"vdom":vdom,"action":"move", "after":2})
    fgt.delete('/api/v2/cmdb/firewall/address/address2', params={"vdom":vdom})
    fgt.delete('/api/v2/cmdb/firewall/address', params={"vdom":vdom})
    """

    # Example of Monitor API requests
    # Uncomment below to run other sample requests
    """
    fgt.get('/api/v2/monitor')
    fgt.get('/api/v2/monitor/firewall/policy', params={"vdom":vdom})
    fgt.post('/api/v2/monitor/firewall/policy/clear_counters', params={"vdom":vdom, "policy":"[4,7]"})
    fgt.get('/api/v2/monitor/firewall/session-top', params={"report_by":"source",
                                                            "sort_by":"bytes",
                                                            "vdom":vdom})
    fgt.get('/api/v2/monitor/firewall/session', params={"vdom":vdom,
                                                        "ip_version":"ipboth",
                                                        "start":0,
                                                        "count":1,
                                                        "summary":True})
    """

    # Always logout after testing is done
    fgt.logout()

