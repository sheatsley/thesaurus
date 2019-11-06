#!/usr/bin/env python3
"""
A command-line interface for thesaurus.com
Author: Ryan Sheatsley
Date: Mon Nov 4 2019
"""


def request(n=5):
    """
    This is the main code for making requests to thesaurus.com.
    It relies on urllib.request and some basic parsing tools to
    return the most synonymous words. Obviously, it depends
    on sys.argv for parsing arguments via the command-line.
    n - minimum of synonyms to show 
    """

    # global imports
    from bs4 import BeautifulSoup
    import functools
    import json
    import operator
    import re
    import sys
    import urllib.request

    # regex for each webpage and elements to search for within the webpage
    regex = {"thesaurus": "window.INITIAL_STATE = ({.*});"}
    synonyms = {"todo"}
    thesaurus = {
        "name": "script",
        "string": re.compile(regex["thesaurus"]),
        "filter": ["searchData", "tunaApiData", "posTabs"],
    }

    # parse arguments
    try:
        arg = ' '.join(sys.argv[1:])
    except:
        print("Error parsing command-line arguments. (Missing search term?)")
        return -1

    # intitiate request, check if word exists
    try:
        with urllib.request.urlopen(
            "https://www.thesaurus.com/browse/" + arg.replace(" ", "%20")
        ) as req:
            page = req.read()
    except urllib.error.HTTPError:
        print(arg, "not found")
        return -1

    # soupify
    try:
        soup = BeautifulSoup(page, features="html.parser")
    except:
        print("Unable to make the soup.")
        return -1

    # parse out the element of interest and convert to JSON
    try:
        subpage = soup.find(thesaurus["name"], string=thesaurus["string"]).text
        element = json.loads(re.match(regex["thesaurus"], subpage).groups()[0])
    except:
        print("Error parsing JSON from webpage.")
        return -1

    # parse and display definitions
    print("Definitions for", arg)
    tabs = functools.reduce(operator.getitem, thesaurus["filter"], element)
    options = set()
    for idx, definition in enumerate(tabs):
        options.add(idx + 1)
        print(idx + 1, "-", "(" + definition["pos"] + ")", definition["definition"])

    # process input for desired definition (if possible)
    num_definitions = len(options)
    if num_definitions > 1:
        print("Select a definition [1-" + str(num_definitions) + "]:")
        while True:
            desired = input()
            try:
                desired = int(desired)
                assert desired in options
                desired -= 1
                break
            except:
                print(
                    "Invalid selection ("
                    + str(desired)
                    + "). Must be between [1-"
                    + str(num_definitions)
                    + "]."
                )
    else:
        desired = 0

    # display synonyms for desired definition
    print("Top synonyms for", arg)
    i = 0
    while True:
        try:
            # show all terms with similarty scores (and then some if i < n)
            synonym = tabs[desired]["synonyms"][i]
            print(str(i + 1).rjust(2), "-", synonym["term"])
            i += 1
            if synonym["similarity"] != "100" and i >= n:
                break
        except:
            break
    return 0


if __name__ == "__main__":
    raise SystemExit(request())
