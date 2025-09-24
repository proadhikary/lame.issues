#!/usr/bin/env python3
import sys
import getpass
import signal
import time
import os
from getpass import getpass
from datetime import datetime
import urllib.request, urllib.parse, urllib.error, threading, webbrowser, ssl
import random

STATUS = 0
RESPONSE = 1
VERBOSE = False

def retry_request(func):
    """Decorator to retry network calls on timeout/URLError with backoff."""
    def wrapper(*args, **kwargs):
        retries = 3
        delay = 2
        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                print(f"[WARN] Network error: {e}. Retry {attempt+1}/{retries}...")
                time.sleep(delay)
                delay *= 2  # exponential backoff
        print("[ERROR] Request failed after retries.")
        return ""  # return empty so caller can handle gracefully
    return wrapper


class Proxy:
    proxy_set = {
        'btech': 22, 'dual': 62, 'diit': 21, 'faculty': 82, 'integrated': 21,
        'mtech': 62, 'phd': 61, 'retfaculty': 82, 'staff': 21, 'irdstaff': 21,
        'mba': 21, 'mdes': 21, 'msc': 21, 'msr': 21, 'pgdip': 21
    }
    google = 'http://www.google.com'

    def __init__(self, username, password, proxy_cat):
        self.username = username
        self.password = password
        self.proxy_cat = proxy_cat
        self.auto_proxy = "http://www.cc.iitd.ernet.in/cgi-bin/proxy." + proxy_cat

        # Set proxy host based on category
        if proxy_cat == 'research':
            self.proxy_host = 'xen03.iitd.ernet.in'
        else:
            self.proxy_host = f'proxy{Proxy.proxy_set[proxy_cat]}.iitd.ernet.in'

        self.urlopener = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=ssl._create_unverified_context()),
            urllib.request.ProxyHandler({'http': f'http://{self.proxy_host}:3128'})
        )

        self.proxy_page_address = f'https://{self.proxy_host}/cgi-bin/proxy.cgi'
        self.loggedout = True
        self.new_session_id()
        self.details()

    def is_connected(self):
        proxies = {'http': f'http://{self.proxy_host}:3128'}
        try:
            proxy_support = urllib.request.ProxyHandler(proxies)
            opener = urllib.request.build_opener(proxy_support)
            response = opener.open(Proxy.google, timeout=10).read().decode('utf-8')
        except Exception:
            return "Not Connected"
        if "<title>IIT Delhi Proxy Login</title>" in response:
            return "Login Page"
        elif "<title>Google</title>" in response:
            return "Google"
        else:
            return "Not Connected"

    def get_session_id(self):
        try:
            response = self.open_page(self.proxy_page_address)
        except Exception:
            return None
        check_token = 'sessionid" type="hidden" value="'
        token_index = response.index(check_token) + len(check_token)
        sessionid = response[token_index:token_index+16]
        return sessionid

    def new_session_id(self):
        self.sessionid = self.get_session_id()
        self.loginform = {
            'sessionid': self.sessionid,
            'action': 'Validate',
            'userid': self.username,
            'pass': self.password
        }
        self.logout_form = {
            'sessionid': self.sessionid,
            'action': 'logout',
            'logout': 'Log out'
        }
        self.loggedin_form = {
            'sessionid': self.sessionid,
            'action': 'Refresh'
        }

    def login(self):
        self.new_session_id()
        response = self.submitform(self.loginform)
        if "Either your userid and/or password does'not match." in response:
            return "Incorrect", response
        elif "You are logged in successfully as " + self.username in response:
            def ref():
                if not self.loggedout:
                    try:
                        res, _ = self.refresh()
                    except Exception as e:
                        print("[ERROR] Refresh failed:", e)
                        res = "Not Connected"
                    print("Refresh", datetime.now(), "Status:", res)
                    if res == 'Session Expired':
                        print("Session Expired. Please run the script again.")
                    else:
                        self.timer = threading.Timer(60.0, ref)
                        self.timer.daemon = True
                        self.timer.start()
            self.timer = threading.Timer(60.0, ref)
            self.timer.daemon = True
            self.timer.start()
            self.loggedout = False
            return "Success", response
        elif "already logged in" in response:
            return "Already", response
        elif "Session Expired" in response:
            return "Expired", response
        else:
            return "Not Connected", response

    def logout(self):
        self.loggedout = True
        response = self.submitform(self.logout_form)
        if "you have logged out from the IIT Delhi Proxy Service" in response:
            return "Success", response
        elif "Session Expired" in response:
            return "Expired", response
        else:
            return "Failed", response

    def refresh(self):
        response = self.submitform(self.loggedin_form)
        if "You are logged in successfully" in response:
            if "You are logged in successfully as " + self.username in response:
                return "Success", response
            else:
                return "Not Logged In", response
        elif "Session Expired" in response:
            return "Expired", response
        else:
            return "Not Connected", response

    def details(self):
        if VERBOSE:
            for property, value in vars(self).items():
                print(property, ": ", value)

    @retry_request
    def submitform(self, form):
        data = urllib.parse.urlencode(form).encode('utf-8')
        response = self.urlopener.open(
            urllib.request.Request(self.proxy_page_address, data=data),
            timeout=10
        ).read()
        return response.decode('utf-8')

    @retry_request
    def open_page(self, address):
        response = self.urlopener.open(address, timeout=10).read()
        return response.decode('utf-8')


def signal_handler(signal_number, frame):
    print('\nLogout', user.logout()[STATUS])
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
    n = len(sys.argv)
    if n < 3:
        print("\n\nUsage: python3 proxy.py username proxycat")
    else:
        uname = sys.argv[1]
        passwd = getpass()
        proxycat = sys.argv[2]
        user = Proxy(username=uname, password=passwd, proxy_cat=proxycat)
        login_status = user.login()[STATUS]
        print('\nLogin', login_status)
        signal.pause()
