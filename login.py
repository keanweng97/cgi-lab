#!/usr/bin/env python3

import json, os, sys, re
import secret, templates

posted_bytes = os.environ.get("CONTENT_LENGTH", 0)
if posted_bytes:
    posted = sys.stdin.read(int(posted_bytes))
    username, password = '', ''
    cred = re.match("username=(\w+)&password=(\w+)", posted)
    if cred:
        username = cred.groups()[0]
        password = cred.groups()[1]

    if(username == secret.username and password == secret.password):
        print("Set-Cookie: login=true")
        print(f"Set-Cookie: username={username}")
        print(f"Set-Cookie: password={password}")
        print(templates.secret_page(username, password))
    else:
        print(templates.after_login_incorrect())

else:
    cookies = os.environ.get('HTTP_COOKIE', 0)
    if cookies:
        cookies = cookies.split(';')
        if 'login=true' in cookies:
            username = 'admin'
            password = 'admin'
            for cookie in cookies:
                if "username" in cookie:
                    username = cookie.split('=')[1]
                if "password" in cookie:
                    password = cookie.split('=')[1]
            print(templates.secret_page(username, password))
    else:
        print(templates.login_page())

    if os.environ['QUERY_STRING']:
        print(f"<p> QUERY_STRING: {os.environ['QUERY_STRING']} </p>")
        print("<ul>")
        for parameter in os.environ['QUERY_STRING'].split('&'):
            (name, value) = parameter.split('=')
            print(f"<li><em>{name}</em> = {value}</li>")
        print("</ul>")