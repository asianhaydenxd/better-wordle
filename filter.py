import string

def has_only_latin_letters(name):
    char_set = string.ascii_letters
    return all((True if x in char_set else False for x in name))

with open('og_words.txt', 'r') as og_txt:
    og_words = og_txt.read().splitlines()

filter_comments = [word.lower() for word in og_words if has_only_latin_letters(word)]

with open('words.txt', 'w') as new_txt:
    new_txt.write('\n'.join(filter_comments))