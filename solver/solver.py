import config
from .word_info import WordInfo, State
from copy import deepcopy

class Solver:
    """
    Solves Wordle Puzzles based on Given Information
    :var remaining: The remaining words to consider
    :var word_info: The WordInfo object containing information about the word
    :var words: The words that have been guessed
    :var results: The results of the guesses
    :var best_guess: The best guess based on the current information
    """

    def __init__(self, fn: str = config.WORD_BANK_FILE, word_length: int = config.WORD_LENGTH):
        """
        Solves Wordle Puzzles based on Given Information
        :var remaining: The remaining words to consider
        :var word_info: The WordInfo object containing information about the word
        :var words: The words that have been guessed
        :var results: The results of the guesses
        :var best_guess: The best guess based on the current information
        """
        with open(fn, 'r') as file:
            self.remaining: list[str] = [line.strip() for line in file]
        self.word_info: WordInfo = WordInfo(word_length)

        self.words: list[str] = []
        self.results: list[str] = []
        self.best_guess = self.get_best_guess()
    
    def __str__(self) -> str:
        """
        Returns the string representation of the Solver object
        :return: The string representation of the Solver object
        """
        gap_size = 4
        gap = ' '*gap_size

        if len(self.words) == 0:
            return '\n'.join([
                f'[=] {self.get_num_remaining()} Remaining',
                f'[=] {len(self.words)} Guesses:',
                '',
                f'[=] Best Guess: {self.best_guess}'
            ])
        
        return '\n'.join([
            f'[=] {self.get_num_remaining()} Remaining',
            f'[=] {len(self.words)} Guesses:',
            gap.join([''] + [f'[{i + 1}] {word}' for i, word in enumerate(self.words)]),
            gap.join([''] + [f'[{i + 1}] {result}'for i, result in enumerate(self.results)]),
            '',
            f'[=] Best Guess: {self.best_guess}'
        ])

    def copy(self) -> 'Solver':
        """
        Returns a copy of the Solver object
        :return: A copy of the Solver object
        """
        return deepcopy(self)

    def get_best_guess(self) -> str:
        # TODO: Implement this function
        return None

    def get_remaining(self) -> list[str]:
        """
        Returns the list of remaining words
        :return: The list of remaining words
        """
        return self.remaining
    
    def get_num_remaining(self) -> int:
        """
        Returns the number of remaining words
        :return: The number of remaining words
        """
        return len(self.remaining)
    
    def add_info(self, word: str, values: str) -> bool:
        """
        Adds information about a letter to the WordInfo object
        :param word: The word that was guessed
        :param values: Whether each position is correct, incorrect, or not in the word
        :return: True if the information was added, False otherwise
        """
        if len(word) != self.word_info.get_word_length() or len(values) != self.word_info.get_word_length():
            return False

        valid_inputs = {'c', 'i', 'n', '1', '2', '3'}
        if any([x not in valid_inputs for x in values]):
            return False

        word = ''.join([c for c in word if c.isalpha()]).lower()

        if not isinstance(values, list):
            conversions = {
                '1': 'c',
                '2': 'i',
                '3': 'n'
            }
            values = [
                State[conversions[x] if x.isdigit() else x.lower()]
                for x in [*values]
            ]

        self.words.append(word)
        self.results.append(''.join([x.name for x in values]))

        self.word_info.add_info(word, values)

        self.filter()
        self.best_guess = self.get_best_guess()
        return True

    def filter(self) -> None:
        """
        Filters the remaining words based on the current information
        :return: None
        """
        self.remaining = [
            word for word in self.remaining
            if self.word_info.is_valid(word)
        ]