"""
A simple module for creating and manipulating a trie
"""


class TriePy:
    # A terminator to represent and end of a path
    __TRIE_TERMINATOR = '!THIS_IS_THE_END!'

    def __init__(self):
        """
        Create an empty trie
        But, since we utilize a dictionary as the
        underlying data structure, we just create an
        empty dictionary.
        """
        self.root = {}

    def addWord(self, word):
        """
        Insert a word into a trie

        Keyword arguments:
        word -- word to parse
        """
        if None is word:
            return None
        current_node = self.root
        for char in word:
            current_node = current_node.setdefault(char, {})
        current_node.setdefault(self.__TRIE_TERMINATOR, {"word":word})

    def containsWord(self, word):
        """
        Checks if a path is found in a trie

        Keyword arguments:
        word -- word to check
        """
        if None is word:
            return False

        current_node = self.root
        for char in word:
            if char in current_node:
                current_node = current_node[char]
            else:
                return False

        # Check if there is a path terminator here since we are at the end of a path
        if self.__TRIE_TERMINATOR in current_node:
            return True
        else:
            return False
