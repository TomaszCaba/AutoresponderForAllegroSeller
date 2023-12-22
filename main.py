import base64
from datetime import datetime, timedelta
import hashlib
import secrets
import string
from time import sleep
import requests
import json
import urllib3
urllib3.disable_warnings()

with open("app_info.json", "r") as app_info_file:
    info = json.load(app_info_file)
    CLIENT_ID = info["CLIENT_ID"]
    CLIENT_SECRET = info["CLIENT_SECRET"]
REDIRECT_URI = "https://localhost:8923"
AUTH_URL = "https://allegro.pl.allegrosandbox.pl/auth/oauth/authorize"
TOKEN_URL = "https://allegro.pl.allegrosandbox.pl/auth/oauth/token"
AUTORESPONSE = "Witaj, otrzymaliśmy twoją wiadomość. Zajmiemy się nią tak szybko jak tylko to będzie możliwe."


def get_threads(token):
    try:
        url = "https://api.allegro.pl.allegrosandbox.pl/messaging/threads"
        headers = {'Authorization': 'Bearer ' + token, 'Accept': "application/vnd.allegro.public.v1+json"}
        threads = requests.get(url, headers=headers, verify=False)
        print(threads.json())
        return threads
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def generate_code_verifier():
    code_verifier = ''.join((secrets.choice(string.ascii_letters) for _ in range(40)))
    return code_verifier


def generate_code_challenge(code_verifier):
    hashed = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    base64_encoded = base64.urlsafe_b64encode(hashed).decode('utf-8')
    code_challenge = base64_encoded.replace('=', '')
    return code_challenge


def get_access_token():
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    authorization_redirect_url = (f"{AUTH_URL}?response_type=code&client_id={CLIENT_ID}"
                                  f"&redirect_uri={REDIRECT_URI}&code_challenge_method=S256"
                                  f"&code_challenge={code_challenge}")
    print("Zaloguj do Allegro - skorzystaj z url w swojej "
          "przeglądarce oraz wprowadź authorization code ze zwróconego url: ")
    print(f"--- {authorization_redirect_url} ---")
    authorization_code = input("Podaj kod: ")
    try:
        data = {'grant_type': 'authorization_code', 'code': authorization_code,
                'redirect_uri': REDIRECT_URI, 'code_verifier': code_verifier}
        access_token_response = requests.post(TOKEN_URL, data=data, verify=False,
                                              allow_redirects=False)
        response_body = access_token_response.json()
        return response_body
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def get_next_token(token):
    try:
        data = {'grant_type': 'refresh_token', 'refresh_token': token, 'redirect_uri': REDIRECT_URI}
        access_token_response = requests.post(TOKEN_URL, data=data, verify=False,
                                              allow_redirects=False, auth=(CLIENT_ID, CLIENT_SECRET))
        new_token = json.loads(access_token_response.text)
        return new_token
    except requests.exceptions.HTTPError as err:
        print("Maybe try to remove token.json file")
        raise SystemExit(err)


def save_token_to_file(token):
    with open("token.json", "w") as token_response_w:
        print(datetime.now())
        token['generated_on'] = str(datetime.now())
        token_response_w.write(json.dumps(token, indent=4))


def main():
    with open("token.json", "r") as token_response:
        lines = token_response.readlines()
        print(f"lynie = {lines}")
        if not lines:
            response = get_access_token()
            access_token = response['access_token']
            save_token_to_file(response)
        else:
            last_token = json.loads(''.join(lines))
            refresh_token = last_token['refresh_token']
            new_token = get_next_token(refresh_token)
            save_token_to_file(new_token)
            access_token = new_token['access_token']
    print(f"access token = {access_token}")
    threads = get_threads(access_token).json()['threads']
    print(get_all_messages(access_token, threads[0]['id'])['messages'])
    print(threads)
    # mark_as_unread(access_token, threads[0]["id"])
    threads = get_threads(access_token).json()['threads']
    for thread in threads:
        print(type(thread['read']))
        if not thread['read']:
            if was_last_message_created_in_24h(access_token, thread['id']):
                if get_all_messages(access_token, thread['id'])['messages'][0]['author']['isInterlocutor']:
                    print("Wiadomość do " + thread['interlocutor']['login'], end=" ")
                    send_autoresponse(access_token, thread['id'])
                    mark_as_read(access_token, threads[0]["id"])


def send_autoresponse(token, thread_id):
    try:
        url = f"https://api.allegro.pl.allegrosandbox.pl/messaging/threads/{thread_id}/messages"
        headers = {'Authorization': 'Bearer ' + token, 'Accept': "application/vnd.allegro.public.v1+json",
                   'Content-Type': 'application/vnd.allegro.public.v1+json'
                   }
        autoresponse_result = requests.post(url, headers=headers, data=json.dumps({
                        "text": AUTORESPONSE,
                        "attachments": []
                   }), verify=False)
        if autoresponse_result.status_code == 201:
            print("została wysłana")
        else:
            print("nie została wysłana")
        sleep(1)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def mark_as_unread(token, thread_id):
    try:
        url = f"https://api.allegro.pl.allegrosandbox.pl/messaging/threads/{thread_id}/read"
        headers = {'Authorization': 'Bearer ' + token, 'Accept': "application/vnd.allegro.public.v1+json"}
        response = requests.put(url, headers=headers, data=json.dumps({"read": False}), verify=False)
        print(response)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def mark_as_read(token, thread_id):
    try:
        url = f"https://api.allegro.pl.allegrosandbox.pl/messaging/threads/{thread_id}/read"
        headers = {'Authorization': 'Bearer ' + token, 'Accept': "application/vnd.allegro.public.v1+json"}
        response = requests.put(url, headers=headers, data=json.dumps({"read": True}), verify=False)
        print(response)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def get_all_messages(token, thread_id):
    try:
        url = f"https://api.allegro.pl.allegrosandbox.pl/messaging/threads/{thread_id}/messages"
        headers = {'Authorization': 'Bearer ' + token, 'Accept': "application/vnd.allegro.public.v1+json"}
        response = requests.get(url, headers=headers, verify=False)
        print(response)
        return response.json()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def was_last_message_created_in_24h(token, thread_id):
    last_message = get_all_messages(token, thread_id)['messages'][0]['createdAt']
    last_message_time = datetime.strptime(last_message, "%Y-%m-%dT%H:%M:%S.%fZ")
    time_from_last_message = datetime.now() - last_message_time
    if time_from_last_message > timedelta(hours=24):
        print("Last message was created in 24 hours")
        return True
    print("Last message was not created in 24")
    return False


def was_last_message_created_by_client(token, thread_id):
    last_message = get_all_messages(token, thread_id)['messages'][0]['author']['isInterlocutor']
    if last_message:
        return True


if __name__ == "__main__":
    main()
