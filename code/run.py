from preprocess import *
from data_download import *
from model import *
import argparse
import os

parser = argparse.ArgumentParser(description="Enter chromedriver path")
# chromedriver path argument
parser.add_argument("-c",
                    "--chromedriver", 
                    type=str,
                    help="Enter your chromedriver.exe path", 
                    required=True)

# data download
parser.add_argument("-d",
                    "--download",
                    type=str,
                    default="no"
                    help="Scrape and download recipe data from drinksmixer.com if yes (default: %(default)s)",
                    choices=["yes","no"]
                    required=False)

args = parser.parse_args()
chrome = args.chromedriver
re_download_data = args.download

if __name__ == "__main__":

    if re_download_data == "yes":
        retrieve_link()
        assert 'list_of_cocktail_recipe_links.pickle' in os.listdir("../data/")
        print("links retrieved and saved")

        download_data(chrome)
        assert 'cocktail_recipe_dict.pickle' in os.listdir("../data/")
        assert 'cocktail_recipe_instruction.pickle' in os.listdir("../data/")
        print("data download complete")


    clean_data()
    assert 'recipe_cleaned_v1.csv' in os.listdir("../data/")
    print("data cleaned")

