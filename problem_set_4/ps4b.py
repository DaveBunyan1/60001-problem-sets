# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
from typing import List, Dict, Tuple


### HELPER CODE ###
def load_words(file_name: str) -> List[str]:
    """
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, "r")
    # wordlist: list of strings
    wordlist: List[str] = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(" ")])
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word(word_list: List[str], word: str) -> bool:
    """
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\\:;'<>?,./\"")
    return word in word_list


def get_story_string() -> str:
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story


### END HELPER CODE ###

WORDLIST_FILENAME = "words.txt"


class Message(object):
    def __init__(self, text: str) -> None:
        """
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        """
        self.message_text = text
        self.valid_words: List[str] = load_words(WORDLIST_FILENAME)

    def get_message_text(self) -> str:
        """
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        """
        return self.message_text

    def get_valid_words(self) -> List[str]:
        """
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.

        Returns: a COPY of self.valid_words
        """
        return self.valid_words.copy()

    def build_shift_dict(self, shift: int) -> Dict[str, str]:
        """
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        """
        encryption_dict: Dict[str, str] = {}
        for i in range(26):
            encryption_dict[string.ascii_lowercase[i]] = string.ascii_lowercase[
                (i + shift) % 26
            ]
            encryption_dict[string.ascii_uppercase[i]] = string.ascii_uppercase[
                (i + shift) % 26
            ]

        return encryption_dict

    def apply_shift(self, shift: int) -> str:
        """
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        """
        encrypted_text: str = ""
        cipher_dictionary: Dict[str, str] = self.build_shift_dict(shift)
        for char in self.message_text:
            if char in " !@#$%^&*()-_+={}[]|\\:;'<>?,./\"":
                encrypted_text += char
            else:
                encrypted_text += cipher_dictionary[char]

        return encrypted_text


class PlaintextMessage(Message):
    def __init__(self, text: str, shift: int) -> None:
        """
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        """
        Message.__init__(self, text)
        self.shift: int = shift
        self.encryption_dict: Dict[str, str] = self.build_shift_dict(shift)
        self.message_text_encrypted: str = self.apply_shift(shift)

    def get_shift(self) -> int:
        """
        Used to safely access self.shift outside of the class

        Returns: self.shift
        """
        return self.shift

    def get_encryption_dict(self) -> Dict[str, str]:
        """
        Used to safely access a copy self.encryption_dict outside of the class

        Returns: a COPY of self.encryption_dict
        """
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self) -> str:
        """
        Used to safely access self.message_text_encrypted outside of the class

        Returns: self.message_text_encrypted
        """
        return self.message_text_encrypted

    def change_shift(self, shift: int) -> None:
        """
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift.

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        """
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text: str) -> None:
        """
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        """
        Message.__init__(self, text)

    def decrypt_message(self) -> Tuple[int, str]:
        """
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create
        the maximum number of valid words, you may choose any of those shifts
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        """
        best_word_count: int = 0
        best_shift: int = 0
        message: str = ""

        for shift in range(26):
            decrypted_message: str = self.apply_shift(shift)
            word_count: int = 0
            for word in decrypted_message.split():
                if is_word(self.valid_words, word):
                    word_count += 1

            if word_count >= best_word_count:
                best_word_count = word_count
                best_shift = shift
                message = decrypted_message

        return (best_shift, message)


if __name__ == "__main__":

    # Example test case (PlaintextMessage)
    # plaintext = PlaintextMessage("hello", 2)
    # print("Expected Output: jgnnq")
    # print("Actual Output:", plaintext.get_message_text_encrypted())

    # Example test case (CiphertextMessage)
    # ciphertext = CiphertextMessage("jgnnq")
    # print("Expected Output:", (24, "hello"))
    # print("Actual Output:", ciphertext.decrypt_message())

    # TODO: WRITE YOUR TEST CASES HERE

    # TODO: best shift value and unencrypted story
    plaintext = PlaintextMessage("hello", 2)
    print("Expected Output: jgnnq")
    print("Actual Output:", plaintext.get_message_text_encrypted())

    plaintext = PlaintextMessage("xyz", 3)
    print("Expected Output: abc")
    print("Actual Output:", plaintext.get_message_text_encrypted())

    plaintext = PlaintextMessage("Test message", 5)
    print("Expected Output: Yjxy rjxxflj")
    print("Actual Output:", plaintext.get_message_text_encrypted())

    ciphertext = CiphertextMessage("jgnnq")
    print("Expected Output: (24, 'hello')")
    print("Actual Output:", ciphertext.decrypt_message())

    ciphertext = CiphertextMessage("mjqqt btwqi")
    print("Expected Output: (21, 'hello world')")
    print("Actual Output:", ciphertext.decrypt_message())

    ciphertext = CiphertextMessage("abc")
    print("Expected Output: (25, 'zab')")
    print("Actual Output:", ciphertext.decrypt_message())

    with open("story.txt") as file:
        story: str = file.readline()
        ciphertext = CiphertextMessage(story)
        print("Story:", ciphertext.decrypt_message())
