from kconfig import *
import os
import commands
import json
import re

(status, output) = commands.getstatusoutput("pwd")
prefix_path = "/home/jry/workspace/linux-4.9.13/"
prefix_config = "CONFIG_"
kconfigs = {}
obj = None
symbol = ""


# store and load functions
def store(data):
    with open('data.json', 'w') as json_file:
        json_file.write(json.dumps(data))

def load():
    with open('data.json') as json_file:
        data = json.load(json_file)
        return data

# auxiliary function
def do_depends(symbol, dic_depends, depends):
    index = dic_depends['count'] + 1
    dic_depends['count'] = index
    dic_depends[index] = depends
    for depend in re.findall(r'[A-Za-z0-9_]+', depends):
        depend = prefix_config + depend
        if kconfigs.has_key(depend):
            if symbol not in kconfigs[depend]['rdepends']:
                kconfigs[depend]['rdepends'].append(symbol) 
        else:
            temp = create_kconfig()
            temp['rdepends'].append(symbol)
            kconfigs.update({depend : temp})
            

def do_select(dic_selects, select):
    index = dic_selects['count'] + 1
    dic_selects['count'] = index   
    dic_selects[index] = select

def is_contained(dics, symbol):
    return dics.has_key(symbol)

def create_kconfig():
    obj = kconfig()
    return obj

# pattern functions
def source(match):
    global obj
    save(match) 
    subfile_path = prefix_path + match.group(1)
    print subfile_path
    procKconfig(subfile_path)

def config(match):
    global obj, symbol
    save(match)
    symbol = prefix_config + match.group(1)
    if is_contained(kconfigs, symbol):
        obj = kconfigs[symbol]
    else:
        obj = create_kconfig()


def bool(match): 
    global obj
    if not obj:
        return
    obj['bool'] = match.group(1) 

def tristate(match):
    global obj
    if not obj:
        return
    obj['tristate'] = match.group(1)

def dependson(match):
    global obj
    if not obj:
        return
    depends = match.group(1)
    if not obj.has_depends:
        dic_depends = {}
        dic_depends['count'] = 0
        obj.has_depends = True
    else:
        dic_depends = obj[r'depends']
    
    do_depends(symbol, dic_depends, depends)
    obj['depends'] = dic_depends

def default(match):
    global obj
    if not obj:
        return
    if obj:
        obj['default'] = match.group(1)

def select(match):
    global obj
    if not obj:
        return
    select = match.group(1)
    if not obj.has_selects:
        dic_selects = {}
        dic_selects['count'] = 0
        obj.has_selects = True
    else:
        dic_selects = obj['selects']

    do_select(dic_selects, select)
    obj['selects'] = dic_selects

def defbool(match):
    global obj
    if not obj:
        return
    obj['defbool'] = match.group(1)

def save(match):
    global obj
    if not obj:
        return
    kconfigs.update({symbol : obj})
    obj = None

# patterns of kconfigs
pattern_set = {r'^source "(.*/[^/]*)"' : source, r'config ([0-9A-Za-z_]{1,})' : config, r'^bool (.*)' : bool, r'^tristate (.*)' : tristate, r'depends on (.*)' : dependson, r'default (.*)' : default, r'select (.*)' : select, r'def_bool (.*)' : defbool, r'^menuconfig|choice|endchoice|comment|menu|endmenu|if|endif| *' : save}

 # process function
def procKconfig(filepath):

    match = re.match(r'^(.*)/([^/]*)$', filepath)
    if not match:
        print "Invalid file path!"
        return 
    if not os.path.exists(filepath):
        print "No such file or directory!"
        return

    fd = open(filepath)
    for line in fd:
        line = line.strip()
        for pattern in pattern_set:
            match = re.match(pattern, line)
            if match:
                pattern_set[pattern](match)
                break


 # main function
if __name__ == "__main__":
    procKconfig("/home/jry/workspace/linux-4.9.13/arch/x86/Kconfig")
    store(kconfigs)
    dataset =  load()
    # print dataset
    for data in dataset:
        if len(kconfigs[data]['rdepends']) > 0:
            print data
            print kconfigs[data]['rdepends']
    print len(dataset)
