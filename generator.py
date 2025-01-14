from deep_translator import GoogleTranslator

# Function that translates input string into target language. Returns translated text
def translate(input : str, target_lang : str) -> str :
    return GoogleTranslator(source = "auto", target = target_lang).translate(input)

# TODO : create a function that will generate a fixed set of vocabulary words on which the exercices
# of the worksheet will be based upon
def get_vocab_bank() -> list[str] : 
    pass

# TODO : create a function that will generate a definition and grammatical usage guide on each vocabulary
# word included in the vocabulary set
def define(vocabulary : list[str]) -> dict :
    pass

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