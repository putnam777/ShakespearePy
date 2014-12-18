# Libraries
from os import path, getcwd
from sys import argv

# Local modules
from Newspeech import *
from Quotes import *
from Utils import *

# Filepaths
NEW_SPEECH = path.join(getcwd(), "Assets", "newspeech.xml")

def main():
    quote = ""

    # 1. Load XML into object from file
    print("Reading file...")
    xml = loadFile(NEW_SPEECH)
    newspeech = Newspeech(xml)
    print("Done reading!")
    print "" # Blank line

    if (len(argv) < 2):
        # No arguments given, so pick a random quote and search for it
        print("Run with no arguments given! Picking a random quote...")
        quote = getRandomQuote()

    else:
        # Assumed everything after the script call is part of the quote
        # Search for the quote provided
        for word in argv:
            if argv.index(word) != 0:
                quote += word + " "

    print("Search string: " + quote)
    print "" # Blank line
    # Search for and display quote
    prettyPrintQuote(newspeech.getSpeech(quote))

def prettyPrintQuote(quoteObject):
    """Pretty-prints a provided ShakespeareQuote object."""
    try:
        print("PLAY: " + quoteObject.getPlay())
        print("SPEAKER: " + quoteObject.getSpeaker())
        print("SPEECH: " + quoteObject.getSpeech())
    except AttributeError:
        print("Quote not found!")        

# Run on startup
main()