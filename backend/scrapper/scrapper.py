# -*- coding: utf-8 -*-
"""
Done By: Abdulrahman

Second Version
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import string
import regex as re

from nltk.stem.isri import ISRIStemmer
stemmer = ISRIStemmer()

normal_alaf = "ا"
forged_alafs = "[أإآ]"
forged_ha = r"ة\b"
normal_ha = "ه"
forged_ya = r"ي\b"
normal_ya = "ى"
punctuation = "[" + string.punctuation + 'ـ؟؛،' + "]"
tashkeels = "[ًٌٍَُِّْ]"
en = "[A-Za-z]"

def get_data(raw):
    data = []
    term = ""
    for x in raw:
        # print(x)
        if re.search(en, x): # found english letters? skip
            # print(re.search(en, x))
            # print(x)
            continue
        x = x.strip()
        if x != "":
            term = term + " " + x
            # print(term)
        elif term != "":
            # print("YES")
            term = " ".join(term.split())
            data.append(term)
            term = ""
    return sorted(data, key=len, reverse=True)

def get_score(sample, query):
    score = 0  # initial score
    for sample_word in sample:  # for each word in the sample
        for query_word in query:  # for each word in the query
            if sample_word == query_word:  # if they are the same
                score = score + 1  # increment the score by 1
    return score  # return the score

def preprocess(text):
    text = re.sub(tashkeels, "", text)
    text = re.sub(punctuation, " ", text)
    text = re.sub(forged_alafs, normal_alaf, text)
    text = re.sub(forged_ha, normal_ha, text)
    text = re.sub(forged_ya, normal_ya, text)
    text = text.split()
    for x in range(len(text)):
        text[x] = stemmer.stem(text[x])
    
    return " ".join(text) 

def launch_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # make the chrome headless
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36' # add the user agent
    chrome_options.add_argument(f'user-agent={user_agent}')
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs) # do not render the images
    driver = webdriver.Chrome("chromedriver", chrome_options=chrome_options) # launch the driver
    return driver

def remove_overlap(matches):
    for x in range(len(matches)):
        if x+1 >= len(matches):
            break
        prev = matches[x]
        match = matches[x+1]
        
        start0 = prev["startInText"]
        end0 = prev["endInText"]
        type0 = prev["tag"]
        len0 = end0 - start0
        
        start1 = match["startInText"]
        end1 = match["endInText"]
        type1 = match["tag"]
        len1 = end1 - start1
        
        if start1 < end0:
            if type0 == type1:
                if len0<len1:
                    matches.remove(prev)
                else:
                    matches.remove(match)
            else:
                if type0 == "hadith" and type1 == "quran":
                    matches.remove(prev)
                else:
                    matches.remove(match)
    return matches

def main(qr, title, url, qAn, hAn):
# =============================================================================
#     Hyperparameters
# =============================================================================
    threshold = 10
    
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
    # print(raw)
    
# =============================================================================
#     Preporcessnig the query
# =============================================================================
    qr = preprocess(qr) #preprocess
    title = preprocess(title)
    vocab = set(qr.split()+title.split())
    
# =============================================================================
#     Deciding the answer
# =============================================================================
    sorted_data = get_data(raw) # sort by the size
    # print(sorted_data)
    
    score = -1
    index = -1
    for x in range(0, threshold, 1): # if not return the highest relevacny
        # print(sorted_data[x])
        if x >= len(sorted_data):
            break
        test = preprocess(sorted_data[x])
        # print(test)
        test = test.split()
        # print(test)
        temp = get_score(test, vocab)*len(sorted_data[x]) # score is counting multiple the length
        # print("Relevacny: " + str(get_score(test, vocab)))
        # print("Length: " + str(len(sorted_data[x])))
        # print("Score: " + str(temp))
        if temp > score:
            score = temp
            index = x
            # print("Index: ", index)
        # print("\n")
    
    found = []
    if score > 0:
        result = sorted_data[index]
        
        quran = qAn.matchAll(inText=sorted_data[index], findErr=False, findMissing=False)
        for x in quran:
            x["tag"] = "quran"
        
        hadith = hAn.f1(sorted_data[index])
        for x in hadith:
            x["tag"] = "hadith"
        
        found = quran+hadith
        if len(found) != 0:
            found  = sorted(found, key=lambda d: d['startInText'])
            
            while 1:
                f = len(found)
                found = remove_overlap(found)
                s = len(found)
                
                if f == s:
                    break
    else:
        result = ""
        found = []

    return result, score, found

# url = "https://binbaz.org.sa/fatwas/9133/%D8%AD%D9%83%D9%85-%D8%A7%D9%84%D8%AA%D9%8A%D9%85%D9%85-%D8%AD%D8%A7%D9%84-%D9%88%D8%AC%D9%88%D8%AF-%D8%A7%D9%84%D9%85%D8%A7%D8%A1-%D9%88%D9%88%D9%82%D8%AA-%D8%AC%D9%88%D8%A7%D8%B2%D9%87"
# qr = "حكم التيمم حال وجود الماء ووقت جوازه"
# main(qr, url, 0, 0)