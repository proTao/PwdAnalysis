import re

# Global dictionary
LDS = {}
L1D2S3 = {}
LDS_NUM = {8: {}}      # 元素为等长的格式
LEN = 0             # 按长度保存在len.txt中


def choose_txt(filename):
    file = open(filename)
    try:
        list_return = file.readlines()
    finally:
        file.close()
    return list_return


def process(l):

    i = 0
    pattern_comp = re.compile('\d+|[a-zA-Z]+|[\W_]+')
    while i < num:
        l[i] = l[i].strip()     # strip '\n'
        pw = l[i]      # 要匹配的字符串
        pw = pw[1:]
        # 统计组成
        str1 = ''
        str2 = ''
        length = 0
        list_comp = re.findall(pattern_comp, pw)
        for var in list_comp:
            if re.match('\d+', var):            # 数字D
                str1 += 'D'
                str2 += ('D:' + str(var.__len__()))
            elif re.match('[a-zA-Z]+', var):    # 字母L
                str1 += 'L'
                str2 += ('L:' + str(var.__len__()))
            else:                               # 标点S
                str1 += 'S'
                str2 += ('S:' + str(var.__len__()))
            str2 += ','     # 修改格式
            length += var.__len__()     # 长度计数器
            # if length == 26:
            #     print('pw:', pw)
        list_lds(str1)      # 放入LDS
        list_l1d2s3(str2)   # 放入L1D2S3
        list_lds_num(length, str2)  # 放入新格式的
        if length == 26:
            print('26:')
            print('pw:', pw)
            print('str: ', str2)
        i += 1
    pass


def list_lds_num(length, str3):

    if length in LDS_NUM.keys():
        if str3 in LDS_NUM[length].keys():
            LDS_NUM[length][str3] += 1
        else:   # 添加key为str3，初始值为1
            # LDS_NUM[length].setdefault(str3, 1)
            LDS_NUM[length][str3] = 1
    else:
        LDS_NUM[length] = {}


def list_lds(str1):     # 得到LDS
    if str1 in LDS.keys():
        LDS[str1] += 1
    else:
        LDS.setdefault(str1, 1)


def list_l1d2s3(str2):      # 得到L1D2S3
    if str2 in L1D2S3.keys():
        L1D2S3[str2] += 1
    else:
        L1D2S3.setdefault(str2, 1)


def fw_lds(path):
    LDS_sorted = sorted(LDS.items(), key=lambda e: e[1], reverse=True)  # 排序
    j = 0
    file1 = open(path, 'w')
    num1 = len(LDS_sorted)
    print('LDS模式数量：', num1)
    while j < num1:
        s1 = LDS_sorted[j][0]   # 项目
        s2 = LDS_sorted[j][1]   # 频数
        s3 = s2 / num * 1000           # 比例:千分之
        s = s1 + str(s2) + ',' + str(s2) + ' ' + str(s3) + '\n'
        file1.writelines(s)
        j += 1
    file1.close()
    print(path, "is OK!")


def fw_l1d2s3(path):
    L1D2S3_sorted = sorted(L1D2S3.items(), key=lambda e: e[
                           1], reverse=True)  # 排序
    j = 0
    file2 = open(path, 'w')
    num2 = len(L1D2S3_sorted)
    print('L1D2S3模式数量：', num2)
    while j < num2:
        s1 = L1D2S3_sorted[j][0]   # 项目
        s2 = L1D2S3_sorted[j][1]   # 频数
        s3 = s2 / num * 1000           # 比例:千分之
        s = s1 + str(s2) + ',' + str(s3) + '\n'
        file2.writelines(s)
        j += 1
    file2.close()
    print(path, "is OK!")


def fw_lds_num():
    list_key = LDS_NUM.keys()   # get keys
    for dic in list_key:
        LDS_NUM_sorted = sorted(LDS_NUM[dic].items(), key=lambda e: e[
                                1], reverse=True)  # 排序
        path = "result/" + str(dic) + '.txt'
        j = 0
        file = open(path, 'w')
        count = len(LDS_NUM_sorted)
        while j < count:
            s1 = LDS_NUM_sorted[j][0]   # 项目
            s2 = LDS_NUM_sorted[j][1]   # 频数
            s3 = s2 / num * 1000           # 比例:千分之
            s = s1 + str(s3) + '\n'
            # s = s1 + str(s2) + ',' + str(s3) + '\n'
            file.writelines(s)
            j += 1
        file.close()
    print('fw_lds_num is done!')


list_pw = choose_txt('data_all.txt')
num = list_pw.__len__()
print('pw总数量：', num)
process(list_pw)
fw_lds_num()
