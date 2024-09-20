import random
import sys
import os

def select_random_values(lst, n):
    if n > len(lst):
        raise ValueError("n cannot be greater than the length of the list")

    random_values = random.sample(lst, n)
    return random_values

class VocabGenerator():
    def __init__(self, vocab_level):
        self.vocab_level = vocab_level
        base_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        vocab_file_path = os.path.join(base_dir, self.vocab_level + "vocab.txt")
        with open(vocab_file_path) as f:
            contents = f.read()
            self.vocab_list = contents.split('\n')
            self.vocab_list = self.vocab_list[0:len(self.vocab_list)-1]
    #Returns an array of generated words
    #works for num_words > 1
    def generateWords(self, num_words):
        return select_random_values(self.vocab_list, num_words)



