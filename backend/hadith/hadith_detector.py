# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 14:36:47 2022
@author: boyou
"""

from . import utils
import dill as pickle
from . import builder
import re
slah = "صلى الله عليه وسلم"

class Hadith_Annotator:
    def load(self, path, filter=[1,3]):
        try:
            with open(path+"data", "rb") as fp:
                data = pickle.load(fp)
                self.table = data
                print("Hadith Data Loaded")
    
            with open(path+"stopwords.txt", "r", encoding="utf8") as fp:
                stopwords = fp.readlines()
                for x in range(len(stopwords)):
                    stopwords[x] = re.sub("\n", "", stopwords[x])
                self.stopwords = stopwords
                print("Stopwords Loaded")
        except FileNotFoundError:
            print("Hadith Data Not Found")
            print("Building the dataset. (This may takes hours)")
            self.build(path, filter)
    
    def build(self, path, filter):
        self.table = builder.build(path, filter)
        print("Data Built")
    
    def f1(self, text):
        found = []
        text = text.split()
        for x in range(len(text)):
            text[x] = utils.normalize(text[x])
        
        for x in range(len(text)):
            if text[x] == "":
                continue
            res = self.f2(text[x::], x)
            if res != -1:
                found.append(res)
        
        found = sorted(found, key=lambda d: d['startInText'])
        while 1:
            f = len(found)
            found = self.f5(found)
            s = len(found)
            
            if f == s:
                break
        return found

    def f2(self, text, st):
        table = self.table
        found = ""
        x = 0
        node = -1
        while x < len(text):
            word = text[x]
            x += 1
            if word == "":
                continue
            if word in table:
                found = found + word + " "
                node = table[word]
                table = node.table
                check = node.word.split()
                if len(check) > 1:
                    for y in range(1, len(check), 1):
                        if x >= len(text):
                            if self.f3(found, node):
                                return self.f4(found, node, st, st+x, 1)
                            else:
                                return -1
                        while text[x] == "":
                            x+=1
                            if x >= len(text):
                                if self.f3(found, node):
                                    return self.f4(found, node, st, st+x, 2)
                                else:
                                    return -1
                        
                        if check[y] == text[x]:
                            found = found + text[x] + " "
                            x += 1
                        else:
                            if self.f3(found, node):
                                return self.f4(found, node, st, st+x, 3)
                            else:
                                return -1
            else:
                if node == -1:
                    return -1
                
                if self.f3(found, node):
                    return self.f4(found, node, st, st+x-1, 4)
                else:
                    return -1
        if self.f3(found, node):
            return self.f4(found, node, st, st+x+1, 5)
        else:
            return -1

    def f3(self, text, node):
        if slah in text:
           le = len(text.split()) - len(slah)
        else:
            le = len(text.split())
        if le >= 5 and len(node.hadiths_ref) < 2 and len(node.hadiths_ref) > 0:
            return True
        else:
            return False
    
    def f4(self, found, node, st, en, c):
        h = list(node.hadiths_ref)[0]
        return {"text": found, 
                "startInText":st, 
                "endInText":en, 
                "ref":
                    {"bk_name":h.bk_name[0],
                     "ch_name":h.ch_name[0],
                     "sec_name":h.sec_name[0],
                     "num":h.num,
                     "grade":h.grade[0]},
                "case":c
                }
    
    def f5(self, found):
        for x in range(len(found)):
            if x+1 >= len(found):
                break
            prev = found[x]
            match = found[x+1]
            
            start0 = prev["startInText"]
            end0 = prev["endInText"]
            len0 = end0 - start0
            
            start1 = match["startInText"]
            end1 = match["endInText"]
            len1 = end1 - start1
            
            if start1 < end0:
                if len0<len1:
                    found.remove(prev)
                else:
                    found.remove(match)
        return found