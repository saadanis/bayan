import glob
import pandas as pd
from . import utils
import dill as pickle
import sys

books = {
    "AbuDaud": [0,"سنن أبي داود", "Sunan Abi Dawud", 0],
    "Bukhari": [1,"صحيح البخاري", "Sahih al-Bukhari", 0],
    "IbnMaja": [2,"سنن ابن ماجه", "Sunan Ibn Majah", 0],
    "Muslim": [3,"صحيح مسلم", "Sahih Muslim", 0],
    "Nesai": [4,"سنن النسائي", "Sunan an-Nasa'i", 0],
    "Tirmizi": [5,"سنن الترمذي", "Sunan at-Tirmidhi", 0]}

class Node:
  def __init__(self, word):
    self.word = word
    self.terminal_flag = False
    self.abs_flag = False
    self.hadiths_ref = set()
    self.table = {}

  def print_info(self):
    print("word: ", self.word, "\n",
          "tr flag: ", self.terminal_flag, "\n",
          "abs_flag: ", self.abs_flag, "\n",
          "ref: ", len(self.hadiths_ref), "\n",
          "table: ", len(self.table))

class Hadith:
    def __init__(self):
      self.bk_num = -1 
      self.bk_name = ["",""]
      self.ch_num = -1
      self.ch_name = ["",""]
      self.sec_num = -1
      self.sec_name = ["",""]
      self.num = -1
      self.speech = ["", ""]
      self.comment = ["",""]
      self.grade = ["",""]
    
    def print_hadith_info_ar(self):
        print("Book: ", self.bk_name[0], "\n",
               "Chapter: ", self.ch_name[0], "\n",
               "Section: ", self.sec_name[0], "\n",
               "Hadith: ", self.speech[0], "\n",
               "Grade: ", self.grade[0])
    
    def get_metadata_ar(self):
        return [self.bk_name[0], self.ch_name[0],
                self.sec_name[0], self.num,
                self.grade[0]]
    
    def get_metadata_en(self):
        return [self.bk_name[1], self.ch_name[1],
                self.sec_name[1], self.grade[1]]
      
def load_data(path="./"):
    colnames=['Chapter_Number', 'Chapter_English',
            'Chapter_Arabic', 'Section_Number',
            'Section_English', 'Section_Arabic',
            'Hadith_number','English_Hadith',
            'English_Isnad', 'English_Matn',
            'Arabic_Hadith' ,'Arabic_Isnad',
            'Arabic_Matn', 'Arabic_Comment',
            'English_Grade', 'Arabic_Grade']

    book_filenames = glob.glob(path+'**//*.csv')
    hadiths = {}
    counter = 0
    for x in range(len(book_filenames)):
        book = get_book_metadata(book_filenames[x])
        temp = pd.read_csv(book_filenames[x], names= colnames, skiprows=1).values.tolist()
        counter = update_collection(hadiths, temp, book, counter)
    return hadiths

def update_collection(hadiths, new_data, book, counter):
    for x in range(len(new_data)):
        book[3] = book[3]+1
        if str(new_data[x][10]) == "nan":
            continue
        hadith = Hadith()
        hadith.bk_num = int(book[0])
        hadith.bk_name = [book[1],book[2]]
        hadith.ch_num = int(new_data[x][0])
        hadith.ch_name = [str(new_data[x][2]),str(new_data[x][1])]
        hadith.sec_num = str(new_data[x][3])
        hadith.sec_name = [str(new_data[x][5]),str(new_data[x][4])]
        hadith.num = str(new_data[x][6])
        hadith.speech = [str(new_data[x][10]),str(new_data[x][7])]
        hadith.comment = [str(new_data[x][13]),""]
        hadith.grade = [str(new_data[x][15]),str(new_data[x][14])]
        
        hadiths[counter] = hadith
        counter += 1
    return counter

def filter_data(data, book_num):
    dataF = {}
    for num in book_num:
        temp = {k:v for k, v in data.items() if v.bk_num == num}
        dataF = dict(dataF.items() | temp.items())
    return dataF
        
def get_book_metadata(path):
    book_name = path.split("\\")[1]
    return books[book_name]

def build_table(data, min_len = 3):
    root_table = {}
    min_len = min_len
    counter = 1
    for num in data:
        hdaith = data[num]
        speech = hdaith.speech[0]
        speech = utils.normalize(speech)
        speech = speech.split()
        builder_controller(speech, hdaith, root_table, min_len)
        print(counter)
        counter = counter+1
    return root_table

def builder_controller(text, ref, table, min_len):
    for x in range(len(text)):
        if len(text[x::]) >= min_len:
            depth = 1
            if text[x] not in table:
                table[text[x]] = Node(text[x])
            
            node = table[text[x]]
            if depth >= min_len:
                node.hadiths_ref.add(ref)
                node.terminal_flag = True
            
            next_table = node.table
            segment_to_add = text[x+1::]
            builder(segment_to_add, ref, next_table, min_len, depth)
    return table 

def builder(text, ref, table, min_len, depth):
    depth = depth+1
    if len(text) == 0:
        return
    
    word = text[0]
    if word not in table:
        table[word] = Node(word)
    
    node = table[word] 
    if depth >= min_len:
        node.hadiths_ref.add(ref)
        node.terminal_flag = True
    
    if len(text) == 1:
        node.abs_flag = True
    
    next_table = node.table
    builder(text[1::], ref, next_table, min_len, depth)

def collapse_controller(table):
    print(len(table))
    counter = 1
    for word in table:
        node = table[word]
        collapse(node)
        print(counter)
        counter = counter  + 1

def collapse(node):
    table = node.table
    if len(table) == 1:
        # check the flags
        word = list(table.keys())[0]
        new_node = table[word]
        if node.terminal_flag == new_node.terminal_flag and node.abs_flag == new_node.abs_flag: 
            # connect two nodes
            node.word = node.word + " " + new_node.word
            node.hadiths_ref = node.hadiths_ref.union(new_node.hadiths_ref)
            node.table = new_node.table
            collapse(node)
        else:
            collapse(new_node)
    else:
        for word in table:
            new_node = table[word]
            collapse(new_node)

def save(name, table):
    with open(name, "wb") as fp:
        pickle.dump(table, fp)

def build(path, min_len = 3, filter=[1,3]):
    try:
        min_len = min_len
        data = load_data(path)
        print("data loaded")
        save(path+"hadiths", data)
        print("data saved")
        if len(filter) != 0:
            data = filter_data(data, filter)
        print("Building Start")
        print(len(data))
        sys.setrecursionlimit(15000)
        table = build_table(data)
        print("Building Done")
        print("Collapsing Start")
        collapse_controller(table)
        print("Collapsing Done")
        save(path+"data", table)
        print("Table Saved")
        return table
    except Exception as e:
        print(e)
        sys.exit(-1)