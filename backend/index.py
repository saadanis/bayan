from flask import Flask, Response, json, request, g, session, render_template
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restful import reqparse
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS, cross_origin
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import threading
import os.path
import os
import json
import time
import sys

from backend.scrapper import scrapper
from backend.custom_search import custom_search
from backend.bert_rerank import bert_rerank
from backend.bert_rerank.arabert.preprocess import ArabertPreprocessor
from backend.quran.QuranDetectorAnnotater import qMatcherAnnotater
from backend.hadith.hadith_detector import Hadith_Annotator
from backend.db import dao

qAn = qMatcherAnnotater("./quran/")
hAn = Hadith_Annotator()
hAn.load("./hadith/")
dao.start_db("./db/")

auth = HTTPBasicAuth()
app = Flask(__name__)
CORS(app, supports_credentials=True, expose_headers='Authorization')

# ORIGIN = '212.71.244.70'
ORIGIN = 'localhost'

print("APP: Loading BERT.", flush=True)
ACCESS_TOKEN = "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"

# TOKENIZER = ""
# MODEL = ""
# PREPROCESSOR = ""

# TOKENIZER = AutoTokenizer.from_pretrained("saadanis/bayan_arabert_2", use_auth_token=ACCESS_TOKEN)
# MODEL = AutoModelForSequenceClassification.from_pretrained("saadanis/bayan_arabert_2", use_auth_token=ACCESS_TOKEN)
# PREPROCESSOR = ArabertPreprocessor("aubmindlab/bert-base-arabertv2")

TOKENIZER = AutoTokenizer.from_pretrained("./bert_rerank/bayan_arabert_2")
MODEL = AutoModelForSequenceClassification.from_pretrained("./bert_rerank/bayan_arabert_2")
PREPROCESSOR = ArabertPreprocessor("aubmindlab/bert-base-arabertv2")

# os.environ["TOKENIZERS_PARALLELISM"] = "false"

print("APP: BERT loaded.", flush=True)

@app.route('/',methods=['GET'])
def home():
    print("APP: index.html served.", flush=True)
    return render_template("index.html")

@app.route('/search',methods=['GET'])
@cross_origin(origin=ORIGIN, allow_headers=['Authorization'], supports_credentials=True)
@auth.login_required
def search():

    parser = reqparse.RequestParser()
    parser.add_argument('query', required=True, help='query is required.')
    parser.add_argument('language', required=True, help='language is required.')
    parser.add_argument('sites', required=True, help='sites is required.')
    parser.add_argument('start', required=True, help='start is required.')
    parser.add_argument('extract', required=True, help='extract is required')
    parser.add_argument('rerank', required=True, help='rerank is required')

    args = parser.parse_args()

    query = args['query']
    language = args['language']
    sites = args['sites']
    sites = sites.split(',')
    start = args['start']
    extract = args['extract']
    rerank = args['rerank']

    results = custom_search.get_results_from_sites(query, language, sites, start)

    for i in range(len(results)):
        results[i]['google_rank'] = i + 1
        if g.email != 'guest':
            results[i]['is_already_saved'] = dao.is_saved(g.email, results[i]['link'], query)

    if(g.email != 'guest'):
        if int(start) == 1:
            dao.add_history(g.email, query)

    if int(extract) == 1 or int(rerank) == 1:

        finalResults = []

        if int(extract) == 1:
            class extractionThread(threading.Thread):
                def __init__(self, threadID, name, query, result):
                    threading.Thread.__init__(self)
                    self.threadID = threadID
                    self.name = name
                    self.query = query
                    self.result = result

                    self.scraped_text = None
                    self.matches = None
                    self.hadiths = None

                    self.score = 0

                    self.index = 0

                def run(self):
                    print(f"{self.name}: Starting",flush=True)
                    
                    try:
                        if self.result['cache'] is None or not self.result['is_scraped']:
                            self.scraped_text, self.score, self.matches = scrapper.main(self.query, self.result['title'], self.result['link'], qAn, hAn)
                        else:
                            self.scraped_text = self.result['cache']
                            self.matches = self.result['matches']
                        
                        self.result['scraper_error'] = False
                            
                    except Exception as e:
                        print(f"{self.name}: Scraper error.")
                        print(f"{self.name}: {Exception} {e}")
                        self.result['scraper_error'] = True
                        self.score = -1

                    if self.score != -1:
                        self.result['snippet'] = self.scraped_text
                        print(f"{self.name}: Scraped from {self.result['title']}")
                    else:
                        print(f"{self.name}: Scraping failed.")
                    
                    if self.matches is not None:
                        self.result['matches'] = self.matches
                    else:
                        self.result['matches'] = []

                    finalResults.append(self.result)

                    print(f"{self.name}: Exiting")

            for i in range(len(results)):
                cache = dao.get_cache(results[i]['link'])
                if cache is not None:
                    results[i]['cache'] = cache[0]
                    results[i]['matches'] = json.loads(cache[1])
                    results[i]['is_scraped'] = dao.is_scraped(results[i]['link'])
                else:
                    results[i]['cache'] = None

            for i in range(len(results)):
                new_thread = extractionThread(i, f"T{i}", query, results[i])
                new_thread.start()

            while len(results) > len(finalResults):
                continue

            for i in range(len(finalResults)):
                if (finalResults[i]['cache'] is None) or (finalResults[i]['cache'] is not None and not finalResults[i]['scraper_error'] and not finalResults[i]['is_scraped']):
                    dao.update_cache(finalResults[i]['link'], finalResults[i]['snippet'], json.dumps(finalResults[i]['matches']), not finalResults[i]['scraper_error'])

            finalResults.sort(key=lambda x: x['google_rank'])

        else:
            finalResults = results.copy()
        
        if int(rerank) == 1:
            rerankingResults = []

            class rerankingThread(threading.Thread):
                def __init__(self, threadID, name, query, results):
                    threading.Thread.__init__(self)
                    self.threadID = threadID
                    self.name = name
                    self.query = query
                    self.results = results

                    self.preprocessed_query = None
                    self.preprocessed_answer = None
                    self.tokenized_example = None
                    self.classification_logits = None
                    self.classification_results = None

                def run(self):
                    print(f"{self.name}: Starting",flush=True)
                    
                    for i in range(len(self.results)):

                        # self.preprocessed_example = PREPROCESSOR(self.query)
                        # self.preprocessed_answer = PREPROCESSOR(self.results[i]['snippet'])

                        self.tokenized_example = TOKENIZER(self.query, self.results[i]['snippet'], return_tensors="pt", truncation=True)
                        self.classification_logits = MODEL(**self.tokenized_example).logits
                        self.classification_results = torch.softmax(self.classification_logits, dim=1).tolist()[0]

                        self.results[i]['scores'] = self.classification_results
                        self.results[i]['label'] = self.classification_results.index(max(self.classification_results))
                        print(f"{self.name}: Predicted {i+1}: {self.classification_results}", flush=True)

                    rerankingResults.extend(self.results)
                    print(f"{self.name}: Exiting")

            # reranking_thread_1 = rerankingThread(f"R1", f"R1", query, results[0:len(finalResults)])
            # reranking_thread_1.start()

            # reranking_thread_2 = rerankingThread(f"R2", f"R2", query, results[int(len(finalResults)/2):len(finalResults)])
            # reranking_thread_2.start()

            # reranking_thread_1 = rerankingThread(f"R1", f"R1", query, results[0:int(len(finalResults)/3)])
            # reranking_thread_1.start()

            # reranking_thread_2 = rerankingThread(f"R2", f"R2", query, results[int(len(finalResults)/3):int(len(finalResults)*2/3)])
            # reranking_thread_2.start()

            # reranking_thread_3 = rerankingThread(f"R3", f"R3", query, results[int(len(finalResults)*2/3):len(finalResults)])
            # reranking_thread_3.start()

            # while len(rerankingResults) < len(finalResults):
            #     continue 

            # finalResults = bert_rerank.rerank_on_label_scores(rerankingResults)

            for i in range(len(finalResults)):
                # print(f"Predicting Result {i+1}", flush=True)

                preprocessed_example = PREPROCESSOR.preprocess(query)
                preprocessed_answer = PREPROCESSOR.preprocess(finalResults[i]['snippet'])

                tokenized_example = TOKENIZER(preprocessed_example, preprocessed_answer, return_tensors="pt", truncation=True)
                classification_logits = MODEL(**tokenized_example).logits
                classification_results = torch.softmax(classification_logits, dim=1).tolist()[0]
                print(f"Result {i+1} prediction: {classification_results}", flush=True)

                finalResults[i]['scores'] = classification_results
                finalResults[i]['label'] = classification_results.index(max(classification_results))

                # finalResults[i]['scores'], finalResults[i]['label'] = bert_rerank.rerank(TOKENIZER, MODEL, f"result {i}", query, finalResults[i]['snippet'])

            finalResults = bert_rerank.rerank_on_label_scores(finalResults)

        response = {
            'results': finalResults
        }
  
    else:
        response = {
            'results': results
        }

    r = Response(
        response = json.dumps(response),
        mimetype = 'application/json',
        status = 200
    )

    print("Got to the end?", flush=True)

    return r


# from urllib.request import urlopen
# from bs4 import BeautifulSoup
# import requests
# import re

# @app.route('/testing',methods=['GET'])
# def testing():

#     f = open('new_dataset_answers.json')
#     new_dataset_answers_data = json.load(f)['data']
#     f.close()

#     # title_re=re.compile(r'<title>(.*?)</title>', re.UNICODE)

#     scores_value = [4,2,1]

#     for j in range(200):

#         # j = i + 50

#         # if new_dataset_answers_data[j]['snippet'] == "":
#         url = new_dataset_answers_data[j]['url']
#         question = new_dataset_answers_data[j]['question']

#         answer = new_dataset_answers_data[j]['answer']
#         snippet = new_dataset_answers_data[j]['snippet']

#         if answer == "":
#             answer = snippet
        
#         question = PREPROCESSOR.preprocess(question)
#         answer = PREPROCESSOR.preprocess(answer)

#         tokenized_example = TOKENIZER(question, answer, return_tensors="pt", truncation=True)
#         classification_logits = MODEL(**tokenized_example).logits
#         classification_results = torch.softmax(classification_logits, dim=1).tolist()[0]
#         # score_index = classification_results.index(max(classification_results))
#         # new_dataset_answers_data[j]['bert_score'] = scores_value[score_index]
#         new_dataset_answers_data[j]['bert_score'] = classification_results


#         print(j, new_dataset_answers_data[j]['label'], new_dataset_answers_data[j]['bert_score'])


#         # results = custom_search.get_results_from_sites("", 'ar', [url], 1)

#         # print(j)

#         # if len(results) > 0:
#         #     snippet = results[0]['snippet']
#         # else:
#         #     snippet = ""
#         # print(snippet)
#         # # print(results)
#         # print("")
#         # new_dataset_answers_data[j]['snippet'] = snippet
#         # soup = BeautifulSoup(urlopen(url))
#         # title = soup.title.get_text()

#         # reqs = requests.get(url)
#         # soup = BeautifulSoup(reqs.text, 'html.parser')

#         # title = soup.find_all('title')
#         # print(title)
#         # print("Title of the website is :", title)

#         # title_re=re.compile(r'<title>(.*?)</title>', re.UNICODE)
#         # try:
#             # r = requests.get(url)
#             # if r.status_code == 200:
#                 # match = title_re.search(r.text)
#                 # if match:
#                     # title = match.group(1)
#                 # else:
#                     # title = ""
#             # else:
#                 # title = ""
#         # except:
#             # title = ""

#         # print(i, title)

#         # if snippet != "":
            

#         # print(j)
#         # try:
#         #     # if not "answer" in new_dataset_answers_data[i]:
#         #     new_dataset_answers_data[j]['answer'], score, matches, hadiths = scrapper.main(question, url, qAn, hAn)
#         # except Exception as e:
#         #     new_dataset_answers_data[j]['answer'] = ""
            
#         # print(new_dataset_answers_data[j]['answer'])

#     json_string = json.dumps({'data': new_dataset_answers_data})
#     with open('new_dataset_answers.json', 'w') as outfile:
#         outfile.write(json_string)

#     r = Response(
#         response = "Done",
#         mimetype = 'application/json',
#         status = 200
#     )

#     return r

@app.route('/sites',methods=['PUT'])
@cross_origin(origin=ORIGIN, allow_headers=['Authorization'], supports_credentials=True)
@auth.login_required
def sites():

    print('entering sites')

    parser = reqparse.RequestParser()
    parser.add_argument('sites', required=True, help='sites is required.')
    args = parser.parse_args()

    sites = args['sites']
    sites = sites.split(',')
    print(sites)

    dao.update_user_sites(g.email, sites)

    r = Response(
        response = json.dumps(dao.get_user_sites(g.email)),
        status = 200
    )

    return r

@app.route('/registration',methods=['POST'])
@cross_origin(origin=ORIGIN, allow_headers=['Authorization'], supports_credentials=True)
def registration():
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, help='name is required.')
    parser.add_argument('email', required=True, help='email is required.')
    parser.add_argument('password', required=True, help='password is required.')
    parser.add_argument('sites', required=True, help='sites is required.')

    args = parser.parse_args()

    name = args['name']
    email = args['email']
    password = args['password']

    sites = args['sites']
    sites = sites.split(',')
    
    if dao.create_user(name, email, password):
        print("APP: User registered.")
        response = {
            'registration': True
        }
        r = Response(
            response = json.dumps(response),
            status = 200
        )
        if dao.update_user_sites(email, sites):
            print("APP: User sites added.")
        else:
            print("APP: User sites failed to add.")
    else:
        print("APP: User failed to register.") 
        response = {
            'registration': False
        }
        r = Response(
            response = json.dumps(response),
            status = 400
        )   

    return r

@app.route('/account',methods=['DELETE'])
@cross_origin(origin=ORIGIN, allow_headers=['Authorization'], supports_credentials=True)
@auth.login_required
def account():

    deleted = dao.delete_user(g.email)

    response = {
        'deleted': deleted
    }

    r = Response(
        response = json.dumps(response),
        status = 200 if deleted else 400
    )

    return r

@app.route('/history',methods=['GET','DELETE'])
@cross_origin(origin=ORIGIN, allow_headers=['Authorization'], supports_credentials=True)
@auth.login_required
def history():
    if request.method == 'GET':
        if g.email != 'guest':
            history = dao.get_history(g.email)
            response = {
                'history': history
            }
            r = Response(
                response = json.dumps(response),
                status = 200
            )
            return r
    elif request.method == 'DELETE':
        parser = reqparse.RequestParser()
        parser.add_argument('query', required=False)
        parser.add_argument('date', required=False)
        args = parser.parse_args()
        query = args['query']
        date = args['date']
        
        if g.email != 'guest':
            if query is None:
                response = {
                    'deleted': dao.delete_all_history(g.email)
                }
            else:
                response = {
                    'deleted': dao.delete_history(g.email, query, date)
                }
            r = Response(
                response = json.dumps(response),
                status = 200
            )
            return r

@app.route('/saved',methods=['GET','DELETE','POST'])
@cross_origin(origin=ORIGIN, allow_headers=['Authorization'], supports_credentials=True)
@auth.login_required
def saved():
    if request.method == 'GET':
        if g.email != 'guest':
            saved = dao.get_saved(g.email)
            response = {
                'saved': saved
            }

            r = Response(
                response = json.dumps(response),
                status = 200
            )
            return r

    elif request.method == 'DELETE':
        parser = reqparse.RequestParser()
        parser.add_argument('url', required=False, help='url is required.')
        args = parser.parse_args()
        url = args['url']
        
        if g.email != 'guest':
            if url is None:
                response = {
                    'deleted': dao.delete_all_saved(g.email)
                }
            else:
                response = {
                    'deleted': dao.delete_saved(g.email, url)
                }
            r = Response(
                response = json.dumps(response),
                status = 200
            )
            return r
    elif request.method == 'POST':
        parser = reqparse.RequestParser()
        parser.add_argument('query', required=True, help='query is required.')
        parser.add_argument('url', required=True, help='url is required.')
        args = parser.parse_args()
        query = args['query']
        url = args['url']

        if g.email != 'guest':

            dao.add_saved(g.email, url, query)
            dao.log(g.email, query, url, 'SVA')

            r = Response(
                status = 200,
                response = json.dumps('saved')
            )
            return r

@app.route('/update',methods=['PUT'])
@cross_origin(origin=ORIGIN, allow_headers=['Authorization'], supports_credentials=True)
@auth.login_required
def update():

    parser = reqparse.RequestParser()
    parser.add_argument('label', required=True)
    parser.add_argument('value', required=True)

    args = parser.parse_args()

    label = args['label']
    value = args['value']

    if label == 'email':
        response = {
            'updated': dao.update_email(g.email, value)
        }
    elif label == 'name':
        response = {
            'updated': dao.update_user(value, g.email, g.password)
        }
    elif label == 'password':
        name = dao.get_user_name(g.email)
        response = {
            'updated': dao.update_user(name, g.email, value)
        }

    r = Response(
        response = json.dumps(response),
        status = 200
    )
    return r

@app.route('/log',methods=['POST'])
@cross_origin(origin=ORIGIN, allow_headers=['Authorization'], supports_credentials=True)
@auth.login_required
def log():
    parser = reqparse.RequestParser()
    parser.add_argument('query', required=True)
    parser.add_argument('url', required=True)
    parser.add_argument('action', required=True)

    args = parser.parse_args()

    query = args['query']
    url = args['url']
    action = args['action']

    # EXP: expands answer.
    # COL: collapses answer.
    # CLK: clicks url.
    # HVR: hovers over verses/hadiths.
    # SVA: saves answer.
    # USV: unsaves answer.

    actions = ['EXP','COL','CLK','HVR','SVA','USV']

    if action in actions:
        dao.log(g.email, query, url, action)
        response = {
            'logged': True
        }
        status = 200
        print('logged',action)
    else:
        response = {
            'logged': False
        }
        status = 400

    r = Response(
        response = json.dumps(response),
        status = status
    )

    return r
    

@app.route('/validation',methods=['GET'])
@cross_origin(origin=ORIGIN, allow_headers=['Authorization'], supports_credentials=True)
@auth.login_required
def validation():
    if g.email == 'guest':
        response = 'Unauthorized Access'
        print("APP: User failed to sign in.")
    else:
        response = json.dumps({
            'name': dao.get_user_name(g.email),
            'sites': dao.get_user_sites(g.email)
        })
        print("APP: User signed in.")

    r = Response (
        response = response,
        status = 200
    )

    return r

@auth.verify_password
def verify_password(email, password):
    if not email:
        g.email = 'guest'
        return True
    else:
        if dao.authenticate_user(email, password):
            g.email = email
            g.password = password
            return True
        else:
            g.email = 'guest'
            return True
