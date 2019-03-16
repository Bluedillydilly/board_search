"""
    IDK yet, just playing around with basc_py4chan.
    Maybe some analytics?
"""

import re
import json
import basc_py4chan as basc
import time

def main():
    """
    main function.
    """
    # variables
    f_name = "post.txt" # name of file output to
    SAVE_TEXT = False # whether or not to output text to file

    all_boards = basc.get_all_boards()
    interested_boards = target_boards()
    print(interested_boards)
    interested_boards = [board for board in all_boards if board.name in interested_boards]
    print(interested_boards)
    search_for = str(input("Word(s) to search for (case insensitive): "))
    SAVE_TEXT = True if str(input("Save output to file?(y/n) ")) is "y" else False

    if not SAVE_TEXT:
        start = time.time()
        for board in interested_boards:
            post_text = find_word(search_for, board)
        print(time.time() - start)
    else:
        output_file = open(f_name, "a") # open file to save text to
        for board in interested_boards: # searches for search_for in each board of interest
            post_text = find_word(search_for, board)
            json.dump(post_text, output_file, indent=2) # outputs posts with search_for to file
        output_file.close()

def target_boards():
    """

    """
    user_question = "Enter board(s) of interest. Seperate by comma. eg 'g, vg, v': "
    user_input = str(input(user_question)).split(", ")
    return user_input

def find_word(words, board):
    """
    Searchs for a on a board.
    """
    word = words # assume one word for now
    word_post_text = {}

    print("Board of interest: ", board)
    print("Word of interest:", word)
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
            dash = "-----"
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

main()
