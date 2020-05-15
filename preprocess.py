import re
import time
import nltk
from nltk.corpus import stopwords
# nltk.download('averaged_perceptron_tagger')
# nltk.download("stopwords")
# lemmitizing
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
# nltk.download("wordnet")
# nltk.download("vader_lexicon")
# sentiment scoring
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

mbti = ["INFP", "INFJ", "INTP", "INTJ", "ENTP", "enfp", "ISTP", "ISFP", "ENTJ", "ISTJ", "ENFJ", "ISFJ", "ESTP", "ESFP", "ESFJ", "ESTJ"]
tags_dict = {
    "ADJ": ["JJ", "JJR", "JJS"],
    "ADP": ["EX", "TO"],
    "ADV": ["RB", "RBR", "RBS", "WRB"],
    "CONJ": ["CC", "IN"],
    "DET": ["DT", "PDT", "WDT"],
    "NOUN": ["NN", "NNS", "NNP", "NNPS"],
    "NUM": ["CD"],
    "PRT": ["RP"],
    "PRON": ["PRP", "PRP$", "WP", "WP$"],
    "VERB": ["MD", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"],
    ".": ["#", "$", "''", "(", ")", ",", ".", ":"],
    "X": ["FW", "LS", "UH"],
}

def unique_words(s):
    unique = set(s.split(' ')) 
    return len(unique)

def emojis(post):
    # does not include emojis made purely from symbols, only :word:
    emoji_count = 0
    words = post.split()
    for e in words:
        if 'http' not in e:
            if e.count(':')==2:
                emoji_count+=1
    return emoji_count

def colons(post):
    # Includes colons used in emojis
    colon_count = 0
    words = post.split()
    for e in words:
        if 'http' not in e:
            colon_count+=e.count(':')
    return colon_count

def lemmitize(s):
    lemmatizer = WordNetLemmatizer()
    new_s = [
                lemmatizer.lemmatize(word)
                for word in s.split(" ")
                if word not in stopwords.words("english")
            ]
    return new_s

def clean(s):
    s = re.sub(
            re.compile(r"https?:\/\/(www)?.?([A-Za-z_0-9-]+).*"),
            lambda match: match.group(2),
            s
        )
    s = re.sub(
        re.compile(r"\S+@\S+"), " ",
        s
        )
    s = s.lower()
    for type_word in mbti:
        s = s.replace(
            type_word.lower(), " ")
    return s

def prep_counts(s):
    clean_s = clean(s)
    d = {
        'link_count':s.count('http'),
        'youtube':s.count('youtube') + s.count('youtu.be'),
        'img_count':len(re.findall(r"(\.jpg)|(\.jpeg)|(\.gif)|(\.png)", s)),
        'upper':len([x for x in s.split() if x.isupper()]),
        'char_count':len(clean_s),
        'word_count':clean_s.count(' ')+1,
        'qm':clean_s.count('?'),
        'em':clean_s.count('!'),
        'colons':colons(clean_s),
        'emojis':emojis(clean_s),
        'unique_words':unique_words(clean_s),
        'ellipses':len(re.findall(r'\.\.\.\ ', clean_s))
        }
    return clean_s, d

def prep_sentiment(s):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(s)
    d = {
        'compound_sentiment':score["compound"],
        'pos_sentiment':score["pos"],
        'neg_sentiment':score["neg"],
        'neu_sentiment':score["neu"]
        }
    return d

def tag_pos(s):
    tagged_words = nltk.pos_tag(word_tokenize(s))
    d = {}
    for tup in tagged_words:
        tag = tup[1]
        for key,val in tags_dict.items():
            if tag in val:
                tag = key
        if tag in d:
            d[tag]+=1
        else:
            d[tag]=1
    return d

def prep_data(s):
    clean_s, d = prep_counts(s)
    d.update(
        prep_sentiment(
            lemmitize(clean_s)
            )
        )
    d.update(
        tag_pos(clean_s))
    return d

if __name__ == "__main__":
    t = time.time()
    string = "I just wanna to go home!!!!!! :sadpanda: https://www.youtube.com/watch?v=TQP20LTI84A"
    print(string)
    print(prep_data(string))
    print(f"Preprocessing Time: {time.time() - t} seconds")