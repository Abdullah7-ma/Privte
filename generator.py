import random
import threading
import curses
from concurrent.futures import ThreadPoolExecutor

def generate_random_number(digits):
    start = 10**(digits-1) if digits > 1 else 0
    end = 10**digits - 1
    return str(random.randint(start, end)).zfill(digits)

def write_chunk(chunk, filename, lock, stdscr, row):
    with lock:
        with open(filename, 'w') as file:
            for number in chunk:
                file.write(number + '\n')
    stdscr.addstr(row, 0, f"{len(chunk)} numbers written to {filename}\n")
    stdscr.refresh()

def write_random_numbers_to_file(digits, count, filename, stdscr, start_row):
    lock = threading.Lock()
    chunk_size = max(1, count // 4)  
    chunks = []

    for _ in range(4):
        chunk = [generate_random_number(digits) for _ in range(chunk_size)]
        chunks.append(chunk)

    with ThreadPoolExecutor(max_workers=4) as executor:
        for i, chunk in enumerate(chunks):
            row = start_row + i
            executor.submit(write_chunk, chunk, filename, lock, stdscr, row)

def main(stdscr):
    curses.curs_set(1)  
    stdscr.clear()

    curses.echo()  

    stdscr.addstr(0, 0, "Enter the number of digits: ")
    stdscr.refresh()
    digits = int(stdscr.getstr().decode('utf-8').strip())

    stdscr.addstr(1, 0, "Enter the number of random numbers to save: ")
    stdscr.refresh()
    count = int(stdscr.getstr().decode('utf-8').strip())

    stdscr.addstr(2, 0, "Enter the filename to save the numbers: ")
    stdscr.refresh()
    filename = stdscr.getstr().decode('utf-8').strip()

    curses.noecho()  

    stdscr.clear()
    stdscr.addstr(0, 0, f"Generating and writing {count} random numbers with {digits} digits to {filename}...\n")
    stdscr.refresh()

    write_random_numbers_to_file(digits, count, filename, stdscr, 3)

    stdscr.addstr(7, 0, f"{count} random numbers with {digits} digits saved to {filename}.\n")
    stdscr.addstr(8, 0, "Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
