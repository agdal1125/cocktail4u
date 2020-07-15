import requests
from bs4 import BeautifulSoup
import time
import pickle
from selenium import webdriver

def retrieve_link():
    """
    Get all cocktail recipe links from https://drinksmixer.com
    Saves collected data as pickle output
    """

    base_url = "http://www.drinksmixer.com/cat/1/"
    pages = range(1,125)  # total 124 pages exist (2019.10.29)

    cocktail_links = []
    cocktail_name_list = []

    for i in pages:
        
        # Set URL
        url = base_url+str(i)
        req = requests.get(url)
        html = req.text
        
        # Parse HTML with bs4
        soup = BeautifulSoup(html,'html.parser')
        
        # Find all recipe links
        drinks_box = soup.find("div",{"class":"m1"}).find("div",{"class":"min"}).find("div",{"class":"clr"}).find("tr")
        urls_in_page = drinks_box.find_all("a")
        
        for link in urls_in_page:    
            cocktail_links.append("http://www.drinksmixer.com" + link["href"])
            cocktail_name_list.append(link.text)
            
            
    print("Links collected in {}".format(time.ctime()))
    print("Total number of links collected: ", len(cocktail_links))

    with open("../data/list_of_cocktail_recipe_links.pickle", "wb") as t:
        pickle.dump(cocktail_links, t)
        print("All collected recipe links are saved as '../data/list_of_cocktail_recipe_links.pickle'")
    t.close()
    return



def download_data(chrome_path_url="/Users/nowgeun/Desktop/chromedriver"):
    """
    Download cocktail data and save them as pickle data

    params
    ------
    chrome_path_url: string; path where your chromedriver.exe exist
    """
    driver = webdriver.Chrome(chrome_path_url)

    # Tracking progress
    done = []

    cocktail_recipes = {}
    cocktail_instructions = {}
    cocktail_descriptions = {}

    for one_url in cocktail_links:
        driver.get(one_url)
        
        # Cocktail name
        cocktail_name = driver.find_element_by_class_name("recipe_title").text

        # Cocktail Recipe (Ingredients)
        cocktail_recipe = driver.find_element_by_class_name("recipe_data").find_elements_by_class_name("ingredient")
        
        # Cocktail Recipe (Instructions)
        try:
            cocktail_inst = driver.find_element_by_xpath("//*[@class='RecipeDirections instructions']")
        except:
            pass
        
        recipe_dict = {} # Recipe of one cocktail
        
        for ingrdnt in cocktail_recipe:
            amount = ingrdnt.find_element_by_class_name("amount").text
            ing_name = ingrdnt.find_element_by_class_name("name").text
            
            recipe_dict[ing_name] = amount
        
        # Save one cocktail recipe to the whole dictionaries
        cocktail_recipes[cocktail_name] = recipe_dict
        
        if cocktail_inst:
            cocktail_instructions[cocktail_name] = cocktail_inst.text.strip()
            
        done.append(one_url)

    with open("../data/cocktail_recipe_dict.pickle", "wb") as f:
        pickle.dump(cocktail_recipes, f)
        print("All collected recipe (ingredients) are saved as '../data/cocktail_recipe_dict.pickle'")

    with open("../data/cocktail_recipe_instruction.pickle", "wb") as j:
        pickle.dump(cocktail_instructions, j)
        print("All collected recipe (instructions) are saved as '../data/cocktail_recipe_instruction.pickle'")

    f.close()
    j,close()
    return

