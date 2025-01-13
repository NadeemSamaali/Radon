# TODO : create a function that will generate a fixed set of vocabulary words on which the exercices
# of the worksheet will be based upon
def get_vocab_bank() -> str[list] : 
    pass

# TODO : create a function that will generate a definition and grammatical usage guide on each vocabulary
# word included in the vocabulary set
def define(vocabulary : str[list]) -> dict :
    pass

# TODO : create a function that will generate a fill in the blank exercice based on a fixed set
# of vocabulary words
def fillin_ex(lang : str, level : float, len : int, vocabulary : str[list]) -> str :
    pass

# TODO : create a function that will generate a translation exercice
def translation_ex(lang : str, level : float, len : int, vocabulary : str[list]) -> str :
    pass

# TODO : create a function which will generate a PDF file worksheet.
def generate_doc(lang : str, level : float, len : int, vocabulary : str[list]) :
    pass