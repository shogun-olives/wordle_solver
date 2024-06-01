import os
from .solver import Solver
import config


def clear_console() -> None:
    """
    Clear the console.
    :return: None
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def get_word(word_length: int = config.WORD_LENGTH) -> str:
    """
    Prompt the user for word that the user inputted
    :return: The word that was guessed
    """
    valid = False
    error_message = None

    while not valid:
        clear_console()
        if error_message is not None:
            print(f'[-] {error_message}')
        print(f'[=] Enter the word guessed')

        user_in = input('[+] ')
        user_in = user_in.strip().lower()
        user_in = ''.join([c for c in user_in if c.isalpha()])

        if len(user_in) != word_length:
            error_message = f'{user_in} is not {word_length} letters long'
        else:
            valid = True

    return user_in


def get_values(word_length: int = config.WORD_LENGTH) -> str:
    """
    Prompt the user for the correctness of the word that the user inputted
    :return: The guess that was inputted
    """
    valid = False
    error_message = None

    while not valid:
        clear_console()
        if error_message is not None:
            print(f'[-] {error_message}')
        print(
            '[*] Input Key:',
            '    [c/1] Correct',
            '    [i/2] Incorrect',
            '    [n/3] Not in word',
            f'[=] Enter the values',
            sep='\n'
        )

        user_in = input('[+] ')
        user_in = user_in.strip().lower()
        user_in = ''.join([c for c in user_in if c.isalnum()])

        valid_inputs = {'c', 'i', 'n', '1', '2', '3'}
        if not all(x in valid_inputs for x in user_in.lower()):
            error_message = f'{user_in} is not a valid input'
        elif len(user_in) != word_length:
            error_message = f'{user_in} is not {word_length} letters long'
        else:
            valid = True

    return user_in


def add_guess(solver: Solver) -> None:
    """
    Add a guess to the solver object
    :param solver: The Solver object to add the guess to
    :return: None
    """
    word = get_word()
    values = get_values()

    clear_console()
    print(
        f'[=] Word:         {word}',
        f'[=] Correctness:  {values}',
        f'[=] Is this correct? (y/n)',
        sep='\n'
    )

    add = input('[+] ').strip().lower()

    if add in ['y', 'yes']:
        solver.add_info(word, values)


def prompt_user(
    wordle_solver: Solver = None
) -> None:
    """
    Prompt the user for input and display the results.
    :param max_letters: The maximum number of letters to use.
    :param dst_dir: The directory containing the word bank files.
    :return: None
    """
    if wordle_solver is None:
        wordle_solver = Solver()
    
    error = None
    
    while True:
        clear_console()
        print(wordle_solver)

        if error is not None:
            print(f'[-] {error}')
        print(
            '\n[*] Inputs:',
            '    [1] Add a guess',
            '    [2] See all remaining words',
            '    [3] Exit',
            sep='\n'
        )
        user_in = input('[+] ').strip().lower()

        if user_in == '1':
            add_guess(wordle_solver)
            error = None
        elif user_in == '2':
            clear_console()
            print('[=] Remaining words:')
            for i, word in enumerate(wordle_solver.get_remaining()):
                idx = f'[{i + 1}]'
                print(f'  {idx:>6} {word}')
            input(f'\n[=] Press any key to continue...')
            error = None
        elif user_in in ['3', 'e', 'exit']:
            error = None
            break
        else:
            error = f'{user_in} is not a valid input'
    
    clear_console()
    print(wordle_solver)