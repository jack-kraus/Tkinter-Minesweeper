from bs4 import BeautifulSoup
import requests
from typing import TypeAlias, Callable

# convert url to soup object
def get_soup(url):
    content = requests.get(url=url).content
    return BeautifulSoup(content, features="lxml")

# get a list of rhymes for a particular word from rhymezone.com
def get_rhymes(word : str) -> set[str]:
    word = word.replace(u" ", u"_") # convert spaces to underscore for rhymezone url
    url = f"https://www.rhymezone.com/r/rhyme.cgi?Word={word}&typeofrhyme=perfect&org1=syl&org2=l&org3=y"
    soup = get_soup(url)

    # get rhymes
    rhymes = soup.find_all("a", {"class": "r"}) # get a list of all r class links
    rhymes = filter(lambda elem: elem["href"][:2] == "d=", rhymes) # if the href starts with "d=" then it's a rhyme link

    # return a set of the strings with no-break spaces converted to spaces
    return set(map(lambda item: item.string.replace(u"\xa0", u" "), rhymes))

# get a list of synonyms for each definition of a particular word from rhymezone.com
def get_synonyms(word : str) -> list[dict]:
    word = word.replace(u" ", u"-") # convert spaces to dash for thesaurus url
    url = f"https://www.thesaurus.com/browse/{word}"
    soup = get_soup(url)

    # get all collections of synonyms (one for each part of speech)
    def_elements = soup.find_all("div", {"data-type":"synonym-and-antonym-card"})
    out = [] # list of all definition dicts
    for def_element in def_elements:
        # get part of speech, definition, and list of synonyms
        part_of_speech = def_element.find("p").get_text().split()[0]
        def_string = def_element.find("strong").string
        synonyms = map(lambda elem: elem.find("a").string, def_element.find_all("li"))

        # append dictionary to output
        out_dict = {"text":def_string, "synonyms":list(synonyms), "part":part_of_speech}
        out.append(out_dict)
    return out

# given two sets of synonyms for a word, get pairs of values (i, j)
# where i is in the first list, j is in the second list, and they rhyme with each other
RhymePair : TypeAlias = tuple[tuple[str, ...], tuple[str, ...]]
def get_intersect(word1_syns : set[str], word2_syns : set[str], callback: Callable[[], None]=None) -> list[RhymePair]:
    # list of pairs
    out = []

    # while there are synonyms left
    while len(word1_syns) > 0:
        if not callback is None:
            callback()

        # get a synonym
        syn = word1_syns.pop()
        syn_rhymes = get_rhymes(syn) # get rhymes of that synonym

        # get intersections with the two sets
        # i.e. words found in both sets that rhyme with current word
        combos1 = syn_rhymes.intersection(word1_syns)
        combos2 = syn_rhymes.intersection(word2_syns)

        # remove any rhymes from the first set and add the current words to the combo set
        word1_syns.difference_update(combos1)
        combos1.add(syn)

        # if we found some rhymes in the second set, append our rhyme pair
        if len(combos2) > 0:
            out.append((tuple(combos1), tuple(combos2)))
    return out