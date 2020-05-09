import re

mbti = ["INFP", "INFJ", "INTP", "INTJ", "ENTP", "enfp", "ISTP", "ISFP", "ENTJ", "ISTJ", "ENFJ", "ISFJ", "ESTP", "ESFP", "ESFJ", "ESTJ"]

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

def clean(s):
    new_s = s.replace(
                    re.compile(r"https?:\/\/(www)?.?([A-Za-z_0-9-]+).*"),
                    lambda match: match.group(2)
                    )\
                .replace(
                    re.compile(r"\S+@\S+"), " "
                    )
                .replace(
                    type_word.lower(), " ")\
                .lower()
    return new_s

def prep_data(s):
        clean_s = clean(s)
        d = {
            'link_count':s.count('http'),
            'upper':len([x for x in s.split() if x.isupper()])
            'char_count':len(clean_s),
            'word_count':clean_s.count(' ')+1
            'qm':clean_s.count('?'),
            'em':clean_s.count('!'),
            'colons':colons(clean_s),
            'emojis':emojis(clean_s),
            'unique_words':unique_words(clean_s),
            'ellipses':len(re.findall(r'\.\.\.\ ', clean_s)),
            'img_count':len(re.findall(r"(\.jpg)|(\.jpeg)|(\.gif)|(\.png)", s))
            }
    return d