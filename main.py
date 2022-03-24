#!/usr/bin/env python3

from typing import List
from getch import Getch
from enum import Enum
import random
import math
import os

LETTERS = 'abcdefghijklmnopqrstuvwxyz'
WORD_LENGTH = 5
GUESSES = 6
IS_UPPERCASE = False

# Debug setting
TEST_WORD = None
SHOW_WORD = False

class Color(Enum):
    GREEN  = '48;5;40'
    YELLOW = '48;5;220'
    GRAY   = '48;5;240'
    NULL   = '48;5;248'

class Wordle:
    def __init__(self, words: List[str]):
        self.words = [word for word in words if len(word) == WORD_LENGTH]

        self.word = random.choices(self.words, weights=[1/(i+1) for i in range(len(self.words))])[0]
        if TEST_WORD is not None: self.word = TEST_WORD

        self.getch = Getch()

        self.screen = ''
        
        self.header = '     Welcome to Wordle!'
        self.input = ''
        self.guesses = []

        self.green_keys = ''
        self.yellow_keys = ''
        self.gray_keys = ''

        self.refresh()

    def get_color_tuples(self, guess):
        first_string = [ (letter, Color.GREEN) if letter == self.word[index] else \
                           (letter, Color.YELLOW) if letter in self.word else \
                           (letter, Color.GRAY) for index, letter in enumerate(guess) ]
        
        second_string = [ (letter, Color.GREEN) if color == Color.GREEN else \
                                   (letter, Color.YELLOW) if letter in self.word and first_string[:index].count((letter, Color.YELLOW)) < self.word.count(letter) - first_string.count((letter, Color.GREEN)) else \
                                   (letter, Color.GRAY) for index, (letter, color) in enumerate(first_string) ]

        return second_string

    def color_guess(self, guess) -> str:
        context_string = self.get_color_tuples(guess)
        
        color_string = [ f'\u001b[{Color.GREEN.value}m {maybe_upper(letter)} ' if color == Color.GREEN else \
                         f'\u001b[{Color.YELLOW.value}m {maybe_upper(letter)} ' if color == Color.YELLOW else \
                         f'\u001b[{Color.GRAY.value}m {maybe_upper(letter)} ' for letter, color in context_string ]

        for letter, color in context_string:
            if color == Color.GREEN: self.green_keys += letter
            elif color == Color.YELLOW: self.yellow_keys += letter
            elif color == Color.GRAY: self.gray_keys += letter
        
        return ''.join(color_string) + '\u001b[0m'

    def is_game_won(self) -> bool:
        try: return self.guesses[-1] == self.word
        except IndexError: return None

    def is_game_over(self) -> str:
        return len(self.guesses) >= GUESSES

    def refresh(self) -> None:
        self.screen = ''

        self.load('    Developed by Hayden\n\n')

        if SHOW_WORD: self.load(f'{self.word}\n')
        
        self.load(f'{self.header}\n\n')

        space_string = ' ' * math.floor(1.5 * (10 - WORD_LENGTH))

        for guess in self.guesses:
            self.load(space_string + self.color_guess(guess) + '\n')

        if not (self.is_game_won() or self.is_game_over()):
            self.load(space_string + f'\u001b[{Color.NULL.value}m')
            for i in range(WORD_LENGTH):
                if i < len(self.input):
                    self.load(f' {maybe_upper(self.input[i])} ')
                else:
                    self.load('   ')
            self.load('\n')

            for i in range(GUESSES - len(self.guesses) - 1): self.load('\u001b[0m' + space_string + f'\u001b[{Color.NULL.value}m' + '   ' * WORD_LENGTH + '\n')

        self.load('\u001b[0m\n')
        for key in 'qwertyuiop\n asdfghjkl\n    zxcvbnm':
            if key not in LETTERS:
                self.load(key)
                continue
                
            color = Color.GREEN.value if key in self.green_keys else \
                    Color.YELLOW.value if key in self.yellow_keys else \
                    Color.GRAY.value if key in self.gray_keys else \
                    Color.NULL.value
            self.load(f'\u001b[{color}m {maybe_upper(key)} \u001b[0m')
        self.load('\n')

        if self.is_game_won() or self.is_game_over():
            self.load('\nBetter Wordle ')
            if WORD_LENGTH != 5: self.load(f'({WORD_LENGTH} letters) ')
                
            if self.is_game_won(): self.load(f'{len(self.guesses)}/{GUESSES}\n')
            else: self.load(f'X/{GUESSES}\n')

            self.load('\n'.join([ ''.join(['🟩' if color == Color.GREEN else \
                                   '🟨' if color == Color.YELLOW else \
                                   '⬛' for letter, color in self.get_color_tuples(guess)]) for guess in self.guesses ]) + '\n')
            
        os.system('clear')
        print(self.screen)

    def load(self, text: str) -> None:
        self.screen += text

    def type(self) -> None:
        self.refresh()
        
        while True:
            char = self.getch.impl()
            self.header = ''
            if char == '\r':
                if len(self.input) < WORD_LENGTH:
                    self.header = '     Not enough letters'
                elif self.input not in self.words:
                    self.header = '      Not in word list'
                else:
                    self.guesses.append(self.input)
                    self.header = ''
                    if self.is_game_over(): self.header = f'      The word is {maybe_upper(self.word)}'
                    if self.is_game_won(): self.header = '          Good job!'
                    self.input = ''
                    self.refresh()
                    return
            elif char == '\x7f':
                self.input = self.input[:-1]
            elif char in LETTERS and len(self.input) < WORD_LENGTH:
                self.input += char
        
            self.refresh()

    def start_game(self):
        while len(self.guesses) < GUESSES:
            self.type()
            if self.guesses[-1] == self.word: break

def maybe_upper(text: str) -> str:
    return text.upper() if IS_UPPERCASE else text

def main():
    with open('words.txt', 'r') as words_txt:
        word_list = [line.strip() \
                     for line in words_txt.readlines()]

    wordle = Wordle(word_list)
    
    wordle.start_game()

if __name__ == '__main__': main()
