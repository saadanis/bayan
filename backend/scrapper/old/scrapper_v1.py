"""
    Version: 1.7
    Author: Abdulrahman
    Purpose: The aim of this code is to get the answer of a query from a certain url Idea: Simply, we will take
        advantage of the html tree structure First, we will cut the extras tags (the one we don't need like title,
        links, nav, etc). While doing that, We will build an identical tree. Each node contain a reference to the tag
        and its score. The Score is the number of query words in the text. The we will use some heuristics to locate
        the best node and return its text after doing some normalization"""

# import numpy as np
from bs4 import BeautifulSoup
import requests
import re
from anytree import Node, RenderTree

qr = "حكم التيمم في الجو البارد"  # Test purpose
u = "https://islamweb.net/ar/fatwa/71322/"


class Container:
    """
    Each object of this class will have 2 variables, a reference to an html element and its score
    """
    def __init__(self, tag):
        """
        The Constructor
        :param tag: reference to an html element <bs4.element.Tag>
        """
        self.tag = tag
        self.score = 0

    def set_score(self, score):
        """
        A setter function to set the html element score
        :param score: the score <int>
        :return: None
        """
        self.score = score

    def __str__(self):
        """
        An override to the print functions
        :return: a formatted string <str>
        """
        return "Tag: " + self.tag.name + ", " + "Score: " + str(
            self.score)


def print_tree(node):
    for pre, fill, node in RenderTree(node):
        print("%s%s" % (pre, node.name))


def get_words(text):
    """
    This function takes a string and return it is own words stored on a list
    :param text: a string <str>
    :return: a list of words <list>
    """
    return text.split(" ")  # split the text by the whitespaces and return it.


def tag_check(tag):
    if tag == "nav" or tag == "a" or tag == "form" or tag == "button" or tag == "li" or tag == "ul" or tag == "style" \
            or tag == "script" or tag == "option" or tag == "label" or tag == "h1" or tag == "h2" or tag == "h3" \
            or tag == "header" or tag == "footer":
        return False
    else:
        return True


def text_processor(text):
    text = re.sub("[a-z,A-Z]", "", text)
    text = " ".join(text.split())
    return text


def get_score(sample, query):
    """
    This function takes 2 lists: query words list, and sample words list. It returns how many times query words have
        been repeated in the sample
    :param sample: a sample words list <list>
    :param query: a query words list <list>
    :return: the score <int>
    """
    # TODO: instead of relying on the equality only, we may process the word to to improve the accuracy
    score = 0  # initial score
    for sample_word in sample:  # for each word in the sample
        for query_word in query:  # for each word in the query
            if sample_word == query_word:  # if they are the same
                score = score + 1  # increment the score by 1
    return score  # return the score


def get_the_answer_node(node):
    """
    1 - Starting from upside, when u find a division return the node.
    2 - Starting from downside, return the first different tag
    :param node: the root of the tree <Node>
    :return: the node that contain the answer <Node>
    """
    height = node.height
    ans = None
    for x in range(height):
        if len(node.children) == 1:
            node = node.children[0]
        elif len(node.children) > 1:
            ans = node

    if ans is not None:
        return ans
    else:
        parent = node.parent
        for x in range(height):
            if node.name.tag.name != parent.name.tag.name:
                return parent
            else:
                temp = parent
                parent = parent.parent
                node = temp


def create_tree(parent_node, tag, q_words):
    """
    This function explore the sub html tree for the tag and complete building the modified tree (recursive method)
    :param parent_node: ...
    :param tag: the html element to be explored which is wrapped in the parent variable <bs4.element.Tag>
    :param q_words: query words <list>
    :return: score
    """

    if not tag_check(tag.name):  # if this tag is faulty, clear its contents and return
        tag.clear()
        return 0
    node = Node(Container(tag), parent=parent_node)  # create the node
    score = 0
    for child in tag.children:
        child_type = str(type(child))
        if child_type == "<class 'bs4.element.Tag'>":
            score = score + create_tree(node, child, q_words)
        elif child_type == "<class 'bs4.element.NavigableString'>":
            score = score + get_score(get_words(child.string), q_words)
    if score == 0:  # if this tag contents is irrelevant, cut it
        # TODO: think about it once again. maybe some information are lost because of this
        node.parent = None
    else:
        node.name.set_score(score)  #
    return score


def get_tree(url, q_words):
    """
    This function gets URL and query words and return a modified html tree and its root. It firstly uses
    BeautifulSoup to get the original html tree. Since the answer mostly will be on the body (not the header or the
    footer), we weill get the body subtree only. We will traverse the body subtree and cut the extras. In the same
    time, we are creating the second tree - using AnyTree library - that will hold the score for each node.
    :param url: Website URL <str>
    :param q_words: Query words <list>
    :return: modified html tree <RenderTree>, and its root <Node>
    """
    # Getting the original tree
    page = requests.get(url)  # get the website page
    soup = BeautifulSoup(page.content, 'html.parser')  # get the html tree
    body_tag = soup.body  # get the body subtree
    root = Node(Container(body_tag))

    score = 0
    for child in body_tag.children:  # for each body child
        child_type = str(type(child))
        if child_type == "<class 'bs4.element.Tag'>":  # if it is a tag
            score = score + create_tree(root, child, q_words)  # explore its children and calculate the score
        elif child_type == "<class 'bs4.element.NavigableString'>":  # if it is a string
            score = score + get_score(get_words(child.string), q_words)  # calculate the score
    root.name.set_score(score)  # set the score

    return RenderTree(root), root  # return the modified tree and its root


def scrapper(url, query):  # main function
    """
    This function take a query (question) and an URL. It search for the answer inside the page and return it
    :param url: Website URL <str>
    :param query: the query <str>
    :return: an answer <str>
    """
    q_words = get_words(query)  # get the query words
    tree, root = get_tree(url, q_words)  # get the modified html tree
    # print_tree(root)  # Test purpose

    node = get_the_answer_node(root)  # from the html tree, find the best node

    #  TODO cut the answer if some keywords appeared

    if node is None:
        return None
    else:
        # print(node.name)  # Test
        # print(node.name.tag.prettify())  # Test
        return text_processor(node.name.tag.text)


# #  Test purpose
# ans = scrapper(u, qr)
# print("\n")
# print(ans)
# scrapper(u, qr)
