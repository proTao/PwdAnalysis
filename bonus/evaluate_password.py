'''
date:2016-10-27
author:tao

思路：
1. 目前考虑用apriori算法的连接剪枝生成候选集的思想生成频繁的子串
2. 利用频繁子串训练出一个2阶或者3阶的Markov模型

'''
import time
import pickle


def selfJoin(str_list):
    '''
    进行长度增长1的自定义笛卡尔连接，比如abc和bcd连接成为abcd
    abc成为前串，bcd称为后串

    str是一个等长字符串集合
    理应是集合对象，但是为了有序，使用列表
    在输入之前对str_list按照字典序排序
    在该函数内部要是对str_list操作的话外部变量也会改变，这样不好
    '''
    result_list = []
    for i in range(len(str_list)):

        # 因为按照字典序有序，可以匹配的后串必然连续出现，
        # 找到一堆连续的可以匹配的串，后面全是不能匹配的
        find_match = False
        for j in range(len(str_list)):
            if str_list[i][:-1] == str_list[j][:-1]:
                find_match = True
                result_list.append(str_list[i] + str_list[j][-1])
            else:
                if find_match:
                    continue
    return result_list


def selfJoin2(str_list):
    '''
    进行长度增长1的自定义笛卡尔连接，比如abc和bcd连接成为abcd
    abc成为前串，bcd称为后串

    str是一个等长字符串集合
    理应是集合对象，但是为了有序，使用列表
    在输入之前对str_list按照字典序排序
    在该函数内部要是对str_list操作的话外部变量也会改变，这样不好
    '''
    result_list = []
    for i in range(len(str_list)):
        for j in range(len(str_list)):
            if str_list[i][:-1] == str_list[j][:-1]:
                result_list.append(str_list[i] + str_list[j][-1])
    return result_list


def splitStringByK(string, k, limit=[]):
    if(len(limit) == 0):
        result_list = []
        for i in range(len(string) - k + 1):
            result_list.append(string[i:i + k])
        return list(result_list)
    else:
        result_list = set()
        for i in range(len(string) - k + 1):
            if(string[i:i + k] in limit):
                result_list.append(string[i:i + k])
        return list(result_list)

a = ['aa', 'ab', 'ac', 'ad', 'ae', 'af',
     'ba', 'bb', 'bc', 'bd', 'be', 'bf',
     'ca', 'cb', 'cc', 'cd', 'ce', 'cf',
     'da', 'db', 'dc', 'dd', 'de', 'df',
     'ea', 'eb', 'ec', 'ed', 'ee', 'ef',
     'fa', 'fb', 'fc', 'fd', 'fe', 'ff']
b = ['cb', 'dc', 'dd', 'cc', 'ac', 'ca', 'cd', 'aa', 'ad',
     'ba', 'da', 'ab', 'bb', 'bc', 'bd', 'db',
     'be', 'ce', 'de', 'ee', 'ea', 'eb', 'ec',
     'ed', 'ae', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff', 'bf', 'cf', 'df', 'ef', 'ff', 'af']
'''
print("排序中")
result_str = ""
for key in sorted(new_dic, key=lambda k: new_dic[k],reverse=True):
    result_str += str(key)
    result_str += ":"
    result_str += str(new_dic[key])
    result_str += '\n'

with open("keyboard_result.txt", 'wb') as f:
    f.write(result_str.encode("utf-8"))
print("success")
'''

'''
time1=time.time()
for i in range(5000):
    selfJoin(a)
time2=time.time()
print(time2-time1)
time1=time.time()
for i in range(5000):
    selfJoin2(a)
time2=time.time()
print(time2-time1)
'''


def get2and3substr():
    split_k = 2
    while(split_k <= 3):
        with open("../data_eng.txt", "r", encoding="utf-8") as f:
            bigger_list = []
            count_sum = 0
            i = -1
            line = f.readline()
            dic = {}
            while(line):
                if(i % 14430 == 0):
                    print('%i%%' % (i / 14430))  # 在字符串中%%才能输出百分号
                line = line[1:-1].lower()  # -1为了去掉'\n'
                substr_list = splitStringByK(line, split_k, bigger_list)
                count_sum += len(substr_list)
                for element in substr_list:
                    if element in dic:
                        dic[element] += 1
                    else:
                        dic.setdefault(element, 1)

                try:
                    line = f.readline()
                except Exception as e:
                    print("readline exception")
                i += 1
            print("100%")

        print(count_sum)
        print("删除小值中")
        with open("dic.pkl", 'wb') as pkl:  # 以写权限打开二进制文件
            pickle.dump(dic, pkl)
        result_dic = {}
        '''
        for key in dic:
            weight=dic[key] / count_sum
            if(weight > 0.0003):
                result_dic.setdefault(key, weight)
        del(dic)
        '''
        for key in dic:
            weight = dic[key] / count_sum
            result_dic.setdefault(key, weight)
        del(dic)
        result_str = ""
        portion = 0
        for key in sorted(result_dic, key=lambda k: result_dic[k]):
            result_str += str(key)
            result_str += ":"
            portion += result_dic[key]
            result_str += str(portion)
            result_str += ","
            result_str += str(result_dic[key])
            result_str += '\n'
        outfile = "dic" + str(split_k) + ".txt"
        with open(outfile, 'wb') as f:
            f.write(result_str.encode("utf-8"))

        str_list = list(result_dic.keys())
        str_list.sort()
        # print(str_list)
        if (split_k == 2):
            bigger_list = selfJoin(str_list)
        # print(bigger_list)

        split_k += 1
    # -- WHILE END -- #


def getDataAndMakMatrix():
    dic3 = {}
    dic2 = {}
    i = 0
    with open("dic3.txt", 'r') as f:
        line = f.readline()
        while(line):
            substr = line[:3]
            portion = line[line.rindex(",") + 1:-1]
            dic3.setdefault(substr, float(portion) )
            line = f.readline()
        print("success")
    with open("dic2.txt", 'r') as f:
        line = f.readline()
        while(line):
            substr = line[:2]
            portion = line[line.rindex(",") + 1:-1]
            dic2.setdefault(substr, float(portion) )
            line = f.readline()
        print("success")
    return (dic2, dic3)


# 把这个值赋为0.0001的原因是在dic2和dic3中最小值都是10^-7
# 那么当字典中找不到时，意味着可能性比弟弟案中的最小值的可能性还要低
# 那么就使其第一个数量级，然后再读字典把每一个值为了好看乘以了10000
# 所以10^-8*10000就是10^-4
minimum_score = 1e-08


def getScore(string):
    if(len(string) == 2):
        if string in dic2:
            return dic2[string]
        else:
            return minimum_score
    elif(len(string) == 3):
        if string in dic3:
            return dic3[string]
        else:
            return minimum_score
    else:
        # 输入有误
        return None


dic2 = {}
dic3 = {}
dic2, dic3 = getDataAndMakMatrix()
while True:
    s = input("input:")
    
    score = getScore(s[0:2])
    # print(score)
    for i in range(len(s) - 2):
        print(s[i:i+3]+":"+str(getScore(s[i: i + 3])))

        score *= getScore(s[i: i + 3])
    print("总得分:"+str(score)+"\n")
    