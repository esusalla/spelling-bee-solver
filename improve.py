#!/usr/bin/env python

import json
import os
import re
import sys

import requests

import solve


def get_game_data():
    url = "https://www.nytimes.com/puzzles/spelling-bee"

    # Setup adapter to automatically retry failed requests
    codes = [413, 429, 500, 502, 503, 504]
    retry = requests.urllib3.util.Retry(total=4, backoff_factor=1, status_forcelist=codes)
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)

    # Create session and mount adapter
    session = requests.Session()
    session.mount("", adapter)

    req = session.get(url)
    game_data = re.search(r"window.gameData = (.*?)</script>", req.text)[1]
    return json.loads(game_data)["yesterday"]


def update_words(guesses, answers, words):
    # Words present in official answers but missing from guesses are added
    to_add = answers - guesses
    # Words present in guesses but missing from official answers are removed
    to_remove = guesses - answers

    words.update(to_add)
    words.difference_update(to_remove)

    with open(f"{BASE_PATH}/words.txt", "w") as outfile:
        for word in sorted(list(words)):
            outfile.write(word + "\n")

    # Return added / removed words for writing to changes log
    return to_add, to_remove


def write_changes(date, letters, added, removed):
    with open(f"{BASE_PATH}/changes.txt", "r+") as outfile:
        previous = outfile.read()
        header = f"# {date}: {', '.join(letters)}\n"

        # check if changes have already been written for day
        if previous.startswith(header):
            return

        # Insert most recent changes at top of file
        outfile.seek(0, 0)
        outfile.write(header)

        words_added = ', '.join(sorted(list(added)))
        outfile.write(f"\t* Added: {words_added}\n")

        words_removed = ', '.join(sorted(list(removed)))
        outfile.write(f"\t* Removed: {words_removed}\n\n")

        outfile.write(previous)


if __name__ == "__main__":
    BASE_PATH = os.path.dirname(os.path.realpath(__file__))

    # Pull previous day's game data, exiting if unable to retrieve
    try:
        game_data = get_game_data()
    except:
        print("BAAD")
        with open(f"{BASE_PATH}/changes.txt", "r+") as outfile:
            previous = outfile.read()
            outfile.seek(0, 0)

            outfile.write("# Unable to retrieve game data\n\n")
            outfile.write(previous)

        sys.exit(1)

    with open(f"{BASE_PATH}/words.txt") as infile:
        words = [word.strip() for word in infile]

    # Generate potential guesses based on current word list
    center, letters = game_data["centerLetter"], game_data["validLetters"]
    pangrams, matches = solve.find_words(center, letters, words)
    guesses = set(pangrams + matches)

    # Improve word list by adding missing words and removing false positives
    answers = set(game_data["answers"])
    added, removed = update_words(guesses, answers, set(words))

    # Write added / removed words to changes log
    date = game_data["printDate"]
    write_changes(date, letters, added, removed)
