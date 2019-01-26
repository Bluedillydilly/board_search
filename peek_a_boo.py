"""
    IDK yet, just playing around with basc_py4chan.
    Maybe some analytics?
"""

import basc_py4chan as basc

def main():
    all_boards = basc.get_all_boards()
    print(all_boards)
    interested_boards = ["wg"]
    interested_boards = [board for board in all_boards if board.name in interested_boards]
    print( interested_boards )
    find_words("lain", interested_boards[0] )

"""
    Searchs for word(s) on a board.
"""
def find_words( words, board ):
    word = words # assume one word for now
    all_t = board.get_all_thread_ids()
    post_irl_word = []
    for id in all_t:
        thread = basc.Thread( board, id)
        thread.expand()
        print("Thread: ", thread)
        t_posts = thread.all_posts
        print("HELLO: ",t_posts)
        if t_posts == [None]:
            continue
        for post in t_posts:
            subject = "" if not post.subject else post.subject
            text = subject + post.text_comment
            if word in text:
                post_irl_word += post.url
    print(post_irl_word)
main()