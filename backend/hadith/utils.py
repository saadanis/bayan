import string
import re

normal_alaf = "ا"
forged_alafs = "[أإآ]"
forged_ha = r"ة\b"
normal_ha = "ه"
forged_ya = r"ي\b"
normal_ya = "ى"
tashkeels = "[ًٌٍَُِّْ]"
punctuation = "[" + string.punctuation + 'ـ؟؛،' + "«»" + "]"

def normalize(text):
    """ This function gets a text and return the normalized one """
    text = re.sub("\u200f", "", text)
    text = re.sub(tashkeels, "", text)
    text = re.sub(punctuation, " ", text)
    text = re.sub(forged_alafs, normal_alaf, text)
    text = re.sub(forged_ha, normal_ha, text)
    text = re.sub(forged_ya, normal_ya, text)
    text = re.sub(' +', ' ', text)
    text = text.strip()
    return text