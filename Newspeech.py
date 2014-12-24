# Used to encode search returns
from ShakespeareSpeech import ShakespeareSpeech

# Tags to search for
PLAY_TAG = "<PLAY>"
SPEAKER_TAG = "<SPEAKER>"
SPEECH_TAG = "<SPEECH>"
OPEN_TAG = "<"
CLOSE_TAG = ">"
PUNCTUATION = [",", "-", ".", "'", ";", '"', "(", ")", "!", "?", "[", "]"]

class Newspeech(object):
    """Stores an XML play or speech file."""

    def __init__(self, body):
        self.body = body
        self.searchBody = self.body.lower()

    def getSpeech(self, searchString):
        """Returns a ShakespeareSpeech object with the relevant speech 
        corresponding to the given search string."""

        index = -1
        invalid = True

        while invalid:
            # Attempt 1: Exact match
            index = self.getNextIndexIgnoreCase(index, searchString)
            if index is -1:
                # Attempt 2: Match ignoring punctuation
                index = self.getNextIndexIgnorePunctAndCase(index, searchString)
                if index is -1:
                    # The string wasn't found in any play!
                    return False
                else:
                    # The quote exists, but the search string isn't perfect.
                    # Perform a last-effort slow search to insert  
                    # and remove punctuation where possible
                    index = self.lookaheadAndCorrect(searchString, index)

            try:
                play = self.backtrack(index, PLAY_TAG)
                speaker = self.backtrack(index, SPEAKER_TAG)
                speech = self.backtrackGetSpeech(index)
                invalid = False
            except:
                invalid = True
        
        # Return the speech and metadata in a new ShakespeareSpeech object for simplicity
        return ShakespeareSpeech(play, speaker, speech)

    def backtrack(self, index, tag):
        """Backtracks from the provided index until the given tag is encountered.
        Returns the text at that tag. For finding a speech body, use backtrackGetSpeech() instead."""

        # Split the body up to the index
        splitBody = self.body[0:index]

        # Find last index of open and close tags
        lastOpenTagIndex = splitBody.rfind(tag)
        # Start searching from after the ">" symbol of the tag
        startIndex = lastOpenTagIndex + len(tag)
        # Find the next tag, whatever it is - close tags can be AFTER the splitBody cutoff!
        nextOpenTagIndex = startIndex + (splitBody[startIndex:].index("<"))

        # Return contents
        return splitBody[startIndex:nextOpenTagIndex]

    def backtrackGetSpeech(self, index):
        """Backtracks from the provided speech index and returns the full speech."""

        startSpeechIndex = self.getPreviousIndex(self.body, CLOSE_TAG, index) + 1
        endSpeechIndex = self.getNextIndex(self.body, OPEN_TAG, index)

        return self.body[startSpeechIndex:endSpeechIndex]

    def getPreviousIndex(self, haystack, needle, index):
        """Returns the previous index of a substring ending at the current index in haystack."""

        return haystack.rfind(needle, 0, index)
        
    def getNextIndex(self, haystack, needle, index):
        """Returns the next index of a substring starting from the current index in haystack."""

        return haystack.find(needle, index + 1)

    def getIndexIgnoreCase(self, needle):
        """Search to find the first index of the needle in the body, ignoring case."""
        
        return self.searchBody.index(needle.lower())

    def getNextIndexIgnoreCase(self, index, needle):
        """Search to find the next index of the needle in the body, ignoring case."""

        return self.getNextIndex(self.searchBody, needle.lower(), index + 1)

    def removePunctuation(self, input):
        """Returns the original input string, stripped of all punctuation."""
        for punct in PUNCTUATION:
            input = input.replace(punct, "")

        return input

    def getNextIndexIgnorePunctAndCase(self, index, needle):
        """Search to find the next index of the needle in the body, ignoring case AND punctuation."""

        return self.getNextIndex(self.removePunctuation(self.searchBody), self.removePunctuation(needle.lower()), index + 1)

    def lookaheadAndCorrect(self, input, index):
        """Given an index in a haystack with all punctuation removed, looks ahead of that index 
        and returns the corresponding index of the full, corrected phrase."""

        tempInput = list(input)
        match = False

        while not match:
            haystackChar = self.searchBody[index]
            tempIndex = index

            for needleChar in tempInput:
                if needleChar is not haystackChar:
                    if needleChar in PUNCTUATION and haystackChar in PUNCTUATION:
                        tempInput = list(''.join(tempInput).replace(needleChar, haystackChar, 1))
                    elif needleChar in PUNCTUATION:
                        tempInput.remove(needleChar)
                    elif haystackChar in PUNCTUATION:
                        tempInput.insert(input.index(needleChar), haystackChar)
                    else:
                        # Miss! Reset and try again
                        match = False
                        tempIndex = index
                        tempInput = list(input)
                        break

                tempIndex += 1
                haystackChar = self.body[tempIndex]
                match = True

            index += 1

        return (index - 1)
                   
            

