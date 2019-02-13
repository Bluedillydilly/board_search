import re

word = "age"
words_in_post = "Hello age."

regex = r".*[^a-zA-Z]age[^a-zA-Z].*"
match = re.match(regex, words_in_post)
print(match)
