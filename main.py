#!/usr/bin/env python3

from typing import List
import random
import os

class Wordle:
    def __init__(self, words: List[str]):
        self.words = words
        self.word = random.choice(self.words)

def main():
    with open('words.txt', 'r') as words_txt:
        word_list = [line.strip() \
                     for line in words_txt.readlines()]
        
    wordle = Wordle(word_list)

    print(wordle.word)

if __name__ == '__main__': main()