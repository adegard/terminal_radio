#!/usr/bin/env python3
import json
import os
import subprocess

LIBRARY_FILE = "radio_library.json"

# ANSI colors
C_RESET = "\033[0m"
C_TITLE = "\033[1;36m"
C_MENU = "\033[1;33m"
C_OPTION = "\033[1;32m"
C_ERROR = "\033[1;31m"

DEFAULT_STATIONS = {
    "Radio Swiss Jazz": "https://stream.srg-ssr.ch/m/rsj/mp3_128"
}

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
    print(f"{C_TITLE}▶ Playing stream:{C_RESET} {url}\n")
    print("Press CTRL+C to return to menu.\n")

    try:
        subprocess.run(
            ["mpv", "--no-terminal", "--really-quiet", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except KeyboardInterrupt:
        print(f"\n{C_ERROR}Stopped playback.{C_RESET}\n")

def add_station(library):
    name = input("Station name: ").strip()
    url = input("Stream URL: ").strip()
    if name and url:
        library[name] = url
        save_library(library)
        print(f"{C_OPTION}Added '{name}' to library.{C_RESET}")
    else:
        print(f"{C_ERROR}Invalid input.{C_RESET}")

def remove_station(library):
    print(f"\n{C_MENU}Stations in library:{C_RESET}")
    names = list(library.keys())

    for i, name in enumerate(names, start=1):
        print(f"{C_OPTION}{i}.{C_RESET} {name}")

    choice = input("\nSelect station number to remove: ").strip()
    if not choice.isdigit():
        print(f"{C_ERROR}Invalid choice.{C_RESET}")
        return

    idx = int(choice) - 1
    if idx < 0 or idx >= len(names):
        print(f"{C_ERROR}Invalid number.{C_RESET}")
        return

    name = names[idx]
    del library[name]
    save_library(library)
    print(f"{C_ERROR}Removed '{name}' from library.{C_RESET}")

def choose_station(library):
    print(f"\n{C_MENU}Available stations:{C_RESET}")
    for i, name in enumerate(library.keys(), start=1):
        print(f"{C_OPTION}{i}.{C_RESET} {name}")

    choice = input("\nChoose a station number: ").strip()
    if not choice.isdigit():
        print(f"{C_ERROR}Invalid choice.{C_RESET}")
        return

    idx = int(choice) - 1
    if idx < 0 or idx >= len(library):
        print(f"{C_ERROR}Invalid number.{C_RESET}")
        return

    name = list(library.keys())[idx]
    play_stream(library[name])

def main():
    library = load_library()

    while True:
        print(f"{C_TITLE}\n=== Internet Radio Player ==={C_RESET}")
        print(f"{C_OPTION}1{C_RESET}. Play Radio Swiss Jazz")
        print(f"{C_OPTION}2{C_RESET}. Play a station from library")
        print(f"{C_OPTION}3{C_RESET}. Add a new station")
        print(f"{C_OPTION}4{C_RESET}. Remove a station")
        print(f"{C_OPTION}5{C_RESET}. Exit\n")

        choice = input("Select an option: ").strip()

        if choice == "1":
            play_stream(DEFAULT_STATIONS["Radio Swiss Jazz"])
        elif choice == "2":
            choose_station(library)
        elif choice == "3":
            add_station(library)
        elif choice == "4":
            remove_station(library)
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print(f"{C_ERROR}Invalid option.{C_RESET}")

if __name__ == "__main__":
    main()
