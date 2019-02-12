"""
    IDK yet, just playing around with basc_py4chan.
    Maybe some analytics?
"""

import basc_py4chan as basc

def main():
    """
    main function.
    """
    all_boards = basc.get_all_boards()
    print(all_boards)
    interested_boards = ["wg"]
    interested_boards = [board for board in all_boards if board.name in interested_boards]
    print(interested_boards)
    find_word("Torrent", interested_boards[0])


def find_word(words, board):
    """
    Searchs for a on a board.
    """
    word = words # assume one word for now
    print("Board of interest: ", board)
    all_ids = board.get_all_thread_ids()
    for t_id in all_ids:
        thread = basc.Thread(board, t_id)
        thread.update(force=True)
        if thread.posts == [None]:
            continue
        if word_in_thread(word, thread):
            print("------------")
            print("Thread with word: ",thread.url)
            print("POST WITH WORD URL: ", thread.url)

def word_in_thread(word, thread):
    """
    Returns whether or not a word is in a thread.
    """
    words_in_thread = ""
    for post in thread:
        word_in_post(word, post)

def word_in_post(word, post):
    """
    TODO
    """
    pass

main()

