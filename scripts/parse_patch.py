#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import os

prefix_path = "/home/jry/workspace/linux-4.9.13/"

#this function returns the pairs composed by file name and path 
#from file modified in patch
def parsePatch(filepath):
    print "parsePatch entry -> path is " + filepath
    result = []
    match = re.match(r'^(.*)/([^/]*)$', filepath)
    if not match:
        print "-*- parsePatch -*- Invalid file path!" + filepath
        return result
    
    fd = open(filepath)    

    for line in fd:
        line = line.strip()
        routs = re.findall(r'^\+\+\+ b/(.*/)([^/]*)$', line)
        if len(routs):
            result.extend(routs)
    
    print routs
    return result

def parseMakefile(filepath, fileName):
    print "parseMakefile entry -> filepath is " + filepath + ", fileName is " + fileName
    match = re.match(r'^(.*)/([^/]*)$', filepath)
    result = []
    if not match:
        print "-*- parseMakefile -*- Invalid file path!" + filepath
        return result
    if not os.path.exists(filepath):
        print "-*- parseMakefile -*- No such file or directory!" + filepath
        return result
    fd = open(filepath)
    all_text = fd.read()
    pattern = r'obj-\$\(([A-Za-z0-9_]+)\)\s*\+=\s*.* ' + fileName 
    print pattern
    match = re.search(pattern, all_text, re.M)
    if match:
        result.append(match.group(1))
        print "what found by \"" + pattern + "\" is -------" + match.group(1)
        return result
    pattern = r'\s([a-z0-9_]+)-objs := .*' + fileName
    print pattern
    match = re.search(pattern, all_text, re.M|re.S)
    if match:
        print "what found by \"" + pattern + "\" is -------" + match.group(1)
        obj = match.group(1) + '.o'
        result = parseMakefile(filepath, obj)
    return result

def endWith(*endstring):
    ends = endstring
    def run(s):
        f = map(s[1].endswith, ends)
        if True in f: return s
    return run

#this function returns pairs with specific postfix
def postfix_filter(dataSet):
    target = endWith('.c')
    return filter(target, dataSet)

def parse(filepath):
    print "parse entry -> filepath is " + filepath
    match = re.match(r'^(.*)/([^/]*)$', filepath)
    result  = []
    if not match:
        print "-*- parse -*- Invalid file path!" + filepath
        return result

    dataSet = parsePatch(filepath)
    f_file = postfix_filter(dataSet)
    for f in f_file:
        path     = prefix_path + f[0] + "Makefile"
        fileName = f[1].replace(".c", ".o")
        result.extend(parseMakefile(path, fileName))
    return result
