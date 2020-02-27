#!/usr/bin/env python3
"""
A command-line interface for thesaurus.com
Author: Ryan Sheatsley
Date: Thu Feb 27 2020
"""

import functools
import operator
import requests
import sys


class Thesaurus:
    """
    This object makes requests to backend APIs used by thesaurus.com. These
    backend APIs return JSON-encoded objects--this module is written for such
    an interface. The two APIs are used for spell-checking and synoynms.
    """

    def __init__(
        self,
        spell_api="https://api-portal.dictionary.com/spellSuggestions/",
        thesaurus_api="https://tuna.thesaurus.com/pageData/",
        local=".",
        min_syns=5,
    ):
        """
        Nearly all class methods rely on the following paramaters:
        word - the word to search for
        spell_api - backend api for spell checking
        thesaurus_api - backend api for synonyms
        local - path to SQLite local storage
        min_syns - desired minimum number of synonyms to show
        """

        # setup args, local storage, and remote apis
        self.local = local
        self.min_syns = min_syns
        self.spell_api = spell_api
        self.thesaurus_api = thesaurus_api
        self.word = None

    def definition(self, options):
        """
        Takes input to select desired definition
        options - set of valid inputs
        """

        # prompt for desired definition
        print("Select a definition [1-" + str(len(options)) + "]:")
        while True:
            selection = input()
            try:
                selection = int(selection)
                if selection not in options:
                    raise LookupError
                return selection - 1
            except LookupError as e:
                print(
                    "Invalid selection:",
                    selection,
                    "Must be between (1-" + str(len(options)) + ").",
                )
        return

    def parse(self, response, word, keys=["data", "definitionData", "definitions"]):
        """
        Parses JSON for definitions and synonyms
        response - JSON object we parse through
        word - argument used to perform the request
        keys - list of desired nested keys in the response
        """

        # parse definitions
        print("Definitions for", word)
        definitions = functools.reduce(operator.getitem, keys, response)
        options = set()
        for idx, definition in enumerate(definitions):
            options.add(idx + 1)
            print(idx + 1, "-", "(" + definition["pos"] + ")", definition["definition"])

        # select definition
        return (
            self.synonyms(
                definitions[self.definition(options)], self.word, self.min_syns
            )
            if len(definitions) > 1
            else self.synonyms(definitions[0], self.word, self.min_syns)
        )

    def request(self, word, thesaurus_api):
        """
        Performs thesuarus request
        word - word to request for
        thesaurus_api - thesaurus api backend
        """

        # TODO check local storage
        if False:
            pass

        # otherwise, query remote api
        else:
            return self.parse(
                requests.get(url=thesaurus_api + word.replace(" ", "%20")).json(),
                self.word,
            )

    def spellcheck(self, word, spell_api, keys=["data", "luna"]):
        """
        Performs spell check request (and some trivial parsing)
        word - word to spellcheck
        keys - list of nested keys in the response
        """

        # perform spell check request and handle misspelled requests
        spelling = functools.reduce(
            operator.getitem,
            keys,
            requests.get(url=spell_api + word.replace(" ", "%20")).json(),
        )
        if len(spelling):
            print("Invalid word:", word, "Did you mean any of the following?")
            options = set()
            for idx, option in enumerate(spelling):
                options.add(idx + 1)
                print(str(idx + 1).rjust(2), "-", option)

            # prompt for desired correction
            while True:
                selection = input()
                try:
                    selection = int(selection)
                    if selection not in options:
                        raise LookupError

                    # some suggestions can actually be invalid?
                    self.word = spelling[selection - 1].replace("'", "")
                    break
                except LookupError as e:
                    print(
                        "Invalid selection:",
                        selection,
                        "Must be between (1-" + str(len(options)) + ").",
                    )
        return self.request(self.word, self.thesaurus_api)

    def synonyms(self, definition, word, min_syns):
        """
        Show synonyms for specific definition of a word
        definition - definition of word to be used
        word - argument used to perform the request
        min_syns - desired minimum number of synonyms shown
        """

        # show all terms with maximum similarity scores (and then some if i < n)
        print("Top synonyms for", word)
        for idx, synonym in enumerate(definition["synonyms"]):
            print(str(idx + 1).rjust(2), "-", synonym["term"])
            if synonym["similarity"] != "100" and idx >= min_syns:
                return 0

    def query(self, word):
        """ 
        Parses arguments from the command line
        word - command line arguments
        """
        try:
            self.word = " ".join(word[1:])
        except:
            print("Error parsing command-line arguments. (Missing search term?)")
            return -1
        return self.spellcheck(self.word, self.spell_api)


if __name__ == "__main__":
    """
    To interact with the Thesaurus object, just pass in the desired word from
    the command line. The main interface is through query().
    """

    th = Thesaurus()
    raise SystemExit(th.query(sys.argv))
