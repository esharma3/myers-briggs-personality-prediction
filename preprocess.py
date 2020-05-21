import re
import time
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


###########################################################################################
#                        PREPARING DATA FOR MACHINE LEARNING                              #
###########################################################################################

# 16 MBTI types
mbti = [
    "INFP",
    "INFJ",
    "INTP",
    "INTJ",
    "ENTP",
    "enfp",
    "ISTP",
    "ISFP",
    "ENTJ",
    "ISTJ",
    "ENFJ",
    "ISFJ",
    "ESTP",
    "ESFP",
    "ESFJ",
    "ESTJ",
]

# part of speech dictionary
tags_dict = {
    "ADJ_avg": ["JJ", "JJR", "JJS"],
    "ADP_avg": ["EX", "TO"],
    "ADV_avg": ["RB", "RBR", "RBS", "WRB"],
    "CONJ_avg": ["CC", "IN"],
    "DET_avg": ["DT", "PDT", "WDT"],
    "NOUN_avg": ["NN", "NNS", "NNP", "NNPS"],
    "NUM_avg": ["CD"],
    "PRT_avg": ["RP"],
    "PRON_avg": ["PRP", "PRP$", "WP", "WP$"],
    "VERB_avg": ["MD", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"],
    ".": ["#", "$", "''", "(", ")", ",", ".", ":"],
    "X": ["FW", "LS", "UH"],
}

# input to the model
features = [
    "clean_posts",
    "compound_sentiment",
    "ADJ_avg",
    "ADP_avg",
    "ADV_avg",
    "CONJ_avg",
    "DET_avg",
    "NOUN_avg",
    "NUM_avg",
    "PRT_avg",
    "PRON_avg",
    "VERB_avg",
    "qm",
    "em",
    "colons",
    "emojis",
    "word_count",
    "unique_words",
    "upper",
    "link_count",
    "ellipses",
    "img_count",
]


def unique_words(s):
    unique = set(s.split(" "))
    return len(unique)


def emojis(post):
    # does not include emojis made purely from symbols, only :word:
    emoji_count = 0
    words = post.split()
    for e in words:
        if "http" not in e:
            if e.count(":") == 2:
                emoji_count += 1
    return emoji_count


def colons(post):
    # Includes colons used in emojis
    colon_count = 0
    words = post.split()
    for e in words:
        if "http" not in e:
            colon_count += e.count(":")
    return colon_count


def lemmitize(s):
    lemmatizer = WordNetLemmatizer()
    new_s = ""
    for word in s.split(" "):
        lemmatizer.lemmatize(word)
        if word not in stopwords.words("english"):
            new_s += word + " "
    return new_s[:-1]


def clean(s):
    # remove urls
    s = re.sub(re.compile(r"https?:\/\/(www)?.?([A-Za-z_0-9-]+).*"), "", s)
    # remove emails
    s = re.sub(re.compile(r"\S+@\S+"), "", s)
    # remove punctuation
    s = re.sub(re.compile(r"[^a-z\s]"), "", s)
    # Make everything lowercase
    s = s.lower()
    # remove all personality types
    for type_word in mbti:
        s = s.replace(type_word.lower(), "")
    return s


def prep_counts(s):
    clean_s = clean(s)
    d = {
        "clean_posts": lemmitize(clean_s),
        "link_count": s.count("http"),
        "youtube": s.count("youtube") + s.count("youtu.be"),
        "img_count": len(re.findall(r"(\.jpg)|(\.jpeg)|(\.gif)|(\.png)", s)),
        "upper": len([x for x in s.split() if x.isupper()]),
        "char_count": len(s),
        "word_count": clean_s.count(" ") + 1,
        "qm": s.count("?"),
        "em": s.count("!"),
        "colons": colons(s),
        "emojis": emojis(s),
        "unique_words": unique_words(clean_s),
        "ellipses": len(re.findall(r"\.\.\.\ ", s)),
    }
    return clean_s, d


def prep_sentiment(s):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(s)
    d = {
        "compound_sentiment": score["compound"],
        "pos_sentiment": score["pos"],
        "neg_sentiment": score["neg"],
        "neu_sentiment": score["neu"],
    }
    return d


def tag_pos(s):
    tagged_words = nltk.pos_tag(word_tokenize(s))
    d = dict.fromkeys(tags_dict, 0)
    for tup in tagged_words:
        tag = tup[1]
        for key, val in tags_dict.items():
            if tag in val:
                tag = key
        d[tag] += 1
    return d


def prep_data(s):
    clean_s, d = prep_counts(s)
    d.update(prep_sentiment(lemmitize(clean_s)))
    d.update(tag_pos(clean_s))
    return pd.DataFrame([d])[features]


###########################################################################################
#                                        MAIN                                             #
###########################################################################################

if __name__ == "__main__":
    t = time.time()
    string = "That somehow managed to be record short yet answer almost all the questions we would've asked, haha! Hi Deb! Welcome to Hou Tian; nice to meet you! I'm Jhenne, one of the mods here-- which means I gotta give you the modly speech :] Make sure to check out the Mandatory Reading up top! Our constantly updated Library is also a great resource, though it isn't mandatory reading-- we like to tell members to 'read as you need', rather than marathon read it all at once. One of the most helpful threads is the Gameplay So Far thread, which breaks down what all has gone down on the boards. (Now, the summary for January isn't tossed up yet, but we'd be happy to break down what you missed if you'd like.) I see that you're interested in Mai! That means both the Trying for a Canon Character page, and the Canon Character Rules and Consequences post will be helpful to check out. If you're ever considering an original character, we have our player-made adoptables list, and our factions, comprised of the Jade Shark/Bending Opposition, Original People of the Flame, and The Bending Crime Syndicates. As far as characters go, in the past tense I play Srai, a Jade Shark [s]that is very very dusty. In the Korraverse I play a reporter named Chihiro, and an ex-taxi dancer/wannabe actress named Naoki, and a Republic City University student named Haruna. I think that's it! If you have any questions, don't hesitate to ask a mod, or drop it right here in this thread so we can get back to you! Again, welcome! #CONFETTI"
    print(string)
    print(prep_data(string))
    print(f"Preprocessing Time: {time.time() - t} seconds")
