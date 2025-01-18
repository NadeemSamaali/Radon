import nltk
import random
import pickle
import math
import os
import asyncio

from googletrans import Translator

from nltk.corpus import words
from nltk.probability import FreqDist

from nltk.corpus import wordnet as wn

# Create worksheets directory if it doesnt exist
directory = "worksheets"
os.makedirs(directory, exist_ok=True)

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
async def get_translation(input : str, target : str) -> str :
    # Initialize the Translator
    translator = Translator()

    # Translate the word asynchronously
    translation = await translator.translate(input, dest=target)

    return translation.text

# Function that fetches the romanization of a word / phonetic pronounciation
async def get_pronunciation(input, target='en'):
    # Initialize the Translator
    translator = Translator()

    # Translate the word asynchronously
    translation = await translator.translate(input, dest=target)
    
    # Check if pronunciation is available and print it
    if translation.pronunciation:
        return translation.pronunciation
    else:
        pass

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
        # print(word, get_word_score(word))
        if get_word_score(word) < 5.1 and len(word) > 3 and word not in output :
            output.append(word)
            i += 1
    return output

# Writes vocabulary bank in markdown
def build_vocab(vocab : list[str], target : str) -> str:

    output = ""
    test_prn = asyncio.run(get_pronunciation(vocab[0], target=target))

    if test_prn == None :

        output = "\n### Vocabulary \nHere are the words that will be covered in this worksheet. \n|Word|Translation|Definition|\n|:----|:----|:----|\n"

        for word in vocab :
            row = f'|{asyncio.run(get_translation(word,target))}|{word}|{get_definiton(word)}|\n'
            output += row
    else :

        output = "\n### Vocabulary \nHere are the words that will be covered in this worksheet. \n|Word|Pronounciation|Translation|Definition|\n|:----|:----|:----|:----|\n"

        for word in vocab :
            row = f'|{asyncio.run(get_translation(word,target))}|{asyncio.run(get_pronunciation(word, target=target))}|{word}|{get_definiton(word)}|\n'
            output += row

    return output

# Writes a sentence containing a specific word
def write_paragraph(word : list[str], lang : str) -> str :
        prompt = f'Write a sentence in {lang}, for each of the following words {word}'
        response = (chat_session.send_message(prompt)).text
        return response

def build_fill_in_the_blank(vocab : list[str], paragraph : list[str]) -> str :

    sentences = paragraph
    filtered = []
    parsed = []    
    for sentence in sentences :
        if sentence != '' :
            filtered.append(sentence)

    for word in filtered :
        parsed.append(word.split('*'))

    parsed = [[word for word in element if word != '' and word != ' '] for element in parsed]
    print(parsed)
    parsed = [element[-1] for element in parsed if len(element) > 1 ]
    print(parsed)
    
    blanks = []
    for i in range(len(parsed)) :
        blanks.append(parsed[i].split(vocab[i]))
    
    parsed = [" ________________ ".join(element) for element in blanks]
    random.shuffle(parsed)

    output = "\n### Fill in the blank \nIn this exercice, fill in the blanks in each sentence with the appropriate vocabulary word from the word bank\n\n"
    for i in range(len(parsed)) :
        output += f'{i+1}. {parsed[i]}\n \n \n' 

    return output

# TODO : create a function that will generate a translation exercice
def build_translation(lang : str, level : float, len : int, vocabulary : list[str]) -> str :
    pass

def generate_doc(lang : str, len : int) :
    directory = "worksheets"
    all_items = os.listdir(directory)
    file_count = sum(1 for item in all_items if os.path.isfile(os.path.join(directory, item)))
    
    output = "# Worksheet"
    vocabulary = get_vocabulary(len)

    output += build_vocab(vocabulary, lang)
    translated_words = [asyncio.run(get_translation(word, lang)) for word in vocabulary]
    paragraph = write_paragraph(translated_words, lang)
    sentences = paragraph.split("\n")

    output += build_fill_in_the_blank(translated_words, sentences)
    print(output)
    
    with open(f'worksheets/sheet_{file_count+1}.md', 'w', encoding='utf-8') as file :
        file.write(output)