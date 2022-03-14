#!/usr/bin/env python3

from typing import List
import random
import os

class Wordle:
    def __init__(self, words: List[str]):
        self.words = words
        self.word = random.choice(self.words)

        self.header = 'Welcome to Wordle!'
        self.input = ''
        self.guesses = []

        self.refresh()

    def refresh(self):
        os.system('clear')

        print(f'{self.header}\n')

        for guess in self.guesses:
            print(f'    {guess[0]} {guess[1]} {guess[2]} {guess[3]} {guess[4]}')
        
        print(f'    ', end='')
        
        for i in range(5):
            if i < len(self.input):
                print(self.input[i].upper(), end=' ')
            else:
                print('_', end=' ')

def main():
    with open('words.txt', 'r') as words_txt:
        word_list = [line.strip() \
                     for line in words_txt.readlines()]
        
    wordle = Wordle(word_list)

if __name__ == '__main__': main()