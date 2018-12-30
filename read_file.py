#!/usr/bin/python
# -*- coding: utf-8 -*-

import ast
import codecs
import re

def parse_file(filename):
    global enc, lines
    enc, enc_len = detect_encoding(filename)
    f = codecs.open(filename, 'r', enc)
    lines = f.read()

    # remove BOM
    lines = re.sub(u'\ufeff', ' ', lines)

    if enc_len > 0:
        lines = re.sub('#.*coding\s*[:=]\s*[\w\d\-]+',  '#' + ' ' * (enc_len-1), lines)

    f.close()
    return parse_string(lines, filename)


def parse_string(string, filename=None):
    tree = ast.parse(string)
    if filename:
        tree.filename = filename
    # print ast.dump(tree)
    return tree


def detect_encoding(path):
    fin = open(path, 'rb')
    prefix = str(fin.read(80))
    encs = re.findall('#.*coding\s*[:=]\s*([\w\d\-]+)', prefix)
    decl = re.findall('#.*coding\s*[:=]\s*[\w\d\-]+', prefix)

    if encs:
        enc1 = encs[0]
        enc_len = len(decl[0])
        try:
            info = codecs.lookup(enc1)
            # print('lookedup: ', info)
        except LookupError:
            # print('encoding not exist: ' + enc1)
            return 'latin1', enc_len
        return enc1, enc_len
    else:
        return 'latin1', -1


