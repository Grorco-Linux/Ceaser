import re
regex = re.compile('[^a-zA-Z]')
def is_english(x,otherwords, englishpercent):

    string = x.lower()
    englishwords = []
    english = []
    with open('top_1000_english', "r") as f:
        for line in f:

            englishwords.append(line.strip('\n').lower())

    for word in string.split():
        if regex.sub('',word) in englishwords:
            english.append(True)
        else:
            english.append(False)
    try:
        odds = (english.count(True)/len(english))+otherwords
    except ZeroDivisionError:
        odds = 100
    if odds > englishpercent:
        return True, odds
    else:
        return False, odds



