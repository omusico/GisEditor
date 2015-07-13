#!/usr/bin/env python3

import os
from os import path
from PIL import ImageFont, Image
from sym import SymbolRules
from datetime import timedelta

#constance
def __readConfig(conf_path):
    conf = {}
    with open(conf_path) as conf_file:
        for line in conf_file:
            k, v = line.rstrip().split('=', 1)
            conf[k] = v
    return conf
__config = __readConfig('./giseditor.conf')
CACHE_DIR = __config['cache_dir']
GPSBABEL_DIR = __config['gpsbabel_dir']

IMG_FONT = ImageFont.truetype("ARIALUNI.TTF", 18) #global use font (Note: the operation is time wasting)
TZ = timedelta(hours=8)
ICON_DIR = './icon'
ICON_SIZE = 24
DEF_SYMBOL = "Waypoint"

#global variables
Sym_rules = SymbolRules('./sym_rule.conf')

def getSymbol(name):
    rule = Sym_rules.getMatchRule(name)
    sym = rule.symbol if rule is not None else DEF_SYMBOL
    return sym

__icons = {}
def getIcon(sym):
    sym = sym.lower()
    icon = __icons.get(sym)
    if icon is None:
        path =  __getIconPath(sym)
        if path is None:
            if sym.lower() == DEF_SYMBOL.lower():
                return None
            else:
                return getIcon(DEF_SYMBOL)
        icon = Image.open(path)
        icon = icon.resize((ICON_SIZE, ICON_SIZE))
        __icons[sym] = icon
    return icon

#get icon path for the sym. case-insensitive, ignore extention
def __getIconPath(sym):
    sym = sym.lower()
    for f in os.listdir(ICON_DIR):
        name, ext = path.splitext(f)
        if sym == name.lower():
            return path.join(ICON_DIR, f)
    return None
