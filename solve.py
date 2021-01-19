#!/usr/bin/env python

import sys


def get_input():
    if len(sys.argv) < 3:
        center = input("Please enter the center letter: ")
        outer = input("Please enter the outer letters: ")
    else:
        center = sys.argv[1]
        outer = sys.argv[2]

    return center.lower(), set((center + outer).lower())


def find_words(center, letters, words):
    pangrams = []
    matches = []

    for word in words:
        # All matching words must contain center letter
        if center in word:
            if all(c in word for c in letters):
                # All entered characters in word characters
                pangrams.append(word)
            elif all(c in letters for c in word):
                # All word characters in entered characters
                matches.append(word)

    return pangrams, matches


if __name__ == "__main__":
    center, letters = get_input()
    with open("words.txt") as infile:
        words = [word.strip() for word in infile]

    pangrams, matches = find_words(center, letters, words)

    print("Pangrams:")
    for pangram in pangrams:
        print(f" - {pangram}")

    print("\nMatches:")
    for match in matches:
        print(f" - {match}")
