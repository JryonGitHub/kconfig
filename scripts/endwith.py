#!/usr/bin/python
def endWith(*endstring):
    ends = endstring
    def run(s):
        f = map(s[1].endswith,ends)
        if True in f: return s
    return run

if __name__ == '__main__':
    import os

    list_file = [('avc','hello.c'), ('bcd','jry.java'), ('jry', 'put.c'), ('kun','rizhai.txt'), ('zhaodan', 'rest.py')]
    print list_file
    a = endWith('.txt','.py')
    

    f_file = filter(a,list_file)
    print f_file
    for i in f_file: print i
