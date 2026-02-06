#!/usr/bin/env python3
import json
import os
import subprocess
import curses

LIBRARY_FILE = "radio_library.json"

DEFAULT_STATIONS = {
    "Radio Swiss Jazz": "https://stream.srg-ssr.ch/m/rsj/mp3_128"
}

ASCII_HEADER = r"""
  ____       _ _        ____       _           
 |  _ \ __ _(_) | ___  |  _ \ __ _| | ___  ___ 
 | |_) / _` | | |/ _ \ | |_) / _` | |/ _ \/ __|
 |  _ < (_| | | |  __/ |  _ < (_| | |  __/\__ \
 |_| \_\__,_|_|_|\___| |_| \_\__,_|_|\___||___/
"""

def load_library():
    if not os.path.exists(LIBRARY_FILE):
        save_library(DEFAULT_STATIONS)
        return DEFAULT_STATIONS
    with open(LIBRARY_FILE, "r") as f:
        return json.load(f)

def save_library(library):
    with open(LIBRARY_FILE, "w") as f:
        json.dump(library, f, indent=4)

def play_stream(url):
    os.system("clear")
    print(f"▶ Playing stream: {url}\n")
    print("Press CTRL+C to return to menu.\n")

    try:
        subprocess.run(
            ["mpv", "--no-terminal", "--really-quiet", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except KeyboardInterrupt:
        print("\nStopped playback.\n")

def add_station(library, stdscr):
    curses.echo()
    stdscr.clear()
    stdscr.addstr("Add new station\n\n")
    stdscr.addstr("Name: ")
    name = stdscr.getstr().decode().strip()
    stdscr.addstr("URL: ")
    url = stdscr.getstr().decode().strip()
    curses.noecho()

    if name and url:
        library[name] = url
        save_library(library)
        stdscr.addstr(f"\nAdded '{name}' to library.\n")
    else:
        stdscr.addstr("\nInvalid input.\n")

    stdscr.addstr("\nPress any key to return...")
    stdscr.getch()

def remove_station(library, stdscr):
    names = list(library.keys())
    if not names:
        stdscr.addstr("\nLibrary is empty.\n")
        stdscr.addstr("\nPress any key to return...")
        stdscr.getch()
        return

    idx = menu(stdscr, names, title="Remove station")
    if idx is None:
        return

    name = names[idx]
    del library[name]
    save_library(library)

    stdscr.clear()
    stdscr.addstr(f"Removed '{name}' from library.\n")
    stdscr.addstr("\nPress any key to return...")
    stdscr.getch()

def choose_station(library, stdscr):
    names = list(library.keys())
    if not names:
        stdscr.addstr("\nLibrary is empty.\n")
        stdscr.addstr("\nPress any key to return...")
        stdscr.getch()
        return

    idx = menu(stdscr, names, title="Choose station")
    if idx is None:
        return

    play_stream(library[names[idx]])

def menu(stdscr, options, title="Menu"):
    curses.curs_set(0)
    idx = 0

    while True:
        stdscr.clear()
        stdscr.addstr(ASCII_HEADER + "\n", curses.color_pair(2))
        stdscr.addstr(f"=== {title} ===\n\n", curses.color_pair(3))

        for i, opt in enumerate(options):
            if i == idx:
                stdscr.addstr(f"> {opt}\n", curses.color_pair(1))
            else:
                stdscr.addstr(f"  {opt}\n")

        key = stdscr.getch()

        if key == curses.KEY_UP:
            idx = (idx - 1) % len(options)
        elif key == curses.KEY_DOWN:
            idx = (idx + 1) % len(options)
        elif key in (10, 13):  # Enter
            return idx
        elif key == 27:  # ESC to cancel
            return None

def main_menu(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)  # highlight
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)   # header
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # title

    library = load_library()

    while True:
        choice = menu(
            stdscr,
            [
                "Play Radio Swiss Jazz",
                "Play from library",
                "Add station",
                "Remove station",
                "Exit"
            ],
            title="Internet Radio Player"
        )

        if choice == 0:
            play_stream(DEFAULT_STATIONS["Radio Swiss Jazz"])
        elif choice == 1:
            choose_station(library, stdscr)
        elif choice == 2:
            add_station(library, stdscr)
        elif choice == 3:
            remove_station(library, stdscr)
        elif choice == 4:
            break

def main():
    curses.wrapper(main_menu)

if __name__ == "__main__":
    main()
