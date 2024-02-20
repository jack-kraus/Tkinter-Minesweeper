from components.word_operations import get_synonyms, get_intersect
from components.loader import Loader

# get set of synonyms for word based on user specified definition(s)
def get_definition(word : str) -> set[str]:
    definitions = get_synonyms(word) # list of definitions for a word
    # exit if none found
    if len(definitions) == 0:
        return None

    # output set of synonyms for definition(s)
    output = set()
    # loop until valid input
    while True:
        # print each definition
        for i in range(len(definitions)):
            i_def_text, i_def_part = definitions[i]["text"], definitions[i]["part"]
            print(f"{i+1}. {i_def_text} ({i_def_part})")
        # convert string to list of values by comma (,)
        choices = input("Which definition(s)?: ").replace(" ", "").split(",")
        # if input is a list of numbers in range, it's valid
        valid = all(choice.isnumeric() and 0 < int(choice) <= len(definitions) for choice in choices)
        if valid:
            # add each set of synonyms to the output set
            for num in map(int, choices):
                output.update(definitions[num-1]["synonyms"])
            return output

# Ask user for a word, repeat until word is found on thesaurus.com and return it
def get_word(val : str) -> tuple[str, list[str]]:
    word_out, word_syn = "", None
    # repeat until word is found
    while word_syn is None:
        word_out = input(f"{val} word: ") # get user input
        word_syn = get_definition(word_out) # get list of definition dicts
        # if incorrect try again
        if word_syn is None:
            print("Invalid word, try again")
    return word_out, word_syn

def print_instructions():
    print("Poetry / Songwriting Tool")
    print("_________________________")
    print("* Input two words, specify a desired definition when asked,")
    print("  and output will show synonyms that rhyme")
    print("* You can choose more than one definition of a word")
    print("  by separating each number with a comma -Ex: 1,2")
    print("* Output: \n  \",\" separates words of the same definition")
    print("  \"(and)\" separates the two groups of words")
    print()

def main() -> None:
    # Loader
    loader = Loader()
    # explanation print
    print_instructions()
    # get two words of definition(s) from user
    word1, word1_syn = get_word("First")
    print()
    word2, word2_syn = get_word("Second")
    print()
    # get list of Rhyme Pairs
    intersects = get_intersect(word1_syn, word2_syn, loader.loop)
    print("\r", end="")
    # print output
    if len(intersects) == 0:
        print("No rhymes found")
    else:
        print(f"Rhyme Pairs: ({word1}, {word2})")
    for intersect in intersects:
        int_1, int_2 = intersect
        print(f"{', '.join(int_1)} (and) {', '.join(int_2)}")

if __name__ == "__main__":
    main()