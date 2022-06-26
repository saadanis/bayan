import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import math
import threading
import time

# PATH = "../bert_rerank/saved_model/"

# print("loading BERT", flush=True)
# tokenizer = AutoTokenizer.from_pretrained(PATH, local_files_only=True)
# model = AutoModelForSequenceClassification.from_pretrained(PATH)

# access_token = "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"
# tokenizer = AutoTokenizer.from_pretrained("saadanis/bayan_arabert", use_auth_token=access_token)
# model = AutoModelForSequenceClassification.from_pretrained("saadanis/bayan_arabert", use_auth_token=access_token)
# print("BERT loaded",flush=True)

def rerank(tokenizer, model, t_name, question, answer):

    print(f"reranking {t_name}",flush=True)

    split_length = 200

    num_of_splits = int(math.ceil(len(answer.split())/split_length))

    splits = []

    for i in range(num_of_splits):
        start_index = i*split_length
        if i < num_of_splits-1: 
            splits.append(' '.join(answer.split()[start_index:(start_index+split_length)]))
        else:
            splits.append(' '.join(answer.split()[start_index:(len(answer.split())-1)]))

    results_from_splits = []

    # class classifierThread(threading.Thread):
    #     def __init__(self, threadID, name, question, split):
    #         threading.Thread.__init__(self)
    #         self.threadID = t_name + threadID
    #         self.name = t_name + name
    #         self.question = question
    #         self.split = split

    #         self.tokenized_example = None
    #         self.classification_logits = None
    #         self.classification_results = None
        
    #     def run(self):
    #         print(f"{self.name}: Starting")
    #         self.tokenized_example = tokenizer(self.question, self.split, return_tensors="pt")
    #         self.classification_logits = model(**self.tokenized_example).logits
    #         self.classification_results = torch.softmax(self.classification_logits, dim=1).tolist()[0]
    #         results_from_splits.append(self.classification_results)
    #         print(f"{self.name}: {self.classification_results}")
    #         print(f"{self.name}: Exiting")

    # for i in range(len(splits)):
    #     new_thread = classifierThread(f"C{i}", f"C{i}", question, splits[i])
    #     new_thread.start()
    
    # while len(splits) > len(results_from_splits):
    #     continue

    for i in range(len(splits)):
        print(f"{t_name} starting",flush=True)
        tokenized_example = tokenizer(question, splits[i], return_tensors="pt")
        print(f"{t_name} tokenized", flush=True)
        try:
            classification_logits = model(**tokenized_example).logits
        except:
            print("model error",flush=True)
        print(f"{t_name} logits",flush=True)
        classification_results = torch.softmax(classification_logits, dim=1).tolist()[0]
        results_from_splits.append(classification_results)

    max_results = get_max_results(results_from_splits)
    label = max_results.index(max(max_results))

    return max_results, label

def get_max_results(results):
    max_results = results[0]
    for i in range(len(results)):
        for j in range(len(results[i])):
            if results[i][j] > max_results[j]:
                max_results[j] = results[i][j]
    
    return max_results

def rerank_on_label_scores(results):

    # results_0 = [r for r in results if r['label'] == 0]
    # results_1 = [r for r in results if r['label'] == 1]
    # results_2 = [r for r in results if r['label'] == 2]

    # results_0 = sorted(results_0, key=lambda x: x['scores'][0], reverse=True)
    # results_1 = sorted(results_1, key=lambda x: x['scores'][1], reverse=True)
    # results_2 = sorted(results_2, key=lambda x: x['scores'][2])

    # ranked_results = results_0 + results_1 + results_2

    ranked_results = sorted(results, key=lambda x: x['scores'][0], reverse=True)

    for i in range(len(ranked_results)):
        ranked_results[i]['bert_rank'] = i + 1
        print(f"[{round(ranked_results[i]['scores'][0], 3)},{round(ranked_results[i]['scores'][1], 3)},{round(ranked_results[i]['scores'][2], 3)}] B:{ranked_results[i]['bert_rank']} G:{ranked_results[i]['google_rank']}")

    return ranked_results
