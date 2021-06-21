#!/usr/bin/python3
"""
    IDK yet, just playing around with basc_py4chan.
    Maybe some analytics?
"""

import json
import time

#thread stuff
import logging
import threading

# local imports
from peek_utils import FindPhrase, AllBoards, IsBoard

def Main():
    f_name = "post.txt" # name of file output to
    searchBoards = TargetBoards()

    # get all relevant boards to the search
    searchBoards = AllBoards() if searchBoards == ["all"] else [b for b in searchBoards if IsBoard(b)]
    
    # check if user provided any valid boards
    if not searchBoards:
        print("no valid boards selected!")
        Main() 
        exit()
    else:
        print("Boards selected:", ", ".join(list(map(lambda x: x.name, searchBoards))))

    search_for = str(input("Word(s) to search for (case insensitive): "))
    SAVE_FILE = open(f_name, "a") if str(input("Save results to " + f_name + "?(y/n) ")) == "y" else False

    threads = [threading.Thread(target=ThreadFunction, args=(search_for, board, SAVE_FILE)) for 
        board in searchBoards]
    # start threads
    for t in threads:
        t.start()
    # join threads
    for t in threads:
        t.join()
    if SAVE_FILE:
        SAVE_FILE.close()

def ThreadFunction(search_for, board, saveToFile):
    logging.info("Thread %s: starting", board.name)
    results = FindPhrase(search_for, board)
    if saveToFile:
        json.dump(results, saveToFile, indent=2)
    logging.info("Thread %s: finishing", board.name)

def TargetBoards():
    user_question = "Enter board(s) of interest. Seperate by comma. eg 'g, vg, v'\nEnter 'all' for all boards: "
    user_boards = str(input(user_question)).lower().split(", ")
    return user_boards


if __name__ == "__main__":
    format = "\n\t%(asctime)s: %(message)s\n"
    logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")
    Main()
