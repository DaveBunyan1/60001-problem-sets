# Problem Set 2, hangman.py
# Name:
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
from typing import List, Set

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, "r")
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist: List[str]):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word: str, letters_guessed: List[str]) -> bool:
    """
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    letters = list(secret_word)
    for letter in letters_guessed:
        while letter in letters:
            letters.remove(letter)

    # Returns true if all letters have been guessed, false otherwise.
    return len(letters) == 0


def get_guessed_word(secret_word: str, letters_guessed: List[str]) -> str:
    """
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    current_guess: str = ""
    for letter in secret_word:
        if letter in letters_guessed:
            current_guess += letter
        else:
            current_guess += "_ "

    return current_guess


def get_available_letters(letters_guessed: List[str]) -> str:
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    return "".join(
        letter for letter in string.ascii_lowercase if letter not in letters_guessed
    )


def check_guess(guessed_letter: str, letters_guessed: List[str]) -> bool:
    """
    Docstring for check_guess

    :param guessed_letter: The letter that was guessed
    :type guessed_letter: str
    :param letters_guessed: The current letters that have been guessed
    :type letters_guessed: List[str]
    :return: Whether or not the guess is valid
    :rtype: bool
    """
    return guessed_letter.isalpha() and guessed_letter not in letters_guessed


def hangman(secret_word: str):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    guesses_left: int = 6
    available_letters: str = string.ascii_lowercase
    warnings_left: int = 3
    letters_guessed: List[str] = []

    vowels: str = "aeiou"

    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print("-------------")

    while guesses_left > 0:
        print(f"You have {guesses_left} guesses left.")
        print("Available letters:", available_letters)
        guessed_letter: str = input("Please guess a letter: ").lower().strip()

        # Check if guess is valid
        if not check_guess(guessed_letter, letters_guessed):
            if guessed_letter in letters_guessed:
                msg = "You have already guessed that letter."
            else:
                msg = "That is not a valid letter."

            if warnings_left > 0:
                warnings_left -= 1
                print(
                    f"Oops! {msg} You have {warnings_left} warnings left:",
                    get_guessed_word(secret_word, letters_guessed),
                )
            else:
                guesses_left -= 1
                print(f"Oops! {msg} You have no warnings left so you lose a guess.")

            print("------------")
            continue

        letters_guessed.append(guessed_letter)
        available_letters = get_available_letters(letters_guessed)

        if guessed_letter in secret_word:
            print("Good guess:", get_guessed_word(secret_word, letters_guessed))
        else:
            print(
                "Oops! That letter is not in my word:",
                get_guessed_word(secret_word, letters_guessed),
            )
            if guessed_letter in vowels:
                guesses_left -= 2
            else:
                guesses_left -= 1

        print("------------")

        if is_word_guessed(secret_word, letters_guessed):
            print("Congratulations, you won!")
            total_score = guesses_left * len(set(secret_word))
            print(f"Your total score for this game is: {total_score}")
            return

    print("Sorry, you ran out of guesses. The word was:", secret_word)


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word: str, other_word: str) -> bool:
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    my_word_without_spaces: str = my_word.replace(" ", "")
    guessed_letters: Set[str] = set(my_word_without_spaces)
    if "_" in guessed_letters:
        guessed_letters.remove("_")

    if len(my_word_without_spaces) != len(other_word):
        return False

    for i in range(len(my_word_without_spaces)):
        if my_word_without_spaces[i] == "_" and other_word[i] in guessed_letters:
            return False
        if (
            my_word_without_spaces[i] != other_word[i]
            and my_word_without_spaces[i] != "_"
        ):
            return False

    return True


def show_possible_matches(my_word: str):
    """
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    possible_matches: List[str] = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            possible_matches.append(word)

    if len(possible_matches) == 0:
        print("No matches found.")
    else:
        print(" ".join(possible_matches))


def hangman_with_hints(secret_word: str):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    guesses_left: int = 6
    available_letters: str = string.ascii_lowercase
    warnings_left: int = 3
    letters_guessed: List[str] = []

    vowels: str = "aeiou"

    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print("-------------")

    while guesses_left > 0:
        print(f"You have {guesses_left} guesses left.")
        print("Available letters:", available_letters)
        guessed_letter: str = input("Please guess a letter: ").lower().strip()

        if guessed_letter == "*":
            print("Possible word matches are:")
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            continue

        # Check if guess is valid
        if not check_guess(guessed_letter, letters_guessed):
            if guessed_letter in letters_guessed:
                msg = "You have already guessed that letter."
            else:
                msg = "That is not a valid letter."

            if warnings_left > 0:
                warnings_left -= 1
                print(
                    f"Oops! {msg} You have {warnings_left} warnings left:",
                    get_guessed_word(secret_word, letters_guessed),
                )
            else:
                guesses_left -= 1
                print(f"Oops! {msg} You have no warnings left so you lose a guess.")

            print("------------")
            continue

        letters_guessed.append(guessed_letter)
        available_letters = get_available_letters(letters_guessed)

        if guessed_letter in secret_word:
            print("Good guess:", get_guessed_word(secret_word, letters_guessed))
        else:
            print(
                "Oops! That letter is not in my word:",
                get_guessed_word(secret_word, letters_guessed),
            )
            if guessed_letter in vowels:
                guesses_left -= 2
            else:
                guesses_left -= 1

        print("------------")

        if is_word_guessed(secret_word, letters_guessed):
            print("Congratulations, you won!")
            total_score = guesses_left * len(set(secret_word))
            print(f"Your total score for this game is: {total_score}")
            return

    print("Sorry, you ran out of guesses. The word was:", secret_word)


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

    ###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.

    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
