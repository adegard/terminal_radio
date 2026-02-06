#!/usr/bin/env python3
import json
import os
import subprocess

LIBRARY_FILE = "radio_library.json"

# Default station to include
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
    print(f"\nStarting stream: {url}\nPress CTRL+C to stop.\n")
    try:
        subprocess.run(["mpv", url])
    except KeyboardInterrupt:
        print("\nStopped playback.")

def add_station(library):
    name = input("Station name: ").strip()
    url = input("Stream URL: ").strip()
    if name and url:
        library[name] = url
        save_library(library)
        print(f"Added '{name}' to library.")
    else:
        print("Invalid input.")

def choose_station(library):
    print("\nAvailable stations:")
    for i, name in enumerate(library.keys(), start=1):
        print(f"{i}. {name}")

    choice = input("\nChoose a station number: ").strip()
    if not choice.isdigit():
        print("Invalid choice.")
        return

    idx = int(choice) - 1
    if idx < 0 or idx >= len(library):
        print("Invalid number.")
        return

    name = list(library.keys())[idx]
    play_stream(library[name])

def main():
    library = load_library()

    while True:
        print("\n=== Internet Radio Player ===")
        print("1. Play Radio Swiss Jazz")
        print("2. Play a station from library")
        print("3. Add a new station")
        print("4. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            play_stream(DEFAULT_STATIONS["Radio Swiss Jazz"])
        elif choice == "2":
            choose_station(library)
        elif choice == "3":
            add_station(library)
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
