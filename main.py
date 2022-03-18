#!/usr/bin/env python3

from typing import List
from getch import Getch
import random
import os

LETTERS = 'abcdefghijklmnopqrstuvwxyz'

class Wordle:
    def __init__(self, words: List[str]):
        self.words = words
        self.word = random.choice(self.words)

        self.getch = Getch()
        
        self.header = 'Welcome to Wordle!'
        self.input = ''
        self.guesses = []

        self.refresh()

    def refresh(self):
        os.system('clear')

        print(f'{self.header}\n')

        for guess in self.guesses:
            guess = guess.upper()
            print(f'    {guess[0]} {guess[1]} {guess[2]} {guess[3]} {guess[4]}')
        
        print(f'    ', end='')
        for i in range(5):
            if i < len(self.input):
                print(self.input[i].upper(), end=' ')
            else:
                print('_', end=' ')
        print('')

    def type(self) -> None:
        self.refresh()
        
        while True:
            char = self.getch.impl()
            if char == ' ':
                if len(self.input) < 5:
                    self.header = 'Not enough letters'
                if self.input not in self.words:
                    self.header = 'Not in word list'
                else:
                    self.header = ''
                    self.guesses.append(self.input)
                    self.input = ''
                    return
            elif char == '\x7f':
                self.input = self.input[:-1]
            elif char in LETTERS and len(self.input) < 5:
                self.input += char
        
            self.refresh()

    def start_game(self):
        while len(self.guesses) < 6:
            self.type()
            if self.guesses[-1] == self.word: break

def main():
    with open('words.txt', 'r') as words_txt:
        word_list = [line.strip() \
                     for line in words_txt.readlines()]

    wordle = Wordle(word_list)
    
    wordle.start_game()

if __name__ == '__main__': main()