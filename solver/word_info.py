from enum import Enum
import config


class State(Enum):
    """
    Enum for the state of a position in a wordle game
    """
    c = 1
    i = 2
    n = 3


class PositionInfo:
    """
    Stores information of a position in a wordle game
    :var found: whether the letter has been found
    :var correct: the correct letter
    :var incorrect: the incorrect letters
    """

    def __init__(self):
        """
        Stores information of a position in a wordle game
        :var found: whether the letter has been found
        :var correct: the correct letter
        :var incorrect: the incorrect letters
        """
        self.found = False
        self.correct: str = ""
        self.incorrect: set[str] = set()
    
    def add_incorrect(self, letter: str) -> bool:
        """
        Adds an incorrect letter to the Position object
        :param letter: The letter to add to the Position object
        :return: True if the letter was added, False otherwise
        """
        if len(letter) != 1 or not letter.isalpha():
            return False
        
        self.incorrect.add(letter.lower())
    
    def set_correct(self, letter: str) -> bool:
        """
        Sets the correct letter to the Position object
        :param letter: The letter to set as the correct letter
        :return: True if the letter was set, False otherwise
        """
        if len(letter) != 1 or not letter.isalpha():
            return False
        
        self.found = True
        self.correct = letter.lower()
    
    def is_valid(self, letter) -> bool:
        """
        Returns whether the letter is valid based on the Position object
        :param letter: The letter to check
        :return: Whether the letter is valid based on the Position object
        """
        if self.found:
            return self.correct == letter
        return letter not in self.incorrect
    

class WordInfo:
    """
    Stores information about every square in the world puzzle
    :var not_in_word: The letters that are not in the word
    :var positions: The PositionInformation for each position in the word
    """

    def __init__(self, word_length: int = config.WORD_LENGTH):
        """
        Stores information about every square in the world puzzle
        :var not_in_word: The letters that are not in the word
        :var positions: The PositionInformation for each position in the word
        """
        self.word_length = word_length
        self.not_in_word: set[str] = set()
        self.positions: list[PositionInfo] = [
            PositionInfo() for _ in range(word_length)
        ]
    
    def get_word_length(self) -> int:
        """
        Returns the length of the word
        :return: The length of the word
        """
        return self.word_length

    def add_info(self, letters: str, values: list[State]) -> bool:
        """
        Adds information about a letter to the WordInfo object
        :param letter: The letter to add information about
        :param positions: The PositionInformation for each position in the word
        :return: None
        """
        if len(letters) != self.word_length or len(values) != self.word_length:
            return False
        
        if any([x not in State for x in values]):
            return False
        
        if any([len(letter) != 1 or not letter.isalpha() for letter in letters]):
            return False
        
        for position, letter, value in zip(self.positions, letters, values):
            if value == State.c:
                position.set_correct(letter.lower())
            elif value == State.i:
                position.add_incorrect(letter.lower())
            elif value == State.n:
                self.not_in_word.add(letter.lower())
        
        return True
    
    def is_valid(self, word: str) -> bool:
        """
        Returns whether the word is valid based on the WordInfo object
        :param word: The word to check
        :return: Whether the word is valid based on the WordInfo object
        """
        return all(
            letter not in self.not_in_word
            for letter in word
        ) and all(
            position.is_valid(letter)
            for position, letter in zip(self.positions, word)
        )