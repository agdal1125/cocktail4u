import pandas as pd
import fasttext
from sklearn.metrics.pairwise import cosine_similarity as cos_sim

# Preprocessing for Embedding

def phrase_to_word(phrase):
    """
    Replace spaces in a phrase to underscores to treat it as one word

    Params
    ----
    phrase: str

    Returns
    ----
    str    returns phrases with spaces as underscores to treat Proper Nouns as one word
    """
    if type(phrase) == str:
        return "_".join(phrase.split())
    
    elif type(phrase) == list:
        return ["_".join(element.split()) for element in phrase]


def create_instruction_corpus():
    """
    Create corpus from cocktail instructions data.

    Returns
    ----
    str    returns corpus of preprocessed cocktail instructions
    """
    with open("./pickle_data/cocktail_recipe_instruction.pickle", "rb") as h:
        cocktail_instructions = pickle.load(h)

    corpus = []

    for key,value in cocktail_instructions.items():
        drink_name = phrase_to_word(key)
        drink_name = drink_name.replace(" recipe","")
        ingred_names = phrase_to_word(list(cocktail_recipes[key].keys()))
        ingred_names = ", ".join(ingred_names)
        
        sentence = "{} is made with {}".format(drink_name, ingred_names)
        
        corpus.append(value + " " + sentence)
    
    corpus = " ".join(corpus)
    with open("../data/instruction_corpus.txt","w") as f:
        f.write(corpus)
    f.close()
    print("corpus data created")
    return




def embed_drinks(corpus_path):
    """
    Embed recipe instruction corpus to pretrained fasttext model

    Params
    ----
    corpus_path: str    filepath to recipe instruction corpus to train and embed
    ing_path: str    filepath to information that contains recipe ingredient x drinks

    Returns
    ----
    pd.DataFrame    pandas dataframe that contains cosine similarity of embedded drinks
    """
    df = pd.read_csv("../data/recipe_cleaned_v1.csv", index_col=0, dtype=str)
    df = df.fillna("0")
    
    model = fasttext.train_unsupervised("../data/instruction_corpus.txt")
    embedded_drinks = [model.get_word_vector(x) for x in df.columns]

    # compute cosine similarity between drinks
    sim_matrix = pd.DataFrame(cos_sim(embedded_drinks), columns=phrase_to_word(list(df.columns)),
                            index=phrase_to_word(list(df.columns)))

    return sim_matrix
    


    
def cos_sim_drinks(sim_matrix, drink, num_result=30):
    """
    Returns the top 30 cosine similarity score of input drink name and other drinks.

    Params
    ----
    sim_matrix: pd.DataFrame    output of 'embed_drinks' function
    drink: str    name of the drink
    num_result: int    length of the result

    Returns
    ----
    Returns top results of similarity scores and drink names
    """
    assert type(num_result) == int, "the number of results you want to see must be an integer"
    assert drink in sim_matrix.columns, "use a proper drink name"

    return sim_matrix.sort_values(by=[drink],ascending=False)[drink][:num_result]

