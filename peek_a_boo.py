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
from peek_utils import find_phrase, all_board_names

def main():
    f_name = "post.txt" # name of file output to
    #SAVE_TEXT = False # whether or not to output text to file
    CHECK_ALL = ["all"] # checks all boards for word(s)
    ALL_BOARDS = all_board_names() # a list of all board objects
    interested_boards = target_boards()

    # get all relevant boards to the search
    if CHECK_ALL == interested_boards:
        interested_boards = ALL_BOARDS 
    else:
        interested_boards = [board for board in ALL_BOARDS if board.name in interested_boards]
    
    # check if user provided any valid boards
    if not interested_boards:
        print("no valid boards selected!")
        main() 
    else:
        print("Boards selected:", ", ".join(list(map(lambda x: x.name, interested_boards))))

    # gets the word(s) of interest
    search_for = str(input("Word(s) to search for (case insensitive): "))
    # whether to output text to a file
    SAVE_FILE = open(f_name, "a") if str(input("Save results to " + f_name + "?(y/n) ")) == "y" else False

    threads = [threading.Thread(target=thread_function, args=(search_for, board, SAVE_FILE)) for 
        board in interested_boards]
    # start threads
    for t in threads:
        t.start()
    # join threads
    for t in threads:
        t.join()
    if SAVE_FILE:
        SAVE_FILE.close()

def thread_function(search_for, board, saveToFile):
    logging.info("Thread %s: starting", board.name)
    results = find_phrase(search_for, board)
    if saveToFile:
        json.dump(results, saveToFile, indent=2)
    logging.info("Thread %s: finishing", board.name)

def target_boards():
    user_question = "Enter board(s) of interest. Seperate by comma. eg 'g, vg, v'\nEnter 'all' for all boards: "
    user_boards = str(input(user_question)).split(", ")
    return user_boards



if __name__ == "__main__":
    format = "\n\t%(asctime)s: %(message)s\n"
    logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")
    main()
