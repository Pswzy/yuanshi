# -*- coding: utf-8 -*-
import codecs
import sys
from bs4 import BeautifulSoup
import io
import json
import pynlpir
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')         #改变标准输出的默认编码
pynlpir.open()
with codecs.open('step_two_home.json', 'r', 'utf-8') as fl:
    load_list=json.load(fl)
    error_list=[]
    print(len(load_list))
    delete_index = []
    for person in load_list:
        person['birth']=pynlpir.segment(person['birth'], pos_names=None, pos_english=False)
        person['home']=pynlpir.segment(person['home'], pos_names=None, pos_english=False)
        person['school']=pynlpir.segment(person['school'], pos_names=None, pos_english=False)
        person['text']=pynlpir.segment(person['text'], pos_names=None, pos_english=False)
    with codecs.open('home_segement.json', 'w', 'utf-8') as result_fl:
        json.dump(load_list, result_fl, skipkeys=False, ensure_ascii=False)