from parse_patch import *
from parse_options import *
import json
import re


prefix_config    = "CONFIG_"
related_kconfigs = []
kconfigs         = {}


def load():
    with open('data.json') as json_file:
        data = json.load(json_file)
        return data


def searchDepends(symbol):
    
    if kconfigs.has_key(symbol):
        config = kconfigs[symbol]
        related_kconfigs.append(symbol)
        # print "kconfigs depending on it are" 
        # print config['rdepends']
        if not config.has_key('depends'):
            return
        dic_depends = config['depends']
        count       = dic_depends['count']
        print dic_depends
        i = 1
        while i <= count:
             depends = dic_depends[str(i)]
             i       = i + 1
             for depend in re.findall(r'[A-Za-z0-9_]+', depends):
                 depend = prefix_config + depend
                 print depend
                 searchDepends(depend)
             
def searchRDepends(symbol):
    if kconfigs.has_key(symbol):
        config = kconfigs[symbol]
        print config['rdepends']
    else:
        print "This config is not in kconfig set!"



if __name__ == "__main__":
    options     = {'inputfile':"", 'outputfile':""}
    parse_args(sys.argv[1:], options)
    configs = parse(options['inputfile'])
    kconfigs    = load()
    
    for config in configs:
        print config
        searchDepends(config)
        print "-*- depends are -*-"
        print "--------------------------------------------"
        for symbol in related_kconfigs:
            print symbol
        print "-*- rdepends are -*-"
        print "--------------------------------------------"
        searchRDepends(config)
        print "--------------------------------------------"


