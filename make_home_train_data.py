# -*- coding: utf-8 -*-
#  L = ( B-EＲ，I-EＲ，B-OBJECT，I -OBJECT，E-OBJECT, O) ，
# 其中各个标记的意义分别是语义关系词汇( 实例属性) 首部、语义关系词汇内部、属性值首部、属性值内部及其他。
import codecs
import sys
import json
import re
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

def character_tagging(input_file, train_file, test_file):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    train_data = codecs.open(train_file, 'w', 'utf-8')
    test_data = codecs.open(test_file, 'w', 'utf-8')
    data_list = json.load(input_data)
    index = 0
    for i,data in enumerate(data_list):
        have_home = True
        homeList = []
        for home in data['home']:
            if home[0] != '':
                # 生成训练数据
                if home[1] == 'ns':
                    homeList.append(re.sub(r"(省|市|县|区|自治区)", '', home[0]))
            else:
                # 生成测试数据
                have_home = False
                break
        if len(homeList) == 0:
            have_home = False
        obj_begin_tag = False
        obj_list = []
        if have_home:
            # 标记数据，生成训练数据
            for word in data['text']:
                re_str = '生|出生|生于|出生于' # 属性正则
                re_type = 'ns' # 属性值词性正则
                re_shi=''
                re_xian=''
                if len(homeList) == 3:
                    re_sheng = homeList[0]
                    re_shi = homeList[1]
                    re_xian = homeList[2]
                elif len(homeList) == 2:
                    re_sheng = homeList[0]
                    re_shi = homeList[1]
                else:
                    re_sheng = homeList[0]
                match_v = re.match(re_str, word[0])
                match_bo = re.search(re_sheng, word[0])
                match_io = None
                match_eo = None
                if re_shi != '':
                    match_io = re.search(re_shi, word[0])
                if re_xian != '':
                    match_eo = re.search(re_xian, word[0])
                match_type = None
                if word[1] is not None:
                    match_type = re.match(re_type, 'ns')
                else:
                    continue
                if match_v is not None:
                    obj_begin_tag = False
                    train_data.write(word[0] + "\t" + word[1] + "\tB-ER\n")
                elif match_bo is not None and match_type is not None:
                    obj_begin_tag = True
                    if len(homeList) == 1:
                        train_data.write(word[0] + "\t" + word[1] + "\tB-OBJECT\n")
                        obj_begin_tag = False
                    else:
                        obj_list.append(word[0])
                elif obj_begin_tag and match_io is not None and match_type is not None:
                    if len(homeList) == 2:
                        train_data.write(obj_list[0] + "\t" + word[1] + "\tB-OBJECT\n")
                        train_data.write(word[0] + "\t" + word[1] + "\tE-OBJECT\n")
                        obj_list = []
                        obj_begin_tag = False
                    else:
                        obj_list.append(word[0])
                elif obj_begin_tag and match_eo is not None and match_type is not None:
                    if len(obj_list) == 2:
                        train_data.write(obj_list[0] + "\t" + word[1] + "\tB-OBJECT\n")
                        train_data.write(obj_list[1] + "\t" + word[1] + "\tI-OBJECT\n")
                        train_data.write(word[0] + "\t" + word[1] + "\tE-OBJECT\n")
                    obj_list = []
                    obj_begin_tag = False
                else:
                    obj_begin_tag = False
                    if len(obj_list) != 0:
                        for obj in obj_list:
                            train_data.write(obj + "\t" + word[1] + "\tO\n")
                        obj_list = []
                    train_data.write(word[0] + "\t" + word[1] + "\tO\n")
        else:
            # 生成测试数据
            test_data.write("index" + str(index) + "\t" + "m" + "\tO\n")
            for word in data['text']:
                if word[1] is not None:
                    test_data.write(word[0] + "\t" + word[1] + "\tO\n")
                else:
                    continue
        test_data.write("\n")
        index += 1
    input_data.close()
    train_data.close()
    test_data.close()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print ("pls use: python make_crf_train_data.py input train_output test_output")
        sys.exit()
    input_file = sys.argv[1]
    train_file = sys.argv[2]
    test_file = sys.argv[3]
    character_tagging(input_file, train_file, test_file)