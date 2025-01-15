import nltk
import random
import pickle

from deep_translator import GoogleTranslator
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk.probability import FreqDist

nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

# Loading brown corpus data . If files doesn't exit, download it and pickle it in assets
try :
    with open("assets/brown_corpus_data.pkl", "rb") as f:
        freq_dist, total_words = pickle.load(f)

except :
    # Download the Brown corpus if not already available
    nltk.download('brown')

    # Precompute the data
    brown_words = brown.words()
    freq_dist = FreqDist(brown_words)
    total_words = len(brown_words)

    # Save precomputed data to a pickle file
    with open("assets/brown_corpus_data.pkl", "wb") as f:
        pickle.dump((freq_dist, total_words), f)

# Function that translates input string into target language. Returns translated text
def translate(input : str, target_lang : str) -> str :
    return GoogleTranslator(source = "auto", target = target_lang).translate(input)

# Function that assigns a score to a word based on its commonality / difficulty
def get_commonality_score(word : str) -> float :
    word = word.lower()
    # Generate the frequency distribution of words in the chosen corpus
    word_frequency = freq_dist[word]
    commonality_score = word_frequency / total_words if word_frequency > 0 else 0
    
    return commonality_score

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