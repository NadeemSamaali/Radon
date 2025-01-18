import nltk
import random
import pickle
import math

from deep_translator import GoogleTranslator
from nltk.corpus import words
from nltk.probability import FreqDist

from nltk.corpus import wordnet as wn

# Loading wordnet from assets
try :
    with open('assets/wordnet.pkl', 'rb') as file:
        wn = pickle.load(file)
except :
    # Download WordNet (if you haven't already)
    nltk.download('wordnet', quiet=True)

    # Serialize the WordNet object
    with open('assets/wordnet.pkl', 'wb') as file:
        pickle.dump(wn, file)

# Loading words_data from assets
try :
    with open('assets/words_data.pkl', 'rb') as file :
        common_words = pickle.load(file)

except :
    nltk.download('words', quiet=True)

    word_list = words.words()

    common_words = [ # Filtering out proper nounds and numbers from data set
        word for word in word_list
        if word.islower() and word.isalpha() 
    ]

    with open('assets/words_data.pkl', 'wb') as file :
        pickle.dump(common_words, file)

# Loading frequency_data from assets
try :
    with open('assets/frequency_data.pkl', 'rb') as file :
        fdist = pickle.load(file)

except :
    fdist = FreqDist(common_words)
    with open('assets/frequency_data.pkl', 'wb') as file :
        pickle.dump(fdist, file)

# Creating and configuring the Gemini 1.5-Falsh-8B Model
import google.generativeai as genai

genai.configure(api_key="AIzaSyBQqnpIRFvNbjrZBDp1Fjgi_IsQmPpgcHU")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

# Function that translates input string into target language. Returns translated text
def get_translation(input : str, target_lang : str) -> str :
    return GoogleTranslator(source = "auto", target = target_lang).translate(input)

# Function that assigns a score to a word based on its commonality / difficulty
def get_word_score(word : str) -> float :

    word = word.lower()
    frequency = fdist[word]
    total_words = len(common_words)

    raw_commonality = frequency / total_words
    commonality_score = raw_commonality #* length_factor

    return -math.log10(commonality_score)

# Function that generates a random english word for a list of nouns, adjectives, or verbs
def get_random_word(list : list) :
    return "".join(random.sample(list, 1))

# Function retrieving the definition of an English word
def get_definiton(word : str) -> str :
    synsets = wn.synsets(word)
    return synsets[0].definition()

# Function that generates a vocabulary bank of commonly used words
def get_vocabulary(count : int) -> list[str] : 
    output = []
    i = 0
    while i < count :
        word = random.sample(common_words, 1)[0]
        # Filtering out words with a word score above 5.3 -- words above that threshhold are of uncommon usage
        if get_word_score(word) < 5.3 and len(word) > 3 and word not in output :
            output.append(word)
            i += 1
    return output

# Writes vocabulary bank in markdown
def build_vocab(vocab : list[str], target : str) -> str:
    output = "## Vocabulary \nHere are the words that will be covered in this worksheet. \n|Word|Translation|Definition|\n|:----|:----|:----|\n"

    for word in vocab :
        row = f'|{get_translation(word,target)}|{word}|{get_definiton(word)}|\n'
        output += row

    return output


# Writes a sentence containing a specific word
def write_paragraph(word : list[str], lang : str) -> str :
        prompt = f'Write a sentence in {lang}, for each of the following words {word}'
        response = (chat_session.send_message(prompt)).text
        return response

"""
# Writes a fill in the blank exercice in language of choice
def build_fill_in_the_blank(lang : str, length : float, vocabulary : list[str]) -> str :
    output = "\n# Fill in the blank \n Fill the blank spaces with the appropriate word from the vocabulary bank. \n\n"
    sentences = []
    blank_sentences = []

    for word in vocabulary :
        for i in range(length) :
            response = write_sentence(word["word"], lang)
            sentences.append(response)

    temp_str = []
    for i in range(len(sentences)) :
        temp_str.extend(sentences[i].split(f'{vocabulary[i]["word"]}'))
        blank_sentences.append(f'{" ____________ ".join(temp_str)}')
        temp_str = []

    random.shuffle(blank_sentences)

    for i in range(len(blank_sentences)) :
        output += f'{i+1}. {blank_sentences[i]}'
    
    return output
"""

# TODO : create a function that will generate a translation exercice
def build_translation(lang : str, level : float, len : int, vocabulary : list[str]) -> str :
    pass

# TODO : create a function which will generate a PDF file worksheet.
def generate_doc(lang : str, level : float, len : int, vocabulary : list[str]) :
    pass