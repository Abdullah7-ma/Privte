#!/usr/bin/python3

import Brute_Tik 
import DDOS
import generator
import threading
import time
import curses

def logo1(stdscr):
    logo = """
      
    ██████╗ ██████╗ ██╗   ██╗████████╗███████╗ ████████╗██╗██╗  ██╗
    ██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝ ╚══██╔══╝██║██║ ██╔╝
    ██████╔╝██████╔╝██║   ██║   ██║   █████╗█████╗██║   ██║█████╔╝ 
    ██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝╚════╝██║   ██║██╔═██╗ 
    ██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗    ██║   ██║██║  ██╗
    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝    ╚═╝   ╚═╝╚═╝  ╚═╝

                            Dev by : Abdullah Bawhab
                            Contact(Instagram) [etuadmin]
                                    [Priv_V1]
    """
    stdscr.clear()
    stdscr.addstr(0, 0, logo, curses.color_pair(1))
    stdscr.refresh()

def bruteforce(stdscr):
    stdscr.clear()
    stdscr.addstr(3, 0, "Executing bruteforce attack...", curses.color_pair(2))
    stdscr.refresh()
    # Replace with your implementation of bruteforce attack
    time.sleep(3)  # Placeholder for demonstration
    stdscr.clear()
    stdscr.addstr(4, 0, "Bruteforce attack completed.", curses.color_pair(2))
    stdscr.refresh()
    stdscr.getch()

def ddos_attack(stdscr):
    stdscr.clear()
    stdscr.addstr(3, 0, "Executing DDOS attack...", curses.color_pair(4))
    stdscr.refresh()
    # Replace with your implementation of DDOS attack
    time.sleep(3)  # Placeholder for demonstration
    stdscr.clear()
    stdscr.addstr(4, 0, "DDOS attack completed.", curses.color_pair(4))
    stdscr.refresh()
    stdscr.getch()

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

    logo1(stdscr)

    stdscr.addstr(15, 0, "Choose an option:", curses.color_pair(1))
    stdscr.addstr(16, 0, "1. Bruteforce", curses.color_pair(1))
    stdscr.addstr(17, 0, "2. Generate Password", curses.color_pair(1))
    stdscr.addstr(18, 0, "3. DDOS Attack", curses.color_pair(1))
    stdscr.addstr(19, 0, "4. Exit", curses.color_pair(1))
    stdscr.refresh()

    while True:
        stdscr.move(20, 0)
        stdscr.clrtoeol()
        stdscr.addstr(20, 0, "Enter your choice: ", curses.color_pair(1))
        stdscr.refresh()
        choice = stdscr.getch() - ord('0')
        if choice == 1:
            Brute_Tik.main()  # Call main function from Brute_Tik module
        elif choice == 2:
            generator.main(stdscr)  # Call main function from generator module with stdscr argument
        elif choice == 3:
            DDOS.main(stdscr)  # Call main function from DDOS module with stdscr argument
        elif choice == 4:
            break
        else:
            stdscr.addstr(21, 0, "Invalid choice. Please enter a valid option (1-4).", curses.color_pair(4))
            stdscr.refresh()
            stdscr.getch()
            stdscr.move(21, 0)
            stdscr.clrtoeol()

if __name__ == "__main__":
    curses.wrapper(main)
