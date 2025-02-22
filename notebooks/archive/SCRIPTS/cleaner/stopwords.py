from nltk.corpus import stopwords as nltk_stopwords
from sklearn.feature_extraction import stop_words

roman_nums = set([
    'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi',
    'xii', 'xiii', 'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx',
    'xxi', 'xxii', 'xxiii', 'xxiv', 'xxv', 'xxvi', 'xxvii', 'xxviii',
    'xxix', 'xxx', 'xxxi', 'xxxii', 'xxxiii', 'xxxiv', 'xxxv', 'xxxvi',
    'xxxvii', 'xxxviii', 'xxxix', 'xl', 'xli', 'xlii', 'xliii', 'xliv',
    'xlv', 'xlvi', 'xlvii', 'xlviii', 'xlix', 'l', 'li', 'lii', 'liii',
    'liv', 'lv', 'lvi', 'lvii', 'lviii', 'lix', 'lx', 'lxi', 'lxii',
    'lxiii', 'lxiv', 'lxv', 'lxvi', 'lxvii', 'lxviii', 'lxix', 'lxx',
    'lxxi', 'lxxii', 'lxxiii', 'lxxiv', 'lxxv', 'lxxvi', 'lxxvii',
    'lxxviii', 'lxxix', 'lxstopwordsxx', 'lxxxi', 'lxxxii', 'lxxxiii', 'lxxxiv',
    'lxxxv', 'lxxxvi', 'lxxxvii', 'lxxxviii', 'lxxxix', 'xc', 'xci',
    'xcii', 'xciii', 'xciv', 'xcv', 'xcvi', 'xcvii', 'xcviii', 'xcix', 'c'
])
try:
    stopwords = set(nltk_stopwords.words('english'))
except:
    stopwords = set()
    print('Warning: NLTK stopwords not used! Please check if the nltk stopwords corpus is avaialable in your system.')
stopwords.update(stop_words.ENGLISH_STOP_WORDS)
stopwords.update(roman_nums)

stopwords = list(stopwords)
