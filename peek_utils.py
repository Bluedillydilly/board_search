import re
import basc_py4chan as basc


def thread_occurrance(phrase, thread):
    """
    Returns whether or not a word is in a thread.

    @param word The word to look for in the thread

    @param thread Where to look for the word
    """
    valid_posts = []
    for post in thread.all_posts:
        result = post_occurrance(phrase, post)
        if result != [] and result is not None:
            valid_posts.append(result)
    return valid_posts


def post_occurrance(phrase, post):
    """
    @param word
    """
    subject = "" if not post.subject else post.subject
    words_in_post = subject + post.text_comment
    if not words_in_post:
        return None
    regex = r".*[^a-zA-Z]"+phrase+r"[^a-zA-Z].*"
    match = re.match(regex, words_in_post, re.I)
    if match == None:
        match = False
    if match:
        return post
    return None

def find_phrase(phrase, board):
    """
    Searchs for a on a board.
    """
    word = phrase # assume one word for now
    word_post_text = {}
    dash = "-----"

    all_ids = board.get_all_thread_ids()
    for t_id in all_ids:
        thread = basc.Thread(board, t_id)
        thread.update(force=True)
        if thread.posts == [None]:
            continue
        occurrences = thread_occurrance(phrase, thread)
        if occurrences == []:
            continue
        print("Thread with word:", thread.url)
        for word_posts in occurrences:
            print(dash, "New Post", dash, "\n", dash, word_posts.url)
            print("Title:", word_posts.subject, "\n", word_posts.text_comment)
            print(dash, "End Post", dash, "\n")
            word_post_text[word_posts.url] = (word_posts.subject, word_posts.text_comment)
    return word_post_text


def all_board_names():
    return basc.get_all_boards()


"""
    1. Per board:
        a. Per thread:
            1. return any posts with mention of target phrase
"""