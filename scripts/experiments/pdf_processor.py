import subprocess
import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
import re
import spacy
import nltk
from haystack.preprocessor.preprocessor import PreProcessor
from haystack.file_converter.pdf import PDFToTextConverter
from haystack.file_converter.pdf import PDFToTextConverter, PreProcessor
In[177]: % history
fname = 'WDR 2013 low res.pdf'
converter = PDFToTextConverter(
    remove_numeric_tables=True, valid_languages=["de", "en"])
%time doc = converter.convert(file_path=fname, meta=None)
converter = PDFToTextConverter(
    remove_numeric_tables=True, valid_languages=["de", "en"])
%time doc = converter.convert(file_path=fname, meta=None)
processor = PreProcessor(clean_empty_lines=True,
                         clean_whitespace=True,
                         clean_header_footer=True,
                         split_by="word",
                         split_length=200,
                         split_respect_sentence_boundary=True)
d = processor.process(doc)
d[0]
d[1]
print()d[1]
print(d[1])
print(d[1]['text'])
print(d[1]['text'])
doc['text'][:1000]
print(doc['text'][:1000])
dd = doc['text'].splitlines()
dd[0]
dd[1]
dd[2]
dd[3]
dd[4]
dd[5]
dd[6]
dd[:10]
dd[:100]
print(d[1]['text'])
print(d[10]['text'])
print(d[50]['text'])
nltk.sent_tokenize(d[50]['text'])
len(nltk.sent_tokenize(d[50]['text']))
len(nltk.sent_tokenize(d[50]['text'].replace('\n', ' ')))
nltk.sent_tokenize(d[50]['text'].replace('\n', ' '))
nltk.sent_tokenize(d[50]['text'].replace('\n', ' ').replace('.', '. '))
nltk.sent_tokenize(d[90]['text'].replace('\n', ' ').replace('.', '. '))
nltk.sent_tokenize(d[90]['text'])
doc['text']
dc = processor.clean(doc)
dc[0]
dc['text'][:100]
doc['text'][:100]
print(dc['text'][1000:2000])
print(doc['text'][1000:2000])
print(doc['text'][5000:6000])
print(doc['text'][10000:11000])
print(doc['text'][20000:21000])
print(doc['text'][27000:28000])
print(doc['text'][37000:38000])
print(dc['text'][37000:38000])
print(doc['text'][37000:38000])
sentences = nltk.sent_tokenize(dc['text'][37000:38000])
len(sentences)
sentences
nlp = spacy.load('en_core_web_md')
nlp = spacy.load('en_core_web_sm')
doc = nlp(dc['text'][37000:38000])
doc.sents
for s in doc.sents:
    print(s)
for s in doc.sents:
    print(s)
[s for s in doc.sents]
len([s for s in doc.sents])
len([s.replace('\n', ' ') for s in doc.sents])
len([s.text.replace('\n', ' ') for s in doc.sents])
[s.text.replace('\n', ' ') for s in doc.sents]
sentences
sents = nltk.sent_tokenize(doc['text'])
%time doc = converter.convert(file_path=fname, meta=None)
sents = nltk.sent_tokenize(doc['text'])
len(sents)
sents[100:110]
sents[:100]
%time doc = converter.convert(file_path=fname, meta=None)
doc['text'][:100]
sents[:10]
sents = nltk.sent_tokenize(doc['text'])
sents[:10]
print(sents[0])
print(sents[0].replace('\n', ' '))
print(sents[0].replace('\n', ' ').strip())
for s in sents:
    print(s.replace('\n', ' ').strip())
    print()
for s in sents:
    print(s.replace('\n', ' ').strip())
    print()
for s in sents:
    print(s.replace('\n', ' ').strip())
    print('------------------------------------')
for s in sents[:500]:
    print(s.replace('\n', ' ').strip())
    print('------------------------------------')
   def normalize_footnote_citations(text: str) -> str:
        r"""This method tries to detect footnotes and normalizes them.

        This is essential to improve the accuracy of SpaCy's sentence
        detector. Sometimes footnote citations are connected with sentence
        endings that prevents the detection of proper sentence boundary.

        The transformation handles common footnote citation formats:
            pattern: ((?:[a-zA-Z\)]+[.,]|\)))(\d+)(\s)
                - This is a normalizer.1 We will use this.
                - This is a normalizer (great).2 We will use this.
                - This is a normalizer (great).3\nWe will use this.
                - The normalizer (2020)8 is working.
            transforms to:
                - This is a normalizer. _1 We will use this.
                - This is a normalizer (great). _2 We will use this.
                - This is a normalizer (great). _3\nWe will use this.
                - The normalizer (2020) _8 is working.

        Args:
            text:
                Text that will be checked and normalized for footnote
                citations.

        Returns:
            normalized text

        """
        footnote_patterns = [
            r'((?:[a-zA-Z\)]+[.,]|\)))(\d+)(\s)'
        ]

        footnote_patterns = '|'.join(footnote_patterns)

        return re.sub(footnote_patterns, r'\1 _\2\3', text)
%time sents = nltk.sent_tokenize(doc['text'])
%time sents = nltk.sent_tokenize(normalize_footnote_citations(doc['text']))
for s in sents[:500]:
    print(s.replace('\n', ' ').strip())
    print('------------------------------------')
%history
w = open('wdr.txt').read()
%time w_sents = nltk.sent_tokenize(normalize_footnote_citations(w))
for s in w_sents[:500]:
    print(s.replace('\n', ' ').strip())
    print('------------------------------------')
doc['text'][:10]
f_split = doc['text'].split('\f')
len(f_split)
f_split[0]
f_split[1]
f_split[2]
f_split[3]
f_split[4]
f_split[5]
f_split[6]
f_split[7]
f_split[8]
f_split[9]
f_split[10]
f_split[11]
f_split[12]
f_split[13]
f_split[14]
f_split[15]
f_split[16]
f_split[17]
f_split[18]
f_split[19]
f_split[20]
f_split[21]
f_split[22]
cvec = CountVectorizer(ngram_range=(1, 4))
cvec.fit(f_split[22])
cvec.fit([f_split[22]])
cvec.vocabulary_
potential_headers = [i.split()[:20] for i in f_split]
len(potential_headers)
potential_headers[:10]
potential_headers[40:45]
potential_headers = [i.split()[:50] for i in f_split]
potential_headers[40:45]
first_words = Counter([i[0] for i in potential_headers])
first_words = Counter([i[0] for i in potential_headers])
first_words = Counter([i[0] for i in potential_headers if len(i)])
first_words.most_common()[:10]
first_words.most_common()[:20]
second_words = Counter([i[:2] for i in potential_headers if len(i)])
second_words = Counter([' '.join(i[:2]) for i in potential_headers if len(i)])
second_words.most_common(10)
Counter([' '.join(i[:3]) for i in potential_headers if len(i)]).most_common(10)
Counter([' '.join(i[:4]) for i in potential_headers if len(i)]).most_common(10)
Counter([' '.join(i[:5]) for i in potential_headers if len(i)]).most_common(10)
Counter([' '.join(i[:6]) for i in potential_headers if len(i)]).most_common(10)
len(f_split)
0.05 * 423
0.01 * 423
Counter([' '.join(i[:1]) for i in potential_headers if len(i)]).most_common(10)
pd.Series(Counter([' '.join(i[:1])
          for i in potential_headers if len(i)]).most_common(10))
pd.Series(dict(Counter([' '.join(i[:1])
          for i in potential_headers if len(i)]).most_common(10)))
pd.Series(dict(Counter([' '.join(i[:1])
          for i in potential_headers if len(i)]).most_common())).describe()
pd.Series(dict(Counter([' '.join(i[:1]) for i in potential_headers if len(
    i)]).most_common())).quantile(0.95)
pd.Series(dict(Counter([' '.join(i[:1]) for i in potential_headers if len(
    i)]).most_common())).quantile(0.9)
pd.Series(dict(Counter([' '.join(i[:1]) for i in potential_headers if len(
    i)]).most_common())).quantile(0.75)
len(f_split) * 0.01
pd.Series(dict(Counter([' '.join(i[:1]) for i in potential_headers if len(i)]).most_common())).quantile(0.75)('Jobs and social cohesion', 12),
pd.Series(dict(Counter([' '.join(i[:1]) for i in potential_headers if len(
    i)]).most_common())).quantile(0.75)
Counter([' '.join(i[:7]) for i in potential_headers if len(i)]).most_common(10)
Counter([' '.join(i[:20])
        for i in potential_headers if len(i)]).most_common(10)
Counter([' '.join(i[:25])
        for i in potential_headers if len(i)]).most_common(10)
Counter([' '.join(i[:50])
        for i in potential_headers if len(i)]).most_common(10)
Counter([' '.join(i[:40])
        for i in potential_headers if len(i)]).most_common(10)
Counter([' '.join(i[:30])
        for i in potential_headers if len(i)]).most_common(10)
Counter([' '.join(i[:24])
        for i in potential_headers if len(i)]).most_common(10)
# page_thresh = len(f_split)
common_p_val = 0.01
page_thresh = len(f_split) * common_p_val
page_thresh
page_thresh = int(len(f_split) * common_p_val)
int(4.6)
Counter([' '.join(i[:1]) for i in potential_headers if len(i)]).most_common(10)
Counter([' '.join(i[:1]) for i in potential_headers if len(i)]).most_common(20)
Counter([' '.join(i[:2]) for i in potential_headers if len(i)]).most_common(20)
idx = 2
common_list = []
while True:
    pg = pd.Series(dict(
        Counter([' '.join(i[:1]) for i in potential_headers if len(i)]).most_common()))
    pg = pg[pg >= page_thresh]
    if pg.empty:
        break
    common_list.append(pg)
common_list = []
while True:
    pg = pd.Series(dict(Counter([' '.join(i[:idx])
                   for i in potential_headers if len(i)]).most_common()))
    pg = pg[pg >= page_thresh]
    if pg.empty:
        break
    common_list.append(pg)
    idx += 1
len(common_list)
%history
common_list[0]
common_list[1]
common_list[3]
common_list[4]
common_list[5]
common_list[6]
common_list[7]
common_list[8]
common_list[9]
common_list[2]
common_list[-1]
common_list[-2]
common_list[::-1][0]
common_list[::-1][1]
common_list[::-1][2]
common_list[::-1].index[:10]
common_list_df = pd.concat(common_list[::-1])
common_list_df.head()
common_list_df.index[-5:]
common_list_df.index[-15:]
f_split_copy = list(f_split)
comms = [i.split() for i in common_list_df.index]
comms[0]
for ix, l in f_split:
    if ix and ix % 10 == 0:
        print(ix)
    for c in comms:
        ixl = len(c)
        if l[:ixl] == c:
            f_split_copy[ix] = l[:ixl]
            break
for ix, l in enumerate(f_split):
    if ix and ix % 10 == 0:
        print(ix)
    for c in comms:
        ixl = len(c)
        if l[:ixl] == c:
            f_split_copy[ix] = l[:ixl]
            break
f_split[22]
f_split_copy[22]
for ix, l in enumerate(f_split):
    ll = l.split(' ')
    if ix and ix % 10 == 0:
        print(ix)
    for c in comms:
        ixl = len(c)
        if ll[:ixl] == c:
            f_split_copy[ix] = ' '.join(ll[ixl:])
            break
f_split[22]
f_split_copy[22]
for ix, l in enumerate(f_split):
    ll = l.replace('\n', ' _\n').split(' ')
    if ix and ix % 10 == 0:
        print(ix)
    for c in comms:
        ixl = len(c)
        if ll[:ixl] == c:
            f_split_copy[ix] = ' '.join(ll[ixl:]).replace('_\n', '\n')
            break
f_split[22]
f_split_copy[22]
for ix, l in enumerate(f_split):
    ll = l.replace('\n', ' _\n').split(' ')
    if ix and ix % 10 == 0:
        print(ix)
    for c in comms:
        ixl = len(c)
        if ll[:ixl] == c:
            f_split_copy[ix] = ' '.join(ll[ixl:]).replace(' _\n', '\n')
            break
f_split_copy[22]
for ix, l in enumerate(f_split):
    ll = l.replace('\n', ' _\n').split(' ')
    if ix and ix % 10 == 0:
        print(ix)
    for c in comms:
        ixl = len(c)
        if ll[:ixl] == c:
            f_split_copy[ix] = (' ' + ' '.join(ll[ixl:])).replace(' _\n', '\n')
            break
f_split_copy[22]
f_split_copy[21]
f_split_copy[25]
f_split_copy[27]
potential_headers = [i.split(' ')[:50] for i in f_split]
idx = 2
common_list = []
while True:
    pg = pd.Series(dict(Counter([' '.join(i[:idx])
                   for i in potential_headers if len(i)]).most_common()))
    pg = pg[pg >= page_thresh]
    if pg.empty:
        break
    common_list.append(pg)
    idx += 1
potential_headers[0]
potential_headers[1]
idx
len(potential_headers)
Counter([' '.join(i[:2]) for i in potential_headers if len(i)]).most_common(20)
Counter([' '.join(i[:3]) for i in potential_headers if len(i)]).most_common(20)
' '.join(['\n'])
' '.join([''])
potential_headers = [i.split(' ')[:50] for i in f_split if len(i)]
Counter([' '.join(i[:3]) for i in potential_headers if len(i)]).most_common(20)
potential_headers = [i.split(' ')[:50] for i in f_split if len(i)]
idx = 2
common_list = []
while True:
    pg = pd.Series(dict(Counter([' '.join(i[:idx])
                   for i in potential_headers if len(i)]).most_common()))
    pg = pg[pg >= page_thresh]
    if pg.empty:
        break
    common_list.append(pg)
    idx += 1
len(common_list)
common_list_df = pd.concat(common_list[::-1])
common_list_df.head()
common_list_df.tail()
for ix, l in enumerate(f_split):
    ll = l.split(' ')
    if ix and ix % 10 == 0:
        print(ix)
    for c in comms:
        ixl = len(c)
        if ll[:ixl] == c:
            f_split_copy[ix] = ' '.join(ll[ixl:])
            break
f_split_copy[27]
c
comms = [i.split(' ') for i in common_list_df.index]
for ix, l in enumerate(f_split):
    ll = l.split(' ')
    if ix and ix % 10 == 0:
        print(ix)
    for c in comms:
        ixl = len(c)
        if ll[:ixl] == c:
            f_split_copy[ix] = ' '.join(ll[ixl:])
            break
f_split_copy[27]
f_split[27]
f_split[23]
f_split_copy[23]
f_split_copy[24]
f_split[24]
%history


def process_for_header(s):
    s = re.sub(r'([^\s])(\n+)', r'\1 \2', s)
    return s


sep = ' '
potential_headers = [process_for_header(i).split(
    sep)[:50] for i in f_split if len(i.split())]

idx = 2
common_list = []

while True:
    pg = pd.Series(dict(Counter([sep.join(i[:idx])
                                 for i in potential_headers if len(i)]).most_common()))
    pg = pg[pg >= page_thresh]
    if pg.empty:
        break
    common_list.append(pg)
    idx += 1

len(common_list)

common_list_df = pd.concat(common_list[::-1])
common_list_df.head()
common_list_df.tail()

comms = [i.split(sep) for i in common_list_df.index]

for ix, l in enumerate(f_split):
    ll = l.split(sep)
    if ix and ix % 10 == 0:
        print(ix)
    for c in comms:
        ixl = len(c)
        if ll[:ixl] == c:
            f_split_copy[ix] = sep.join(ll[ixl:])
            break
f_split[24]
f_split_copy[24]


def process_for_header(s):
    s = re.sub(r'([^\s])(\n+)', r'\1 \2', s)
    return s


sep = ' '
potential_headers = [process_for_header(i).split(
    sep)[:50] for i in f_split if len(i.split())]

idx = 2
common_list = []

while True:
    pg = pd.Series(dict(Counter([sep.join(i[:idx])
                                 for i in potential_headers if len(i)]).most_common()))
    pg = pg[pg >= page_thresh]
    if pg.empty:
        break
    common_list.append(pg)
    idx += 1

len(common_list)

common_list_df = pd.concat(common_list[::-1])
common_list_df.head()
common_list_df.tail()

comms = [i.split(sep) for i in common_list_df.index]

for ix, l in enumerate(f_split):
    ll = process_for_header(l).split(sep)
    if ix and ix % 10 == 0:
        print(ix)
    for c in comms:
        ixl = len(c)
        if ll[:ixl] == c:
            f_split_copy[ix] = sep.join(ll[ixl:])
            break
f_split_copy[24]
f_split[24]
f_split_copy[24]
f_split_copy[25]
f_split[25]


class PDFToTextProcessor:
    def __init__(self):
        pass

    @staticmethod
    def process_for_header(s):
        s = re.sub(r'([^\s])(\n+)', r'\1 \2', s)
        return s

    def remove_headers(self, pages, common_p_val=0.01):
        pages_copy = list(pages)
        page_thresh = int(len(pages) * common_p_val)

        sep = ' '
        potential_headers = [PDFToTextProcessor.process_for_header(
            i).split(sep)[:50] for i in pages if len(i.split())]

        idx = 2
        common_list = []

        while True:
            pg = pd.Series(dict(Counter([sep.join(i[:idx])
                                         for i in potential_headers if len(i)]).most_common()))
            pg = pg[pg >= page_thresh]
            if pg.empty:
                break
            common_list.append(pg)
            idx += 1

        len(common_list)

        common_list_df = pd.concat(common_list[::-1])
        common_list_df.head()
        common_list_df.tail()

        comms = [i.split(sep) for i in common_list_df.index]

        for ix, l in enumerate(pages):
            ll = PDFToTextProcessor.process_for_header(l).split(sep)
            if ix and ix % 10 == 0:
                print(ix)
            for c in comms:
                ixl = len(c)
                if ll[:ixl] == c:
                    pages_copy[ix] = sep.join(ll[ixl:])
                    break

        return pages_copy

pdftp = PDFToTextProcessor()
ww = pdftp.remove_headers(f_split, common_p_val=0.01)
ww[27]
f_split[27]


class PDFToTextProcessor:
    def __init__(self):
        pass

    @staticmethod
    def process_for_header(s):
        s = re.sub(r'([^\s])(\n+)', r'\1 \2', s)
        return s

    def remove_headers(self, pages, common_p_val=0.01):
        pages_copy = list(pages)
        page_thresh = int(len(pages) * common_p_val)

        sep = ' '
        potential_headers = [PDFToTextProcessor.process_for_header(
            i).split(sep)[:50] for i in pages if len(i.split())]

        idx = 2
        common_list = []

        while True:
            pg = pd.Series(dict(Counter([sep.join(i[:idx])
                                         for i in potential_headers if len(i)]).most_common()))
            pg = pg[pg >= page_thresh]
            if pg.empty:
                break
            common_list.append(pg)
            idx += 1

        len(common_list)

        common_list_df = pd.concat(common_list[::-1])
        common_list_df.head()
        common_list_df.tail()

        comms = [i.split(sep) for i in common_list_df.index]

        for ix, l in enumerate(pages):
            ll = PDFToTextProcessor.process_for_header(l).split(sep)
            # if ix and ix % 10 == 0:
            #     print(ix)
            for c in comms:
                ixl = len(c)
                if ll[:ixl] == c:
                    pages_copy[ix] = sep.join(ll[ixl:]).replace(' \n', '\n')
                    break

        return pages_copy

pdftp = PDFToTextProcessor()
ww = pdftp.remove_headers(f_split, common_p_val=0.01)
ww[27]
f_split[27]
pdoc = ' '.join(ww)
sents = nltk.sent_tokenize(pdoc)
for s in sents[:500]:
    print(s.replace('\n', ' ').strip())
    print('------------------------------------')
%time w_sents = nltk.sent_tokenize(normalize_footnote_citations(pdocs))
%time w_sents = nltk.sent_tokenize(normalize_footnote_citations(pdoc))
for s in w_sents[:500]:
    print(s.replace('\n', ' ').strip())
    print('------------------------------------')


class PDFToTextProcessor:
    def __init__(self):
        pass

    @staticmethod
    def process_for_header(s):
        s = re.sub(r'([^\s])(\n+)', r'\1 \2', s)
        return s

    @staticmethod
    def read_pdf(fname: str) -> List[str]:

        command = ["pdftotext", str(fname), "-"]
        output = subprocess.run(command, stdout=subprocess.PIPE, shell=False)
        document = output.stdout.decode(errors="ignore")
        pages = document.split("\f")
        pages = pages[:-1]  # the last page in the split is always empty.

        return pages

    def pdf_to_text(fname: str, common_p_val: float = 0.01, joiner: str = ' ') -> str:
        pages = PDFToTextProcessor.read_pdf(fname)

        return joiner.join(PDFToTextProcessor.remove_headers(pages, common_p_val))

    @staticmethod
    def remove_headers(pages, common_p_val=0.01):
        pages_copy = list(pages)
        page_thresh = int(len(pages) * common_p_val)

        sep = ' '
        potential_headers = [PDFToTextProcessor.process_for_header(
            i).split(sep)[:50] for i in pages if len(i.split())]

        idx = 2
        common_list = []

        while True:
            pg = pd.Series(dict(Counter([sep.join(i[:idx])
                                         for i in potential_headers if len(i)]).most_common()))
            pg = pg[pg >= page_thresh]
            if pg.empty:
                break
            common_list.append(pg)
            idx += 1

        len(common_list)

        common_list_df = pd.concat(common_list[::-1])
        common_list_df.head()
        common_list_df.tail()

        comms = [i.split(sep) for i in common_list_df.index]

        for ix, l in enumerate(pages):
            ll = PDFToTextProcessor.process_for_header(l).split(sep)
            # if ix and ix % 10 == 0:
            #     print(ix)
            for c in comms:
                ixl = len(c)
                if ll[:ixl] == c:
                    pages_copy[ix] = sep.join(ll[ixl:]).replace(' \n', '\n')
                    break

        return pages_copy

from typing import List


class PDFToTextProcessor:
    def __init__(self):
        pass

    @staticmethod
    def process_for_header(s):
        s = re.sub(r'([^\s])(\n+)', r'\1 \2', s)
        return s

    @staticmethod
    def read_pdf(fname: str) -> List[str]:

        command = ["pdftotext", str(fname), "-"]
        output = subprocess.run(command, stdout=subprocess.PIPE, shell=False)
        document = output.stdout.decode(errors="ignore")
        pages = document.split("\f")
        pages = pages[:-1]  # the last page in the split is always empty.

        return pages

    def pdf_to_text(fname: str, common_p_val: float = 0.01, joiner: str = ' ') -> str:
        pages = PDFToTextProcessor.read_pdf(fname)

        return joiner.join(PDFToTextProcessor.remove_headers(pages, common_p_val))

    @staticmethod
    def remove_headers(pages, common_p_val=0.01):
        pages_copy = list(pages)
        page_thresh = int(len(pages) * common_p_val)

        sep = ' '
        potential_headers = [PDFToTextProcessor.process_for_header(
            i).split(sep)[:50] for i in pages if len(i.split())]

        idx = 2
        common_list = []

        while True:
            pg = pd.Series(dict(Counter([sep.join(i[:idx])
                                         for i in potential_headers if len(i)]).most_common()))
            pg = pg[pg >= page_thresh]
            if pg.empty:
                break
            common_list.append(pg)
            idx += 1

        len(common_list)

        common_list_df = pd.concat(common_list[::-1])
        common_list_df.head()
        common_list_df.tail()

        comms = [i.split(sep) for i in common_list_df.index]

        for ix, l in enumerate(pages):
            ll = PDFToTextProcessor.process_for_header(l).split(sep)
            # if ix and ix % 10 == 0:
            #     print(ix)
            for c in comms:
                ixl = len(c)
                if ll[:ixl] == c:
                    pages_copy[ix] = sep.join(ll[ixl:]).replace(' \n', '\n')
                    break

        return pages_copy

pdftp = PDFToTextProcessor()


class PDFToTextProcessor:
    def __init__(self):
        pass

    @staticmethod
    def process_for_header(s):
        s = re.sub(r'([^\s])(\n+)', r'\1 \2', s)
        return s

    @staticmethod
    def read_pdf(fname: str) -> List[str]:

        command = ["pdftotext", str(fname), "-"]
        output = subprocess.run(command, stdout=subprocess.PIPE, shell=False)
        document = output.stdout.decode(errors="ignore")
        pages = document.split("\f")
        pages = pages[:-1]  # the last page in the split is always empty.

        return pages

    def pdf_to_text(fname: str, common_p_val: float = 0.01, joiner: str = ' ') -> str:
        pages = PDFToTextProcessor.read_pdf(fname)

        return joiner.join(PDFToTextProcessor.remove_headers(pages, common_p_val))

    @staticmethod
    def remove_headers(pages, common_p_val=0.01):
        pages_copy = list(pages)
        page_thresh = int(len(pages) * common_p_val)

        sep = ' '
        potential_headers = [PDFToTextProcessor.process_for_header(
            i).split(sep)[:50] for i in pages if len(i.split())]

        idx = 2
        common_list = []

        while True:
            pg = pd.Series(dict(Counter([sep.join(i[:idx])
                                         for i in potential_headers if len(i)]).most_common()))
            pg = pg[pg >= page_thresh]
            if pg.empty:
                break
            common_list.append(pg)
            idx += 1

        len(common_list)

        common_list_df = pd.concat(common_list[::-1])
        common_list_df.head()
        common_list_df.tail()

        comms = [i.split(sep) for i in common_list_df.index]

        for ix, l in enumerate(pages):
            ll = PDFToTextProcessor.process_for_header(l).split(sep)
            # if ix and ix % 10 == 0:
            #     print(ix)
            for c in comms:
                ixl = len(c)
                if ll[:ixl] == c:
                    pages_copy[ix] = sep.join(ll[ixl:]).replace(' \n', '\n')
                    break

        return pages_copy

pdftp = PDFToTextProcessor()
%time ee = pdftp.pdf_to_text('WDR 2013 low res.pdf')


class PDFToTextProcessor:
    def __init__(self):
        pass

    @staticmethod
    def normalize_footnote_citations(text: str) -> str:
        r"""This method tries to detect footnotes and normalizes them.

        This is essential to improve the accuracy of SpaCy's sentence
        detector. Sometimes footnote citations are connected with sentence
        endings that prevents the detection of proper sentence boundary.

        The transformation handles common footnote citation formats:
            pattern: ((?:[a-zA-Z\)]+[.,]|\)))(\d+)(\s)
                - This is a normalizer.1 We will use this.
                - This is a normalizer (great).2 We will use this.
                - This is a normalizer (great).3\nWe will use this.
                - The normalizer (2020)8 is working.
            transforms to:
                - This is a normalizer. _1 We will use this.
                - This is a normalizer (great). _2 We will use this.
                - This is a normalizer (great). _3\nWe will use this.
                - The normalizer (2020) _8 is working.

        Args:
            text:
                Text that will be checked and normalized for footnote
                citations.

        Returns:
            normalized text

        """
        footnote_patterns = [
            r'((?:[a-zA-Z\)]+[.,]|\)))(\d+)(\s)'
        ]

        footnote_patterns = '|'.join(footnote_patterns)

        return re.sub(footnote_patterns, r'\1 _\2\3', text)

    @staticmethod
    def process_for_header(s):
        s = re.sub(r'([^\s])(\n+)', r'\1 \2', s)
        return s

    @staticmethod
    def read_pdf(fname: str) -> List[str]:

        command = ["pdftotext", str(fname), "-"]
        output = subprocess.run(command, stdout=subprocess.PIPE, shell=False)
        document = output.stdout.decode(errors="ignore")
        pages = document.split("\f")
        pages = pages[:-1]  # the last page in the split is always empty.

        return pages

    @staticmethod
    def pdf_to_text(fname: str, common_p_val: float = 0.01, joiner: str = ' ') -> str:
        pages = PDFToTextProcessor.read_pdf(fname)

        return joiner.join(PDFToTextProcessor.remove_headers(pages, common_p_val))

    @staticmethod
    def remove_headers(pages, common_p_val=0.01):
        pages_copy = list(pages)
        page_thresh = int(len(pages) * common_p_val)

        sep = ' '
        potential_headers = [PDFToTextProcessor.process_for_header(
            i).split(sep)[:50] for i in pages if len(i.split())]

        idx = 2
        common_list = []

        while True:
            pg = pd.Series(dict(Counter([sep.join(i[:idx])
                                         for i in potential_headers if len(i)]).most_common()))
            pg = pg[pg >= page_thresh]
            if pg.empty:
                break
            common_list.append(pg)
            idx += 1

        len(common_list)

        common_list_df = pd.concat(common_list[::-1])
        common_list_df.head()
        common_list_df.tail()

        comms = [i.split(sep) for i in common_list_df.index]

        for ix, l in enumerate(pages):
            ll = PDFToTextProcessor.process_for_header(l).split(sep)
            # if ix and ix % 10 == 0:
            #     print(ix)
            for c in comms:
                ixl = len(c)
                if ll[:ixl] == c:
                    pages_copy[ix] = sep.join(ll[ixl:]).replace(' \n', '\n')
                    break

        return pages_copy

pdftp = PDFToTextProcessor()
%time ee = pdftp.pdf_to_text('WDR 2013 low res.pdf')
len(ee)
%time e_sents = nltk.sent_tokenize(normalize_footnote_citations(ee))
for s in e_sents[:500]:
    print(s.replace('\n', ' ').strip())
    print('------------------------------------')
%history
