"""
    IDK yet, just playing around with basc_py4chan.
    Maybe some analytics?
"""

import basc_py4chan as basc
import re

def main():
    """
    main function.
    """
    all_boards = basc.get_all_boards()
    interested_boards = ["g"]
    interested_boards = [board for board in all_boards if board.name in interested_boards]
    words = "cyberpunk"
    find_word(words, interested_boards[0])


def find_word(words, board):
    """
    Searchs for a on a board.
    """
    word = words # assume one word for now
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
            print("--New Post--")
            print(word_posts.text_comment)
        #print("Thread with word: ", thread.url)
        #print("POST WITH WORD URL: ", thread.url)

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
        print(match)
        return post
    return None

main()
