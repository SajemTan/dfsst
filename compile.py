#!/usr/bin/env python3

import json
import sys
import yaml

class Day:
    def __init__(self):
        self.vocab = []
        self.comments = []
        self.sentences = []
        self.reading = ''
    def from_yaml(self, blob, number):
        def st_en(txt):
            ls = txt.strip().split('$')
            ret = []
            en = True
            for t in ls:
                if t:
                    ret.append((t, 'en' if en else 'st'))
                en = not en
            return ret
        for voc_ent in blob['vocab']:
            voc = st_en(voc_ent)
            if len(voc) < 2:
                raise Exception(f'In day {number}, expected vocab entry with gloss!')
            if voc[0][1] != 'st':
                raise Exception(f'In day {number}, expected vocab entry to start with ST word!')
            self.vocab.append((voc[0][0], voc[1:]))
        self.comments = [st_en(c) for c in blob['comments']]
        for sent_ln in blob['sentences']:
            sent = st_en(sent_ln)
            if len(sent) != 2 or sent[0][1] != 'st' or sent[1][1] != 'en':
                raise Exception(f'In day {number}, expected ST sentence with English translation')
            self.sentences.append({'st': sent[0][0], 'en': sent[1][0]})
        if 'reading' in blob:
            self.reading = blob['reading']
    def all_st(self):
        def yieldtxt(ls):
            for t, l in ls:
                if l == 'st':
                    yield t
        for w, d in self.vocab:
            yield w
            yield from yieldtxt(d)
        for c in self.comments:
            yield from yieldtxt(c)
        for s in self.sentences:
            yield s['st']
        if self.reading:
            yield self.reading
    def to_json(self):
        def txt2json(ls):
            return [{'lang': l, 'txt': t} for t, l in ls]
        blob = {
            'vocab': [{'word': w, 'def': txt2json(d)} for w, d in self.vocab],
            'comments': [txt2json(c) for c in self.comments],
            'sentences': self.sentences
        }
        if self.reading:
            blob['reading'] = self.reading
        return blob

def validate(days):
    # TODO:
    # - check that all words appear in the vocabulary before they're used
    # - check that every new vocab word is in the exercises
    # - check that we don't go too long without using a word
    return True

def save_html(days):
    def read_file(fname):
        with open(fname) as fin:
            return fin.read()
    blob = [d.to_json() for d in days]
    with open('build/dfsst.html', 'w') as fout:
        fout.write(read_file('template.html').format(
            data = json.dumps(blob),
            js = read_file('dfsst.js')
        ))

with open('lessons.yaml') as fin:
    blob = yaml.safe_load(fin)
    days = []
    for b in blob:
        d = Day()
        d.from_yaml(b, len(days))
        days.append(d)
    if validate(days):
        save_html(days)
    else:
        sys.exit(1)
