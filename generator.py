from deep_translator import GoogleTranslator

# Nltk imports
import nltk
from nltk.corpus import wordnet as wn
import random

nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

# Function that translates input string into target language. Returns translated text
def translate(input : str, target_lang : str) -> str :
    return GoogleTranslator(source = "auto", target = target_lang).translate(input)

# Function that generates a list of N english words (nouns, adjectives, verbs)
def get_random_words(pos : str, count : int) :
    synsets = list(wn.all_synsets(pos))
    words = set(lemma.name() for syn in synsets for lemma in syn.lemmas())
    words_list = list(words)  # Convert the set to a list
    return random.sample(words_list, count)

# =Function retrieving the definition of an English word
def get_definiton(word : str) -> str :
    synonyms = wn.synsets(word)
    return synonyms[0].definition()

# TODO : create a function that will generate a fixed set of vocabulary words on which the exercices
# of the worksheet will be based upon
def get_vocab_bank(level : int, target : str) -> list[str] : 
    words = get_random_words('n', level)
    words += get_random_words('v', level)
    words += get_random_words('a', level)
    return [{"word" : translate(word, target), "translation" : word, "definition" : get_definiton(word)} for word in words]

# TODO : create a function that will generate a fill in the blank exercice based on a fixed set
# of vocabulary words
def fillin_ex(lang : str, level : float, len : int, vocabulary : list[str]) -> str :
    pass

# TODO : create a function that will generate a translation exercice
def translation_ex(lang : str, level : float, len : int, vocabulary : list[str]) -> str :
    pass

# TODO : create a function which will generate a PDF file worksheet.
def generate_doc(lang : str, level : float, len : int, vocabulary : list[str]) :
    pass