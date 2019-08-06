"""
    IDK yet, just playing around with basc_py4chan.
    Maybe some analytics?
"""

import re
import json
import basc_py4chan as basc
import time

#thread stuff
import logging
import threading

def main():
    """
    main function.
    """
    # variables
    f_name = "post.txt" # name of file output to
    SAVE_TEXT = False # whether or not to output text to file
    CHECK_ALL = "all" # checks all boards for word(s)
    ALL_BOARDS = basc.get_all_boards() # a list of all board objects
    
    interested_boards = target_boards()
    print(interested_boards)

    # get all relevant boards to the search
    if CHECK_ALL in interested_boards:
        interested_boards = ALL_BOARDS 
    else:
        interested_boards = [board for board in ALL_BOARDS if board.name in interested_boards]
    
    # check if user provided any valid boards
    if not interested_boards:
        print("no valid boards selected")
        return 

    # gets the word(s) of interest
    search_for = str(input("Word(s) to search for (case insensitive): "))
    # whether to output text to a file
    SAVE_FILE = open(f_name, "a") if str(input("Save results to " + f_name + "?(y/n) ")) is "y" else False

    threads = [threading.Thread(target=thread_function, args=(search_for, board, SAVE_FILE)) for 
        board in interested_boards]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    if SAVE_FILE:
        SAVE_FILE.close()

def thread_function(search_for, board, file):
    logging.info("Thread %s: starting", board.name)
    results = find_word(search_for, board)
    if file:
        json.dump(results, file, indent=2)
    logging.info("Thread %s: finishing", board.name)

def target_boards():
    """

    """
    user_question = "Enter board(s) of interest. Seperate by comma. eg 'g, vg, v'\nEnter 'all' for all boards: "
    user_input = str(input(user_question)).split(", ")
    return user_input

def find_word(words, board):
    """
    Searchs for a on a board.
    """
    word = words # assume one word for now
    word_post_text = {}
    dash = "-----"

    all_ids = board.get_all_thread_ids()
    for t_id in all_ids:
        thread = basc.Thread(board, t_id)
        thread.update(force=True)
        if thread.posts == [None]:
            continue
        occurrences = word_in_thread(word, thread)
        if occurrences is None:
            continue
        print("Thread with word:", thread.url)
        for word_posts in occurrences:
            print(dash, "New Post", dash, "\n", dash, word_posts.url)
            print("Title:", word_posts.subject, "\n", word_posts.text_comment)
            print(dash, "End Post", dash, "\n")
            word_post_text[word_posts.url] = (word_posts.subject, word_posts.text_comment)
    return word_post_text

def word_in_thread(word, thread):
    """
    Returns whether or not a word is in a thread.
    """
    valid_posts = []
    for post in thread.all_posts:
        result = word_in_post(word, post)
        if result != [] and result is not None:
            valid_posts.append(result)
    return None if valid_posts == [] else valid_posts

def word_in_post(word, post):
    """
    TODO
    """
    subject = "" if not post.subject else post.subject
    words_in_post = subject + post.text_comment
    if not words_in_post:
        return None
    regex = r".*[^a-zA-Z]"+word+r"[^a-zA-Z].*"
    match = re.match(regex, words_in_post, re.I)
    if match is None:
        match = False
    if match:
        return post
    return None

if __name__ == "__main__":
    format = "\n\t%(asctime)s: %(message)s\n"
    logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")
    main()
