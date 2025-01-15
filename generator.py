import nltk
import random
import pickle

from deep_translator import GoogleTranslator
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk.probability import FreqDist

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

# Loading words list from assets - If file doesn't exist, download it and pickle it in assets
try : 
    with open("assets/words_list", "rb") as f :
        n_list, v_list, a_list = pickle.load(f)
except :
    nltk.download("wordnet")
    nltk.download("omw-1.4")

    synsets_n = list(wn.all_synsets('n'))
    synsets_v = list(wn.all_synsets('v'))
    synsets_a = list(wn.all_synsets('a'))

    nouns = set(lemma.name() for syn in synsets_n for lemma in syn.lemmas())
    verbs = set(lemma.name() for syn in synsets_v for lemma in syn.lemmas())
    adjectives = set(lemma.name() for syn in synsets_a for lemma in syn.lemmas())

    n_list, v_list, a_list = list(nouns), list(verbs), list(adjectives)

    # Save precomputed data to a pickle file
    with open("assets/words_list", "wb") as f:
        pickle.dump((n_list, v_list, a_list), f)

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
def get_random_word(list : list) :
    return "".join(random.sample(list, 1))

# Function retrieving the definition of an English word
def get_definiton(word : str) -> str :
    synonyms = wn.synsets(word)
    return synonyms[0].definition()

# Function that generates a vocabulary bank based on desired level of difficulty 
def get_vocab_bank(count : int, target : str, level : float) -> list[str] : 

    vocab_bank = []
    word_types = [n_list, v_list, a_list]
    word = ""

    for word_type in word_types :
        for i in range(count) :
            commonality_score, word = 0, ""
            while commonality_score < 5e-6 - level*2e-6 :
                word = get_random_word(word_type)
                commonality_score = get_commonality_score(word)
                print(word, commonality_score)
            vocab_bank.append({"word" : translate(word, target), "translation" : word, "definition" : get_definiton(word)})
    
    return vocab_bank

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