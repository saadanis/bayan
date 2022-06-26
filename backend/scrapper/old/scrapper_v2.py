# -*- coding: utf-8 -*-
"""
Done By: Abdulrahman

Second Version
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import unicodedata
import string


def get_data(raw):
    data = []
    term = ""
    for x in raw:
        x = x.strip()
        if x != "":
            term = term + x
        elif term != "":
            data.append(term)
            term = ""
        else:
            continue
    
    return sorted(data, key=len)

def get_score(sample, query):
    score = 0  # initial score
    for sample_word in sample:  # for each word in the sample
        for query_word in query:  # for each word in the query
            if sample_word == query_word:  # if they are the same
                score = score + 1  # increment the score by 1
    return score  # return the score

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def preprocess(s):
    s = strip_accents(s)
    s = s.replace("ال", "")
    s = s.translate(str.maketrans('', '', string.punctuation+'؟؛،'))
    return s

def launch_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # make the chrome headless
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36' # add the user agent
    chrome_options.add_argument(f'user-agent={user_agent}')
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs) # do not render the images
    driver = webdriver.Chrome("chromedriver", chrome_options=chrome_options) # launch the driver
    return driver

def main(qr,url):
# =============================================================================
#     Hyperparameters
# =============================================================================
    threshold = -10
    
# =============================================================================
#     Getting the HTML tree
# =============================================================================
    content = requests.get(url).content # load the html
    i = content.find(b'\xd8\xa7') # check if first arabic alpabet exist
    # print(i)
    if i == -1: # if no possible answer, use silenium
        driver = launch_chrome()
        driver.get(url)
        content = driver.page_source
        driver.quit()
    soup = BeautifulSoup(content, 'html.parser') # parse the html 
    raw = soup.body.text.splitlines()
    
# =============================================================================
#     Preporcessnig the query
# =============================================================================
    qr = preprocess(qr) #preprocess
    vocab = qr.split()
    
# =============================================================================
#     Deciding the answer
# =============================================================================
    sorted_data = get_data(raw) # sort by the size
    # if get_score(strip_accents(sorted_data[-1]), vocab) > 0: # return the biggest text if there is relevancy 
    #     return sorted_data[-1]
    
    score = -1
    index = -1
    for x in range(threshold, 0, 1): # if not return the highest relevacny
        # print(sorted_data[x])
        test = preprocess(sorted_data[x])
        # print(test)
        test = test.split()
        # print(test)
        temp = get_score(test, vocab)*len(sorted_data[x]) # score is counting multiplt the length
        # print("Relevacny: " + str(get_score(test, vocab)))
        # print("Length: " + str(len(sorted_data[x])))
        # print("Score: " + str(temp))
        if temp > score:
            score = temp
            index = x
            # print("Index: ", index)
    
    return sorted_data[index], score
