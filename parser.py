import nltk
import sys

# importing the ascii charcters into the script 
import string 

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """ 
S -> NP VP | S Conj S | S Conj VP 
PP -> P NP | P 
AP -> Adj | Adj AP
NP -> N | Det NP | AP NP | PP NP 
VP -> V | V NP | VP PP | Adv VP | VP Adv 
"""



grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # tokenizes the words in the sentence 
    tokens = nltk.word_tokenize(sentence)

    # make the characters in the words all lowercase 
    tokens = [word.lower() for word in tokens]
    #print(tokens)

    # filters the worlds so that the only remaining words are ones with one at least on alphabetical letter 
    alphabet       = list(string.ascii_lowercase)
    filtered_words = []

    for word in tokens:
        for letter in word:
            if letter in alphabet:
                filtered_words.append(word)
                break

            else:
                continue 

    #print(filtered_words)
    return filtered_words

    #raise NotImplementedError


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    Noun_phrases = []

    for subtree in tree.subtrees():

        if subtree.label() == 'NP':
            Noun_phrases.append(subtree)


    return Noun_phrases


    #raise NotImplementedError


if __name__ == "__main__":
    main()
