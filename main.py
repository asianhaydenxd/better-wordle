#!/usr/bin/env python3

from typing import List
import random
import os

class Wordle:
    def __init__(self, words: List[str]):
        self.words = words
        self.word = random.choice(self.words)

        self.header = 'Welcome to Wordle!'

        self.refresh()

    def refresh(self):
        os.system('clear')

        print(f'{self.header}\n')
        print(f'    _ _ _ _ _')

def main():
    with open('words.txt', 'r') as words_txt:
        word_list = [line.strip() \
                     for line in words_txt.readlines()]
        
    wordle = Wordle(word_list)

if __name__ == '__main__': main()