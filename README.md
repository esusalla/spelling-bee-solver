# Spelling Bee Solver
New York Times [Spelling Bee](https://www.nytimes.com/puzzles/spelling-bee) puzzle solver

![alt text](assets/spelling-bee.png "Spelling Bee")

The New York Times publishes a daily Spelling Bee puzzle that consists of seven different letters. The objective is to construct as many words as possible using the provided letters. Each word must be at least four characters long and each must also contain the center letter somewhere within the word ("O" in the example image above). Letters can be used more than once in each word, and words that contain all seven letters from the day's puzzle (pangrams) are worth more points.

This project consists of a small script for solving the daily puzzle ("solve.py") by finding words in a dictionary ("words.txt") that meet the above stipulations. It differentiates between pangrams and normal words that fulfill the criteria. The project also includes a script for automatically improving the dictionary of words ("improve.py") by updating it each day with valid words that were missing and removing words that the New York Times considers invalid (based on the previous day's answers, which are also provided by the New York Times). The improvement script can be set up to run daily using cron, systemd timers, or something similar. Daily changes to the dictionary including both additions and removals are also tracked ("changes.txt").
