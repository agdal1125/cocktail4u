import pickle
import pandas as pd
import numpy as np
import re


def frac_to_dec_converter(num_strings):

    """
    Takes a list of strings that contains fractions and convert them into floats.

    @Params
    - list_of_texts: list of str

    @Returns
    - list of floats

    @Example:
    [ln] >> frac_to_dec_converter(["1", "1/2", "3/2"])
    [Out] >> [1.0, 0.5, 1.5]
    """
    result = []

    for frac_str in num_strings:
        try:
            converted = float(frac_str)
        except ValueError:
            num, denom = frac_str.split('/')
            try:
                leading, num = num.split(' ')
                total = float(leading)
            except ValueError:
                total = 0
            frac = float(num) / float(denom)
            converted = total + frac

        result.append(converted)
        
    return result


def unit_unify(list_of_texts):
    """
    Takes a list of strings that contains liquid units, and convert them into fluid ounces.
    
    @Params
    - list_of_texts: list of str
    
    @Returns
    - list of str
    
    @Example:
    [ln] >> detector(["1 oz", "2ml", "4cup"])
    [Out] >> ["1 oz", "0.067628 oz", "32 oz"]
    """
    # use regex to find units
    # Defining re pattern
    pattern = r"(^[\d -/]+)(oz|ml|cl|tsp|teaspoon|tea spoon|tbsp|tablespoon|table spoon|cup|cups|qt|quart|drop|drops)"
    
    # Create Empty list to store refined data
    new_list = []
    
        # use oz as standard unit
    liquid_units = {"oz":1,
                    "ml":0.033814,
                    "cl": 0.33814,
                    "tsp":0.166667,
                    "teaspoon":0.166667,
                    "tea spoon":0.166667,
                    "tbsp":0.5,
                    "tablespoon":0.5,
                    "table spoon":0.5,
                    "cup": 8,
                    "cups": 8,
                    "qt":0.03125,
                    "quart":0.03125,
                    "drop":0.0016907
                }
    
    # Search
    for text in list_of_texts:
        re_result = re.search(pattern, text)
        
        # If there is a matching result
        if re_result:
            # Seperate the matched pattern into two groups: amount(numbers), unit(measurement)
            amount = re_result.group(1).strip()
            unit = re_result.group(2).strip()

            # Convert all unit into oz
            ### Checking range in values 
            if "-" in amount:
                ranged = True
            else:
                ranged = False
            
            ### Replace non digit characters to plus sign
            ###### Dealing with exception type1: (1 /12 oz should be 1/12 oz)
            amount = re.sub(r"(\d) (/\d)",r"\1\2",amount) 
            amount = amount.replace("-","+").replace(" ","+").strip()
            ###### Dealing with exception type2: (1 - 2 produces 1+++2)
            amount = re.sub(r"[+]+","+",amount)
            ### Split them and add
            amount_in_dec = frac_to_dec_converter(amount.split("+"))
            amount = np.sum(amount_in_dec)
            
            if ranged:
                to_oz = (amount*liquid_units[unit])/2
            else:
                to_oz = amount*liquid_units[unit]

            # append refined string to the new list
            new_list.append(str(round(to_oz,2))+" oz")

        else:
            new_list.append(text)
            
    return new_list


def clean_data():
    """
    preprocess data before modeling
    1. remove unnecessary suffix
    2. fill na with empty string
    3. convert fraction to decimal
    4. unify different measurements
    """

    with open("../data/cocktail_recipe_dict.pickle", "rb") as g:
        cocktail_recipes = pickle.load(g)
    
    with open("../data/cocktail_recipe_instruction.pickle", "rb") as h:
        cocktail_instructions = pickle.load(h)

    data_dict = {}

    # Remove suffix ' recipe'
    for key,value in cocktail_recipes.items():
        data_dict[key.replace(" recipe","")] = value
    df = pd.DataFrame(data_dict)

    # Fill NA with empty string
    df = df.fillna("")

    # unify different measurement units
    for drink in df.columns:
        df[drink] = unit_unify(df[drink])
    
    df.to_csv("../data/recipe_cleaned_v1.csv")
    print("successfully processed")
    return



if __name__ == "__main__":
    clean_data()
